Name:       kernel-hardened
Version:    5.15.25.1
Release:    1%{?dist}
Provides:   installonlypkg(kernel-hardened)
Summary:    The hardened linux kernel

Group:      System Environment/Base
License:    GPLv2 and Redistributable, no modification permitted
URL:        https://github.com/noatsecure/kernel-hardened
Source0:    https://mirror.ubrco.de/archlinux/extra/os/x86_64/linux-hardened-5.15.25.hardened1-1-x86_64.pkg.tar.zst
BuildArch:  x86_64
BuildRequires: tar, zstd

%description
The hardened Linux kernel; originally from the Arch Linux repository and repackaged for Fedora Linux

%prep
# Define RPM macro for the specified filesystem path
%define _libmodules %{_prefix}/lib/modules

# Define RPM macro for the name of the directory containing the compiled kernel and its modules
%define _kerneldir 5.15.25-hardened1-1-hardened

# Define RPM macro for the number of levels to use when extracting the kernel directory from %SOURCE0
%define _tarstrip 3

%install
# Create the /usr/lib/modules directory within %buildroot
%{__mkdir} -p %{buildroot}%{_libmodules}

# Change directory
cd %{buildroot}%{_libmodules}

# Uncompress the kernel archive
%{__tar} --use-compress-program=unzstd -x -f %{SOURCE0} --strip %{_tarstrip}

%files
%{_libmodules}/%{_kerneldir}

%post
# Generate the initramfs image within /boot as well as the conf file for /boot/loader/entries
kernel-install add %{_kerneldir} %{_libmodules}/%{_kerneldir}/vmlinuz

%postun
# Prior to uninstalling the kernel, remove associated files from /boot
kernel-install remove %{_kerneldir}
