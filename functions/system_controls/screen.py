from screen_brightness_control import get_brightness, set_brightness

def modify_screen_brightness(brightness):
    set_brightness(brightness)
    return f"I changed the screen brightness to {brightness}"
