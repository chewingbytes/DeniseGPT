import os
import shutil

def find_folder(folder, starting_point=None):
    if starting_point is None:
        start_dir = os.path.join(os.path.expanduser('~'), "Desktop")
    else:
        start_dir = os.path.join(os.path.expanduser('~'), starting_point)
        
    for root, dirs, files in os.walk(start_dir):
        if folder in dirs:
            folder_path = os.path.join(root, folder)
            contents = os.listdir(folder_path)
            results = f"folder path:, {folder_path}, folder contents: {contents}"
            return results
            
    return "no results found"

def find_file(file, starting_point=None):
    if starting_point is None:
        start_dir = os.path.expanduser('~')
    else:
        start_dir = os.path.join(os.path.expanduser('~'), starting_point)
        
    for root, dirs, files in os.walk(start_dir):
        if file in files:
            file_path = os.path.join(root, file)
            results = f"the {file} file is located at:, {file_path}"
            return results
            
    return 'no results found'


def create_folder(parent_dir, folder_name):
    folder_path = os.path.join(os.path.expanduser('~'), parent_dir)

    if os.path.isdir(folder_path):
        new_folder_path = os.path.join(folder_path, folder_name)

        try:
            os.makedirs(new_folder_path, exist_ok=True)
            success_message = f"Folder '{folder_name}' created at: {folder_path}"
            return success_message
        except Exception as e:
            error_message = f"An error occurred: {e}"
            return error_message

    else:
        missing_directory_message = f"Parent folder '{folder_path}' does not exist."
        return missing_directory_message

def copy_file(source, source_origin, destination, destination_origin):
    source_dir = os.path.join(os.path.expanduser('~'), source_origin)
    destination_dir = os.path.join(os.path.expanduser('~'), destination_origin)
    
    source_path = None
    destination_path = None
    
    for root, dirs, files in os.walk(source_dir):
        if source in files:
            source_path = os.path.join(root, source)
            print("source path:", source_path)
            break

    if not source_path:
        return f"Source file '{source}' not found in '{source_dir}'"
        
    for root, dirs, files in os.walk(destination_dir):
        if destination in dirs:
            destination_path = os.path.join(root, destination)
            print("destination path:", destination_path)
            break
    
    if not destination_path:
        return f"Destination folder '{destination}' not found in '{destination_dir}'"

    try:
        dest = shutil.copy(source_path, destination_path)
        print("Destination path:", dest) 
        success_message = f'Successfully moved {source} to {destination}'
        return success_message
        
    except Exception as e:
        return f"An error occurred: {e}"

def delete_file(file, file_origin):
    file_dir = os.path.join(os.path.expanduser('~'), file_origin)
    for root, dirs, files in os.walk(file_dir):
        if file in files:
            file_path = os.path.join(root, file)
            print("file_path:", file_path)
            try: 
                os.remove(file_path)
                success_message = f"File '{file_path}' has been deleted."
                return success_message
            except Exception as e:
                error_message = f"An error occurred while deleting file: {e}"
                return error_message
            
        else:
            not_found_error = f"File '{file_path}' not found."
            return not_found_error
                
def delete_folder(folder, folder_origin):
    folder_dir = os.path.join(os.path.expanduser('~'), folder_origin)
    
    folder_path = None
    for root, dirs, files in os.walk(folder_dir):
        if folder in dirs:
            folder_path = os.path.join(root, folder)
            break

    if not folder_path:
        return f"Folder '{folder}' not found in '{folder_origin}'."

    try:
        shutil.rmtree(folder_path)
        success_message = f"Folder '{folder_path}' and all its contents have been deleted."
        return success_message
    
    except FileNotFoundError:
        return f"Error: The folder '{folder_path}' was not found."
    
    except PermissionError:
        return f"Error: Permission denied while attempting to delete '{folder_path}'."
    
    except OSError as e:
        return f"OS error occurred while deleting folder: {e.strerror}."
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"
