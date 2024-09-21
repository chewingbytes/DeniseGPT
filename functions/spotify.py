import os
import requests
from dotenv import load_dotenv

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Define a global variable for the access token
global_access_token = None

def get_authorization_token_from_spotify():
    global global_access_token  # Declare the variable as global to modify it
    try:
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": spotify_client_id,
            "client_secret": spotify_client_secret
        }

        response = requests.post(url, headers=headers, data=data)
        response_output = response.json()

        # Unpack the JSON object
        global_access_token = response_output.get('access_token')
        token_type = response_output.get('token_type')
        expires_in = response_output.get('expires_in')

        token_string = (
            f"Access Token: {global_access_token}\nToken Type: {token_type}\nExpires In: {expires_in} seconds"
        )

        print(f"Access token retrieved:\n{token_string}")
        return token_string

    except Exception as error:
        print('Error getting the auth token:', error)
        return str(error)

def pause_playback():
    if global_access_token is None:
        print("Error: No access token available.")
        return "No access token available."

    url = "https://api.spotify.com/v1/me/player/pause"
    headers = {
        "Authorization": f"Bearer {global_access_token}"
    }

    response = requests.put(url, headers=headers)

    if response.status_code == 204:
        print("Playback paused successfully.")
        return "Playback paused successfully."
    else:
        try:
            error_obj = response.json()
        except ValueError:
            error_obj = {"error": "Unable to parse response as JSON", "status": response.status_code, "message": response.text}
        
        error_string = f"Failed to pause playback. Error: {error_obj}"
        print(error_string)
        return error_string