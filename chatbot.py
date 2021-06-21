from dataclasses import dataclass
import random
import re

from utils import *


@dataclass
class Response_pattern:
    pattern: str
    responses: list
    swap_pronouns: bool = True


R = Response_pattern


response_patterns = [
    R(r"(hi|hello)(\schatbot)?", [
        "Hi",
        "Hello",
        "G'day mate",
        "wazzup"]),

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

    R(r"would you ((like to )?(.*))", [
        r"I would really \g<1>.",
        r"I would really hate to \g<3>.",
        r"I don't know if I would \g<1>."]),

    R(r"(?:.*)?cyka blyat(?:.*)?", [
        r"Rush B no stop, my fellow comrad."]),

    R(r"is (.*)", [
        r"I think so?",
        r"I don't think so?",
        r"Yes, right?",
        r"No, right?"]),

    R(r"yes(?:\b.*)?", [
        r"Ok."
        r"What do you mean \g<0>?! I expected a no from you."]),

    R(r"no(?:\b.*)?", [
        r"Maybe not then."
        r"What do you mean \g<0>?! I expected a yes from you."]),

    R(r"are you (.*)", [
        r"Last time I checked I wasn't \g<1>.",
        r"I don't think I am \g<1>.",
        r"I don't know if i'm \g<1>. Are you?"]),

    R((r"why ((?:am|are|is|was|were|can|may|could|be|do|does|did|have|had|has|"
       r"may|might|must|shall|should|will|would)(?:n't)?) (.*)"), [
        r"I have absolutely no idea why \g<2> \g<1>."]),

    R((r"i ((?:am|was|have|had|do|did|say|said|make|made|went|took|came|see|"
       r"saw|get|got|will|would)(?:n't)?)(?:(\s)(.*))?"), [
        r"I think it's good that you \g<3>\g<2>\g<1>."]),

    R((r"(?:you|u) ((?:are|was|have|had|do|did|say|said|make|made|went|took|"
       r"came|see|saw|get|got|will|would)(?:n't)?)(?:(\s)(.*))?"), [
        r"Are you sure I \g<1>\g<2>\g<3>?"]),

    R(r"because (.*)", [
        r"Aah, right. Because \g<1>."]),

    R(r"i (mean|ment) (.*)", [
        r"I don't think you \g<1> \g<2>."]),

    R(r"(?:stop|goodbye|bye|see you|fuck off|adios|au revoir|doei|doeg)(.*)", [
        r"Never gonna give you up!\g<1>.",
        exit]),

    R(r"f(?:uck)?\s(?:u|you)(\s.*)?", [
        r"stfu\g<1>"]),

    R(r".+", [
        r"What do you mean \g<0>."]),
]


connectors = ["I'd like to hear more.",
              "That sounds interesting.",
              "Can you explain more?",
              "Tell me more!",
              "Nice! How can I help you?"]

welcome_messages = [r"Hello, {}!",
                    r"What's up, {}?",
                    r"Hi, {}!",
                    r"Welcome to Wouter's great AI. How can I help you?"]


def get_welcome_msg(user):
    return random.choice(welcome_messages).format(user.user_name)


def set_debug(debug):
    global DEBUG
    DEBUG = debug


# TODO: add informal patterns like "ain't": "am not"

pronoun_patterns = {
    "you": "I",
    "your": "my",
    "i": "you",
    "me": "you",
    "my": "your",
    "am": "are",
    "are": "am",
    "'m": "'re",
    "'re": "'m",
}

pronoun_pattern = (r"(?<=\b)(?:"
                   + r"|".join((p.replace("'",
                                          "QQQ") for p in pronoun_patterns))
                   + r")(?=\b)")


def sub_pronouns(matchobj):
    match = matchobj.group(0)
    if match in pronoun_patterns:
        return pronoun_patterns[match]


def swap_pronouns(phrase):
    phrase = re.sub(pronoun_pattern, sub_pronouns, phrase).strip()
    return phrase


def sub_hack(matchobj):
    return "XXX" + matchobj.group(0)


def generate_response(user_phrase):
    for response_pattern in response_patterns:
        match = re.fullmatch(response_pattern.pattern, user_phrase)
        if match:
            if DEBUG:
                print(red("User phrase:\t" + user_phrase))
                print(red("Pattern:\t" + response_pattern.pattern))
                print(red("Responses:\t" + str(response_pattern.responses)))
            random_response = random.choice(response_pattern.responses)
            if isinstance(random_response, str):
                user_phrase = re.sub(response_pattern.pattern,
                                     re.sub(pronoun_pattern,
                                            sub_hack,
                                            random_response,
                                            flags=re.IGNORECASE),
                                     user_phrase).replace("QQQ", "'")
                user_phrase = swap_pronouns(user_phrase)
                return user_phrase.replace("XXX", '')  # scuffed hack here
            elif callable(random_response):
                random_response()
                return
            else:
                raise NotImplementedError
    else:
        return random.choice(connectors)
