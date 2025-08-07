#!/usr/bin/env python3
"""
Teste do bot de WhatsApp sem APIs externas
Simula conversas para verificar a lógica do bot
"""

import os
import sys
from whatsapp_bot import handle_whatsapp_message

# Configurar variáveis de ambiente para teste
os.environ["TWILIO_ACCOUNT_SID"] = "test_sid"
os.environ["TWILIO_AUTH_TOKEN"] = "test_token"
os.environ["TWILIO_PHONE_NUMBER"] = "whatsapp:+5511999999999"
os.environ["DRIVER_PHONE"] = "whatsapp:+5511888888888"
os.environ["DRIVER_PIX"] = "teste@pix.com"
os.environ["GOOGLE_MAPS_API_KEY"] = "test_key"

def simulate_conversation():
    """Simula uma conversa completa com o bot"""
    
    print("🤖 TESTE DO BOT DE WHATSAPP")
    print("=" * 50)
    
    # Telefone do cliente teste
    test_phone = "whatsapp:+5511123456789"
    
    # Sequência de mensagens para testar
    messages = [
        "oi",
        "2",  # 2 passageiros
        "Centro, Cuiabá",  # Partida
        "Arsenal, Cuiabá",  # Destino  
        "confirmar"  # Confirma a corrida
    ]
    
    print("Iniciando simulação de conversa...")
    print("-" * 30)
    
    for i, message in enumerate(messages, 1):
        print(f"\n👤 CLIENTE: {message}")
        
        try:
            # Chama o handler do bot (mesmo código do webhook)
            response = handle_whatsapp_message(test_phone, message)
            
            # Extrai só o texto da resposta XML
            import re
            response_text = re.search(r'<Message>(.*?)</Message>', response, re.DOTALL)
            if response_text:
                bot_reply = response_text.group(1).strip()
                print(f"🤖 BOT: {bot_reply}")
            else:
                print(f"🤖 BOT: [Resposta XML]: {response}")
                
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            break
            
        print("-" * 30)
    
    print("\n✅ Simulação concluída!")

def interactive_test():
    """Modo interativo para testar mensagens"""
    
    print("🤖 MODO INTERATIVO")
    print("=" * 50)
    print("Digite mensagens para testar o bot")
    print("Digite 'sair' para encerrar")
    print("-" * 30)
    
    test_phone = "whatsapp:+5511123456789"
    
    while True:
        try:
            message = input("\n👤 Você: ").strip()
            
            if message.lower() in ['sair', 'exit', 'quit']:
                break
                
            if not message:
                continue
                
            # Processa mensagem
            response = handle_whatsapp_message(test_phone, message)
            
            # Extrai resposta
            import re
            response_text = re.search(r'<Message>(.*?)</Message>', response, re.DOTALL)
            if response_text:
                bot_reply = response_text.group(1).strip()
                print(f"🤖 Bot: {bot_reply}")
            else:
                print(f"🤖 Bot: [XML]: {response}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
    
    print("\n👋 Teste encerrado!")

def test_pricing_system():
    """Testa o sistema de preços"""
    
    print("💰 TESTE DO SISTEMA DE PREÇOS")
    print("=" * 50)
    
    from distance_calculator import get_smart_distance_and_duration
    from pricing import calculate_price
    
    test_routes = [
        ("Centro, Cuiabá", "Arsenal, Cuiabá", 1),
        ("Centro, Cuiabá", "Arsenal, Cuiabá", 2),
        ("Goiabeiras, Cuiabá", "Duque de Caxias, Cuiabá", 1),
        ("Endereço desconhecido", "Outro endereço", 3)
    ]
    
    for pickup, destination, passengers in test_routes:
        print(f"\n📍 {pickup} → {destination} | {passengers} passageiro(s)")
        
        # Calcula distância
        distance_data = get_smart_distance_and_duration(pickup, destination)
        
        if distance_data:
            distance = distance_data['distance_km']
            duration = distance_data['duration_minutes']
            method = distance_data.get('method', 'unknown')
            
            # Calcula preço
            price = calculate_price(distance, passengers)
            
            print(f"   📏 Distância: {distance:.1f} km")
            print(f"   ⏱️ Tempo: {duration} min")
            print(f"   💵 Preço: R$ {price:.2f}")
            print(f"   🔧 Método: {method}")
        else:
            print("   ❌ Erro no cálculo")
        
        print("-" * 30)

if __name__ == "__main__":
    print("ESCOLHA O TIPO DE TESTE:")
    print("1 - Simulação automática de conversa")
    print("2 - Teste interativo")
    print("3 - Teste do sistema de preços")
    print("4 - Todos os testes")
    
    choice = input("\nDigite sua opção (1-4): ").strip()
    
    if choice == "1":
        simulate_conversation()
    elif choice == "2":
        interactive_test()
    elif choice == "3":
        test_pricing_system()
    elif choice == "4":
        simulate_conversation()
        print("\n" + "=" * 50)
        test_pricing_system()
    else:
        print("Opção inválida!")