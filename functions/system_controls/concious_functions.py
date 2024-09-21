from screen_brightness_control import get_brightness
import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def get_current_volume():
    vol = volume.GetMasterVolumeLevelScalar() * 100
    current_volume = f"{vol:.0f}%"
    return current_volume
    

def get_current_brightness():
    current_brightness = get_brightness()
    return str(current_brightness)

def get_current_time():
    now = datetime.datetime.now()
    time = now.strftime("%I:%M %p, %A, %B %d, %Y")  
    return time