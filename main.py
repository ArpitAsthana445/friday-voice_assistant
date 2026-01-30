import os
import time
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicli  # make sure this file is included in repo
from openai import OpenAI
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Speak function
def speak(text):
    print({text})  
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        speak("OpenAI API key not found. Please set your environment variable.")
        return "API key missing"

    client = OpenAI(api_key=api_key)
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant, skilled like Alexa and Siri"},
            {"role": "user", "content": command},
        ]
    )
    return completion.choices[0].message.content

# Process command function
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c:
        webbrowser.open("https://www.facebook.com")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicli.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I could not find the song {song}")
    elif "search" in c:
        search_query = c.replace("search", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak(f"Searching {search_query}")
    else:
        output = aiprocess(c)
        speak(output)

# Main program
if __name__ == "__main__":
    speak("Hii sir")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            word = recognizer.recognize_google(audio)
            if word.lower() == "friday":
                speak("ya")
                time.sleep(0.5)

                with sr.Microphone() as source:
                    print("Friday active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                processCommand(command)

        except Exception as e:
            print("Error:", e)
