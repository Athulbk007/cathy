# views.py

import speech_recognition as sr
import pyttsx3
import requests
import datetime
import wikipedia
from django.shortcuts import render
import webbrowser

def voice_assistant(request):
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print("User said: ", query)
        response_text = process_query(query)
        engine.say(response_text)
        engine.runAndWait()
    except Exception as e:
        print("Error: ", str(e))
        response_text = "Sorry, I couldn't understand. Please try again."

    return render(request, 'home.html', {'response_text': response_text})

def process_query(query):
    query = query.lower()

    if 'open youtube' in query:
        youtube_url = 'https://www.youtube.com/'
        webbrowser.open(youtube_url)
        return "I'm opening YouTube in your web browser..."
    
    elif "play" in query:
        play_url = "https://www.youtube.com/watch?v=aJOTlE1K90k&list=PLxA687tYuMWhkqYjvAGtW_heiEL4Hk_Lx&ab_channel=Maroon5VEVO"
        webbrowser.open(play_url)
        return "Playing a song on YouTube."

    elif 'weather' in query:
        return get_weather()

    elif 'search' in query:
        return "I'm sorry, searching the web is not implemented in this version."

    elif 'time' in query:
        return get_current_time()

    elif 'wikipedia' in query:
        search_query = query.replace('wikipedia', '').strip()
        return search_wikipedia(search_query)

    else:
        return "I'm sorry, I don't know how to help with that."

def get_weather():
    # Replace 'YOUR_WEATHER_API_KEY' with your actual API key from a weather data provider.
    api_key = 'YOUR_WEATHER_API_KEY'
    city = 'Kochi'  # Replace with the desired city or get it from user input.
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather_description = data['weather'][0]['description'].capitalize()
            temperature = data['main']['temp'] - 273.15  # Convert temperature from Kelvin to Celsius.
            return f"The weather in {city} is currently {weather_description}. The temperature is {temperature:.2f}°C."
        else:
            return "Sorry, I couldn't fetch the weather data at the moment."

    except requests.RequestException as e:
        return "Sorry, I couldn't fetch the weather data at the moment."



def get_current_time():
    now = datetime.datetime.now()
    time_string = now.strftime("%H:%M")
    return f"The current time is {time_string}."

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=1)
        return f"According to Wikipedia: {summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please be more specific in your search."
    except wikipedia.exceptions.PageError as e:
        return f"Sorry, I couldn't find any information on that topic in Wikipedia."
    except Exception as e:
        return "Sorry, an error occurred while searching Wikipedia."

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print("Speech Recognition request error: {0}".format(e))
    
    return ""

def open_website(url):
    webbrowser.open(url, new=2)

def scroll_page(direction):
    if direction == "up":
        # Simulate scroll-up command here
        print("Scrolling up...")
    elif direction == "down":
        # Simulate scroll-down command here
        print("Scrolling down...")
    else:
        print("Invalid command. Please say 'scroll up' or 'scroll down'.")

print("Welcome! How can I assist you?")
while True:
        command = listen_for_command()

        if "open website" in command:
            website_name = command.split("open website", 1)[1].strip()
            if website_name:
                url = f"https://www.{website_name}.com"
                open_website(url)
            else:
                print("Please specify a website name after 'open website'.")

        elif "search in website" in command:
            query = command.split("search in website", 1)[1].strip()
            if query:
                # Replace example.com with the website you want to search
                url = f"https://www.google.com/search?q={query}"
                open_website(url)
            else:
                print("Please specify a search query after 'search in website'.")

        elif "scroll up" in command:
            scroll_page("up")

        elif "scroll down" in command:
            scroll_page("down")

        elif "about the command" in command:
            print("This program allows you to interact with it using voice commands.")
            print("Supported commands:")
            print("- 'open website [website_name]': Opens the specified website.")
            print("- 'search in website [query]': Performs a search on the specified website.")
            print("- 'scroll up': Scrolls up on the currently opened webpage.")
            print("- 'scroll down': Scrolls down on the currently opened webpage.")
            print("- 'about the command': Provides information about the available voice commands.")

        elif "exit" in command:
            print("Goodbye!")
            break

        else:
            print("Command not recognized. Please try again.")





