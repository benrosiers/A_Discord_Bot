import sounddevice as sd
from pynput import keyboard
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import pygetwindow as gw

# Parameters
duration = 10  # seconds

# Get a list of all input devices
devices = sd.query_devices()

# Find the VoiceMeeter device
voicemeeter_device = None
for idx, device in enumerate(devices):
    if 'VoiceMeeter' in device['name']:
        voicemeeter_device = idx

# Check if we found the device
if voicemeeter_device is None:
    print('Could not find VoiceMeeter device')
    exit(1)

# Callback for keyboard listener
def on_press(key):
    if str(key) == 'Key.space':
        active_window = gw.getActiveWindow()
        if "Discord" in active_window.title:
            print('Recording...')
            myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2, device=voicemeeter_device)
            sd.wait()
            sf.write('audio/output.wav', myrecording, fs)
            sound = AudioSegment.from_wav('audio/output.wav')
            sound.export('audio/output.mp3', format='mp3')

# Setting up keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
