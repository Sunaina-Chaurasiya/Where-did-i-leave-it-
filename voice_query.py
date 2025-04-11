# voice_query.py

import speech_recognition as sr
from database import get_item_location

def extract_item_name(query, known_items):
    for item in known_items:
        if item in query.lower():
            return item
    return None
# Install: pip install pyttsx3
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    
    # Customize voice (optional)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female
    engine.setProperty('rate', 150)  # Speed (words per minute)
    
    engine.say(text)
    engine.runAndWait()

def get_voice_query_and_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"📝 You said: {query}")

        # Define list of tracked items
        tracked_items = ["tv","wallet", "bottle", "phone", "bag", "keys","cell phone","tie", "person"]

        item = extract_item_name(query, tracked_items)

        if item:
            result = get_item_location(item)
            if result:
                location, timestamp = result
                print(f"📍 Your {item} was last seen at: {location} 🕒 {timestamp}")
                text='Your ',item,'was last seen at:', location,'at',timestamp
                speak(text)
            else:
                print(f"❌ No records found for: {item}")
        else:
            print("🤖 I couldn't recognize any known item in your query.")

    except sr.UnknownValueError:
        print("😕 Could not understand the audio.")
    except sr.RequestError as e:
        print(f"🚫 API error: {e}")

if __name__ == "__main__":
    get_voice_query_and_search()

