from smolagents import tool
import sys
import os

# Add the project root directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.mapbox_tools import geocode_location, search_nearby_places
import os



def explore_restaurants_in_berlin():
    # Step 1: Convert the location "Berlin" to coordinates
    location_result = geocode_location("Get me the restaurants around Berlin City Center, Germany")
    
    if not location_result["success"]:
        return f"Failed to geocode location: {location_result['message']}"
    
    # Extract coordinates
    lat = location_result["latitude"]
    lng = location_result["longitude"]
    address = location_result["formatted_address"]
    
    print(f"Located: {address} at coordinates: {lat}, {lng}")
    
    # Step 2: Define search radius (1000 meters = 1km)
    radius = 1000
    
    # Step 3: Search for restaurants near the coordinates
    restaurants = search_nearby_places(
        latitude=lat,
        longitude=lng,
        radius=radius,
        category="food_and_drink"
    )
    
    if not restaurants["success"]:
        return f"Failed to find restaurants: {restaurants['message']}"
    
    # Step 4: Format and return the results
    result = f"Found {restaurants['places_found']} restaurants within {radius}m of Berlin City Center:\n\n"
    
    for i, place in enumerate(restaurants["places"], 1):
        result += f"{i}. {place['name']}\n"
        result += f"   Address: {place['address']}\n"
        result += f"   Categories: {', '.join(place['types'])}\n\n"
    
    return result

if __name__ == "__main__":
    print(explore_restaurants_in_berlin())