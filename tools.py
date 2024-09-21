tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather_info",
            "description": "Get the current weather only in degree celsius in a given location by latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {
                    "description": "Latitude of the location",
                    },
                    "lon": {
                        "type": "string",
                        "description": "Longitude of the location",
                    },
                },
                "required": ["lat", "lon"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "change_talking_speed",
            "description": "based on the query, decide to talk faster or slower. The speed of talking rate is calculated by speed of speech in words per minute (default is 200)",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_words_per_minute": {
                        "type": "integer",
                        "description": "the current speed of speech in words per minute",
                    },
                    "words_per_minute": {
                        "type": "integer",
                        "description": "the speed of speech in words per minute",
                    },
                },
                "required": ["current_words_per_minute", "words_per_minute"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_authorization_token_from_spotify",
            "description": "based on the user's query, get the authorization token from spotify. The token expires every hour, so you are to remind the user regarding this.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "pause_playback",
            "description": "pause the song playing on spotify playing on the current device",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_telegram_messages",
            "description": """
            You are tasked to retrieve the user details, specifically name, and the limit (number of messages to be taken from telegram). The query will provide the following parameters:
                    1. Name (default=None): The name associated with the messages you want to retrieve. If not specified, retrieve messages regardless of the name.
                    2. Limit (default=5): The number of messages to retrieve. If not specified, use the default limit of 5 messages.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "name associated with the messages we want to retrieve",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "the number of messages to retrieve",
                    },
                },
                "required": ["name", "limit"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "look_at_screen",
            "description": "Look at the screen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "the user's query"},
                },
                "required": ["query"],
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_folder",
            "description": "Based on the user's query, you might potentially receive two arguments, the folder to find, and the starting point. If the starting point is not defined, just browse through the entire tree system, and counter-wise.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder": {"type": "string", "description": "the folder to find"},
                    "starting_point": {
                        "type": "string",
                        "description": "the starting point of which to find the folder from",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_file",
            "description": "Based on the user's query, you might potentially receive two arguments, the file to find, and the starting point. If the starting point is not defined, just browse through the entire tree system, and counter-wise.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {"type": "string", "description": "the file to find"},
                    "starting_point": {
                        "type": "string",
                        "description": "the starting point of which to find the file from",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_folder",
            "description": "Based on the user's query, you will receive two arguments, the specified directory to create the new folder in, and the name of the new folder. Create the new folder in the specified directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "parent_dir": {
                        "type": "string",
                        "description": "the specified directory to create the new folder in",
                    },
                    "folder_name": {
                        "type": "string",
                        "description": "the new folder's name",
                    },
                },
                "required": ["parent_dir", "folder_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "copy_file",
            "description": "Based on the user's query, you will receive four arguments, the file name and the directory that contains said file that he wants to move, and the destination name and directory that contains said destination that he wants to move the file to. Copy the file and send it to the destination.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "the file name of the file that user wants to copy and send.",
                    },
                    "source_origin": {
                        "type": "string",
                        "description": "the directory that contains the file that the user wants to copy and send.",
                    },
                    "destination": {
                        "type": "string",
                        "description": "the destination name of the destination that the user wants to send the file to.",
                    },
                    "destination_origin": {
                        "type": "string",
                        "description": "the directory that contains the destination that the user wants to send the file to."
                    }
                },
                "required": ["source", "source_origin", "destination", "destination_origin"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Based on the user's query, delete the file respectively according to the user's request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "the file name of the file the user wants to remove"
                    },
                    "file_origin": {
                        "type": "string",
                        "description": "the folder or origin where the file is in"
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_folder",
            "description": "Based on the user's query, delete the folder respectively according to the user's request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder": {
                        "type": "string",
                        "description": "the folder name of the folder the user wants to remove"
                    },
                    "folder_origin": {
                        "type": "string",
                        "description": "the folder or origin where the folder is in"
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "modify_volume",
            "description": "You should already know the current volume of the device. Depending on the user's query, decide whether to raise or lower the volume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "volume": {
                        "type": "integer",
                        "description": "the volume to be changed to in percentage"
                    },
                },
                "required": ["volume"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "modify_screen_brightness",
            "description": "You should already know the current screen brightness of the device. Based on the user's query, decide to raise or lower the brightness.",
            "parameters": {
                "type": "object",
                "properties": {
                    "brightness": {
                        "type": "integer",
                        "description": "the brightness of the screen to be changed to"
                    },
                },
                "required": ["brightness"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "based on the user's query, open the app",
            "parameters": {
                "type": "object",
                "properties": {
                    "app": {
                        "type": "string",
                        "description": "the app name"
                    },
                },
                "required": ["app"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "close_app",
            "description": "based on the user's query, close the app",
            "parameters": {
                "type": "object",
                "properties": {
                    "app": {
                        "type": "string",
                        "description": "the app name"
                    },
                },
                "required": ["app"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "store_reminders",
            "description": "You should already know the current date and time. Based on the user's query, devise a proper title, description, and timestamp (eg.2024-09-15 10:00:00) for the reminder given.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title name"
                    },
                    "description": {
                        "type": "string",
                        "description": "the title description"
                    },
                },
                "required": ["title", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "insert_user_data",
            "description": "Insert user(my)'s data into the database for retrieval when required.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "a suitable title for the data sent"
                    }, 
                    "details": {
                        "type": "string",
                        "description": "clear and consise details of the user-provided details"
                    },
                },
                "required": ["name", "details"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "insert_code_context",
            "description": "This function inserts code context into the database. Based on the user's query, you might potentially receive three arguments, the user's intention, the directory to find, and the starting point. If the starting point is not defined, just browse through the entire tree system, and counter-wise.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "This is the user's query on what to do regarding the project directory (maybe what i want to fix regarding the code in a specific file etc.)"
                    },
                    "folder_name": {
                        "type": "string",
                        "description": "the folder to find which houses the program code"
                    },
                    "starting_point": {
                        "type": "string",
                        "description": "the starting point of which to find the folder from",
                    },
                },
                "required": ["query", "folder_name"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consult_program_model",
            "description": "Based on the user's query, return the user's query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "the user's query"
                    },
                    "project_name": {
                        "type": "string",
                        "description": "the project's name"
                    },
                },
                "required": ["query", "project_name"],
            }
        }
    },
]
    