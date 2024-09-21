import os
import datetime
import networkx as nx
from functions.programming.declarations import IGNORE_EXTENSIONS, IGNORE_FILES, IGNORE_FOLDERS, file_types
from functions.programming.file_ranking import extract_dependencies, rank_files_by_importance
from functions.programming.parser import parse_code
from database import create_connection, check_project_exists, submit_project_details, submit_file_details, insert_log, get_logs

# Function to check if a folder should be ignored
def should_ignore_folder(folder_name):
    return folder_name in IGNORE_FOLDERS

# Function to check if a file should be ignored based on its name or extension
def should_ignore_file(file_name):
    # Check if the file is in the ignore list or has an ignored extension
    return (file_name in IGNORE_FILES or 
            any(file_name.endswith(ext) for ext in IGNORE_EXTENSIONS))

# Function to read the content of a file
def read_file_content(file_path):
    """Reads and returns the content of a given file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None

# Function to get the file extension
def get_file_extension(file_name):
    return os.path.splitext(file_name)[1]

def add_log(logs, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    logs.append(formatted_message)

# Main function to traverse the directory and process files
async def insert_code_context(query, folder_name, starting_point=None):
    from main import speak
    logs = ["Logs:"]
    if starting_point is None:
        start_dir = os.path.join(os.path.expanduser('~'), "Desktop")
    else:
        start_dir = os.path.join(os.path.expanduser('~'), starting_point)

    speak("Alright. Hold on sir.")

    add_log(logs, "Started processing...")
    add_log(logs, "Looking through computer filesystem now...")

    try:
        for root, dirs, files in os.walk(start_dir):
            if folder_name in dirs:
                folder_path = os.path.join(root, folder_name)
                add_log(logs, f"Found requested folder: {folder_path}")

                connection = create_connection()
                if connection:
                    if not check_project_exists(connection, str(folder_name)):
                        speak(f"i will be creating another project in your database index as, {folder_name}")
                        add_log(logs, f"Project does not exist in context memory for this directory. Creating new entry indexed {folder_name} in database")
                        connection = create_connection()
                        if connection:
                            response = submit_project_details(connection, str(folder_name))
                            if response == f"Project details inserted successfully indexed as {folder_name}":
                                add_log(logs, f"New Entry successfully created indexed as {folder_name}")
                                try:
                                    for folder_root, subdirs, subfiles in os.walk(folder_path):
                                        subdirs[:] = [d for d in subdirs if not should_ignore_folder(d)]
                                        
                                        for file_name in subfiles:
                                            if not should_ignore_file(file_name):
                                                file_path = os.path.join(folder_root, file_name)
                                                file_content = read_file_content(file_path)

                                                if file_content:
                                                    file_extension = get_file_extension(file_name)
                                                    language_name = file_types.get(file_extension)

                                                    if language_name:
                                                        try:
                                                            print(f"\nProcessing file: {file_path} as {language_name} \n")
                                                            important_attributes = await parse_code(file_path, language_name, file_content)
                                                            connection = create_connection()
                                                            if connection:
                                                                await submit_file_details(connection, file_name, str(important_attributes), file_content, folder_name)
                                                        except Exception as e:
                                                            print(f"Error processing {file_name}: {str(e)}")
                                                            continue
                                                    else:
                                                        print(f"File type {file_extension} is not recognized for {file_name}")
                                                        continue
                                            else:
                                                print(f'Ignoring file: {file_name}')

                                    success_message = f"Successfully uploaded the files into the database for {folder_name}"
                                    add_log(logs, success_message)
                                    print(logs)
                                    return logs

                                except Exception as e:
                                    error_message = f"Error walking through requested folder: {str(e)}"
                                    add_log(logs, error_message)
                                    print(logs)
                                    return logs

                            else:
                                error_message = f"Failed to create new entry for {folder_name}"
                                add_log(logs, error_message)
                                print(logs)
                                return logs

                    else:
                        message = f"{folder_name}, project directory found. Do you want me to refresh the context memory for this particular directory?"
                        add_log(logs, message)
                        print(logs)
                        return logs
            
        error_message = f"Unable to find {folder_name} in the filesystem."
        add_log(logs, error_message)
        print(logs)
        return logs
    
    except:
        print("Error")
        add_log(logs, "error")
        print(logs)
        return logs