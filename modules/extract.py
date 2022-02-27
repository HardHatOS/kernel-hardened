#!/usr/bin/env python3
from os import chdir
from pathlib import Path,PurePath
from subprocess import run

######################
### CUSTOM MODULES ###
######################
from messages import error,info

############
### MAIN ###
############
def main(dirname, filename):
    # Change directory into $dirname
    chdir(dirname)
    # Display informational message to stdout
    info(f"Extracting the contents of: {filename}")
    # Extract the contents of $filename
    run(['tar', '--use-compress-program=unzstd', '-x', '-f', filename])
    try:
        # Return the path to the linux-hardened directory within the specified path. This directory name uses the version number so it can't be hardcoded
        for directory in Path(PurePath(dirname, 'usr', 'lib', 'modules')).iterdir(): return(directory)
    except FileNotFoundError:
        # If the path is no longer valid (eg. the packaging format changes), then display an error message to stdout
        error(f"The extracted file directory structure has changed, you will need to edit this script.")
