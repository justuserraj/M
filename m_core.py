# m_core.py
import speech_recognition as sr
import pyttsx3
import datetime
import calendar
import webbrowser
import os
import json
import requests
import pyjokes
import re
import pyperclip
import threading
import queue
from translate import Translator
import wikipedia
import yfinance as yf
import shutil
from PyPDF2 import PdfReader
from wikipedia_search import search_wikipedia
from news_control import get_news
from weather_control import get_weather
from stocks import get_stock_price
from knowledge_base import load_knowledge_base, find_best_answer, save_fact, save_knowledge_base, save_synonym
from conversation_engine import respond_to_greeting, handle_gratitude
from file_manager import create_text_file, list_directory, delete_file, delete_folder
from nlp_processor import process_command
from email_reader import read_unread_emails, read_most_recent_email, send_email, read_sent_emails
from email_contacts import load_contacts, save_contacts
from prank import show_fake_error
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import time
from server import command_queue, run_server
import nltk
import ssl
from ml_features import analyze_sentiment
from wikipedia.exceptions import DisambiguationError, PageError, RedirectError, HTTPTimeoutError
from pdf_qa import answer_question_from_pdf, set_pdf_content
from sys_monitor import get_system_report
import pyautogui # For controlling media using keyboard shortcuts
# VEDRA INTENT CLASSIFIER IMPORT
from intent_classifier import load_and_train_classifier, classify_intent, VEDRA_INTENT_CLASSIFIER 
# LLM BRAIN IMPORTS
from llm_brain import get_llm_response, execute_agent_command, AVAILABLE_TOOL_DESCRIPTIONS, web_search 


# Fix for NLTK SSL error
try:
    _create_unverified_https_context = ssl._create_unverified_https_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Initializations
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')

# Global variables and constants
# REMINDER: Your stored API key is 520659376199bc11641b9f131aaa5de6
WEATHER_API_KEY = "520659376199bc11641b9f131aaa5de6" 
EMAIL_USERNAME = "justuserraj@gmail.com"
EMAIL_PASSWORD = "aukv vcre wffn rlos" 
tasks = []
phrasings = {}
clipboard_history = []
server_thread = None
knowledge_base = {}
last_pdf_text = ""
current_pdf_path = ""
user_data = {} 
VEDRA_INTENT_CLASSIFIER = None # Global placeholder for the trained DNN

# State variables for multi-turn commands
last_command = ""
last_response = ""
last_unrecognized_command = ""


def speak(text):
    """Function to speak text."""
    print(text)
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id) 
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"FATAL AUDIO ERROR: Could not generate speech. Error: {e}")


def get_audio():
    """Function to listen for user's voice command."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""
    
    try:
        print("Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")
        return command.lower()
    except Exception as e:
        return ""


def media_control(action):
    """Controls media playback using global keyboard shortcuts."""
    if action == "play_pause":
        pyautogui.press('playpause')
        return "Toggling play/pause."
    elif action == "next":
        pyautogui.press('nexttrack')
        return "Skipping to the next track."
    elif action == "previous":
        pyautogui.press('prevtrack')
        return "Skipping to the previous track."
    return "Media control command not recognized."


def get_current_volume():
    """Gets the current system volume level (0.0 to 1.0)."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume.GetMasterVolumeLevelScalar()
    except Exception as e:
        print(f"Error getting volume: {e}")
        return None


def set_volume_level(level):
    """Sets the system volume to a specific level (0.0 to 1.0)."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level, None)
        return "Volume adjusted."
    except Exception as e:
        print(f"Error setting volume: {e}")
        return "Sorry, I couldn't adjust the volume."


def get_command_text():
    """Gets a command from the user via keyboard input."""
    command = input("Type your command here: ")
    return command.lower()


def save_user_data(data):
    """Saves user data to the user_data.json file."""
    try:
        with open("user_data.json", "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving user data: {e}")


def save_personal_detail(key, value):
    """Saves a personal detail to the user_data.json file."""
    global user_data
    try:
        user_data["details"][key] = value
        save_user_data(user_data)
        return f"Okay, I've saved that your {key} is {value}."
    except Exception as e:
        print(f"Error saving personal detail: {e}")
        return "I'm sorry, I couldn't save that information."


def save_synonym(new_phrase, canonical_phrase):
    """Saves a new phrase as a synonym for an existing command."""
    global phrasings
    try:
        phrasings[new_phrase] = canonical_phrase
        with open("phrasings.json", "w") as f:
            json.dump(phrasings, f, indent=4)
        return "Okay, I've learned that."
    except Exception as e:
        print(f"Error saving synonym: {e}")
        return "I'm sorry, I couldn't save that."


def do_local_calculation(command):
    """Performs a simple calculation from the command."""
    try:
        # Simple evaluation logic to handle basic math expressions
        calculation = command.replace("calculate", "").strip()
        
        # Security check: only allow basic arithmetic
        if re.match(r'^[\d\s\.\+\-\*\/\(\)]+$', calculation):
            # Replace common word operators
            calculation = calculation.replace('times', '*').replace('x', '*').replace('divided by', '/').replace('plus', '+').replace('minus', '-')
            
            result = eval(calculation)
            speak(f"The answer is {result}.")
        else:
            speak("Sorry, I can only perform basic arithmetic calculations.")
    except Exception:
        speak("Sorry, I couldn't perform that calculation.")


def tell_date():
    """Tells the current date."""
    now = datetime.datetime.now()
    day_name = calendar.day_name[now.weekday()]
    date_str = now.strftime("%B %d, %Y")
    speak(f"Today is {day_name}, {date_str}.")


def tell_time():
    """Tells the current time."""
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    speak(f"The current time is {time_str}.")


def get_to_do(tasks):
    """Reads out the to-do list."""
    if tasks:
        speak("Here is your to-do list:")
        for i, task in enumerate(tasks):
            speak(f"Item {i+1}: {task}")
    else:
        speak("Your to-do list is empty.")


def add_to_do(tasks, item):
    """Adds an item to the to-do list."""
    tasks.append(item)
    speak(f"I have added {item} to your to-do list.")


def delete_to_do(tasks, item):
    """Deletes an item from the to-do list."""
    # Simple matching logic, should be improved in a real app
    
    # Try to find the item in the list directly or by case-insensitive check
    item_lower = item.lower()
    found_task = next((t for t in tasks if t.lower() == item_lower), None)

    if found_task:
        tasks.remove(found_task)
        speak(f"I've deleted {item} from your to-do list.")
    else:
        speak(f"I'm sorry, I could not find {item} in your to-do list.")


def open_application(app_name):
    """Opens a specified application."""
    try:
        os.startfile(app_name)
        return f"Opening {app_name}."
    except FileNotFoundError:
        return f"Sorry, I could not find the application {app_name}."
    except Exception as e:
        return f"An error occurred while opening the application: {e}"


def translate_text(text_to_translate, target_language):
    """Translates text to a target language."""
    try:
        translator = Translator(to_lang=target_language)
        translation = translator.translate(text_to_translate)
        speak(f"The translation is: {translation}")
    except Exception as e:
        speak("I'm sorry, I could not translate that text.")
        print(f"Translation error: {e}")


def read_pdf(file_path):
    """Reads the content of a PDF file."""
    global last_pdf_text, current_pdf_path
    try:
        # Clean up path to handle common user input formats
        file_path = file_path.strip().replace('"', '').replace("'", "")
        
        if not os.path.exists(file_path):
            speak(f"Sorry, the file at '{file_path}' does not exist. Please check the path and try again.")
            return

        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() or ""

            last_pdf_text = full_text
            current_pdf_path = file_path
            set_pdf_content(full_text)
            speak("I have read the PDF and am ready to answer your questions about it.")

    except Exception as e:
        speak(f"I encountered an error while trying to read the PDF: {e}. Please ensure the file is not corrupted.")
        last_pdf_text = ""
        current_pdf_path = ""
        set_pdf_content("")
        # print(f"PDF Read Error: {e}")


def learn_from_wikipedia(topic):
    """Fetches a summary of a topic from Wikipedia and saves it to the knowledge base."""
    global knowledge_base
    try:
        # Use wikipedia.search to find the best match and then get summary
        search_results = wikipedia.search(topic)
        if not search_results:
             return f"Sorry, I could not find any relevant Wikipedia page for '{topic}'."
             
        canonical_topic = search_results[0]
        summary = wikipedia.summary(canonical_topic, sentences=2)

        knowledge_base[canonical_topic] = summary
        save_knowledge_base(knowledge_base)

        return f"I have learned about {canonical_topic} for you. Here is a brief summary: {summary}"
    except (DisambiguationError, RedirectError) as e:
        if isinstance(e, DisambiguationError):
            return f"The topic '{topic}' is too broad. Possible pages are: {', '.join(e.options[:5])}"
        else:
            return f"I was redirected to another page for '{topic}', please try a more specific search."
    except PageError:
        return f"Sorry, I could not find a Wikipedia page for '{topic}'."
    except HTTPTimeoutError:
        return "I am experiencing a network timeout while trying to access Wikipedia. Please try again."
    except Exception as e:
        print(f"An unexpected error occurred while learning: {e}")
        return "I encountered an error and could not learn about that topic."


def lock_computer():
    """Locks the Windows computer screen."""
    try:
        # Windows command to lock the workstation
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Computer locked."
    except Exception as e:
        print(f"Lock computer error: {e}")
        return "Sorry, I couldn't lock the computer."

def shutdown_computer():
    """Shuts down the computer."""
    try:
        # Windows command to shutdown in 1 second
        os.system("shutdown /s /t 1") 
        return "Shutting down the computer."
    except Exception as e:
        print(f"Shutdown computer error: {e}")
        return "Sorry, I couldn't initiate shutdown."


def greet_user():
    """Greets the user based on the time of day and user data."""
    global user_data
    # Initialize user data from file or default
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Default user data (using saved weather key for consistency)
        user_data = {"name": "User", "honorific": "Sir/Ma'am", "default_city": "Patna", "details": {}}
        with open("user_data.json", "w") as f:
            json.dump(user_data, f, indent=4)

    current_time = datetime.datetime.now()
    if 5 <= current_time.hour < 12:
        greeting = "Good morning"
    elif 12 <= current_time.hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    honorific = user_data.get("honorific", "Sir/Ma'am")
    name = user_data.get("name", "User")

    speak(f"{greeting}, {honorific} {name}!")
    speak(f"Welcome to your personal assistant. You can choose to use your voice or type your commands.")

def main():
    global clipboard_history, last_command, last_response, user_data, contacts, reminders, server_thread, tasks, knowledge_base, phrasings, last_unrecognized_command, last_pdf_text, current_pdf_path, VEDRA_INTENT_CLASSIFIER

    # Load initial data defensively
    try:
        knowledge_base_loaded = load_knowledge_base()
        knowledge_base = knowledge_base_loaded if isinstance(knowledge_base_loaded, dict) else {}
    except:
        knowledge_base = {}

    try:
        with open("phrasings.json", "r") as f:
            phrasings_loaded = json.load(f)
            phrasings = phrasings_loaded if isinstance(phrasings_loaded, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        phrasings = {}
        with open("phrasings.json", "w") as f:
            json.dump(phrasings, f, indent=4)

    try:
        contacts_loaded = load_contacts()
        contacts = contacts_loaded if isinstance(contacts_loaded, dict) else {}
    except:
        contacts = {}
    
    # --- VEDRA DNN INTENT CLASSIFIER INIT ---
    VEDRA_INTENT_CLASSIFIER = load_and_train_classifier()

    current_mode = "text"
    greet_user()

    # Define a simple map for fallback command execution
    COMMAND_FUNCTION_MAP = {
        "search on web": lambda query: webbrowser.open(f"https://www.google.com/search?q={query}") or f"Searching for {query} on Google.",
        "open notepad": lambda: speak(open_application("notepad.exe")),
        "open calculator": lambda: speak(open_application("calc.exe")),
        "open browser": lambda: webbrowser.open("https://www.google.com") or "Opening browser to Google.",
    }
    
    # --- TOOL FUNCTION MAP FOR LLM AGENT ---
    TOOL_FUNCTION_MAP = {
        "get_weather": lambda city: get_weather(city, api_key=WEATHER_API_KEY),
        "get_news": get_news,
        "search_wikipedia": search_wikipedia,
        "get_stock_price": get_stock_price,
        "web_search": web_search, # NEW GENERAL SEARCH TOOL
        # Add local system calls that are not already handled by hardcoded checks
        "list_directory": list_directory,
        "create_text_file": create_text_file,
        "delete_file": delete_file,
        "open_application": open_application,
        "set_volume_level": set_volume_level,
    }
    
    last_command = ""
    last_response = ""
    last_unrecognized_command = ""
    reminders = {}

    while True:
        try:
            raw_command = None

            # 1. Check for commands from the phone server queue
            try:
                raw_command = command_queue.get(block=False)
            except queue.Empty:
                pass

            # 2. Get input based on current mode
            if not raw_command and current_mode == "text":
                raw_command = get_command_text()

            if not raw_command:
                continue

            command = raw_command.replace("?", "").strip().lower()
            print(f"DEBUG: Processing command: {command}")
            clean_command = re.sub(r'[^\w\s]', '', command)
            
            # Use synonyms/phrasings to map user command to a canonical form
            canonical_command = phrasings.get(clean_command, clean_command)

            command_handled = False

            # --- Multi-turn commands ---
            if "yes" in command and "ask_to_learn" in last_command:
                speak("Great. What command should I run for that? For example, say 'search on web' or 'open notepad'.")
                last_command = "awaiting_command_to_learn"
                command_handled = True

            elif "no" in command and "ask_to_learn" in last_command:
                speak("Okay, no problem. I won't learn that command.")
                last_command = ""
                last_unrecognized_command = ""
                command_handled = True

            elif "this command is" in command and "awaiting_command_to_learn" in last_command:
                match = re.search(r'this command is (.+)', command)
                if match:
                    new_phrase = last_unrecognized_command
                    canonical_phrase = match.group(1).strip()
                    # Check if the canonical phrase is a known command or phrase
                    known_commands = list(COMMAND_FUNCTION_MAP.keys()) + list(phrasings.values())
                    if canonical_phrase in known_commands:
                        speak_text = save_synonym(new_phrase, canonical_phrase)
                        speak(speak_text)
                        last_response = speak_text
                    else:
                        speak("I'm sorry, that command is not in my list of known commands. Please provide a command I already know.")
                else:
                    speak_text = "Sorry, I didn't understand the command. Please say 'this command is [known command]'"
                    speak(speak_text)
                    last_response = speak_text
                last_command = ""
                last_unrecognized_command = ""
                command_handled = True

            # --- High-priority commands: PDF Q&A ---
            elif "done with pdf" in command or "stop reading pdf" in command or "exit pdf mode" in command:
                last_pdf_text = ""
                current_pdf_path = ""
                set_pdf_content("")
                speak("Okay, I am done with that document. What would you like to do next?")
                last_command = ""
                command_handled = True

            elif "read pdf" in command:
                match = re.search(r'read pdf (.+)', command)
                if match:
                    file_path = match.group(1).strip()
                    read_pdf(file_path) 
                    last_command = "pdf_read"
                else:
                    speak("Sorry, please provide a file path like 'read pdf C:\\path\\to\\file.pdf'")
                command_handled = True

            elif ("what is" in command or "who is" in command or "why" in command or "tell me about") and last_command == "pdf_read":
                if last_pdf_text:
                    speak("Just a moment, I am looking for the answer in the document.")
                    answer = answer_question_from_pdf(last_pdf_text, command) 
                    speak(answer)
                    last_command = "pdf_read" 
                else:
                    speak("I am currently not reading any PDF. Please use the 'read pdf' command first.")
                    last_command = ""
                command_handled = True
                
            # --- High-priority commands: Learning/Memory ---
            elif "learn from" in command and "wikipedia" not in command:
                url_match = re.search(r'(https?://\S+)', command)
                if url_match:
                    url = url_match.group(1).strip()
                    # Simple heuristic for topic extraction from URL
                    topic = url.split('/')[-1].replace('_', ' ').split('.')[0]
                    speak_text = f"Okay, I'll try to learn about {topic} for you."
                    speak(speak_text)
                    response = learn_from_wikipedia(topic)
                    speak(response)
                    last_response = response
                    knowledge_base = load_knowledge_base()
                else:
                    speak_text = "I'm sorry, I couldn't find a valid URL to learn from."
                    speak(speak_text)
                    last_response = speak_text
                last_command = ""
                command_handled = True

            elif "learn about" in command:
                topic = command.replace("learn about", "").strip()
                if topic:
                    speak_text = f"Okay, looking up {topic} for you."
                    speak(speak_text)
                    last_response = speak_text
                    response = learn_from_wikipedia(topic)
                    speak(response)
                    last_response = response
                    knowledge_base = load_knowledge_base()
                else:
                    speak_text = "I'm sorry, what would you like me to learn about?"
                    speak(speak_text)
                    last_response = speak_text
                last_command = ""
                command_handled = True

            elif "remember that" in command:
                match = re.search(r'remember that (.+)', command)
                if match:
                    fact_string = match.group(1).strip()
                    try:
                        # Check for personal details format: 'my [key] is [value]'
                        if "my " in fact_string and (" is " in fact_string or " are " in fact_string):
                            parts = re.split(r'\s(is|are)\s', fact_string.split("my ")[1], 1)
                            if len(parts) == 3:
                                key = parts[0].strip()
                                value = parts[2].strip()
                                speak_text = save_personal_detail(key, value)
                                speak(speak_text)
                                last_response = speak_text
                            else:
                                raise ValueError("Personal detail format error")
                        # Check for general fact format: '[question] is [answer]'
                        else:
                            parts = re.split(r'\s(is|are)\s', fact_string, 1)
                            if len(parts) == 3:
                                question = parts[0]
                                answer = parts[2]
                                speak_text = save_fact(question, answer)
                                speak(speak_text)
                                last_response = speak_text
                                knowledge_base = load_knowledge_base()
                            else:
                                raise ValueError("General fact format error")

                    except ValueError:
                        speak_text = "I'm sorry, I couldn't understand that fact. Please use the format 'remember that [something] is [something else]' or 'remember that my [something] is [something else]'."
                        speak(speak_text)
                        last_response = speak_text
                    except Exception as e:
                        speak_text = "I had trouble saving that fact."
                        speak(speak_text)
                        last_response = speak_text
                        print(f"Error parsing fact: {e}")
                else:
                    speak_text = "I'm sorry, I didn't get the fact you wanted me to remember."
                    speak(speak_text)
                    last_response = speak_text
                last_command = ""
                command_handled = True

            # --- General Commands: Hardcoded Keyword Checks ---
            if not command_handled:
                
                # Mode Switching
                if "manual command" in command or "give me the manual access" in command:
                    current_mode = "text"
                    print("I am now running in manual command mode. Type your commands below.")
                    speak("I am now running in manual command mode. Type your commands below.")
                    command_handled = True

                elif "phone command" in command or "switch to phone mode" in command or "voice command" in command or "switch to voice mode" in command:
                    if not server_thread or not server_thread.is_alive():
                        server_thread = threading.Thread(target=run_server)
                        server_thread.daemon = True
                        server_thread.start()
                        print("Server running. Connect your phone to: http://[YOUR_IP_ADDRESS]:5000") 
                    current_mode = "voice"
                    speak("I have switched to phone command mode.")
                    command_handled = True

                # Volume Control
                elif "increase volume" in command or "volume up" in command:
                    current_level = get_current_volume()
                    if current_level is not None:
                        new_level = min(current_level + 0.1, 1.0)
                        speak_text = set_volume_level(new_level)
                        speak(speak_text)
                        last_response = speak_text
                    command_handled = True
                elif "decrease volume" in command or "volume down" in command:
                    current_level = get_current_volume()
                    if current_level is not None:
                        new_level = max(current_level - 0.1, 0.0)
                        speak_text = set_volume_level(new_level)
                        speak(speak_text)
                        last_response = speak_text
                    command_handled = True
                elif "set volume to" in command:
                    match = re.search(r'set volume to (\d+)', command)
                    if match:
                        level_percent = int(match.group(1))
                        level_float = min(max(level_percent / 100.0, 0.0), 1.0)
                        speak_text = set_volume_level(level_float)
                        speak(speak_text)
                        last_response = speak_text
                    else:
                        speak_text = "Sorry, I couldn't understand the volume level."
                        speak(speak_text)
                        last_response = speak_text
                    command_handled = True

                # Media Control 
                elif any(word in command for word in ["play music", "pause music", "resume music"]):
                    speak_text = media_control("play_pause")
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                    
                elif any(word in command for word in ["next song", "skip song", "next track"]):
                    speak_text = media_control("next")
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                    
                elif any(word in command for word in ["previous song", "go back", "previous track"]):
                    speak_text = media_control("previous")
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                
                # System Control
                elif "lock computer" in command:
                    speak_text = lock_computer()
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                    
                elif "shutdown computer" in command or "turn off computer" in command:
                    speak_text = shutdown_computer()
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                
                # System Info
                elif "system health" in command or "cpu usage" in command or "memory load" in command:
                    speak_text = get_system_report()
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True

                # Weather
                elif "weather" in command or "raining" in command:
                    city = ""
                    if "in" in command:
                        parts = command.split(" in ")
                        if len(parts) > 1:
                            city = parts[1].strip()

                    city_to_check = city if city else user_data.get("default_city", "Patna")
                    weather_info = get_weather(city_to_check, api_key=WEATHER_API_KEY)

                    if weather_info:
                        if "raining" in command:
                            if "rain" in weather_info or "shower" in weather_info:
                                speak_text = f"Yes, it is currently raining in {city_to_check}."
                                speak(speak_text)
                                last_response = speak_text
                            else:
                                speak_text = f"No, it is not currently raining in {city_to_check}."
                                speak(speak_text)
                                last_response = speak_text
                        else:
                            speak(weather_info)
                            last_response = weather_info
                    else:
                        speak_text = "I was unable to get the weather information."
                        speak(speak_text)
                        last_response = speak_text
                    command_handled = True
                
                # Joke/Time/Date/Calculation
                elif "tell me a joke" in command or "tell me something funny" in command:
                    speak_text = pyjokes.get_joke()
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True

                elif "what time is it" in command or "time" in command:
                    tell_time()
                    command_handled = True
                elif "tell me the date" in command or "date" in command:
                    tell_date()
                    command_handled = True

                elif "calculate" in command or any(op in command for op in ['+', '-', '*', '/', 'times', 'x', 'divided by', 'plus', 'minus']):
                    do_local_calculation(command)
                    command_handled = True
                
                # To-Do List
                elif "what is on my to-do list" in command or "read my to-do list" in command:
                    get_to_do(tasks)
                    command_handled = True
                elif "add" in command and "to my to-do list" in command:
                    item = command.replace("add", "").replace("to my to-do list", "").strip()
                    add_to_do(tasks, item)
                    command_handled = True
                elif "delete" in command and "from my to-do list" in command:
                    item = command.replace("delete", "").replace("from my to-do list", "").strip()
                    delete_to_do(tasks, item)
                    command_handled = True
                
                # Clipboard History
                elif "save this" in command or "save the clipboard" in command:
                    text_to_save = pyperclip.paste()
                    if text_to_save:
                        clipboard_history.append(text_to_save)
                        speak_text = f"Okay, I've saved '{text_to_save[:50]}...' to your clipboard history."
                        speak(speak_text)
                        last_response = speak_text
                    else:
                        speak_text = "It seems your clipboard is empty."
                        speak(speak_text)
                        last_response = speak_text
                    command_handled = True

                # File Management
                elif "create file" in command or "make file" in command:
                    match = re.search(r'(?:create|make)\s+file\s+(.+)', command)
                    if match:
                        file_name = match.group(1).strip()
                        speak_text = create_text_file(file_name)
                        speak(speak_text)
                        last_response = speak_text
                    else:
                        speak("Please tell me the name of the file you want to create.")
                    command_handled = True

                elif "list files" in command or "what's in the directory" in command:
                    speak_text = list_directory()
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                
                elif "delete file" in command or "remove file" in command:
                    match = re.search(r'(?:delete|remove)\s+file\s+(.+)', command)
                    if match:
                        file_path = match.group(1).strip()
                        speak_text = delete_file(file_path)
                        speak(speak_text)
                        last_response = speak_text
                    else:
                        speak("Please tell me the path or name of the file to delete.")
                    command_handled = True
                
                elif "delete folder" in command or "remove folder" in command:
                    match = re.search(r'(?:delete|remove)\s+folder\s+(.+)', command)
                    if match:
                        folder_path = match.group(1).strip()
                        speak_text = delete_folder(folder_path)
                        speak(speak_text)
                        last_response = speak_text
                    else:
                        speak("Please tell me the path or name of the folder to delete.")
                    command_handled = True
                
                # Email/Prank
                elif "read unread emails" in command:
                    speak_text = read_unread_emails()
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                
                elif "send email to" in command:
                    # Multi-turn logic or better parsing needed here for robust sending, 
                    # but for now, rely on a specific syntax or simply inform the user.
                    speak("I need to know the recipient, subject, and body to send an email. For example: send email to Pratik with subject Test and body Hello.")
                    command_handled = True

                elif "show fake error" in command or "prank" in command:
                    speak_text = show_fake_error()
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                
                # Exit
                elif "exit" in command or "bye" in command or "goodbye" in command or "stop" in command:
                    speak("Goodbye! Have a great day.")
                    if server_thread and server_thread.is_alive():
                        try:
                            requests.post('http://localhost:5000/shutdown')
                        except requests.exceptions.ConnectionError:
                            pass
                    break 

            # --- LAST FALLBACK: NLP Processor & Conversation Engine ---
            if not command_handled:
                # 1. Check conversation engine (greetings, gratitude)
                if any(phrase in command for phrase in ["hello", "hi", "how are you"]):
                    speak_text = respond_to_greeting(command)
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                elif any(phrase in command for phrase in ["thank you", "thanks"]):
                    speak_text = handle_gratitude(command)
                    speak(speak_text)
                    last_response = speak_text
                    command_handled = True
                
                # 2. Check knowledge base and find best answer
                if not command_handled:
                    # Defensive check applied here to prevent 'str' object has no attribute 'get' error
                    if isinstance(knowledge_base, dict):
                        best_answer = find_best_answer(command, knowledge_base)
                        if best_answer:
                            speak(best_answer)
                            last_response = best_answer
                            command_handled = True
                    # If not handled, it falls to the final DNN check
                
                # 3. Custom DNN Intent Classification and Fallback Logic (FINAL DECISION CORE)
                if not command_handled:
                    
                    intent, confidence = classify_intent(clean_command, VEDRA_INTENT_CLASSIFIER)

                    if confidence > 0.85:
                        # High confidence: Attempt local execution first via NLP Processor/Hardcoded logic
                        print(f"[DNN CLASSIFIER: {intent} Intent detected with {confidence:.2f} confidence. Attempting local execution.]")
                        
                        # Use the general NLP processor for final guess commands (e.g., search, open apps)
                        processed_result = process_command(canonical_command, COMMAND_FUNCTION_MAP)
                        
                        if processed_result and processed_result.startswith(("Searching", "Opening")):
                            speak(processed_result)
                            last_response = processed_result
                            command_handled = True
                        
                        else:
                            # If local execution fails, but confidence is high:
                            
                            if intent in ["Query", "Conversation"]:
                                # Query/Conversation tasks go to the LLM for intelligence
                                print(f"[DNN CLASSIFIER: Local execution failed. Falling back to LLM Agent Core for complex {intent} task.]")
                                try:
                                    speak("I'm consulting my primary intelligence core for that information...")
                                    
                                    # 1. Get the LLM's raw output.
                                    llm_raw_output = get_llm_response(clean_command, AVAILABLE_TOOL_DESCRIPTIONS) 
                                    
                                    # 2. Pass the raw output and the function map to the new agent executor
                                    agent_result = execute_agent_command(llm_raw_output, TOOL_FUNCTION_MAP) 
                                    
                                    speak(agent_result)
                                    last_response = agent_result
                                    
                                except Exception as e:
                                    print(f"LLM Agent Core error: {e}")
                                    speak("I'm sorry, an unexpected error occurred in the primary intelligence core.")
                                    last_response = "I'm sorry, an unexpected error occurred in the primary intelligence core."
                                command_handled = True # LLM handled the error path
                                
                            elif intent == "System":
                                # System tasks go to the 'Ask to Learn' flow, as the LLM can't directly fix a local failure
                                print("[DNN CLASSIFIER: System command failed local execution. Initiating 'Ask to Learn' flow for a local action.]")
                                speak_text = f"I recognize that as a System command, but I don't know the exact steps for '{command}'. Would you like me to learn this command? Say 'yes' or 'no'."
                                speak(speak_text)
                                last_unrecognized_command = clean_command
                                last_command = "ask_to_learn"
                                last_response = speak_text
                                command_handled = True # Handled by the learning prompt


                    else:
                        # Low confidence: The old 'ask to learn' fallback for completely unknown commands
                        speak_text = f"I'm sorry, I don't know how to handle the command '{command}'. Would you like me to learn this command? Say 'yes' or 'no'."
                        speak(speak_text)
                        last_unrecognized_command = clean_command
                        last_command = "ask_to_learn"
                        last_response = speak_text
                        command_handled = True

        except Exception as e:
            if "KeyboardInterrupt" in str(e):
                break
            speak_text = "I'm sorry, an unexpected error occurred."
            speak(speak_text)
            last_response = speak_text
            print(f"Main loop error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()