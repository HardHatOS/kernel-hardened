#!/usr/bin/env python3
from pathlib import Path,PurePath
from ssl import create_default_context
from urllib.request import urlopen

######################
### CUSTOM MODULES ###
######################
from messages import error,info

###########
### URL ###
###########
# URL that redirects to an Arch Linux mirror that has the linux-hardened package
url = 'https://archlinux.org/packages/extra/x86_64/linux-hardened/download'

#################
### FUNCTIONS ###
#################
def ssl():
    # Define Python's default SSL context
    context = create_default_context()
    # [DISABLED] Enforce the same TLS version for the minimum as the maximum. For now this causes issues with a lot of mirrors, so the default minimum version is TLSv1.2
    #context.minimum_version = context.maximum_version
    # Return the SSL context
    return(context)

############
### MAIN ###
############
def main():
    # Display informational message to stdout
    info(f"The hardened kernel package is now being downloaded from: {url}")
    # Request the linux-hardened package from the $url. Here, the context is set to the return variable of the ssl() function, which enforces strong TLS
    request = urlopen(url, context = ssl())
    # The $url points to a mirror, so obtain the actual URL that was used to download the package from
    redirect_url = request.geturl()
    # If the return status is anything besides 200, then the download failed
    if request.status != 200: error(f"Unable to download the linux-hardened package from: {redirect_url}")
    # Display the mirror that was used to stdout
    info(f"The following mirror was used to download the linux-hardened package: {redirect_url}")
    # Define the full path for the output file based on the $download_dir and the package name
    pkg_file = PurePath(redirect_url).name
    # Return the $redirect_url, $pkg_file, and the binary contents for the linux-hardened compressed file
    return(redirect_url, pkg_file, request.read())
