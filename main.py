#!/usr/bin/env python3
# Welcome to Wouter's great AI. How can I help you?

import sys

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

from chatbot import *
from user_management import *
from utils import *


DEBUG = True  # increases verbosity
set_debug(DEBUG)


def calibrate():
    print(green("Calibrating... "), end='')
    sys.stdout.flush()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
    print(green("done"))


def welcome(welcome_message):
    print(blue(welcome_message))
    if not DEBUG:
        say(welcome_message)


def listen(text):
    print(green("Listening..."), end='\r')
    print("\033[K", end='')
    # return input("input: ")
    with sr.Microphone() as source:
        if text is not None:
            print(text)
        audio = r.listen(source, phrase_time_limit=10)
    return r.recognize_google(audio)  # language="zh-CN")


def say(text):
    # print(f"saying {text=}")
    tts = gTTS(text, tld="co.uk", lang="en")
    with open(".tmp.mp3", 'wb') as f:
        tts.write_to_fp(f)
    playsound(".tmp.mp3")


def get_user_input():
    while True:
        try:
            if DEBUG:
                raise KeyboardInterrupt
            user_phrase = listen(None)
        except KeyboardInterrupt:
            user_phrase = input(magenta("What do you want to say: "))
            print("\033[A\033[K", end='')
        if user_phrase != '':
            print(yellow(user_phrase))
            if user_phrase:
                break
    return user_phrase


def give_user_output(output):
    print(blue(output))
    if not DEBUG:
        say(output)


def home():
    if DEBUG:
        print(debug("Connection was successful"))
    print(blue("[R]egister or [L]ogin: "), end="\033[33m")
    choice = input().lower()
    if choice == "r":
        register()
        return home()
    elif choice == "l":
        if (usr := login()):
            return usr
        else:
            return home()
    else:
        print(blue(""))
        return home()


if __name__ == "__main__":
    user = home()
    if not DEBUG:
        r = sr.Recognizer()
        calibrate()
        clear_home()
    welcome(get_welcome_msg(user))

    while True:
        user_phrase = get_user_input()

        chatbot_response = generate_response(user_phrase.lower())
        give_user_output(chatbot_response)
