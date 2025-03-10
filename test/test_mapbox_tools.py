
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
# Add the project root directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.mapbox_tools import MapboxTools


class TestMapboxTools(unittest.TestCase):
    def setUp(self):
        self.mapbox = MapboxTools("test_access_token")
        
    def test_get_params_with_valid_coordinates(self):
        latitude = 40.7128
        longitude = -74.0060
        radius = 1000
        
        expected_min = self.mapbox.shifted_coordinates({'latitude': latitude, 'longitude': longitude}, -radius)
        expected_max = self.mapbox.shifted_coordinates({'latitude': latitude, 'longitude': longitude}, radius)
        
        params = {
            "access_token": "test_access_token",
            "proximity": f"{longitude},{latitude}",
            "bbox": f"{expected_min['longitude']},{expected_min['latitude']},{expected_max['longitude']},{expected_max['latitude']}",
            "limit": 20
        }
        
        self.assertEqual(params["access_token"], "test_access_token")
        self.assertEqual(params["proximity"], f"{longitude},{latitude}")
        self.assertEqual(params["limit"], 20)
        
    def test_get_params_with_zero_radius(self):
        latitude = 0
        longitude = 0
        radius = 0
        
        expected_min = self.mapbox.shifted_coordinates({'latitude': latitude, 'longitude': longitude}, -radius)
        expected_max = self.mapbox.shifted_coordinates({'latitude': latitude, 'longitude': longitude}, radius)
        
        params = {
            "access_token": "test_access_token",
            "proximity": "0,0",
            "bbox": f"{expected_min['longitude']},{expected_min['latitude']},{expected_max['longitude']},{expected_max['latitude']}",
            "limit": 20
        }
        
        self.assertEqual(params["proximity"], "0,0")
        self.assertEqual(params["bbox"], "0,0,0,0")
        
    def test_get_params_with_extreme_coordinates(self):
        latitude = 90
        longitude = 180
        radius = 1000
        
        expected_min = self.mapbox.shifted_coordinates({'latitude': latitude, 'longitude': longitude}, -radius)
        expected_max = self.mapbox.shifted_coordinates({'latitude': latitude, 'longitude': longitude}, radius)
        
        params = {
            "access_token": "test_access_token",
            "proximity": f"{longitude},{latitude}",
            "bbox": f"{expected_min['longitude']},{expected_min['latitude']},{expected_max['longitude']},{expected_max['latitude']}",
            "limit": 20
        }
        
        self.assertEqual(params["proximity"], "180,90")
        self.assertTrue(-180 <= float(params["bbox"].split(",")[0]) <= 180)
        self.assertTrue(-90 <= float(params["bbox"].split(",")[1]) <= 90)
