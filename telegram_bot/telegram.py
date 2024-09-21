import sys
import asyncio
import requests
import base64
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from pdf2image import convert_from_path
from openai import OpenAI
from pdf_functions import pdf_analysis, summary
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import create_connection, insert_pdf_details, get_all_pdf_details

load_dotenv()

telegram_api_key = os.getenv("TELEGRAM_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
openAiClient = OpenAI(api_key=openai_key)

# Initialize the Bot and Dispatcher
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello there, Bryan")

@dp.message(lambda message: message.document)
async def handle_file(message: Message) -> None:
    document = message.document
    file_id = document.file_id
    file_info = await message.bot.get_file(file_id)
    
    # Get the directory of the current script
    base_directory = os.path.dirname(__file__)
    
    # Resolve the target directory dynamically
    target_directory = os.path.join(base_directory, 'files_from_telebot')
    
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    # Create a new folder named after the file inside 'files_from_telebot'
    file_folder = os.path.join(target_directory, os.path.splitext(document.file_name)[0])
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    
    # Define the full file path within the new folder
    file_path = os.path.join(file_folder, document.file_name)
    
    # Download the file to the specified path
    await message.bot.download_file(file_info.file_path, file_path)
    
    # Check the file type and handle accordingly
    if document.mime_type == 'application/pdf':
        # Call the function to convert PDF to images
        images_analysis = await pdf_analysis(file_path, file_folder)
        await message.answer(f"PDF has been saved in {os.path.join(file_folder, 'images')}")
        result = await summary(images_analysis)
        await message.answer(result)
        connection = create_connection()
        if connection: 
            insert_pdf_details(connection, result)
            await message.answer("The pdf has been saved in your database for your viewing.")
        else:
            print("failed to connect to the database")
            await message.answer("failed to connect to your database")

    elif document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' or \
         document.mime_type == 'application/msword':
        await message.answer("Word document has been saved.")
    else:
        await message.answer("File has been saved.")

async def main() -> None:
    bot = Bot(token=telegram_api_key)
    print("\nTelebot started...")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling has been cancelled")

if __name__ == "__main__":
    asyncio.run(main())
