from database import create_connection, insert_data

def send_user_data(name, details):
    connection = create_connection()
    if connection:
        insert_data(connection, name, details)
        success_message = f"The provided user data {name}, with details: {details} has been successfully stored and available for you when needed"
        return success_message