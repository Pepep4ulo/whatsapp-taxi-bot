from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Ride:
    """Data class for ride information"""
    id: str
    customer_phone: str
    customer_name: Optional[str]
    passengers: int
    pickup_location: str
    destination: str
    distance_km: float
    duration_minutes: int
    price: float
    status: str  # 'pending', 'confirmed', 'cancelled', 'completed'
    created_at: datetime
    confirmed_at: Optional[datetime] = None
    
    def to_dict(self):
        """Convert ride to dictionary"""
        return {
            'id': self.id,
            'customer_phone': self.customer_phone,
            'customer_name': self.customer_name,
            'passengers': self.passengers,
            'pickup_location': self.pickup_location,
            'destination': self.destination,
            'distance_km': self.distance_km,
            'duration_minutes': self.duration_minutes,
            'price': self.price,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create ride from dictionary"""
        return cls(
            id=data['id'],
            customer_phone=data['customer_phone'],
            customer_name=data.get('customer_name'),
            passengers=data['passengers'],
            pickup_location=data['pickup_location'],
            destination=data['destination'],
            distance_km=data['distance_km'],
            duration_minutes=data['duration_minutes'],
            price=data['price'],
            status=data['status'],
            created_at=datetime.fromisoformat(data['created_at']),
            confirmed_at=datetime.fromisoformat(data['confirmed_at']) if data.get('confirmed_at') else None
        )

@dataclass
class CustomerSession:
    """Data class for customer session state"""
    phone: str
    step: str  # 'start', 'passengers', 'pickup', 'destination', 'quote_sent'
    passengers: Optional[int] = None
    pickup_location: Optional[str] = None
    destination: Optional[str] = None
    current_ride_id: Optional[str] = None
    
    def to_dict(self):
        return {
            'phone': self.phone,
            'step': self.step,
            'passengers': self.passengers,
            'pickup_location': self.pickup_location,
            'destination': self.destination,
            'current_ride_id': self.current_ride_id
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            phone=data['phone'],
            step=data['step'],
            passengers=data.get('passengers'),
            pickup_location=data.get('pickup_location'),
            destination=data.get('destination'),
            current_ride_id=data.get('current_ride_id')
        )
