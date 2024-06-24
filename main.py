import speech_recognition as sr
import webbrowser
import pyttsx3
from newsapi import NewsApiClient
from setuptools import setup
import musicLibrary
import requests
import google.generativeai as genai
# from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsApiKey = 'NEWS_API_KEY'


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command1):
    genai.configure(api_key='GEMINI_API_KEY')

    model = genai.GenerativeModel()
    response = model.generate_content(command1)

    return response.text


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open('https://www.google.com')
    elif "jarvis" in c.lower():
        speak("hello sir, how may i help you")
    elif "youtube" in c.lower():
        webbrowser.open('https://www.youtube.com')
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "khabar" in c.lower():
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApiKey}')
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])

    else:
        # let openAi handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis")
    # Listen for the wake word
    # obtain audio from the microphone
    while True:
        r = sr.Recognizer()

        # recognize speech using Sphinx
        print("Recognizing...")
        try:
            # with sr.Microphone() as source:
            #     print("Listening...!")
            #     audio = r.listen(source, timeout=2, phrase_time_limit=1)
            # word = r.recognize_google(audio)
            # if word.lower() == "hello":
            #     speak("Yes sir")
            with sr.Microphone() as source:
                print("Listening...!")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
                command = r.recognize_google(audio)
                print(command)
                processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
