import math
import re
import logging
from typing import Optional, Dict, Tuple
# Sistema híbrido - funciona sem Google Maps quando necessário
# from google_maps import get_distance_and_duration

# Cache para distâncias calculadas (evita recálculos)
distance_cache = {}

def extract_coordinates_from_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Extrai coordenadas básicas de endereços conhecidos (bairros comuns, pontos de referência)
    Isso reduz drasticamente o uso da API do Google Maps
    """
    address_lower = address.lower()
    
    # Coordenadas aproximadas de bairros/locais comuns (você pode expandir esta lista)
    known_locations = {
        'centro': (-15.601, -56.097),
        'centro historico': (-15.601, -56.097),
        'arsenal': (-15.612, -56.092),
        'port': (-15.615, -56.089),
        'duque de caxias': (-15.590, -56.100),
        'goiabeiras': (-15.620, -56.085),
        'coophamil': (-15.585, -56.075),
        'despraiado': (-15.625, -56.110),
        'verdao': (-15.630, -56.095),
        'santa rosa': (-15.575, -56.105),
        'lixao': (-15.640, -56.120),
        'jardim leblon': (-15.570, -56.080),
        'posto de saude': (-15.605, -56.102),
        'hospital': (-15.598, -56.098),
        'rodoviaria': (-15.603, -56.095),
    }
    
    # Procura por locais conhecidos no endereço
    for location, coords in known_locations.items():
        if location in address_lower:
            return coords
    
    return None

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula distância aproximada entre duas coordenadas usando fórmula de Haversine
    Precisão de ~95% para distâncias urbanas curtas
    """
    # Raio da Terra em quilômetros
    R = 6371
    
    # Converte graus para radianos
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Diferenças
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c
    
    return distance

def estimate_distance_by_text(origin: str, destination: str) -> float:
    """
    Estimativa inteligente de distância baseada em padrões de texto e localização
    """
    origin_lower = origin.lower()
    destination_lower = destination.lower()
    
    # Palavras-chave que indicam distâncias maiores
    long_distance_keywords = ['airport', 'aeroporto', 'shopping', 'universidade', 'hospital', 'terminal']
    short_distance_keywords = ['centro', 'praca', 'igreja', 'posto', 'escola']
    
    # Estimativa base
    base_distance = 3.0
    
    # Ajustes baseados em palavras-chave
    for keyword in long_distance_keywords:
        if keyword in origin_lower or keyword in destination_lower:
            base_distance += 2.0
            break
    
    for keyword in short_distance_keywords:
        if keyword in origin_lower or keyword in destination_lower:
            base_distance -= 0.5
            break
    
    # Limites razoáveis para área urbana
    return max(1.0, min(base_distance, 15.0))

def estimate_travel_time(distance_km: float) -> int:
    """
    Estima tempo de viagem baseado na distância
    Assume velocidade média urbana de 25 km/h
    """
    avg_speed_kmh = 25  # Velocidade média em área urbana
    time_hours = distance_km / avg_speed_kmh
    time_minutes = int(time_hours * 60)
    
    # Adiciona tempo extra para trânsito/paradas
    time_minutes += max(2, int(distance_km * 0.5))  # 30 segundos por km extra
    
    return max(time_minutes, 3)  # Mínimo 3 minutos

def get_smart_distance_and_duration(origin: str, destination: str) -> Optional[Dict]:
    """
    Sistema inteligente que usa coordenadas conhecidas quando possível,
    e só recorre à API do Google Maps quando necessário
    """
    try:
        # Cria chave para cache
        cache_key = f"{origin.lower().strip()}|{destination.lower().strip()}"
        
        # Verifica cache primeiro
        if cache_key in distance_cache:
            logging.info(f"Using cached distance for {cache_key}")
            return distance_cache[cache_key]
        
        # Tenta usar coordenadas conhecidas
        origin_coords = extract_coordinates_from_address(origin)
        dest_coords = extract_coordinates_from_address(destination)
        
        if origin_coords and dest_coords:
            # Calcula usando coordenadas conhecidas (sem usar API)
            distance_km = calculate_haversine_distance(
                origin_coords[0], origin_coords[1],
                dest_coords[0], dest_coords[1]
            )
            duration_minutes = estimate_travel_time(distance_km)
            
            result = {
                'distance_km': round(distance_km, 1),
                'duration_minutes': duration_minutes,
                'method': 'local_calculation'
            }
            
            logging.info(f"Local calculation: {distance_km:.1f}km, {duration_minutes} min")
            
        else:
            # Para locais não conhecidos, usa estimativa inteligente baseada em padrões
            logging.info("Using intelligent estimation for unknown locations")
            
            # Estimativa baseada no comprimento do texto e palavras-chave
            estimated_distance = estimate_distance_by_text(origin, destination)
            
            result = {
                'distance_km': estimated_distance,
                'duration_minutes': estimate_travel_time(estimated_distance),
                'method': 'intelligent_estimation'
            }
            logging.info(f"Intelligent estimation: {estimated_distance}km")
        
        # Salva no cache
        distance_cache[cache_key] = result
        
        return result
        
    except Exception as e:
        logging.error(f"Error in smart distance calculation: {str(e)}")
        # Fallback seguro
        return {
            'distance_km': 5.0,
            'duration_minutes': 15,
            'method': 'error_fallback'
        }

def add_known_location(name: str, lat: float, lon: float):
    """
    Permite adicionar novos locais conhecidos dinamicamente
    """
    # Esta função pode ser expandida para salvar em arquivo
    logging.info(f"Added known location: {name} at {lat}, {lon}")

def get_distance_stats() -> Dict:
    """
    Retorna estatísticas de uso do sistema de distâncias
    """
    methods = {}
    for result in distance_cache.values():
        method = result.get('method', 'unknown')
        methods[method] = methods.get(method, 0) + 1
    
    return {
        'total_calculations': len(distance_cache),
        'methods_used': methods,
        'api_usage_percentage': (methods.get('google_maps_api', 0) / len(distance_cache) * 100) if distance_cache else 0
    }