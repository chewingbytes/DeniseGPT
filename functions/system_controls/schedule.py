import functions.system_controls.schedule as schedule
from datetime import datetime
from database import create_connection, insert_reminder

async def reminders(title, description, timestamp): 
    connection = create_connection()
    if connection: 
        insert_reminder(connection, title, description, timestamp)
        success_message = f"reminder successfully stored with title: {title}, description: {description}, and timestamp: {timestamp}"
        return success_message


