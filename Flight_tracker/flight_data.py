class FlightData:
    """Stores information about a flight including price and route details"""
    
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops):
        """
        Create a new FlightData instance
        
        Args:
            price: Flight price
            origin_airport: IATA code for origin airport
            destination_airport: IATA code for destination airport
            out_date: Departure date
            return_date: Return date
            stops: Number of stops (0 for direct flights)
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops
    
    def __str__(self):
        """String representation of flight data"""
        flight_type = "Direct" if self.stops == 0 else f"{self.stops} stop(s)"
        return (f"{flight_type} flight from {self.origin_airport} to {self.destination_airport}: "
                f"£{self.price} ({self.out_date} - {self.return_date})")

def create_empty_flight():
    """Create a FlightData object with placeholder values"""
    return FlightData(
        price="N/A",
        origin_airport="N/A",
        destination_airport="N/A",
        out_date="N/A",
        return_date="N/A",
        stops="N/A"
    )

def extract_flight_details(flight_data):
    """
    Extract relevant details from a flight offer
    
    Args:
        flight_data: Flight offer data from API
        
    Returns:
        tuple: (price, origin, destination, out_date, return_date, stops)
    """
    # Get price
    price = float(flight_data["price"]["grandTotal"])
    
    # Get outbound flight details
    outbound = flight_data["itineraries"][0]
    outbound_segments = outbound["segments"]
    origin = outbound_segments[0]["departure"]["iataCode"]
    
    # Calculate stops
    stops = len(outbound_segments) - 1
    
    # Get destination (last segment's arrival)
    destination = outbound_segments[-1]["arrival"]["iataCode"]
    
    # Extract dates (removing time part)
    out_date = outbound_segments[0]["departure"]["at"].split("T")[0]
    
    # Get return flight date
    return_segments = flight_data["itineraries"][1]["segments"]
    return_date = return_segments[0]["departure"]["at"].split("T")[0]
    
    return price, origin, destination, out_date, return_date, stops

def find_cheapest_flight(data):
    """
    Find the cheapest flight from API response data
    
    Args:
        data: Flight search API response data
        
    Returns:
        FlightData: Object containing details of the cheapest flight
    """
    # Check if we have valid flight data
    if not data or not data.get('data') or len(data['data']) == 0:
        print("No valid flight data available")
        return create_empty_flight()
    
    flights = data['data']
    cheapest_price = float('inf')
    cheapest_flight_details = None
    
    # Find the cheapest flight
    for flight in flights:
        try:
            price, origin, destination, out_date, return_date, stops = extract_flight_details(flight)
            
            if price < cheapest_price:
                cheapest_price = price
                cheapest_flight_details = (price, origin, destination, out_date, return_date, stops)
                print(f"Found cheaper flight to {destination}: £{price}")
                
        except (KeyError, IndexError) as e:
            print(f"Error processing flight data: {e}")
            continue
    
    # If we found a valid flight, return it
    if cheapest_flight_details:
        return FlightData(*cheapest_flight_details)
    
    # Otherwise return empty flight data
    return create_empty_flight()