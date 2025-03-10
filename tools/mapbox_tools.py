import requests
from typing import Dict, List, Optional
from smolagents import tool
import math, os

# constants
WGS84_AVG_EARTH_RADIUS = 637100080.0  # in centimeters
_180_div_PI = 180.0 / math.pi

MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")

@tool
def geocode_location(location: str) -> Dict:
    """Converts a location name to latitude and longitude coordinates using Mapbox.
    Args:
        location: A string describing a location (e.g., 'New York City', 'Paris, France')
    """
    # URL encode the location
    encoded_location = requests.utils.quote(location)
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{encoded_location}.json?access_token={MAPBOX_ACCESS_TOKEN}"
    
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and data.get('features') and len(data['features']) > 0:
        # Mapbox returns coordinates as [longitude, latitude]
        lng, lat = data['features'][0]['center']
        place_name = data['features'][0]['place_name']
        return {
            "success": True,
            "latitude": lat,
            "longitude": lng,
            "formatted_address": place_name
        }
    else:
        return {
            "success": False,
            "error": "GEOCODE_FAILED",
            "message": "Could not geocode the location"
        }
    
@tool
def search_nearby_places(latitude: float, longitude: float, radius: int = 1000, category: str = "food_and_drink") -> Dict:
    """Searches for restaurants around a specific location using Mapbox Search API.
    Args:
        latitude: The latitude coordinate of the center point
        longitude: The longitude coordinate of the center point
        radius: The radius (in meters) to search within
        category: Point of Interest (POI) category to search
    """
    # Mapbox Search API endpoint
    url = f"https://api.mapbox.com/search/searchbox/v1/category/{category}"

    min_latlong = shifted_coordinates({'latitude': latitude, 'longitude': longitude}, -radius, -radius)
    max_latlong = shifted_coordinates({'latitude': latitude, 'longitude': longitude}, radius, radius)
    
    # Parameters for the API request
    params = {
        "access_token": MAPBOX_ACCESS_TOKEN,
        "proximity": f"{longitude},{latitude}",  # Note: Mapbox uses lon,lat order
        "bbox": f"{min_latlong['longitude']},{min_latlong['latitude']},{max_latlong['longitude']},{max_latlong['latitude']}",
        "limit": 20  # Maximum number of results to return
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200 and "features" in data:
        places = []
        for place in data["features"]:
            properties = place.get("properties", {})
            geometry = place.get("geometry", {})
            
            # Extract coordinate information
            coordinates = geometry.get("coordinates", [0, 0]) if geometry.get("type") == "Point" else [0, 0]
            
            places.append({
                "name": properties.get("name", "Unknown"),
                "address": properties.get("address", "No address available"),
                "place_id": place.get("id", ""),
                "categories": properties.get("category", {}).get("names", []),
                "types": [properties.get("category", {}).get("primary", "restaurant")],
                "location": {
                    "lng": coordinates[0],
                    "lat": coordinates[1]
                },
                "distance": properties.get("distance", None)  # Distance in meters
            })
        
        return {
            "success": True,
            "places_found": len(places),
            "places": places
        }
    else:
        error_message = data.get("message", "Unknown error") if isinstance(data, dict) else "Failed to parse response"
        return {
            "success": False,
            "error": f"SEARCH_FAILED: {response.status_code}",
            "message": error_message
        }
        
def shifted_coordinates(curr_pos: Dict, lon_meter: float, lat_meter: float) -> Dict:
     """
     Shift the coordinates of the current position by the specified meters.
     Args:
        curr_pos (dict): A dictionary with 'latitude' and 'longitude' keys.
        lon_meter (float): The shift in meters along the longitude.
        lat_meter (float): The shift in meters along the latitude.
     """
     
     # Convert degrees to radians  
     coslat = math.cos(curr_pos['latitude'] * (1 / _180_div_PI))
     # convert to cm
     dlon = lon_meter * 100.0 / WGS84_AVG_EARTH_RADIUS / coslat
     dlat = lat_meter * 100.0 / WGS84_AVG_EARTH_RADIUS
     shifted_pos = {}
     shifted_pos['longitude'] = curr_pos['longitude'] + dlon * _180_div_PI
     shifted_pos['latitude'] = curr_pos['latitude'] + dlat * _180_div_PI
     return shifted_pos