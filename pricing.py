import logging

def calculate_price(distance_km: float, passengers: int) -> float:
    """
    Calculate ride price based on distance and number of passengers
    
    Pricing rules:
    - R$1.50 per km
    - Minimum R$15 for 1 passenger
    - Fixed R$18 for 2+ passengers (if higher than distance-based price)
    
    Args:
        distance_km: Distance in kilometers
        passengers: Number of passengers
        
    Returns:
        float: Final price in BRL
    """
    try:
        # Base calculation: R$1.50 per km
        base_price = distance_km * 1.50
        
        if passengers == 1:
            # For 1 passenger: minimum R$15
            final_price = max(base_price, 15.0)
            
        else:
            # For 2+ passengers: minimum R$18 or distance-based price, whichever is higher
            final_price = max(base_price, 18.0)
        
        logging.info(f"Price calculated: {distance_km:.1f}km, {passengers} passengers = R${final_price:.2f}")
        
        return round(final_price, 2)
        
    except Exception as e:
        logging.error(f"Error calculating price: {str(e)}")
        # Return minimum price as fallback
        return 15.0 if passengers == 1 else 18.0

def get_price_breakdown(distance_km: float, passengers: int) -> dict:
    """
    Get detailed price breakdown for transparency
    
    Returns:
        dict: Breakdown of price calculation
    """
    try:
        base_price = distance_km * 1.50
        minimum_price = 15.0 if passengers == 1 else 18.0
        final_price = max(base_price, minimum_price)
        
        return {
            'distance_km': distance_km,
            'passengers': passengers,
            'rate_per_km': 1.50,
            'base_price': round(base_price, 2),
            'minimum_price': minimum_price,
            'final_price': round(final_price, 2),
            'price_used': 'distance' if base_price >= minimum_price else 'minimum'
        }
        
    except Exception as e:
        logging.error(f"Error getting price breakdown: {str(e)}")
        return {
            'error': str(e),
            'final_price': 15.0 if passengers == 1 else 18.0
        }
