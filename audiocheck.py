import speech_recognition as sr
import webbrowser
import pyttsx3
import time
from openai import OpenAI

# 1. Engine Initialization (SAPI5 for Windows stability)
try:
    engine = pyttsx3.init('sapi5')
except:
    engine = pyttsx3.init()

# Awaaz ki settings
engine.setProperty('rate', 180)  # Thodi normal speed
engine.setProperty('volume', 1.0) # Full volume

def speak(text):
    print(f"Friday: {text}")
    # Ye block engine ko hang hone se bachata hai
    if engine._inLoop:
        engine.endLoop()
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    try:
        client = OpenAI() # API Key environment variable se lega
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Friday, like Alexa or Siri."},
                {"role": "user", "content": command},
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "I am having trouble connecting to OpenAI. Please check your API key."

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "search" in c:
        search_query = c.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching for {search_query}")
    else:
        # OpenAI handle karega
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    speak("System Online. Hii sir")

    while True: 
        try:
            # Step 1: Wake word 'Friday' ke liye sunna
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("\nListening for wake word 'Friday'...")
                # phrase_time_limit se mic jaldi band hota hai taaki speak() jaldi chale
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
            
            # Mic yahan band ho gaya
            word = recognizer.recognize_google(audio)
            print(f"Recognized: {word}")

            if word.lower() == "friday":
                # Step 2: Response dena
                speak("ya") 
                
                # Step 3: Command sunna
                with sr.Microphone() as source:
                    print("Friday is listening for your command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    
                processCommand(command)

        except sr.UnknownValueError:
            # Jab kuch sunai na de toh error na dikhaye
            pass
        except Exception as e:
            print(f"Error: {e}")