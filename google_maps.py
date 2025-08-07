import os
import requests
import logging

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

def get_distance_and_duration(origin: str, destination: str):
    """
    Get distance and duration between two locations using Google Maps Distance Matrix API
    
    Returns:
        dict: {'distance_km': float, 'duration_minutes': int} or None if error
    """
    try:
        if not GOOGLE_MAPS_API_KEY:
            logging.error("Google Maps API key not found")
            return None
            
        # Distance Matrix API endpoint
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        
        params = {
            'origins': origin,
            'destinations': destination,
            'units': 'metric',
            'mode': 'driving',
            'key': GOOGLE_MAPS_API_KEY,
            'language': 'pt-BR',
            'region': 'BR'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if the API response is valid
        if data['status'] != 'OK':
            logging.error(f"Google Maps API error: {data['status']}")
            return None
            
        # Get the first (and only) element from the matrix
        element = data['rows'][0]['elements'][0]
        
        if element['status'] != 'OK':
            logging.error(f"Route calculation error: {element['status']}")
            return None
            
        # Extract distance and duration
        distance_meters = element['distance']['value']
        duration_seconds = element['duration']['value']
        
        # Convert to km and minutes
        distance_km = distance_meters / 1000
        duration_minutes = duration_seconds // 60
        
        logging.info(f"Route calculated: {distance_km:.1f}km, {duration_minutes} minutes")
        
        return {
            'distance_km': distance_km,
            'duration_minutes': duration_minutes
        }
        
    except requests.RequestException as e:
        logging.error(f"HTTP error getting route data: {str(e)}")
        return None
        
    except KeyError as e:
        logging.error(f"Unexpected API response format: {str(e)}")
        return None
        
    except Exception as e:
        logging.error(f"Error calculating route: {str(e)}")
        return None

def geocode_address(address: str):
    """
    Convert address to coordinates using Google Geocoding API
    
    Returns:
        dict: {'lat': float, 'lng': float, 'formatted_address': str} or None if error
    """
    try:
        if not GOOGLE_MAPS_API_KEY:
            logging.error("Google Maps API key not found")
            return None
            
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        
        params = {
            'address': address,
            'key': GOOGLE_MAPS_API_KEY,
            'language': 'pt-BR',
            'region': 'BR'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['status'] != 'OK' or not data['results']:
            logging.error(f"Geocoding error: {data['status']}")
            return None
            
        result = data['results'][0]
        location = result['geometry']['location']
        
        return {
            'lat': location['lat'],
            'lng': location['lng'],
            'formatted_address': result['formatted_address']
        }
        
    except Exception as e:
        logging.error(f"Error geocoding address: {str(e)}")
        return None
