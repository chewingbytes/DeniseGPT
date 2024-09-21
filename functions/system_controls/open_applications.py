from AppOpener import open, close

def open_app(app):
    try:
        open(app)
        return f'succesfully opened {app}'

    except Exception as error:
        error_message = f"error opening {app}: {error}"
        return error_message
        

def close_app(app):
    try:
        close(app)
        return f'successfully closed {app}'
    
    except Exception as error:
        error_message = f"error closing {app}: {error}"
        return error_message