#!/usr/bin/env python3
# Welcome to Wouter and Ruben's great AI. How can I help you?

import sys
import random
import re

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound



r = sr.Recognizer()
with sr.Microphone() as source:
    print("Calibrating")
    r.adjust_for_ambient_noise(source)


def red(s):
    return f"\033[31m{s}\033[0m"
def green(s):
    return f"\033[32m{s}\033[0m"
def yellow(s):
    return f"\033[33m{s}\033[0m"
def blue(s):
    return f"\033[34m{s}\033[0m"
def magenta(s):
    return f"\033[35m{s}\033[0m"


def listen(text):
    print(green("Please say something..."), end='\r')
    print("\x1b[K", end='')
    # return input("input: ")
    with sr.Microphone() as source:
        if text != None:
            print(text)
        audio = r.listen(source, phrase_time_limit=10)
    return r.recognize_google(audio)#, language="zh-CN")


def say(text):
    # print(f"saying {text=}")
    tts = gTTS(text)
    with open(".tmp.mp3", 'wb') as f:
        tts.write_to_fp(f)
    playsound(".tmp.mp3")
    




static_responses = {
    (r"(hi|hello)(\schatbot)?",):  ["Hi", "Hello", "G'day mate", "wazzup"],
    ("no",): ["Ok.", "Maybe not then."],
    ("what's up", "how do you feel", "how are you(\s\w+)?"): ["Great!", "Fantastic!", "I'm good, thanks! How about you?"],
}



dynamic_responses = {
    r"good (\w+)":      r"Good \g<1>!",
    r"i think (.*)":    r"What makes you think \g<1>?",
    r"i (.*) you":      r"Why do you \g<1> me?",
    r"i feel (.*)":     r"Why do you feel \g<1>?",
    r"i am (.*)":       r"Why are you \g<1>?",
    r"i'm (.*)":       r"Why are you \g<1>?",
    r"i want to (.*)":  r"Why do you want to \g<1>?",
    r"i like (?!you$)(.*)": r"Why do you like \g<1>?",
}


connectors = ["I'd like to hear more.", "That sounds interesting.", "Can you explain more?", "Tell me more!", "Nice! How can I help you?"]

welcome_messages = ["Hello!", "What's up?", "Hi!", "Welcome to Wouter and Ruben's great AI. How can I help you?"]



pronoun_patterns = {
    r"(\s|^)i\s": " you ",
    r"(\s|^)my\s": " your ",
    r"(\s|^)you\s": " me ",
    r"(\s|^)your\s": " my ",
}

def swap_pronouns(phrase):
    for pronoun_pattern in pronoun_patterns:
        return re.sub(pronoun_pattern, pronoun_patterns[pronoun_pattern], phrase).strip()


def generate_response(user_phrase):
    for pattern_group in static_responses:
        for pattern in pattern_group:
            match = re.fullmatch(pattern, user_phrase)
            if match:
                return random.choice(static_responses[pattern_group])
    for pattern in dynamic_responses:
        match = re.fullmatch(pattern, user_phrase)
        if match:
            return swap_pronouns(re.sub(pattern, dynamic_responses[pattern], user_phrase))
    else:
        return random.choice(connectors)


welcome_message = random.choice(welcome_messages)
say(welcome_message)
print(blue(welcome_message))

while True:
    while True:
        try:
            user_phrase = listen(None)
        except KeyboardInterrupt:
            user_phrase = input(magenta("What do you want to say: "))
        print(yellow(str(user_phrase)))
        if user_phrase != None:
            break
    chatbot_response = generate_response(user_phrase.lower())
    say(chatbot_response)
    print(blue(chatbot_response))
