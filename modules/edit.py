#!/usr/bin/env python3
from pathlib import Path,PurePath

######################
### CUSTOM MODULES ###
######################
from messages import error,warn

#################
### FUNCTIONS ###
#################
def obtain_current_version(contents):
    # Iterate through all entries within the $contents list
    for entry in contents:
        # Check if the current $entry starts with the $version_line
        if entry.startswith('Version:'):
            # If so, then return the version number only by splitting the $entry via the semicolon delimiter and then keeping only the last part of the split; `strip` removes extraneous whitespace
            return(entry.split(':')[-1].strip())
    # If the for-loop above did not exist within $contents, then display an error message to stdout and exit 1
    error(f"Unable to find the line within the .spec file that defines the current version.")

def define_new_version(kernel_dir):
    # Split the $kernel_dir via the dash character
    lst = kernel_dir.split('-')
    # The very first entry within $lst is going to be the current kernel version
    version = lst[0]
    # Iterate through the rest of the $lst starting from index 1
    for entry in lst[1:]:
        try:
            # Convert the current $entry into an integer
            revision = int(entry)
        except ValueError:
            # If $entry cannot be converted into type int, then continue to the next $entry
            continue
        # The $version string now includes the $revision number(s) as well
        version = f"{version}.{revision}"
    # Return the final $version
    return(version)

def all_replacements(current_version, redirect_url, kernel_dir, tarstrip):
    # Define the new version number, which includes revision numbers as well
    new_version = define_new_version(kernel_dir)
    # If the $current_version and $new_version are the same, then return bool False
    if current_version == new_version: return(False)
    # Define a dictionary that will contain all of the lines that will be modified
    replacements = dict()
    # Replacement for the 'Version' line
    replacements['Version:'] = f"Version:    {new_version}\n"
    # Replacement for the 'Source0' line
    replacements['Source0:'] = f"Source0:    {redirect_url}\n"
    # Replacement for the kernel directory RPM macro 
    replacements['%define _kerneldir'] = f"%define _kerneldir {kernel_dir}\n"
    # Replacement for the `tar` strip RPM macro
    replacements['%define _tarstrip'] = f"%define _tarstrip {tarstrip}\n"
    # Return the $replacements dictionary
    return(replacements)

def edit(contents, replacements):
    # Iterate through each key within the $replacements dictionary, and then iterate through each entry within $contents list. If the current line within $contents starts with $key, then replace the line with the $key's value, otherwise keep the line as-is
    for key in replacements: contents = [replacements[key] if entry.startswith(key) else entry for entry in contents]
    # Return the new $contents list
    return(contents)

############
### MAIN ###
############
def main(spec_file, redirect_url, kernel_dir, tarstrip):
    # Open the $spec_file and obtain its contents
    with open(spec_file, 'r') as f: contents = f.readlines()
    # Create a dictionary where the keys are the start of the line within $contents to edit, and the values are the replacement line
    replacements = all_replacements(obtain_current_version(contents), redirect_url, kernel_dir, tarstrip)
    # If the current version in the .spec file is equal to the new version, then there's nothing left to do so return bool False
    if replacements is False: return(False)
    # Edit the specified lines to reflect the new changes
    contents = edit(contents, replacements)
    # Once the replacement is done, overwrite the $spec_file with the new $contents
    with open(spec_file, 'w') as f: f.write(''.join(contents))
    # Return bool True to signify the $spec_file needs to be commited and pushed to the git repository
    return(True)
