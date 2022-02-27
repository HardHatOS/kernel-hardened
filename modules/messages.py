#!/usr/bin/env python3

#################
### FUNCTIONS ###
#################
def error(msg = False):
    # If an error message was specified, then display it to stdout
    if msg: print(f"ERROR: {msg}")
    # Exit with an error
    exit(1)

def info(msg):
    # Display the informational message to stdout
    print(f"INFO: {msg}")

def warn(msg):
    # Display the warning message to stdout
    print(f"WARN: {msg}")
