
import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import wikipedia
import pandas as pd
import webbrowser
import time
import os

# -------------------- Voice Engine --------------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # speaking speed
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    gui_log(f"Jarvis: {text}")

# -------------------- GUI Setup --------------------
root = tk.Tk()
root.title("JarvisAI - PIFARM Advanced")
root.geometry("500x600")
root.configure(bg="#0f0f0f")

# Avatar placeholder (replace 'avatar.png' with your own image)
try:
    from PIL import Image, ImageTk
    avatar_img = Image.open("avatar.png").resize((150,150))
    avatar_photo = ImageTk.PhotoImage(avatar_img)
    avatar_label = tk.Label(root, image=avatar_photo, bg="#0f0f0f")
    avatar_label.pack(pady=10)
except:
    avatar_label = tk.Label(root, text="🤖", font=("Arial", 50), bg="#0f0f0f", fg="white")
    avatar_label.pack(pady=20)

# Log Window
log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, bg="#1a1a1a", fg="white")
log_area.pack(padx=10, pady=10)
log_area.insert(tk.END, "Jarvis Initialized...\n")
log_area.configure(state='disabled')

def gui_log(text):
    log_area.configure(state='normal')
    log_area.insert(tk.END, text + "\n")
    log_area.see(tk.END)
    log_area.configure(state='disabled')

# -------------------- Command Handling --------------------
def process_command(command):
    command = command.lower()
    gui_log(f"You said: {command}")
    
    # -------------------- Wikipedia Search --------------------
    if "wikipedia" in command:
        try:
            query = command.replace("wikipedia", "").strip()
            gui_log(f"Searching Wikipedia for '{query}'...")
            summary = wikipedia.summary(query, sentences=2)
            speak(summary)
        except:
            speak("Sorry, I could not find that on Wikipedia.")
    
    # -------------------- Excel / Pandas Example --------------------
    elif "excel" in command or "data" in command:
        try:
            speak("Please enter the Excel file name (with extension):")
            filename = input("Excel file: ")
            if os.path.exists(filename):
                df = pd.read_excel(filename)
                gui_log(f"Excel Data Preview:\n{df.head()}")
                speak(f"Data loaded. I can tell you number of rows and columns. Rows: {df.shape[0]}, Columns: {df.shape[1]}")
            else:
                speak("File not found.")
        except Exception as e:
            speak(f"Error loading Excel file: {e}")
    
    # -------------------- Open WordPress --------------------
    elif "wordpress" in command:
        speak("Opening WordPress dashboard in your browser.")
        webbrowser.open("https://wordpress.com/log-in")
    
    # -------------------- Web Search --------------------
    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    
    # -------------------- Greetings --------------------
    elif "hello" in command or "hi" in command:
        speak("Hello! I am Jarvis, your PIFARM AI assistant.")
    elif "how are you" in command:
        speak("I am fully operational and ready to assist you!")
    
    # -------------------- Exit --------------------
    elif "exit" in command or "quit" in command:
        speak("Shutting down. Goodbye!")
        root.destroy()
        os._exit(0)
    
    else:
        speak("I heard you, but I am not sure how to respond to that yet.")

# -------------------- Voice Listening Thread --------------------
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen():
    while True:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                gui_log("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = recognizer.recognize_google(audio)
                process_command(command)
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            gui_log("Could not understand audio.")
        except sr.RequestError:
            gui_log("Request failed. Check internet connection.")
        except Exception as e:
            gui_log(f"Error: {e}")

# Start listening in a separate thread
threading.Thread(target=listen, daemon=True).start()

# -------------------- Run GUI --------------------
root.mainloop()