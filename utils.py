def red(s): # Debug messages
    return f"\033[1;31m{s}\033[0m"
def green(s): # Status updates
    return f"\033[32m{s}\033[0m"
def yellow(s): # User input
    return f"\033[33m{s}\033[0m"
def blue(s): # Chatbot output
    return f"\033[34m{s}\033[0m"
def magenta(s):
    return f"\033[35m{s}\033[0m"