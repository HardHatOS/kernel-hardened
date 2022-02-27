#!/usr/bin/env python3
from pathlib import Path,PurePath

######################
### CUSTOM MODULES ###
######################
from git import commit,remove
from messages import info

#################
### FUNCTIONS ###
#################
def outdated_packages(dirname):
    # Find the older compressed package(s)
    packages = [f for f in Path(dirname).iterdir() if f.as_posix().endswith('.tar.zst')]
    # Remove the older package(s)
    [remove(f) for f in packages]
    # Commit the changes for the older package(s)
    [commit(f"Removed: {PurePath(f).name}", f) for f in packages]

############
### MAIN ###
############
def main(dirname, filename, binary_contents):
    # If there is an existing Arch Linux kernel package, then remove it from the repository and commit the changes
    outdated_packages(dirname)
    # Display informational message to stdout
    info(f"Writing the binary data of the hardened kernel package to: {filename}")
    # Write the new $filename file, which is the linux-hardended compressed package from the Arch Linux repositories
    with open(filename, 'wb') as f: f.write(binary_contents)
    # Return the $filename
    return(filename)
