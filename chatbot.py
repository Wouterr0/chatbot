#!/usr/bin/env python3
# Welcome to Wouter and Ruben's great AI. How can I help you?

import sys
import random
import re
from collections import OrderedDict

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound


DEBUG = False

if not DEBUG:
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
    tts = gTTS(text, tld="co.uk", lang="en")
    with open(".tmp.mp3", 'wb') as f:
        tts.write_to_fp(f)
    playsound(".tmp.mp3")



responses = OrderedDict([
    (r"(hi|hello)(\schatbot)?", [
        "Hi",
        "Hello",
        "G'day mate",
        "wazzup"]),
    (r"no", [
        "Ok.",
        "Maybe not then."]),
    (r"(what's up|how do you feel|how are you)(\s\w+)?", [
        "Great! How about you?",
        "Fantastic! How are you?",
        "I'm good, thanks! How are you today?"]),
    (r"good (\w+)", [
        r"Good \g<1>!"]),
    (r"i think (.*)", [
        r"What makes you think \g<1>?"]),
    (r"i (\w+) you", [
        r"Why do you \g<1> me?"]),
    (r"i feel (.*)", [
        r"Why do you feel \g<1>?"]),
    (r"(i am|i'm) (.*)", [
        r"Why are you \g<2>?"]),
    (r"i want to (.*)", [
        r"Why do you want to \g<1>?"]),
    (r"i like (?!you$)(.*)", [
        r"Why do you like \g<1>?"]),
    (r"what's your (.*)", [
        r"I don't have a \g<1>."]),
    (r"would you like to (.*)", [
        r"I don't know."]),
    (r"are you (.*)", [
        r"Last time I checked I wasn't \g<1>.",
        r"I don't think I am \g<1>.",
        r"I don't know if i'm \g<1>. Are you?"]),
    (r"why (am|are|is|was|were|will)(n't)? (.*)", [
        r"I have absolutely no idea why \g<3> \g<1>\g<2>."]),
    (r"because (.*)", [
        r"Aah, right. Because \g<1>."]),
    (r"stop (.*)", [
        r"I will never stop \g<1>."]),
    (r".+", [
        r"What do you mean \g<0>."]),
])


connectors = ["I'd like to hear more.", "That sounds interesting.", "Can you explain more?", "Tell me more!", "Nice! How can I help you?"]

welcome_messages = ["Hello!", "What's up?", "Hi!", "Welcome to Wouter's great AI. How can I help you?"]



pronoun_patterns = OrderedDict([
    (r"(\s|^)you\s",   " me "),
    (r"(\s|^)your\s",  " my "),
    (r"(\s|^)(I|i)\s", " you "),
    (r"(\s|^)my\s",    " your "),
    (r"(\s|^)am\s",    " are "),
])


def swap_pronouns(phrase):
    for pronoun_pattern in pronoun_patterns:
        phrase = re.sub(pronoun_pattern, pronoun_patterns[pronoun_pattern], phrase).strip()
    return phrase


def generate_response(user_phrase):
    for pattern in responses:
        match = re.fullmatch(pattern, user_phrase)
        if match:
            print(red(user_phrase), red(swap_pronouns(user_phrase)), sep='\n')
            return re.sub(pattern, random.choice(responses[pattern]), swap_pronouns(user_phrase))
    else:
        return random.choice(connectors)


welcome_message = random.choice(welcome_messages)
if not DEBUG:
    say(welcome_message)
print(blue(welcome_message))

while True:
    while True:
        try:
            if DEBUG:
                raise KeyboardInterrupt
            user_phrase = listen(None)
        except KeyboardInterrupt:
            user_phrase = input(magenta("What do you want to say: "))
        print(yellow(user_phrase))
        if user_phrase != None:
            break
    chatbot_response = generate_response(user_phrase.lower())
    if not DEBUG:
        say(chatbot_response)
    print(blue(chatbot_response))
