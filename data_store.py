import json
import os
import logging
from datetime import datetime
from typing import List, Optional
from models import Ride, CustomerSession

# File paths for data storage
RIDES_FILE = 'rides.json'
SESSIONS_FILE = 'sessions.json'

def ensure_data_files():
    """Ensure data files exist"""
    for file_path in [RIDES_FILE, SESSIONS_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

def save_ride(ride: Ride):
    """Save a ride to the data store"""
    try:
        ensure_data_files()
        
        # Read existing rides
        with open(RIDES_FILE, 'r') as f:
            rides = json.load(f)
        
        # Add new ride
        rides.append(ride.to_dict())
        
        # Save back to file
        with open(RIDES_FILE, 'w') as f:
            json.dump(rides, f, indent=2)
            
        logging.info(f"Ride {ride.id} saved successfully")
        
    except Exception as e:
        logging.error(f"Error saving ride: {str(e)}")

def get_ride(ride_id: str) -> Optional[Ride]:
    """Get a specific ride by ID"""
    try:
        ensure_data_files()
        
        with open(RIDES_FILE, 'r') as f:
            rides = json.load(f)
        
        for ride_data in rides:
            if ride_data['id'] == ride_id:
                return Ride.from_dict(ride_data)
                
        return None
        
    except Exception as e:
        logging.error(f"Error getting ride {ride_id}: {str(e)}")
        return None

def update_ride_status(ride_id: str, new_status: str):
    """Update the status of a ride"""
    try:
        ensure_data_files()
        
        with open(RIDES_FILE, 'r') as f:
            rides = json.load(f)
        
        for ride_data in rides:
            if ride_data['id'] == ride_id:
                ride_data['status'] = new_status
                if new_status == 'confirmed':
                    ride_data['confirmed_at'] = datetime.now().isoformat()
                break
        
        with open(RIDES_FILE, 'w') as f:
            json.dump(rides, f, indent=2)
            
        logging.info(f"Ride {ride_id} status updated to {new_status}")
        
    except Exception as e:
        logging.error(f"Error updating ride status: {str(e)}")

def get_all_rides() -> List[Ride]:
    """Get all rides"""
    try:
        ensure_data_files()
        
        with open(RIDES_FILE, 'r') as f:
            rides_data = json.load(f)
        
        rides = [Ride.from_dict(ride_data) for ride_data in rides_data]
        
        # Sort by creation date (newest first)
        rides.sort(key=lambda x: x.created_at, reverse=True)
        
        return rides
        
    except Exception as e:
        logging.error(f"Error getting all rides: {str(e)}")
        return []

def save_session(session: CustomerSession):
    """Save a customer session"""
    try:
        ensure_data_files()
        
        with open(SESSIONS_FILE, 'r') as f:
            sessions = json.load(f)
        
        # Remove existing session for this phone number
        sessions = [s for s in sessions if s['phone'] != session.phone]
        
        # Add new session
        sessions.append(session.to_dict())
        
        with open(SESSIONS_FILE, 'w') as f:
            json.dump(sessions, f, indent=2)
            
    except Exception as e:
        logging.error(f"Error saving session: {str(e)}")

def get_session(phone: str) -> Optional[CustomerSession]:
    """Get a customer session by phone number"""
    try:
        ensure_data_files()
        
        with open(SESSIONS_FILE, 'r') as f:
            sessions = json.load(f)
        
        for session_data in sessions:
            if session_data['phone'] == phone:
                return CustomerSession.from_dict(session_data)
                
        return None
        
    except Exception as e:
        logging.error(f"Error getting session: {str(e)}")
        return None

def get_ride_stats():
    """Get statistics about rides"""
    try:
        rides = get_all_rides()
        
        total_rides = len(rides)
        confirmed_rides = len([r for r in rides if r.status == 'confirmed'])
        pending_rides = len([r for r in rides if r.status == 'pending'])
        cancelled_rides = len([r for r in rides if r.status == 'cancelled'])
        
        total_revenue = sum(r.price for r in rides if r.status == 'confirmed')
        
        # Recent rides (last 10)
        recent_rides = rides[:10]
        
        return {
            'total_rides': total_rides,
            'confirmed_rides': confirmed_rides,
            'pending_rides': pending_rides,
            'cancelled_rides': cancelled_rides,
            'total_revenue': total_revenue,
            'recent_rides': recent_rides
        }
        
    except Exception as e:
        logging.error(f"Error getting ride stats: {str(e)}")
        return {
            'total_rides': 0,
            'confirmed_rides': 0,
            'pending_rides': 0,
            'cancelled_rides': 0,
            'total_revenue': 0.0,
            'recent_rides': []
        }
