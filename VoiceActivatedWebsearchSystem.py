import speech_recognition as sr
import webbrowser as wb
import sys
import time
import requests
from bs4 import BeautifulSoup
import pyttsx3
import random
from datetime import datetime
import pytz

# Configure UTF-8 encoding for console
sys.stdout.reconfigure(encoding='utf-8')

# Initialize speech engine
def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

# Function to display text with typing effect
def scrollTxt(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)

# Weather fetching function
def temp(city="tamil nadu"):
    try:
        url = f"https://www.google.com/search?q=weather+{city}"
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')

        # Extract temperature and sky conditions
        temp_div = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'})
        weather_div = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'})
        other_info_divs = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})

        if temp_div and weather_div and len(other_info_divs) > 5:
            temp = temp_div.text.replace('\u202f', ' ')
            str_weather = weather_div.text.replace('\u202f', ' ')
            data = str_weather.split('\n')
            sky = data[1] if len(data) > 1 else 'N/A'  # Extract only the sky condition, if available

            # Print and speak only relevant details (no "Other Details" section)
            print(f"Temperature: {temp}")
            print(f"Sky: {sky}")

            # Speak and display the relevant weather details only once
            speak(f"The temperature in {city} is {temp} and the sky is {sky}.")
            scrollTxt(f"Temperature: {temp}\nSky: {sky}")
        else:
            print("Could not fetch weather data. Please try again.")
            speak("I couldn't fetch the weather details. Please try again.")

    except Exception as e:
        print(f"Error fetching weather: {e}")
        speak("An error occurred while fetching the weather.")

# Function to get the current time in a specific location
def get_time(location="India"):
    try:
        # Define timezone mappings for some global locations
        timezones = {
            'india': "Asia/Kolkata",
            'usa': "US/Eastern",
            'london': "Europe/London",
            'paris': "Europe/Paris",
            'tokyo': "Asia/Tokyo",
            'sydney': "Australia/Sydney",
            'dubai': "Asia/Dubai",
            'new york': "US/New_York",
        }

        location = location.lower()

        # If the location is available in our timezone mapping, use that
        if location in timezones:
            timezone = pytz.timezone(timezones[location])
            location_time = datetime.now(timezone)
            current_time = location_time.strftime("%I:%M %p")  # Format: HH:MM AM/PM
            print(f"The current time in {location.capitalize()} is {current_time}.")
            speak(f"The current time in {location.capitalize()} is {current_time}.")
        else:
            speak(f"Sorry, I don't have time data for {location}. Please try another location.")

    except Exception as e:
        print(f"Error fetching time: {e}")
        speak("An error occurred while fetching the time.")

# Main program
def main():
    speak("Hi, welcome!")
    scrollTxt("Hi, Welcome\nHow can I help you?")
    speak("How can I help you?")

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Adjusted timeout and phrase time limit
            recognized_text = recognizer.recognize_google(audio).lower()

            print(f"Recognized: {recognized_text}")

            if 'google' in recognized_text or 'search' in recognized_text:
                query = recognized_text.replace('google', '').replace('search', '').strip()
                if query:
                    url = f"https://www.google.com/search?q={query}"
                    wb.get().open_new(url)
                    speak(f"Searching Google for {query}.")
                else:
                    speak("Please specify what you want to search for.")
            elif 'youtube' in recognized_text or 'video' in recognized_text:
                query = recognized_text.replace('youtube', '').replace('video', '').strip()
                if query:
                    url = f"https://www.youtube.com/results?search_query={query}"
                    wb.get().open_new(url)  # This opens YouTube directly with the search term
                    speak(f"Searching YouTube for {query}.")
                else:
                    speak("Please specify what you want to search on YouTube.")
            elif 'amazon' in recognized_text:
                query = recognized_text.replace('amazon', '').strip()
                if query:
                    url = f"https://www.amazon.in/s?k={query}"
                    wb.get().open_new(url)  # This opens Amazon with the search term
                    speak(f"Searching Amazon for {query}.")
                else:
                    url = "https://www.amazon.in"
                    wb.get().open_new(url)  # Opens Amazon homepage
                    speak("Opening Amazon.")
            elif 'flipkart' in recognized_text:
                query = recognized_text.replace('flipkart', '').strip()
                if query:
                    url = f"https://www.flipkart.com/search?q={query}"
                    wb.get().open_new(url)  # This opens Flipkart with the search term
                    speak(f"Searching Flipkart for {query}.")
                else:
                    url = "https://www.flipkart.com"
                    wb.get().open_new(url)  # Opens Flipkart homepage
                    speak("Opening Flipkart.")
            elif 'temperature' in recognized_text or 'weather' in recognized_text:
                speak("Please mention the city name.")
                try:
                    with sr.Microphone() as source:
                        print("Listening for city name...")
                        city_audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                        city = recognizer.recognize_google(city_audio)
                        print(f"City recognized: {city}")
                        temp(city)
                except sr.UnknownValueError:
                    print("Could not understand the city name.")
                    speak("I couldn't understand the city name. Please try again.")
                except sr.WaitTimeoutError:
                    print("Listening timed out while waiting for the city name.")
                    speak("You didn't respond in time. Please try again.")
                except Exception as e:
                    print(f"An error occurred while getting the city name: {e}")
                    speak("An error occurred while getting the city name.")
            elif 'time' in recognized_text:
                location = recognized_text.replace('time in', '').strip()
                if location:
                    get_time(location)
                else:
                    speak("Please specify the location for which you want the time.")
            elif 'tell me a joke' in recognized_text:
                joke_list = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "Why did the scarecrow win an award? Because he was outstanding in his field!"
                ]
                joke = random.choice(joke_list)
                speak(joke)
                scrollTxt(joke)
            else:
                speak("Sorry, I didn't understand that command.")
                print("Unrecognized command.")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        speak("I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Error with the speech recognition service: {e}")
        speak("There was an error with the speech recognition service.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        speak("An unexpected error occurred.")

# Run the program
if __name__ == "__main__":
    main()
