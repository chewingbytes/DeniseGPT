import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='../.env')

def get_weather_info(lat, lon):
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"

        response = requests.get(api_url)

        if response.status_code != 200:
            raise Exception(f"HTTP error! Status: {response.status_code}")

        data = response.json()
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']
        visibility = data['visibility']
        rain_volume = data['rain']['1h'] if 'rain' in data else 0
        cloudiness = data['clouds']['all']

        weather_string = (
            f"Temperature: {temperature} °C\n"
            f"Feels Like: {feels_like} °C\n"
            f"Description: {description}\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Humidity: {humidity}%\n"
            f"Visibility: {visibility} meters\n"
            f"Rain Volume: {rain_volume} mm\n"
            f"Cloudiness: {cloudiness}%"
        )

        print(f"weather details:\n{weather_string}")
        return weather_string

    except Exception as error:
        error_message = f"Error fetching weather information: {error}"
        return error_message
