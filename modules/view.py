#!/usr/bin/env python3
from pathlib import Path,PurePath
from subprocess import CalledProcessError,run

######################
### CUSTOM MODULES ###
######################
from messages import error,info

#################
### FUNCTIONS ###
#################
def stdout(archive, output):
     # Decode stdout from bytes to str
    output = output.stdout.decode()
    # Find the 'vmlinuz' kernel file within the archive
    vmlinuz = [entry for entry in output.split() if entry.endswith('vmlinuz')]
    try:
        # Unnest the $vmlinuz list, which should only have a single entry
        vmlinuz = vmlinuz[0]
    except IndexError:
        # If the kernel file could not be found, then display an error message to stdout and exit
        error(f"Unable to find the 'vmlinuz' kernel file within the archive: '{archive}'")
    # Obtain the parts of the relative path to $vmlinuz
    vmlinuz_parts = PurePath(vmlinuz).parts
    # The path structure will look like so: ['path', 'to', '5.15.21-hardened1-3-hardened', 'vmlinuz'] for example. So [-1] is 'vmlinuz', and [-2] is the parent kernel directory
    kernel_dir_index = -2
    # Obtain the name of the parent kernel directory
    kernel_dir = vmlinuz_parts[kernel_dir_index]
    # Determine how many levels the $kernel_dir is nested. This number will be used with `tar` in the spec file to extract only the $kernel_dir
    strip = len(vmlinuz_parts[:kernel_dir_index])
    # Return the $kernel_dir and `tar` strip count
    return(kernel_dir, strip)

############
### MAIN ###
############
def main(archive):
    try:
        # View the contents of $archive
        output = run(['tar', '-t', '-f', archive], check = True, capture_output = True)
    except CalledProcessError:
        # If the command failed, then show the stderr message from the `tar` command
        print(output.stderr.decode())
        # Display an error message to stdout and exit
        error(f"Unable to view the contents of the archive: '{archive}'")
    # Parse the $output and obtain the name of the kernel directory ($kernel_dir) and how many levels it's nested ($strip)
    [kernel_dir, strip] = stdout(archive, output)
    # Return the variables
    return(kernel_dir, strip)
