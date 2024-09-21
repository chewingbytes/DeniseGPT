from pdf2image import convert_from_path
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import requests

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openAiClient = OpenAI(api_key=openai_key)

async def pdf_analysis(pdf_file_path: str, file_folder: str) -> None:
    images = convert_from_path(pdf_file_path)
    
    images_folder = os.path.join(file_folder, 'images')
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    
    for i, image in enumerate(images):
        image_file_path = os.path.join(images_folder, f'page_{i + 1}.png')
        image.save(image_file_path, 'PNG')
    
    images_analysis = await get_details_from_images(images_folder)
    return images_analysis

async def summary(analysis_from_images):
    response = openAiClient.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", "content": "you will receive detailed analysis of pdf pages. Give a detailed overall summary. You are not to use formatting in your response."
            },
            {
                "role": "user", "content": f"analysis from images: {analysis_from_images}"
            },
        ]
    )

    message = response.choices[0].message.content
    return message

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
async def get_details_from_images(images_directory: str):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_key}'
    }

    responses = []

    for filename in os.listdir(images_directory):
        image_path = os.path.join(images_directory, filename)

        base64_image = encode_image(image_path)

        payload = {
                "model": "gpt-4-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Whats in this image? Be descriptive and concise."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
            }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        responses.append(response.json())

    analysis_responses = ""

    if len(responses) > 1:
        for i, res in enumerate(responses):
            analysis_responses += f'Response for image {i + 1}, \n\n{res}\n\n'
    elif responses:
        analysis_responses = f'Response for the image, \n\n{responses[0]}'

    return analysis_responses