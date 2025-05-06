import time
from datetime import datetime, timedelta
import logging
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("flight_finder")

def setup_services():
    """Initialize and connect to all required services"""
    logger.info("Setting up services...")
    
    try:
        data_manager = DataManager()
        flight_search = FlightSearch()
        notification_manager = NotificationManager()
        
        return data_manager, flight_search, notification_manager
        
    except Exception as e:
        logger.error(f"Error setting up services: {e}")
        raise

def update_destination_codes(data_manager, flight_search, destinations):
    """Update missing IATA codes for destinations"""
    logger.info("Updating destination codes...")
    
    updated = False
    
    for destination in destinations:
        if not destination.get("iataCode"):
            city = destination.get("city", "Unknown")
            logger.info(f"Getting IATA code for {city}...")
            
            # Get code and add delay to avoid rate limiting
            destination["iataCode"] = flight_search.get_destination_code(city)
            time.sleep(1)
            updated = True
    
    # Update codes in database if changes were made
    if updated:
        data_manager.destination_data = destinations
        data_manager.update_destination_codes()
    
    return destinations

def search_for_flights(flight_search, destinations, origin_code, search_period):
    """Search for flights to all destinations"""
    logger.info(f"Searching flights from {origin_code}...")
    
    tomorrow, six_months_later = search_period
    results = []
    
    for destination in destinations:
        city = destination.get("city", "Unknown")
        destination_code = destination.get("iataCode")
        
        if not destination_code or destination_code in ["N/A", "Not Found"]:
            logger.warning(f"No valid IATA code for {city}, skipping flight search")
            continue
        
        # Search for direct flights first
        logger.info(f"Searching direct flights to {city}...")
        flights = flight_search.check_flights(
            origin_code,
            destination_code,
            from_time=tomorrow,
            to_time=six_months_later
        )
        
        cheapest_flight = find_cheapest_flight(flights)
        
        # If no direct flights, try with connections
        if cheapest_flight.price == "N/A":
            logger.info(f"No direct flights to {city}, trying with connections...")
            indirect_flights = flight_search.check_flights(
                origin_code,
                destination_code,
                from_time=tomorrow,
                to_time=six_months_later,
                is_direct=False
            )
            cheapest_flight = find_cheapest_flight(indirect_flights)
        
        # Add to results
        results.append({
            "destination": destination,
            "flight": cheapest_flight
        })
        
        # Avoid rate limiting
        time.sleep(1)
    
    return results

def check_for_deals(flight_results):
    """Find flights that are cheaper than our target price"""
    logger.info("Checking for flight deals...")
    
    deals = []
    for result in flight_results:
        destination = result["destination"]
        flight = result["flight"]
        
        # Skip flights with no price data
        if flight.price == "N/A":
            continue
            
        lowest_price = destination.get("lowestPrice", float("inf"))
        
        if flight.price < lowest_price:
            logger.info(f"Deal found: {destination['city']} for £{flight.price} (below £{lowest_price})")
            deals.append(result)
    
    return deals

def format_deal_message(deal):
    """Format notification message for a flight deal"""
    destination = deal["destination"]
    flight = deal["flight"]
    
    city = destination.get("city", "your destination")
    
    if flight.stops == 0:
        message = (
            f"Low price alert! Only £{flight.price} to fly direct "
            f"from {flight.origin_airport} to {flight.destination_airport}, "
            f"on {flight.out_date} until {flight.return_date}."
        )
    else:
        message = (
            f"Low price alert! Only £{flight.price} to fly "
            f"from {flight.origin_airport} to {flight.destination_airport}, "
            f"with {flight.stops} stop(s) "
            f"departing on {flight.out_date} and returning on {flight.return_date}."
        )
    
    return message

def send_notifications(notification_manager, deals, email_list):
    """Send notifications for all flight deals"""
    logger.info(f"Sending notifications for {len(deals)} deals...")
    
    for deal in deals:
        message = format_deal_message(deal)
        city = deal["destination"].get("city", "your destination")
        
        # Send WhatsApp notification
        notification_manager.send_whatsapp(message_body=message)
        
        # Send email notifications
        if email_list:
            notification_manager.send_emails(email_list=email_list, email_body=message)
            logger.info(f"Notifications sent for {city} deal")

def main():
    """Main flight finder program"""
    try:
        # Initialize services
        data_manager, flight_search, notification_manager = setup_services()
        
        # Set search parameters
        ORIGIN_CITY_IATA = "LON"
        tomorrow = datetime.now() + timedelta(days=1)
        six_months_from_today = datetime.now() + timedelta(days=(6 * 30))
        search_period = (tomorrow, six_months_from_today)
        
        # Get destination data
        destinations = data_manager.get_destination_data()
        logger.info(f"Found {len(destinations)} destinations to check")
        
        # Update missing IATA codes
        destinations = update_destination_codes(data_manager, flight_search, destinations)
        
        # Get customer emails
        customers = data_manager.get_customer_emails()
        email_list = [row.get("whatIsYourEmail?") for row in customers if "whatIsYourEmail?" in row]
        logger.info(f"Found {len(email_list)} customer email addresses")
        
        # Search for flights
        flight_results = search_for_flights(flight_search, destinations, ORIGIN_CITY_IATA, search_period)
        
        # Check for deals
        deals = check_for_deals(flight_results)
        
        if deals:
            logger.info(f"Found {len(deals)} flight deals!")
            send_notifications(notification_manager, deals, email_list)
        else:
            logger.info("No flight deals found today")
            
    except Exception as e:
        logger.error(f"Program error: {e}")
        raise

if __name__ == "__main__":
    main()