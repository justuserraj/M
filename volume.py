from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(f"M: {text}")
    engine.say(text)
    engine.runAndWait()

def get_volume_controller():
    """Gets the volume controller for the default speaker."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(level):
    """Sets the system volume to a specific level (0-100)."""
    try:
        volume = get_volume_controller()
        level = max(0.0, min(1.0, level / 100.0))
        volume.SetMasterVolumeLevelScalar(level, None)
        speak(f"Volume set to {int(level * 100)} percent.")
    except Exception as e:
        speak("Sorry, I'm having trouble adjusting the volume.")
        print(f"Volume control error: {e}")

def increase_volume():
    """Increases the system volume by a small increment."""
    try:
        volume = get_volume_controller()
        current_level = volume.GetMasterVolumeLevelScalar()
        new_level = min(1.0, current_level + 0.1)  # Increase by 10%
        volume.SetMasterVolumeLevelScalar(new_level, None)
        speak("Volume increased.")
    except Exception as e:
        speak("Sorry, I'm having trouble adjusting the volume.")
        print(f"Volume control error: {e}")

def decrease_volume():
    """Decreases the system volume by a small increment."""
    try:
        volume = get_volume_controller()
        current_level = volume.GetMasterVolumeLevelScalar()
        new_level = max(0.0, current_level - 0.1)  # Decrease by 10%
        volume.SetMasterVolumeLevelScalar(new_level, None)
        speak("Volume decreased.")
    except Exception as e:
        speak("Sorry, I'm having trouble adjusting the volume.")
        print(f"Volume control error: {e}")