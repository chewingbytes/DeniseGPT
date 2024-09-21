import pyvolume

def modify_volume(volume):
    pyvolume.custom(percent=volume)
    return f"I changed the volume to {volume}%"
