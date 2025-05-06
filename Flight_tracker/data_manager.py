import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DataManager:
    """Manages data retrieval and updates to external data sources"""
    
    def __init__(self):
        """Initialize DataManager with API credentials and endpoints"""
        # Get API credentials from environment variables
        username = os.environ.get("SHEETY_USERNAME")
        password = os.environ.get("SHEETY_PASSWORD")
        
        # Get API endpoints from environment variables
        self.prices_endpoint = os.environ.get("SHEETY_PRICES_ENDPOINT")
        self.users_endpoint = os.environ.get("SHEETY_USERS_ENDPOINT")
        
        # Validate required environment variables
        if not all([username, password, self.prices_endpoint, self.users_endpoint]):
            raise ValueError("Missing required Sheety API credentials or endpoints")
            
        # Set up authentication
        self._auth = HTTPBasicAuth(username, password)
        
        # Initialize data containers
        self.destination_data = []
        self.customer_data = []
    
    def get_destination_data(self):
        """
        Retrieve destination data from the Sheety API
        
        Returns:
            list: List of destination dictionaries
        """
        try:
            response = requests.get(url=self.prices_endpoint, auth=self._auth)
            response.raise_for_status()
            
            data = response.json()
            self.destination_data = data.get("prices", [])
            
            return self.destination_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving destination data: {e}")
            return []
    
    def update_destination_codes(self):
        """Update IATA codes in the destination data sheet"""
        updated_count = 0
        
        for destination in self.destination_data:
            # Skip if there's no ID or IATA code
            if "id" not in destination or "iataCode" not in destination:
                continue
                
            # Prepare update data
            update_data = {
                "price": {
                    "iataCode": destination["iataCode"]
                }
            }
            
            try:
                # Send update request
                response = requests.put(
                    url=f"{self.prices_endpoint}/{destination['id']}",
                    json=update_data,
                    auth=self._auth
                )
                response.raise_for_status()
                updated_count += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Error updating destination {destination.get('city', 'unknown')}: {e}")
        
        print(f"Updated {updated_count} destination(s) with IATA codes")
    
    def get_customer_emails(self):
        """
        Retrieve customer email data from the Sheety API
        
        Returns:
            list: List of customer data dictionaries
        """
        try:
            response = requests.get(url=self.users_endpoint, auth=self._auth)
            response.raise_for_status()
            
            data = response.json()
            self.customer_data = data.get("users", [])
            
            return self.customer_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving customer data: {e}")
            return []