import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class FlightSearch:
    """Handles flight search operations using the Amadeus API"""
    
    # Class-level constants for API endpoints
    IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
    FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
    
    def __init__(self):
        """Initialize flight search with API credentials and authentication token"""
        self._api_key = os.environ.get("AMADEUS_API_KEY")
        self._api_secret = os.environ.get("AMADEUS_SECRET")
        
        # Validate API credentials
        if not self._api_key or not self._api_secret:
            raise ValueError("Missing Amadeus API credentials in environment variables")
            
        self._token = self._authenticate()
        
    def _authenticate(self):
        """Get authentication token from Amadeus API"""
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        
        try:
            response = requests.post(
                url=self.TOKEN_ENDPOINT, 
                headers=headers, 
                data=auth_data
            )
            response.raise_for_status()  # Raise exception for HTTP errors
            
            token_data = response.json()
            token = token_data['access_token']
            expires_in = token_data['expires_in']
            
            print(f"Authentication successful. Token expires in {expires_in} seconds")
            return token
            
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            raise
    
    def get_destination_code(self, city_name):
        """
        Get IATA code for a city
        
        Args:
            city_name: Name of the city to search for
            
        Returns:
            str: IATA code for the city or error message if not found
        """
        if not city_name:
            return "N/A"
            
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        
        try:
            response = requests.get(
                url=self.IATA_ENDPOINT,
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Try to extract the IATA code from response
            if "data" in data and data["data"]:
                return data["data"][0].get('iataCode', "Not Found")
            else:
                print(f"No airport data found for {city_name}")
                return "N/A"
                
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error getting destination code for {city_name}: {e}")
            return "N/A"
        except requests.exceptions.RequestException as e:
            print(f"Request error getting destination code for {city_name}: {e}")
            return "N/A"
        except (KeyError, IndexError) as e:
            print(f"Data error getting destination code for {city_name}: {e}")
            return "N/A"

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        """
        Search for flights between two cities on specified dates
        
        Args:
            origin_city_code: IATA code of departure city
            destination_city_code: IATA code of destination city
            from_time: Departure date as datetime object
            to_time: Return date as datetime object
            is_direct: Whether to search for direct flights only
            
        Returns:
            dict or None: Flight offer data or None if request failed
        """
        if not all([origin_city_code, destination_city_code, from_time, to_time]):
            print("Missing required parameters for flight search")
            return None
            
        headers = {"Authorization": f"Bearer {self._token}"}
        
        # Format dates as YYYY-MM-DD
        departure_date = from_time.strftime("%Y-%m-%d")
        return_date = to_time.strftime("%Y-%m-%d")
        
        params = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "GBP",
            "max": "10",
        }

        try:
            response = requests.get(
                url=self.FLIGHT_ENDPOINT,
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') else "unknown"
            print(f"Flight search failed with status code: {status_code}")
            print(f"Error details: {e}")
            print("For more information, see: "
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error during flight search: {e}")
            return None