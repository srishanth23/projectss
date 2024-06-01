import speech_recognition as sr
import pyttsx3
import datetime
import requests

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return "Sorry, I did not get that."
    except sr.RequestError:
        return "Sorry, my speech service is down."

def tell_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def tell_date():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d")

def search_web(query):
    api_key = 'YOUR_API_KEY'
    search_engine_id = 'YOUR_SEARCH_ENGINE_ID'
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}"
    response = requests.get(url)
    results = response.json()
    try:
        return results['items'][0]['snippet']
    except KeyError:
        return "No results found."

def main():
    speak("Hello! How can I help you today?")
    while True:
        command = recognize_speech()
        if "hello" in command:
            speak("Hello! How can I assist you?")
        elif "time" in command:
            speak(f"The current time is {tell_time()}")
        elif "date" in command:
            speak(f"Today's date is {tell_date()}")
        elif "search" in command:
            speak("What do you want to search for?")
            query = recognize_speech()
            result = search_web(query)
            speak(f"Here is what I found: {result}")
        elif "exit" in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
