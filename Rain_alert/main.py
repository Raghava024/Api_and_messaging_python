import requests
from twilio.rest import Client

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = "__YOUR_OWM_API_KEY__"
ACCOUNT_SID = "__YOUR_TWILIO_ACCOUNT_ID__"
AUTH_TOKEN = "__YOUR_TWILIO_AUTH_TOKEN__"

LOCATION = {
    "lat": 46.947975,
    "lon": 7.447447,
}

RAIN_THRESHOLD_CODE = 700
FORECAST_HOURS = 4

def fetch_weather_data(location, hours, api_key):
    params = {
        **location,
        "cnt": hours,
        "appid": api_key
    }
    response = requests.get(OWM_ENDPOINT, params=params)
    response.raise_for_status()
    return response.json()["list"]

def is_rain_expected(weather_list):
    return any(int(hour["weather"][0]["id"]) < RAIN_THRESHOLD_CODE for hour in weather_list)

def notify_rain_alert(account_sid, auth_token):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella.",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER"
    )
    print(f"Message status: {message.status}")

def main():
    weather_forecast = fetch_weather_data(LOCATION, FORECAST_HOURS, API_KEY)
    if is_rain_expected(weather_forecast):
        notify_rain_alert(ACCOUNT_SID, AUTH_TOKEN)

if __name__ == "__main__":
    main()
