#!/usr/bin/env python3
from os import environ
from pathlib import PurePath
from subprocess import run

######################
### CUSTOM MODULES ###
######################
from messages import error,info

############
### MAIN ###
############
def add(name):
    # Display informational message to stdout
    info(f"Adding the following file/directory to the repository: {name}")
    # Add the $name file/directory to commit
    run(['git', 'add', name])

def commit(msg, name = False):
    # Check if a specific file/directory is the target of this commit
    if name:
        # If so, then create a commit for only the specified $name file/directory
        run(['git', 'commit', name, '-m', msg])
    else:
        # Otherwise commit every change made within the repository
        run(['git', 'commit', '-a', '-m', msg])

def config():
    # Obtain the commit author's name from the specified environment variable
    user_name = environ['CI_COMMIT_AUTHOR']
    # If the $user_name is empty, then display an error message to stdout and exit 1
    if not user_name: error("The 'CI_COMMIT_AUTHOR' environment variable has not been set!")
    # Obtain the commit author's email from the specified environment variable
    user_email = environ['CI_COMMIT_AUTHOR_EMAIL']
    # If the $user_email is empty, then display an error message to stdout and exit 1
    if not user_email: error("The 'CI_COMMIT_AUTHOR_EMAIL' environment variable has not been set!")
    # Configure the git user name
    run(['git', 'config', '--global', 'user.name', user_name])
    # Configure the git user email
    run(['git', 'config', '--global', 'user.email', user_email])

def push():
    # Push the new $directory to the repository
    run(['git', 'push'])

def remove(name):
    # Display informational message to stdout
    info(f"Removing the following file/directory from the repository: {name}")
    # Create the commit message
    msg = f"Removed: {PurePath(name).name}"
    # Remove the $name file/directory
    run(['git', 'rm', '-r', name])
