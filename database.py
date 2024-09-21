import json
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        if connection.is_connected():
            print("Connection to the database was successful!")
            return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None


def close_connection(connection, cursor):
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Database connection closed.")


def insert_message(connection, message, sender):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO messages (message, sender) VALUES (%s, %s)"
        values = (message, sender)
        cursor.execute(query, values)
        connection.commit()
        print("Message inserted successfully.")
    except Error as e:
        print(f"Error inserting message: {e}")
    finally:
        close_connection(connection, cursor)


def get_previous_messages(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT message, sender FROM messages ORDER BY id DESC LIMIT 4"
        cursor.execute(query)
        messages = cursor.fetchall()
        messages_list = [{"message": msg[0], "sender": msg[1]} for msg in messages]
        result = {
            "message_history": "Message History",
            "messages": messages_list
        }
        print(result)
        return json.dumps(result)
    except Error as e:
        print(f"Error retrieving messages: {e}")
        return json.dumps([])
    finally:
        close_connection(connection, cursor)
    

def insert_reminder(connection, title, description, reminder_time):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO reminders (title, description, reminder_time) VALUES (%s, %s, %s)"
        values = (title, description, reminder_time)
        cursor.execute(query, values)
        connection.commit()
        print("Reminder inserted successfully.")
    except Error as e:
        print(f"Error inserting reminder: {e}")
    finally:
        close_connection(connection, cursor)


def insert_data(connection, name, details):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO user_details (name, details) VALUES (%s, %s)"
        values = (name, details)
        cursor.execute(query, values)
        connection.commit()
        print('Data inserted successfully.')
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        close_connection(connection, cursor)
    

def insert_pdf_details(connection, details):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO pdf_details (details) VALUES (%s)"
        cursor.execute(query, (details,))
        connection.commit()
        print("PDF details inserted successfully.")
    except Error as e:
        print(f"Error inserting PDF details: {e}")
    finally:
        close_connection(connection, cursor)


def get_all_pdf_details(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT details, created_at FROM pdf_details"
        cursor.execute(query)
        pdf_details = cursor.fetchall()

        pdf_details_string = ""
        for detail in pdf_details:
            pdf_details_string += f"Details: {detail[0]}, Created At: {detail[1]}\n"

        print(pdf_details_string)
        return pdf_details_string
    except Error as e:
        print(f"Error retrieving PDF details: {e}")
        return ""
    finally:
        close_connection(connection, cursor)


async def submit_file_details(connection, filename, important_attributes, file_content, project_name):
    try:
        cursor = connection.cursor()
        
        project_id = get_project_id(connection, project_name) 
        print(f"Project Id of {project_id} for {project_name} found. ")
        
        cursor = connection.cursor()

        query = """
        INSERT INTO project_files_metadata (filename, important_attributes, file_content, project_id)
        VALUES (%s, %s, %s, %s)
        """

        values = (filename, important_attributes, file_content, project_id)
        cursor.execute(query, values)
        connection.commit()
        print(f"Inserting file metadata for file, {filename}")
        return True
    except Error as e:
        return False
    finally:
        close_connection(connection, cursor)


def check_project_exists(connection, project_name:str):
    try:
        cursor = connection.cursor()
        check_query = """
        SELECT COUNT(*) FROM projects WHERE project_name = %s
        """
        cursor.execute(check_query, (project_name,))
        count = cursor.fetchone()[0]
        return count > 0
    except Error as e:
        error = f"Error checking project existence: {e}"
        print(error)
        return False
    finally:
        cursor.close()


def submit_project_details(connection, project_name):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO projects (project_name)
        VALUES (%s)
        """
        values = (project_name,)
        cursor.execute(query, values)
        connection.commit()
        success = f"Project details inserted successfully indexed as {project_name}"
        print(success)
        return success
    except Error as e:
        error = f"Error inserting project details: {e}"
        print(error)
    finally:
        close_connection(connection, cursor)


def get_project_id(connection, project_name: str):
    try:
        cursor = connection.cursor()

        # Get the project_id if the project already exists
        query = """
        SELECT project_id FROM projects WHERE project_name = %s
        """
        cursor.execute(query, (project_name,))
        project_id = cursor.fetchone()
        return project_id[0] if project_id else None
    except Exception as e:
        print(f"Error fetching project_id: {e}")
        return None
    finally:
        cursor.close()


def insert_log(connection, log_message):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO logs (log_message) VALUES (%s)"
        values = (log_message,)
        cursor.execute(query, values)
        connection.commit()
        print("Log inserted successfully.")
    except Error as e:
        print(f"Error inserting log: {e}")
    finally:
        close_connection(connection, cursor)


def get_logs(connection, limit):
    try:
        cursor = connection.cursor()
        query = "SELECT log_message, log_timestamp FROM logs ORDER BY log_timestamp ASC LIMIT %s"
        cursor.execute(query, (limit,))
        logs = cursor.fetchall()

        logs_list = [{"log_message": log[0], "log_timestamp": log[1].strftime('%Y-%m-%d %H:%M:%S')} for log in logs]
        result = {
            "log_history": f"Last {limit} Logs",
            "logs": logs_list
        }

        print(json.dumps(result, indent=4))  # Pretty-printing the result
        return json.dumps(result)
    except Error as e:
        print(f"Error retrieving logs: {e}")
        return json.dumps([])
    finally:
        close_connection(connection, cursor)

def get_file_details(project_id):
    try:
        connection = create_connection()
        if connection: 
            cursor = connection.cursor()
            query = """
            SELECT filename, important_attributes 
            FROM project_files_metadata 
            WHERE project_id = %s
            """
            cursor.execute(query, (project_id,))
            file_details = cursor.fetchall()

            if file_details:
                result = []
                for file in file_details:
                    result.append({
                        "filename": file[0],
                        "important_attributes": file[1]
                    })
                print("result from get_file_details:", result)
                return result
            else:
                return "No files found for the given project ID."
    except Error as e:
        print(f"Error retrieving file details: {e}")
        return None
    finally:
        cursor.close()

def get_code_contents(file_name):
    connection = None
    cursor = None
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT filename, file_content FROM project_files_metadata WHERE filename = %s"
            cursor.execute(query, (file_name,))
            file_data = cursor.fetchone()  

            if file_data:
                return {"file_name": file_data[0], "file_content": file_data[1]}
            else:
                return "File not found"
    except Error as e:
        print(f"Error retrieving file content: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
