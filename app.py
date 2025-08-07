import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from whatsapp_bot import handle_whatsapp_message
from data_store import get_all_rides, get_ride_stats
from distance_calculator import get_distance_stats

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    """Main dashboard page"""
    stats = get_ride_stats()
    distance_stats = get_distance_stats()
    return render_template('index.html', stats=stats, distance_stats=distance_stats)

@app.route('/rides')
def rides():
    """Page to view all rides"""
    all_rides = get_all_rides()
    return render_template('rides.html', rides=all_rides)

@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Webhook endpoint for WhatsApp messages"""
    try:
        # Get the incoming message data
        incoming_msg = request.form.get('Body', '').strip()
        from_number = request.form.get('From', '')
        
        logging.info(f"Received message from {from_number}: {incoming_msg}")
        
        # Handle the message
        response = handle_whatsapp_message(from_number, incoming_msg)
        
        return response, 200
        
    except Exception as e:
        logging.error(f"Error handling WhatsApp message: {str(e)}")
        return "Error processing message", 500

@app.route('/api/rides')
def api_rides():
    """API endpoint to get rides data"""
    rides = get_all_rides()
    return jsonify(rides)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
