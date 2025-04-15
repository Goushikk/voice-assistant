import tkinter as tk
import threading
import sounddevice as sd
import numpy as np
import whisper
import openai
import pvporcupine
import pyttsx3
import struct
import tempfile
import scipy.io.wavfile
import webbrowser
import time
import os
from datetime import datetime

# CONFIG
openai.api_key = "YOUR_OPENAI_API_KEY"
ACCESS_KEY = "YOUR_PORCUPINE_ACCESS_KEY"
WAKE_WORD_PATH = "hey-assistant.ppn"  # Path to .ppn file from Picovoice console
WHISPER_MODEL = "base"
LOG_FILE = "conversation_logs.txt"

# Init AI & audio
model = whisper.load_model(WHISPER_MODEL)
tts = pyttsx3.init()

# GUI setup
root = tk.Tk()
root.title("AI Voice Assistant")
root.geometry("500x450")

status_label = tk.Label(root, text="Status: Idle", font=("Helvetica", 14))
status_label.pack(pady=10)

vu_canvas = tk.Canvas(root, width=400, height=20, bg='black')
vu_rect = vu_canvas.create_rectangle(0, 0, 0, 20, fill='green')
vu_canvas.pack(pady=5)

sensitivity_label = tk.Label(root, text="Mic Sensitivity:")
sensitivity_label.pack()
sensitivity_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
sensitivity_slider.set(5)
sensitivity_slider.pack()

response_box = tk.Text(root, wrap=tk.WORD, height=15, width=60)
response_box.pack(pady=10)

def speak(text):
    tts.say(text)
    tts.runAndWait()

def transcribe(audio, fs):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        scipy.io.wavfile.write(f.name, fs, audio)
        result = model.transcribe(f.name)
    return result["text"]

def log_conversation(user_input, response):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] User: {user_input}\n")
        f.write(f"[{datetime.now()}] Assistant: {response}\n\n")

def ask_gpt(prompt):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res["choices"][0]["message"]["content"]

def execute_command(text):
    if "open google" in text.lower():
        webbrowser.open("https://www.google.com")
        return "Opening Google."
    elif "open youtube" in text.lower():
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    elif "open notepad" in text.lower():
        os.system("notepad.exe")
        return "Opening Notepad."
    # Add more as needed
    return None

def listen_and_respond():
    duration = 5
    fs = 16000
    sensitivity = sensitivity_slider.get()
    
    status_label.config(text="Listening...")
    root.update()

    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    for _ in range(duration * 10):
        level = np.abs(audio).mean() / (10000 / sensitivity)
        vu_canvas.coords(vu_rect, 0, 0, level * 400, 20)
        vu_canvas.update()
        time.sleep(0.1)

    sd.wait()
    text = transcribe(audio, fs)

    if text.strip():
        response_box.insert(tk.END, f"\nYou: {text}\n")
        cmd_response = execute_command(text)
        if cmd_response:
            response_box.insert(tk.END, f"Assistant: {cmd_response}\n")
            speak(cmd_response)
            log_conversation(text, cmd_response)
        else:
            status_label.config(text="Thinking...")
            root.update()
            response = ask_gpt(text)
            response_box.insert(tk.END, f"Assistant: {response}\n")
            speak(response)
            log_conversation(text, response)
    else:
        speak("I didn’t catch that.")

    status_label.config(text="Idle")
    vu_canvas.coords(vu_rect, 0, 0, 0, 20)

def wake_word_listener():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[WAKE_WORD_PATH]
    )

    stream = sd.RawInputStream(
        samplerate=porcupine.sample_rate,
        blocksize=porcupine.frame_length,
        dtype='int16',
        channels=1
    )
    stream.start()
    status_label.config(text="Waiting for wake word")
    root.update()

    try:
        while True:
            data = stream.read(porcupine.frame_length)[0]
            pcm = struct.unpack_from("h" * porcupine.frame_length, data)
            result = porcupine.process(pcm)
            if result >= 0:
                speak("Yes?")
                listen_and_respond()
    except Exception as e:
        print("Error:", e)
    finally:
        stream.stop()
        porcupine.delete()

# Run wake word listener in background
threading.Thread(target=wake_word_listener, daemon=True).start()

# Start GUI loop
root.mainloop()
