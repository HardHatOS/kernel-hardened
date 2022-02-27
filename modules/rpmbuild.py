#!/usr/bin/env python3
from pathlib import Path,PurePath
from subprocess import CalledProcessError,run
from sys import argv

######################
### CUSTOM MODULES ###
######################
from git import add,commit,config,push
from messages import info,error

#################
### FUNCTIONS ###
#################
def args():
    try:
        # Argument 1: Full path to the directory that will hold the buildroot
        dirname = Path(argv[1]).expanduser().resolve()
    except IndexError:
        # If argument 1 was not defined, then display an error message to stdout and exit
        error('Argument 1: Directory that contains the source files and will contain the buildroot for `rpmbuild`')
    try:
        # Argument 2: Full path to the spec file
        spec_file = Path(argv[2]).expanduser().resolve()
    except IndexError:
        # If argument 2 was not defined, then display an error message to stdout and exit
        error('Argument 2: Full path to the spec file')
    # Verify $dirname is a valid directory
    isdir(dirname)
    # Verify $spec_file is a valid file
    isfile(spec_file)
    # Return the arguments
    return(dirname, spec_file)

def isdir(directory):
    # If $directory is valid, then return bool True
    if Path(directory).is_dir(): return(True)
    # If the $directory is not a valid directory, then display an error message to stdout
    error(f"Unable to locate directory: '{directory}'")

def isfile(filename):
    # If $filename is valid, then return bool True
    if Path(filename).is_file(): return(True)
    # If the $filename is not a valid filename, then display an error message to stdout
    error(f"Unable to locate file: '{filename}'")

def define(dirname, spec_file):
    # Define the directory that will serve as the build directory 
    builddir = ['--define', f"_builddir {dirname}"]
    # Define the directory that the build should take place in
    buildrootdir = ['--define', f"_buildrootdir {Path(dirname, 'buildrootdir')}"]
    # Define the directory that will hold the output RPM file 
    rpmdir_dir = Path(dirname, 'rpm')
    # Use the $rpmdir_dir in the command for `rpmbuild`
    rpmdir = ['--define', f"_rpmdir {rpmdir_dir}"]
    # Define the directory that contains the source files
    sourcedir = ['--define', f"_sourcedir {dirname}"]
    # Define the directory that contains the spec file
    specdir = ['--define', f"_specdir {PurePath(spec_file).parent}"]
    # Define the directory that will hold the output RPM file (.src.rpm), which is the same as $rpmdir above
    srcrpmdir = ['--define', f"_srcrpmdir {rpmdir_dir}"]
    # Define the type of build to perform
    # -ba: Build both the binary and source RPM
    # -bb: Only build the binary RPM package
    ba_spec_file = ['-ba', spec_file]
    # Define the full `rpmbuild` command
    cmd = ['rpmbuild'] + builddir + buildrootdir + rpmdir + sourcedir + specdir + srcrpmdir + ba_spec_file
    # Return the `rpmbuild` command as well as the $rpmdir_dir, which specifies the directory containing both the RPM and source RPM packages
    return(cmd, rpmdir_dir)

############
### MAIN ###
############
def main(dirname, spec_file):
    # Define the full `rpmbuild` command to execute as well as the directories that will contain the output RPM and source RPM packages
    [cmd, rpmdir_dir] = define(dirname, spec_file) 
    try:
        # Execute the `rpmbuild` command
        run(cmd, check = True)
    except CalledProcessError:
        # If the $cmd was unsuccessful, then return False in place of the $rpmdir
        return(False)
    # Return the directories that will contain the RPM and source RPM files
    return(PurePath(rpmdir_dir).name)

#############
### START ###
#############
if __name__ == '__main__':
    # If this script was called, then obtain the working directory ($dirname) as well as the full path to the spec file
    [dirname, spec_file] = args()
    # Start the main function
    rpmdir_dir = main(dirname, spec_file)
    # Check if $rpmdir_dir was defined, meaning the  the `rpmbuild` command was successful
    if rpmdir_dir:
        # Set up the git user's name and email
        config()
        # If so, then add the $rpmdir to the repository
        add(rpmdir_dir)
        # Create a commit message for both directories
        commit("Added the output RPM and source RPM directory from the `rpmbuild` command")
        # Push the changes to the repositories
        push()
