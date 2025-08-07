import logging
from typing import Dict

def calculate_price_with_zones(pickup: str, destination: str, passengers: int) -> Dict:
    """
    Sistema de preços por zonas que não depende de API externa
    Mais econômico e previsível para o cliente
    """
    pickup_lower = pickup.lower()
    destination_lower = destination.lower()
    
    # Define zonas da cidade com preços fixos
    zones = {
        'centro': ['centro', 'centro historico', 'arsenal', 'port', 'rodoviaria', 'hospital'],
        'zona_norte': ['coophamil', 'jardim leblon', 'santa rosa'],
        'zona_sul': ['goiabeiras', 'duque de caxias'],
        'zona_leste': ['despraiado', 'verdao'],
        'zona_oeste': ['lixao'],
        'outros': []  # Locais não mapeados
    }
    
    # Tabela de preços por zona (origem -> destino)
    zone_prices = {
        ('centro', 'centro'): 15.00,
        ('centro', 'zona_norte'): 18.00,
        ('centro', 'zona_sul'): 16.00,
        ('centro', 'zona_leste'): 20.00,
        ('centro', 'zona_oeste'): 22.00,
        ('zona_norte', 'centro'): 18.00,
        ('zona_norte', 'zona_norte'): 15.00,
        ('zona_norte', 'zona_sul'): 20.00,
        ('zona_sul', 'centro'): 16.00,
        ('zona_sul', 'zona_sul'): 15.00,
        ('zona_leste', 'centro'): 20.00,
        ('zona_oeste', 'centro'): 22.00,
    }
    
    def get_zone(address: str) -> str:
        address_lower = address.lower()
        for zone_name, locations in zones.items():
            for location in locations:
                if location in address_lower:
                    return zone_name
        return 'outros'
    
    pickup_zone = get_zone(pickup)
    destination_zone = get_zone(destination)
    
    # Busca preço na tabela
    price_key = (pickup_zone, destination_zone)
    reverse_key = (destination_zone, pickup_zone)
    
    if price_key in zone_prices:
        base_price = zone_prices[price_key]
    elif reverse_key in zone_prices:
        base_price = zone_prices[reverse_key]
    else:
        # Preço padrão para zonas não mapeadas
        if pickup_zone == 'outros' or destination_zone == 'outros':
            base_price = 25.00  # Preço mais alto para locais desconhecidos
        else:
            base_price = 20.00  # Preço médio entre zonas
    
    # Ajuste por número de passageiros
    if passengers >= 2:
        base_price = max(base_price, 18.00)  # Mínimo R$18 para 2+ pessoas
    else:
        base_price = max(base_price, 15.00)  # Mínimo R$15 para 1 pessoa
    
    return {
        'price': base_price,
        'pickup_zone': pickup_zone,
        'destination_zone': destination_zone,
        'method': 'zone_based_pricing',
        'estimated_distance': get_estimated_distance_by_zone(pickup_zone, destination_zone)
    }

def get_estimated_distance_by_zone(origin_zone: str, dest_zone: str) -> float:
    """
    Estima distância baseada nas zonas (aproximação)
    """
    distance_matrix = {
        ('centro', 'centro'): 2.5,
        ('centro', 'zona_norte'): 4.0,
        ('centro', 'zona_sul'): 3.5,
        ('centro', 'zona_leste'): 6.0,
        ('centro', 'zona_oeste'): 8.0,
        ('zona_norte', 'zona_norte'): 2.0,
        ('zona_norte', 'zona_sul'): 5.5,
        ('zona_sul', 'zona_sul'): 2.0,
        ('outros', 'centro'): 7.0,
    }
    
    key = (origin_zone, dest_zone)
    reverse_key = (dest_zone, origin_zone)
    
    if key in distance_matrix:
        return distance_matrix[key]
    elif reverse_key in distance_matrix:
        return distance_matrix[reverse_key]
    else:
        return 5.0  # Distância padrão

def should_use_zone_pricing(pickup: str, destination: str) -> bool:
    """
    Determina se deve usar preços por zona ou cálculo por distância
    """
    pickup_lower = pickup.lower()
    destination_lower = destination.lower()
    
    # Lista de palavras-chave que indicam locais conhecidos
    known_keywords = [
        'centro', 'arsenal', 'port', 'hospital', 'rodoviaria',
        'coophamil', 'jardim', 'santa rosa', 'goiabeiras',
        'duque de caxias', 'despraiado', 'verdao', 'lixao'
    ]
    
    pickup_known = any(keyword in pickup_lower for keyword in known_keywords)
    destination_known = any(keyword in destination_lower for keyword in known_keywords)
    
    return pickup_known and destination_known

def get_pricing_explanation(method: str, pickup_zone: str = None, dest_zone: str = None) -> str:
    """
    Retorna explicação do método de preço usado
    """
    if method == 'zone_based_pricing':
        return f"Preço por zona: {pickup_zone} → {dest_zone}"
    elif method == 'local_calculation':
        return "Cálculo local baseado em coordenadas"
    elif method == 'google_maps_api':
        return "Cálculo preciso via Google Maps"
    else:
        return "Estimativa padrão"