def bold(s):
    return f"\033[1m{s}\033[0m"
def red(s): # Debug messages and error exit messages
    return f"\033[1;31m{s}\033[0m"
def green(s): # Status updates
    return f"\033[1;32m{s}\033[0m"
def yellow(s): # User input
    return f"\033[1;33m{s}\033[0m"
def blue(s): # Chatbot output
    return f"\033[1;34m{s}\033[0m"
def magenta(s):
    return f"\033[1;35m{s}\033[0m"
def debug(s):
    return f"\033[1;31m{s}\033[0m"
def clear_home():
    print("\033[2J\033[H", end='')