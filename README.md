[![CI](https://github.com/HardHatOS/kernel-hardened/actions/workflows/kernel-hardened.yml/badge.svg)](https://github.com/noatsecure/kernel-hardened/actions/workflows/kernel-hardened.yml)

# kernel-hardened

## About
This repository tracks the hardened Linux kernel from the Arch Linux repositories ([link](https://archlinux.org/packages/extra/x86_64/linux-hardened)). This is performed using GitHub's continuous integration, where the `ci-kernel-hardened.py` script is ran every 3 hours to check for new updates. If there are any, then the `kernel-hardened.spec` file is automatically updated, triggering the Hard Hat Copr repository ([link](https://copr.fedorainfracloud.org/coprs/hardhatos/release)) to automatically start the build process for the latest version of Fedora Linux.

## Instructions
All commands will need to be entered as the root user.

1. Enable the Hard Hat Copr repository: `dnf copr enable hardhatos/release`
  
2. Update the cache: `dnf update`
  
3. Install the package: `dnf install kernel-hardened`

## Known Issues
- If you boot into the hardened kernel at least once then the next time you boot into the vanilla Fedora kernel you will have to wait for SELinux to perform a full system relabel. Once the relabel is complete the system will reboot one last time, so make sure you choose the vanilla kernel again to avoid having to go through this process.
