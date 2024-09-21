from pydantic import BaseModel
from PIL import ImageGrab
import requests
import json
import os
import base64
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openAiClient = OpenAI(api_key=openai_key)

async def look_at_screen(query):
    try:
        # Get the current working directory (assumed to be the base directory)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Define the path to the screenshots folder relative to the base directory
        screenshot_folder = os.path.join(base_dir, "screenshots")

        # Ensure the screenshots folder exists
        os.makedirs(screenshot_folder, exist_ok=True)

        # Capture the screenshot
        screenshot = ImageGrab.grab()

        # Generate a unique filename using a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"screenshot_{timestamp}.png"

        # Define the path for the screenshot file
        screenshot_path = os.path.join(screenshot_folder, screenshot_filename)

        # Save the screenshot
        screenshot.save(screenshot_path)

        # Close the screenshot object
        screenshot.close()

        result = await analyze_screenshot(query, screenshot_path)
        return result

    except:
        error = "An error has occured"
        return error


# def get_screenshot_file_paths():
    # # Get the current working directory (assumed to be the base directory)
    # base_dir = os.path.dirname(os.path.abspath(__file__))

    # # Define the path to the screenshots folder relative to the base directory
    # screenshot_folder = os.path.join(base_dir, "screenshots")

    # # Ensure the screenshots folder exists
    # if not os.path.exists(screenshot_folder):
        # print(f"The folder '{screenshot_folder}' does not exist.")
        # return []

    # # Get all file paths in the screenshots folder
    # screenshot_files = [
        # os.path.join(screenshot_folder, file)
        # for file in os.listdir(screenshot_folder)
        # if os.path.isfile(os.path.join(screenshot_folder, file))
    # ]

    # return screenshot_files

# async def choose_images(query):
    # screenshot_paths = get_screenshot_file_paths()
    # screenshots = []

    # for path in screenshot_paths:
        # # Extract the filename from the full path
        # filename = os.path.basename(path)

        # # Extract the timestamp from the filename
        # timestamp = filename[len("screenshot_") : filename.rfind(".")]

        # screenshots.append({"timestamp": timestamp, "filepath": path})

        # for info in screenshots:
            # screenshot_details = (
                # f"timestamp: {info['timestamp']} filepath: {info['filepath']}"
            # )

    # response = openAiClient.chat.completions.create(
        # model="gpt-4o",
        # messages=[
            # {
                # "role": "system",
                # "content": fr"""based on the user's query, determine which file path based on the timestamps provided by producing the file path alone. 
                            # If there are multiple images you want to use, stack them like this:
                            # C:\Users\ASUS\Desktop\Development\decimal\functions\screenshots\screenshot_20240813_174535.png
                            # C:\Users\ASUS\Desktop\Development\decimal\functions\screenshots\screenshot_20240813_174522.png
                            # Here is an example of the output that you should provide:
                            # C:\Users\ASUS\Desktop\Development\decimal\functions\screenshots\screenshot_20240813_174535.png
                            
                            # {screenshot_details}
                            # """,
            # },
            # {"role": "user", "content": query},
        # ],
    # )

    # response_message = response.choices[0].message.content
    # print(f"Screenshots to analyze based on user query", {response_message})
    # return response_message
    
async def analyze_screenshot(query, file_path):
    result = vision_model(query, file_path.strip())
    print("result:", result)
    return result

def vision_model(query, chosen_path):
    # Encode the image
    base64_image = encode_image(chosen_path)

    # Set up headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_key}",
    }

    # Set up payload
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query or "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        return content

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            print(f"Encoded image length: {len(encoded_image)} characters")
            return encoded_image
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None