# Nutthakorn #################################

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
from time import ctime
import threading
import speech_recognition as speech
from gtts import gTTS
from googletrans import Translator
import random
import playsound
import os
import requests
import webbrowser



Lam = Translator()
data = speech.Recognizer()


#r = sr.Recognizer()

def record_audio(ask=False):
    with speech.Microphone() as source:
            if ask:
                alexis_speak(ask)

            #audio = data.listen(source,timeout=10 ,phrase_time_limit=10)
            audio = data.listen(source,timeout=10 ,phrase_time_limit=10)
            voice_data = ''
            try:
                voice_data = data.recognize_google(audio, None,'th')
                print('คุณพูดว่า : ',voice_data)
                trans_to_eng = Lam.translate(voice_data, src='th', dest='en')
                print('แปล : ',f'{trans_to_eng.text}')
                print('-----------------------------------------')
                trans_to_eng = trans_to_eng.text
                alexis_speak(trans_to_eng)

            except speech.UnknownValueError:
                alexis_speak('sorry, I did not get that')
            except speech.RequestError:
                alexis_speak('sorry, my speec service is down')
            return voice_data


def alexis_speak(audio_string):
    tts = gTTS(text=audio_string,lang='en')
    r = random.randint(1,10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    if 'what is your name' in voice_data:
        alexis_speak('My name is Alexis')
    if 'what time is it' in voice_data:
        alexis_speak(ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        alexis_speak('Here is what I found for' + search)
    if 'find location' in voice_data:
        search = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        alexis_speak('Here is the location of' + location)
    if 'exit' in voice_data:
        exit()
    


time.sleep(1)
alexis_speak('How can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)