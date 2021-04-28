from dataclasses import dataclass
import random
import re

from utils import *

@dataclass
class Response_pattern:
    pattern: str
    responses: list
    swap_pronouns: bool = False


R = Response_pattern


response_patterns = [
    R(r"(hi|hello)(\schatbot)?", [
        "Hi",
        "Hello",
        "G'day mate",
        "wazzup"]),
    
    R(r"no", [
        "Ok.",
        "Maybe not then."]),
    
    R(r"(what's up|how do you feel|how are you)(\s\w+)?", [
        "Great! How about you?",
        "Fantastic! How are you?",
        "I'm good, thanks! How are you today?"]),
    
    R(r"good (\w+)", [
        r"Good \g<1>!"]),
    
    R(r"i think (.*)", [
        r"What makes you think \g<1>?"]),
    
    R(r"i (\w+) you", [
        r"Why do you \g<1> me?"]),
    
    R(r"i feel (.*)", [
        r"Why do you feel \g<1>?"]),
    
    R(r"(i am|i'm) (.*)", [
        r"Why are you \g<2>?"]),
    
    R(r"i want to (.*)", [
        r"Why do you want to \g<1>?"]),
    
    R(r"i like (?!you$)(.*)", [
        r"Why do you like \g<1>?"]),
    
    R(r"what's your (.*)", [
        r"I don't have a \g<1>."]),
    
    R(r"would you like to (.*)", [
        r"I don't know."]),
    
    R(r"are you (.*)", [
        r"Last time I checked I wasn't \g<1>.",
        r"I don't think I am \g<1>.",
        r"I don't know if i'm \g<1>. Are you?"]),
    
    R(r"why ((?:am|are|is|was|were|will)(?:n't)?) (.*)", [
        r"I have absolutely no idea why \g<2> \g<1>."]),
    
    R(r"because (.*)", [
        r"Aah, right. Because \g<1>."]),
    
    R(r"i mean (.*)", [
        r"I don't think you ment \g<1>."]),
    
    R(r"stop (.*)", [
        r"I will never stop \g<1>."]),
    
    R(r".+", [
        r"What do you mean \g<0>."], True),
]


connectors = ["I'd like to hear more.", "That sounds interesting.", "Can you explain more?", "Tell me more!", "Nice! How can I help you?"]

welcome_messages = ["Hello!", "What's up?", "Hi!", "Welcome to Wouter's great AI. How can I help you?"]

def get_welcome():
    return random.choice(welcome_messages)

def set_debug(debug):
    global DEBUG
    DEBUG = debug

pronoun_patterns = {
    "you":  "I",
    "your": "my",
    "i":    "you",
    "my":   "your",
    "am":   "are",
    "are":  "am",
}

def sub_pronouns(matchobj):
    match = matchobj.group(0)
    if match in pronoun_patterns:
        return pronoun_patterns[match]

def swap_pronouns(phrase):
    pronoun_pattern = r"(?<=\b)(?:" + '|'.join((p for p in pronoun_patterns)) + r")(?=\b)"
    phrase = re.sub(pronoun_pattern, sub_pronouns, phrase).strip()
    return phrase



def generate_response(user_phrase):
    for response_pattern in response_patterns:
        match = re.fullmatch(response_pattern.pattern, user_phrase)
        if match:
            if response_pattern.swap_pronouns:
                user_phrase = swap_pronouns(user_phrase)
            if DEBUG:
                print(red("User phrase:\t" + user_phrase))
                print(red("Pattern:\t" + response_pattern.pattern))
            return re.sub(response_pattern.pattern, random.choice(response_pattern.responses), user_phrase)
    else:
        return random.choice(connectors)
