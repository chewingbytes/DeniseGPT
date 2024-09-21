from functions.programming.program_tools import tools
from database import (
    get_project_id,
    create_connection,
    get_file_details,
    get_code_contents,
)
from dotenv import load_dotenv
from openai import OpenAI
from mysql.connector import Error
import os
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openAiClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def retrieve_project_id(project_name):
    try:
        connection = create_connection()
        if connection:
            result = get_project_id(connection, project_name)
            return result
        else:
            raise ConnectionError("Failed to create a database connection.")
    except Exception as e:
        print(f"Error retrieving project ID: {e}")
        return None


def consult_program_model(query, project_name):
    try:
        project_id = retrieve_project_id(project_name)
        if not project_id:
            raise ValueError(f"Project ID for {project_name} could not be retrieved.")

        basic_prompt = f"""
        You are the programming king. You are wise, creative and witty.
        
        You are currently working in the project folder named {project_name} with project id of {project_id}

        {get_file_details(project_id)}

        You are to call the function get_code_content to get the actual code contents. Just provide the file_name.

        You are to give me a comprehensive response regarding the query and the codebase context you are provided below.

        """

        response = openAiClient.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": basic_prompt},
                {"role": "user", "content": query},
            ],
            tools=tools,
            tool_choice="required",
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            available_functions = {
                "get_code_content": get_code_contents,
            }

            function_calling_messages = [
                {
                    "role": "system",
                    "content": f"""
                You are the programming king. You are wise, creative and witty.
            
                You are currently working in the project folder named {project_name} with project id of {project_id}

                You will receive a bunch of code contents from files which you should fix or build from according to the query from me.

                You are to give me a comprehensive response regarding the query and the codebase context you are provided below.
                    """,
                },
                {
                    "role": "user", "content": query
                }
            ]

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                function_calling_messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": function_response,
                    }
                )
            
            second_response = openAiClient.chat.completions.create(
                model="gpt-4o",
                messages=function_calling_messages,
            )

            second_message = second_response.choices[0].message.content
            print("second message:", second_message)
            return second_message

    except Exception as e:
        print(f"Error during OpenAI request: {e}")
        return "error"