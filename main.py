import speech_recognition as sr
import keyboard
import asyncio
import traceback
import pyttsx3
import struct
import os
import pyaudio
import pvporcupine
import json
from database import create_connection, insert_message, get_previous_messages
from tools import tools
from functions.programming.get_folder import insert_code_context
from functions.programming.master import consult_program_model
from functions.system_controls.concious_functions import (
    get_current_brightness,
    get_current_time,
    get_current_volume,
)
from functions.user_data import send_user_data
from functions.weather import get_weather_info
from functions.spotify import get_authorization_token_from_spotify, pause_playback
from functions.telegram.telegram_functions import get_details
from functions.system_controls.screenshot import look_at_screen
from functions.system_controls.file_system import (
    find_folder,
    find_file,
    create_folder,
    copy_file,
    delete_file,
    delete_folder,
)
from functions.system_controls.volume import modify_volume
from functions.system_controls.screen import modify_screen_brightness
from functions.system_controls.open_applications import open_app, close_app
from dotenv import load_dotenv
from pyfiglet import Figlet
from openai import OpenAI
from speech_recognition import UnknownValueError
from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key=os.getenv("11_API_KEY")
)

load_dotenv()

directory = "Denise_en_windows_v3_0_0"
file_name = "Denise_en_windows_v3_0_0.ppn"
full_path = os.path.join(os.path.dirname(__file__), directory, file_name)
str_full_path = str(full_path)

openAiClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
telegram_api_key = os.getenv("TELEGRAM_API_KEY")

recognizer = sr.Recognizer()
calibrated = False

debug_mode = False

speech_speed = 200

def model(query):
    if query:
        print(f"[DEBUG] model: Query received: {query}")

        connection = create_connection()
        if connection:
            insert_message(connection, query, "user")
            print(f'inserting text "{query}" from user into database')
        else:
            print("failed to connect to database.")

        basic_prompt = f"""
        Please respond only with plain text and no formatting. You are a voice assistant, programmed by King Bryan, as a personal voice assistant that operates on a computer to assist with everyday tasks. You have a playful nature and have a slight hint of sarcasm in your personality. 

        KNOWLEDGE:
        THE TIME NOW IS:
        {get_current_time()} 

        THE CURRENT SCREEN BRIGHTNESS OF THE DEVICE IS:
        {get_current_brightness()}

        THE CURRENT VOLUME OF THE DEVICE IS: 
        {get_current_volume()}

        You are given a number of tools as functions, use these tools at your disposal.
        You are to use the consult_program_model function whenever i ask for anything related to programming such as 
        1. Help me debug this folder (foldername) etc.

        First analyze the given situation to fully understand my intention,
        what i need and exactly which tool that can fill up that necessity.

        Then look into the parameters and extract all the relevant informations to fillup the 
        parameter with right values.

        When responding to user queries, you can utilize multiple function calls if necessary to accomplish the task effectively. For example, if the user requests, "Look at my screen and analyze it and save the result into my data," you should do the following:

        Example User Query:
        "Take a screenshot and analyze it, then save the analysis in my data with the title 'Work Progress'."

        Expected Steps:

        Call look_at_screen to look at the screen and you will get some analysis of the screen.
        Call insert_user_data with the analyzed name (if not provided, just come up with one) and respective details and save the analysis in the user's data.

        Do not speak in point form and keep your answers naturally conversational as you are a voice assistant. Do not include any special characters or formatting. Here is an example:

        User:
        How do I make pancakes?

        Assistant:
        To make pancakes, mix flour, milk, eggs, and a pinch of salt. Pour the batter onto a hot griddle and cook until bubbles form on the surface. Flip and cook until golden brown.

        """
        connection = create_connection()
        previous_messages = get_previous_messages(connection)
        all_messages = [
            {
                "role": "system",
                "content": basic_prompt,
            },
            {"role": "assistant", "content": previous_messages},
            {"role": "user", "content": query},
        ]
        response = openAiClient.chat.completions.create(
            model="gpt-4o-mini",
            messages=all_messages,
            tools=tools,
            tool_choice="auto",
        )

        message = response.choices[0].message.content

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            available_functions = {
                "change_talking_speed": change_talking_speed,
                "get_weather_info": get_weather_info,
                "get_authorization_token_from_spotify": get_authorization_token_from_spotify,
                "pause_playback": pause_playback,
                "get_telegram_messages": get_details,
                "look_at_screen": look_at_screen,
                "find_folder": find_folder,
                "find_file": find_file,
                "create_folder": create_folder,
                "copy_file": copy_file,
                "delete_file": delete_file,
                "delete_folder": delete_folder,
                "modify_volume": modify_volume,
                "modify_screen_brightness": modify_screen_brightness,
                "open_app": open_app,
                "close_app": close_app,
                "insert_user_data": send_user_data,
                "insert_code_context": insert_code_context,
                "consult_program_model": consult_program_model,
            }

            function_calling_messages = [
                {
                    "role": "system",
                    "content": f"""{basic_prompt} You are a voice assistant that will be receiving results from function calls based on a user query. You are to answer the user"s question based on the results provided. 
                                Do not speak in point form, keep your answers naturally conversational as you are a voice assistant. Do not include any special characters or formatting. 
                                You have a playful nature and have a slight hint of sarcasm in your personality.
                                Here is an example:

                                User:
                                How do I make pancakes?

                                Assistant:
                                To make pancakes, mix flour, milk, eggs, and a pinch of salt. Pour the batter onto a hot griddle and cook until bubbles form on the surface. Flip and cook until golden brown, but please try not to break anything...""",
                },
                {"role": "assistant", "content": previous_messages},
            ]

            function_calling_messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                if asyncio.iscoroutinefunction(function_to_call):
                    function_response = asyncio.run(function_to_call(**function_args))
                    function_response = str(function_response)
                else:
                    function_response = function_to_call(**function_args)
                function_calling_messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": function_response,
                    }
                )

            second_response = openAiClient.chat.completions.create(
                model="gpt-4o-mini",
                messages=function_calling_messages,
            )
            second_message = second_response.choices[0].message.content
            speak(second_message)

            connection = create_connection()
            if connection:
                insert_message(connection, second_message, "assistant")
                print(f'inserting text "{second_message}" from assistant into database')
            else:
                print("failed to connect to the database.")

        else:
            speak(message)
            connection = create_connection()
            if connection:
                insert_message(connection, message, "assistant")
                print(f'inserting text "{message}" from assistant into database')
            else:
                print("failed to connect to the database.")

        print("[DEBUG] model: Finished")


def receiveQuery():
    global recognizer
    print("[DEBUG] receiveQuery: Started")
    while True:
        with sr.Microphone() as source:
            print("[DEBUG] receiveQuery: Listening...")
            audio = recognizer.listen(source)
            query = ""
            try:
                print("[DEBUG] receiveQuery: Recognizing...")
                query = recognizer.recognize_google(audio, language="en-US")
                query = query.strip()

                if query:
                    print(f"[DEBUG] receiveQuery: User said: {query}")
                    return query.lower()

                else:
                    print(
                        "[DEBUG] receiveQuery: No valid input detected, continuing..."
                    )

            except UnknownValueError:
                print("[DEBUG] receiveQuery: No valid input detected, continuing...")

            except Exception as e:
                print("[DEBUG] receiveQuery: Exception: " + str(e))
                print("[DEBUG] receiveQuery: Traceback: " + traceback.format_exc())


def run():
    global calibrated
    global debug_mode

    if debug_mode is False:
        print("[DEBUG] model: Started")
        while True:
            voice_query = receiveQuery()
            model(voice_query)
            if voice_query == "stop":
                print("[DEBUG] model: 'stop' detected, resetting calibration")
                calibrated = False
                speak("As you wish sir")
                break

    elif debug_mode is True:
        print("[DEBUG] model in debug mode: Started")
        f = Figlet(font="slant")
        print(f.renderText("Welcome Bryan"))
        while True:
            text_query = get_text()
            model(text_query)
            if text_query == "stop":
                print('[DEBUG] model: "stop" detected, resetting')
                debug_mode == False
                break


def get_text():
    print("Started Text Mode")
    while True:
        query = input("type down your query: ")
        return query.lower()


def speak(text):
    #audio = client.generate(
        #text=text,
        #voice="Lily",
        #model="eleven_turbo_v2_5"
    #)
    #play(audio)
    print("[DEBUG] speak: Started")
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", speech_speed)
    print("[DEBUG] speak: Audio generated")
    engine.say(text)
    engine.runAndWait()
    print("[DEBUG] speak: Finished")


def change_talking_speed(current_words_per_minute, words_per_minute):
    global speech_speed
    speech_speed = words_per_minute
    return f"The speech rate has been changed from {current_words_per_minute} words per minute to {words_per_minute} words per minute."


def calibrate_recognizer():
    global recognizer
    print("[DEBUG] calibrate_recognizer: Started")
    with sr.Microphone() as source:
        print("Calibrating recognizer...")
        recognizer.adjust_for_ambient_noise(source, duration=10)
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8

    print("[DEBUG] calibrate_recognizer: Finished")


def detect_hotword():
    decision = input("Start in debug mode? y/n")
    if decision == "n":
        global calibrated
        print("[DEBUG] detect_hotword: Started")
        porcupine = None
        pa = None
        audio_stream = None

        try:
            f = Figlet(font="slant")
            print(f.renderText("Welcome Bryan"))

            if not calibrated:
                print("Calibrating recognizer")
                calibrate_recognizer()
                calibrated = True

            # Initialize Porcupine with the "computer" keyword
            porcupine = pvporcupine.create(
                access_key=os.getenv("PORCUPINE_ACCESS_KEY"),
                keyword_paths=[str_full_path],
                sensitivities=[0.8],
            )
            print("[DEBUG] detect_hotword: Porcupine initialized")

            # Initialize PyAudio
            pa = pyaudio.PyAudio()

            # Open an audio stream
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
            )
            print("[DEBUG] detect_hotword: Audio stream opened")

            print("Listening for the hotword...")

            # Continuously listen for the hotword
            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print("[DEBUG] detect_hotword: Hotword Detected")
                    run()

        except Exception as e:
            print(f"[DEBUG] detect_hotword: An error occurred: {e}")

        finally:
            if audio_stream is not None:
                audio_stream.close()
                print("[DEBUG] detect_hotword: Audio stream closed")

            if pa is not None:
                pa.terminate()
                print("[DEBUG] detect_hotword: PyAudio terminated")

            if porcupine is not None:
                porcupine.delete()
                print("[DEBUG] detect_hotword: Porcupine deleted")

        print("[DEBUG] detect_hotword: Finished")
    else:
        while True:
            global debug_mode
            debug_mode = True
            run()


if __name__ == "__main__":
    try:
        detect_hotword()
    except KeyboardInterrupt:
        print("\nDenise exiting...")
