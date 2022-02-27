#!/usr/bin/env python3
from os import chdir
from pathlib import Path,PurePath
from sys import argv,path

#############
### PATHS ###
#############
# Current working directory of this script
cwd = Path(PurePath(argv[0]).parent).resolve()

################################
### CUSTOM MODULES DIRECTORY ###
################################
# Define the full path to the directory containing all the custom modules used in this script
modules_dir = Path(cwd, 'modules')

# Check if $modules_dir is a valid directory. An if-else statement is used since `path.append` allows you to add non-existant directories without error
if Path(modules_dir).is_dir():
    # If so, then add the $modules_dir to the path
    path.append(modules_dir.as_posix())
else:
    # Display an error message to stdout
    print(f"ERROR: Unable to locate the modules directory at the following location: {modules_dir}")
    # Exit with an error
    exit(1)

######################
### CUSTOM MODULES ###
######################
from download import main as download
from edit import main as edit
from git import commit,config,push
from messages import error,info
from view import main as view
from write import main as write

#################
### FUNCTIONS ###
#################
def args():
    try:
        # Argument 1: Full path to the .spec file
        spec_file = Path(argv[1]).resolve()
    except IndexError:
        # If argument 1 was not specified, then display an error message to stdout and exit
        error('Argument 1: Specify the path to the .spec file')
    # Return the arguments
    return(spec_file)

def isfile(filename):
    # Check if $filename is a valid file, and if so, return bool True
    if Path(filename).is_file(): return(True)
    # Otherwise, if the $filename is not a valid file display an error message to stdout and exit
    error(f"Unable to locate the following file: '{filename}'")

############
### MAIN ###
############
def main(spec_file):
    # Verify the $spec_file is a valid file
    isfile(spec_file)
    # Setup the global git configuration
    config()
    # Obtain the binary contents of the linux-hardened package from the Arch Linux repository
    [redirect_url, pkg_filename, binary_contents] = download()
    # First, write the $binary_contents data obtained from the Arch Linux mirror to a new $pkg_filename 
    pkg_filename = write(cwd, Path(cwd, pkg_filename), binary_contents)
    # View the tar archive and obtain the name of the kernel directory, which changes based on version number
    [kernel_dir, tarstrip] = view(pkg_filename)
    # Edit the spec file, used by `rpmbuild` to build a RPM package
    update = edit(spec_file, redirect_url, kernel_dir, tarstrip)
    # Check if $update is True, meaning the $spec_file was updated to a new kernel version
    if update is True:
        # Define the commit message
        commit(f"Updated to: {PurePath(pkg_filename).name}", spec_file)
        # Finally, push all changes to the repository
        push()
    else:
        # Otherwise, display an informational message that there's nothing to do
        info('The kernel is up-to-date, no action needed')
    
#############
### START ###
#############
if __name__ == '__main__':
    # Obtain the full path to the .spec file
    spec_file = args()
    # Execute the main function
    main(spec_file)
