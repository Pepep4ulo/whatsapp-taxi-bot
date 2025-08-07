import os
import logging
import uuid
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from distance_calculator import get_smart_distance_and_duration
from pricing import calculate_price
from data_store import save_ride, update_ride_status, get_session, save_session, get_ride
from models import Ride, CustomerSession

# Twilio credentials
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

# Driver information
DRIVER_PHONE = os.environ.get("DRIVER_PHONE", "whatsapp:+5511999999999")
VEHICLE_INFO = "Sandero Branco (QBI9I82)"
DRIVER_PIX = os.environ.get("DRIVER_PIX", "motorista@pix.com")

def send_whatsapp_message(to_phone: str, message: str):
    """Send WhatsApp message using Twilio"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        sent_message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        
        logging.info(f"Message sent to {to_phone} with SID: {sent_message.sid}")
        return True
        
    except Exception as e:
        logging.error(f"Error sending WhatsApp message: {str(e)}")
        return False

def handle_whatsapp_message(from_phone: str, message_body: str):
    """Handle incoming WhatsApp messages"""
    try:
        # Get or create customer session
        session = get_session(from_phone)
        if not session:
            session = CustomerSession(phone=from_phone, step='start')
        
        response = MessagingResponse()
        
        # Handle different conversation steps
        if message_body.lower() in ['oi', 'olá', 'solicitar', 'corrida', 'taxi', 'uber']:
            # Start new ride request
            session.step = 'passengers'
            save_session(session)
            
            reply = (
                "🚗 *Motorista Particular - Sandero Branco*\n\n"
                "Olá! Vou te ajudar a solicitar sua corrida.\n\n"
                "Quantos passageiros serão? (1-4)"
            )
            
        elif session.step == 'passengers':
            # Handle passenger count
            try:
                passengers = int(message_body.strip())
                if 1 <= passengers <= 4:
                    session.passengers = passengers
                    session.step = 'pickup'
                    save_session(session)
                    
                    reply = (
                        f"✅ {passengers} passageiro(s) confirmado(s)!\n\n"
                        "Agora me informe o *endereço de partida* (rua, número, bairro):"
                    )
                else:
                    reply = "Por favor, informe um número de passageiros entre 1 e 4."
                    
            except ValueError:
                reply = "Por favor, informe apenas o número de passageiros (1-4)."
                
        elif session.step == 'pickup':
            # Handle pickup location
            session.pickup_location = message_body.strip()
            session.step = 'destination'
            save_session(session)
            
            reply = (
                f"📍 *Partida:* {session.pickup_location}\n\n"
                "Agora me informe o *endereço de destino*:"
            )
            
        elif session.step == 'destination':
            # Handle destination and calculate quote
            session.destination = message_body.strip()
            
            # Get distance and duration using smart system (local + API when needed)
            if session.pickup_location and session.destination and session.passengers:
                distance_data = get_smart_distance_and_duration(session.pickup_location, session.destination)
                
                if distance_data:
                    distance_km = distance_data['distance_km']
                    duration_minutes = distance_data['duration_minutes']
                    
                    # Calculate price
                    price = calculate_price(distance_km, session.passengers)
                
                    # Create ride record
                    ride_id = str(uuid.uuid4())[:8]
                    ride = Ride(
                        id=ride_id,
                        customer_phone=from_phone,
                        customer_name=None,
                        passengers=session.passengers,
                        pickup_location=session.pickup_location,
                        destination=session.destination,
                        distance_km=distance_km,
                        duration_minutes=duration_minutes,
                        price=price,
                        status='pending',
                        created_at=datetime.now()
                    )
                
                    save_ride(ride)
                    session.current_ride_id = ride_id
                    session.step = 'quote_sent'
                    save_session(session)
                    
                    reply = (
                        f"💰 *COTAÇÃO - Corrida #{ride_id}*\n\n"
                        f"📍 *Partida:* {session.pickup_location}\n"
                        f"🎯 *Destino:* {session.destination}\n"
                        f"👥 *Passageiros:* {session.passengers}\n"
                        f"📏 *Distância:* {distance_km:.1f} km\n"
                        f"⏱️ *Tempo estimado:* {duration_minutes} min\n"
                        f"💵 *Valor:* R$ {price:.2f}\n\n"
                        f"🚗 *Veículo:* {VEHICLE_INFO}\n\n"
                        "Para *CONFIRMAR* a corrida, responda: *CONFIRMAR*\n"
                        "Para *CANCELAR*, responda: *CANCELAR*"
                    )
                
            else:
                reply = (
                    "❌ Não consegui calcular a rota entre os endereços informados.\n\n"
                    "Por favor, verifique os endereços e tente novamente.\n"
                    "Digite o endereço de destino:"
                )
                
        elif session.step == 'quote_sent':
            # Handle confirmation or cancellation
            message_lower = message_body.lower().strip()
            
            if message_lower == 'confirmar':
                if session.current_ride_id:
                    ride = get_ride(session.current_ride_id)
                    if ride:
                        # Update ride status
                        update_ride_status(session.current_ride_id, 'confirmed')
                        
                        # Send confirmation to customer
                        reply = (
                            f"✅ *CORRIDA CONFIRMADA!*\n\n"
                            f"📱 *Corrida:* #{session.current_ride_id}\n"
                            f"💵 *Valor:* R$ {ride.price:.2f}\n\n"
                            f"🚗 *Veículo:* {VEHICLE_INFO}\n"
                            f"💳 *PIX:* {DRIVER_PIX}\n\n"
                            f"📍 *Partida:* {ride.pickup_location}\n"
                            f"🎯 *Destino:* {ride.destination}\n\n"
                            "O motorista foi notificado e entrará em contato em breve!\n\n"
                            "Para uma nova corrida, digite: *SOLICITAR*"
                        )
                        
                        # Notify driver
                        driver_message = (
                            f"🚨 *NOVA CORRIDA CONFIRMADA!*\n\n"
                            f"📱 *ID:* #{session.current_ride_id}\n"
                            f"📞 *Cliente:* {from_phone}\n"
                            f"👥 *Passageiros:* {ride.passengers}\n\n"
                            f"📍 *PARTIDA:*\n{ride.pickup_location}\n\n"
                            f"🎯 *DESTINO:*\n{ride.destination}\n\n"
                            f"📏 *Distância:* {ride.distance_km:.1f} km\n"
                            f"⏱️ *Tempo:* {ride.duration_minutes} min\n"
                            f"💵 *Valor:* R$ {ride.price:.2f}"
                        )
                        
                        send_whatsapp_message(DRIVER_PHONE, driver_message)
                        
                        # Reset session
                        session.step = 'start'
                        session.current_ride_id = None
                        save_session(session)
                        
                    else:
                        reply = "❌ Erro: Corrida não encontrada. Digite *SOLICITAR* para uma nova cotação."
                        
            elif message_lower == 'cancelar':
                if session.current_ride_id:
                    update_ride_status(session.current_ride_id, 'cancelled')
                
                reply = (
                    "❌ *Corrida cancelada.*\n\n"
                    "Para solicitar uma nova corrida, digite: *SOLICITAR*"
                )
                
                # Reset session
                session.step = 'start'
                session.current_ride_id = None
                save_session(session)
                
            else:
                current_ride = get_ride(session.current_ride_id) if session.current_ride_id else None
                price_text = f"R$ {current_ride.price:.2f}" if current_ride else "indisponível"
                
                reply = (
                    "Por favor, responda apenas:\n"
                    "• *CONFIRMAR* - para confirmar a corrida\n"
                    "• *CANCELAR* - para cancelar\n\n"
                    f"💵 Valor da corrida: {price_text}"
                )
                
        else:
            # Default response
            reply = (
                "🚗 *Motorista Particular*\n\n"
                "Para solicitar uma corrida, digite: *SOLICITAR*\n\n"
                "Como posso ajudá-lo?"
            )
        
        response.message(reply)
        return str(response)
        
    except Exception as e:
        logging.error(f"Error in handle_whatsapp_message: {str(e)}")
        response = MessagingResponse()
        response.message("❌ Ocorreu um erro. Tente novamente ou digite *SOLICITAR* para uma nova corrida.")
        return str(response)
