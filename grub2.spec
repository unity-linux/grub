%define Werror_cflags %nil
# Modules always contain just 32-bit code
%define _libdir %{_exec_prefix}/lib

# 64bit intel machines use 32bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%global efi_arch x86_64-efi
%endif

%ifarch %arm
%global efi_arch arm-uboot
%endif

%ifarch %ix86
%global efi_arch i386-efi
%endif

%global tarversion 2.02
%global pc_arch i386-pc

# Use 'commits since release tag' from git describe as the version minor
# so we can sanely implement snapshots without reconfiguring the spec.
# Using './make_snapshot_patch' creates a patch with the %%{git} (minor) 
# number in the name.
# Add the patch name as Patch0000: in SOURCES/grub.patches
%define git	0
Name:		grub2
Version:	2.02.%{git}
Release:	%mkrel 4
Summary:	Bootloader with support for Linux, Multiboot and more
Group:		System/Boot and Init
License:	GPLv3+ and GPLv2
# unicode font is GPLv2
URL:		http://www.gnu.org/software/grub/
#Source0:	ftp://alpha.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
Source0:	http://ftp.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
Source2:	grub.default
Source3:	README.Mageia
Source4:	README.efi
Source6:	gitignore
Source7:	grub.patches
# pf2 fonts may be regenerated in SOURCES using ./mkfonts
Source8:	mkfonts
Source9:	unicode.pf2
Source10:	MageiaLogo-Bold-16.pf2
Source11:	MageiaLogo-Bold-20.pf2
Source12:	MageiaLogo-Bold-28.pf2
Source13:	MageiaLogo-Regular-20.pf2
Source14:	grub2-mageia-default.png
Source15:	MageiaLogoFonts-bdf.tar.gz
Source20:	theme.txt
Source21:	make_snapshot_patch

#
# Fedora patches:
#
# generate with do-rebase
# Include Fedora patches in Source7
%{expand:%(while read line; do echo $line; done < %{SOURCE7})}

# And these are:
# git checkout debuginfo
# git format-patch fedora-23..
Patch10001:	10001-Put-the-correct-.file-directives-in-our-.S-files.patch
Patch10002:	10002-Make-it-possible-to-enabled-build-id-sha1.patch
Patch10004:	10004-Add-grub_qdprintf-grub_dprintf-without-the-file-lin.patch
###Patch10005:	10005-Make-a-gdb-dprintf-that-tells-us-load-addresses.patch

#
# Mga patches:
#
Patch20001:	grub2-2.00-mga-add_failsafe-10_linux.in.patch
Patch20002:	grub2-2.00-mga-dont_write_sparse_file_error_to_screen.patch
Patch20003:	grub2-2.00-mga-dont_write_diskfilter_error_to_screen.patch
Patch20004:	grub2-2.00-mga-dont_check_uuid_in_installer.patch
Patch20005:	grub2-2.00-mga-remove-unrestricted_when_password_set.patch
Patch20006:	grub2-2.02-mga-translate-theme-label.patch
#
# SuSE Patch:
#
# Fixes Mga#15846 - Grub2 doesn't install the bootloader on btrfs if we
# have a dualboot with windows starting at sector 63
Patch30001:	grub2-setup-try-fs-embed-if-mbr-gap-too-small.patch


BuildRequires:	autoconf
BuildRequires:	autogen
BuildRequires:	automake
BuildRequires:	binutils
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	flex
BuildRequires:	freetype2-devel
BuildRequires:	freetype-devel
BuildRequires:	freetype-devel
BuildRequires:	pkgconfig(fuse) 
BuildRequires:	gettext-devel
BuildRequires:	git
BuildRequires:	glibc-devel
BuildRequires:	help2man
BuildRequires:	liblzo-devel
BuildRequires:	libusb-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	python
BuildRequires:	rpm-devel
BuildRequires:	ruby
BuildRequires:	texinfo

Provides:	bootloader
Provides:	grub2bootloader = %{version}-%{release}
Requires:	%{name}-common = %{version}-%{release}

%description
This is the second version of the GRUB (Grand Unified Boot-loader), a highly
configurable and customizable boot-loader with modular architecture.
It supports a wide range of kernel formats, file systems, computer
architectures and hardware devices.
Refer to the README.Mageia file that is part of this package's documentation
for more information.

%ifnarch %arm
%package efi
Summary:	Boot-loader with support for EFI
Group:		System/Boot and Init

Requires(post):	efibootmgr
Provides:	bootloader
Provides:	grub2bootloader = %{version}-%{release}
Requires:	%{name}-common = %{version}-%{release}

%description efi
This is the second version of the GRUB (Grand Unified Boot-loader), a highly
configurable and customizable boot-loader with modular architecture.
It supports a wide range of kernel formats, file systems, computer
architectures and hardware devices.
Refer to the README.Mageia file that is part of this package's documentation
for more information.
%endif

%ifarch %arm
%package uboot
Summary:	Boot-loader with support for  UBOOT
Group:		System/Boot and Init

Provides:	bootloader
Provides:	grub2bootloader = %{version}-%{release}
Requires:	%{name}-common = %{version}-%{release}

%description uboot
configurable and customizable boot-loader with modular architecture.
It supports a wide range of kernel formats, file systems, computer
architectures and hardware devices.
%endif

%package common
Summary:	Provides files common to both grub2 and grub2-efi
Group:		System/Boot and Init
Conflicts:	memtest86+ < 5.01-7
Conflicts:	%{name} < 2.02-0.git9752.19.mga5
Conflicts:	%{name}-efi < 2.02-0.git9752.19.mga5
Recommends:	os-prober >= 1.53
Recommends:	xorriso
Requires:	grub2bootloader = %{version}-%{release}
Requires:	console-setup

%description common
Common files used by both grub2 and grub2-efi.

%package mageia-theme
Summary:	Provides a graphical theme with a custom Mageia background for grub2
Group:		System/Boot and Init

Requires:	grub2bootloader = %{version}
Requires(post):	sed
Requires(post):	coreutils
Conflicts:	grub2-mageia3-theme-dejavu
Conflicts:	grub2-mageia4-theme-dejavu
Conflicts:	grub2-mageia5-theme-dejavu
Conflicts:	grub2-mageia6-theme-dejavu
Conflicts:	grub2-mageia-theme-dejavu

BuildArch:	noarch

%description mageia-theme
This package provides a custom Mageia graphical theme.
It is provided as a separate package so it may be easily excluded from
minimal installations where a graphical theme is not required.

%prep
%setup -q -n grub-%{tarversion}

cp %{SOURCE6} .gitignore
git init
echo '![[:digit:]][[:digit:]]_*.in' > util/grub.d/.gitignore
echo '!*.[[:digit:]]' > util/.gitignore
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git config gc.auto 0
git add .
git commit -a -q -m "%{tarversion} baseline."
git apply %{patches} </dev/null
git config --unset user.email
git config --unset user.name

# README.Mageia
cp %{SOURCE3} .
 
%ifnarch %arm
# README.efi
cp %{SOURCE4} .

cd ..
rm -rf grub-efi-%{tarversion}
mv grub-%{tarversion} grub-efi-%{tarversion}
%endif

%setup -q -n grub-%{tarversion}

cp %{SOURCE6} .gitignore
git init
echo '![[:digit:]][[:digit:]]_*.in' > util/grub.d/.gitignore
echo '!*.[[:digit:]]' > util/.gitignore
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git config gc.auto 0
git add .
git commit -a -q -m "%{tarversion} baseline."
git apply %{patches} </dev/null
git config --unset user.email
git config --unset user.name
find . -name "*.0???" -delete

# README.Mageia
cp %{SOURCE3} .
# README.efi
cp %{SOURCE4} .

%build
cd ..
pushd grub-%{tarversion}
./autogen.sh
%configure2_5x TARGET_LDFLAGS=-static			\
%ifarch %arm
	  --with-platform=uboot				\
%else
	 --with-platform=pc				\
%endif
	  --disable-werror				\
	  --enable-grub-mkfont				\
	  --program-transform-name=s,grub,%{name},	\
	  --with-bootdir=/boot				\
	  --with-grubdir=/%{name}			\
	  CFLAGS="-g"
%make_build
popd

%ifnarch %arm
pushd grub-efi-%{tarversion}
./autogen.sh
%configure2_5x TARGET_LDFLAGS=-static			\
	  --with-platform=efi				\
%ifarch x86_64
	  --target=x86_64				\
%endif
	  --disable-werror				\
	  --enable-grub-mkfont				\
	  --program-transform-name=s,grub,%{name},	\
	  --with-bootdir=/boot				\
	  --with-grubdir=/%{name}			\
	  CFLAGS="-g"
%make_build
popd
%endif

%install
cd ..
%ifnarch %arm
pushd grub-efi-%{tarversion}
%make_install
popd
%endif

pushd grub-%{tarversion}
%make_install

# (bor) grub.info is harcoded in sources
mv %{buildroot}%{_infodir}/grub.info %{buildroot}%{_infodir}/%{name}.info

# Theme
install -d %{buildroot}/boot/%{name}/themes/maggy
install -D -m 644 %{SOURCE20} %{buildroot}/boot/%{name}/themes/maggy
install -D -m 644 %{SOURCE10} %{buildroot}/boot/%{name}/themes/maggy
install -D -m 644 %{SOURCE11} %{buildroot}/boot/%{name}/themes/maggy
install -D -m 644 %{SOURCE12} %{buildroot}/boot/%{name}/themes/maggy
install -D -m 644 %{SOURCE13} %{buildroot}/boot/%{name}/themes/maggy
# Install 4:3 default in case default.jpg is missing
install -D -m 644 %{SOURCE14} %{buildroot}/boot/%{name}/themes
ln -sf ../grub2-mageia-default.png %{buildroot}/boot/%{name}/themes/maggy/grub2-mageia-default.png

# Ghost config files
install -d %{buildroot}/boot/%{name}
install -d %{buildroot}/boot/%{name}/fonts

# Workaround for RHL Bug 817187
install -d %{buildroot}%{_datadir}/locale/en/LC_MESSAGES
cp -f %{buildroot}%{_datadir}/locale/en@quot/LC_MESSAGES/grub.mo \
      %{buildroot}%{_datadir}/locale/en/LC_MESSAGES/grub.mo
      
cat > %{buildroot}/boot/%{name}/custom.cfg <<EOF
# Set non-graphical text/background colours
set menu_color_normal=cyan/blue
set menu_color_highlight=white/blue
# Add any extra custom menu entries in here:

EOF

# Provide 'update-grub' and update-grub2 symlink for *buntu exiles ;) 
cat > %{buildroot}%{_bindir}/update-grub <<EOF
#!/bin/sh
su --login root -c "/usr/sbin/grub2-mkconfig -o /boot/grub2/grub.cfg"

EOF
chmod +x %{buildroot}%{_bindir}/update-grub
ln -s %{_bindir}/update-grub %{buildroot}%{_bindir}/update-grub2

# Defaults
install -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/default/grub

# Remove "GNU/Linux" in menu selections
sed -i 's/ GNU\/Linux//' %{buildroot}%{_sysconfdir}/grub.d/10_linux

cp %{SOURCE9} %{buildroot}%{_datadir}/grub/

%find_lang grub

popd

# Don't run debuginfo on all the grub modules and whatnot; it just
# rejects them, complains, and slows down extraction.
%global finddebugroot "%{_builddir}/%{?buildsubdir}/debug"

%global dip RPM_BUILD_ROOT=%{finddebugroot} %{__debug_install_post}
%define __debug_install_post (						\
	mkdir -p %{finddebugroot}/usr					\
	mv ${RPM_BUILD_ROOT}/usr/bin %{finddebugroot}/usr/bin		\
	mv ${RPM_BUILD_ROOT}/usr/sbin %{finddebugroot}/usr/sbin		\
	%{dip}								\
	install -m 0755 -d %{buildroot}/usr/lib/ %{buildroot}/usr/src/	\
	cp -al %{finddebugroot}/usr/lib/debug/				\\\
		%{buildroot}/usr/lib/debug/				\
	cp -al %{finddebugroot}/usr/src/debug/				\\\
		%{buildroot}/usr/src/debug/ )				\
	mv %{finddebugroot}/usr/bin %{buildroot}/usr/bin		\
	mv %{finddebugroot}/usr/sbin %{buildroot}/usr/sbin		\
	%{nil}
 
%post
if [ $1 -eq 2 ]; then
      touch /boot/grub2/updtrans
fi

%ifnarch %arm
%post efi
if [ $1 -eq 2 ]; then
      touch /boot/grub2/updtrans
fi
%endif

%posttrans common
# On update re-install grub2 to where it was installed by drakboot if possible,
# otherwise next boot may fail due to mismatched boot code.
   if [ -f /boot/grub2/updtrans ] && [ -f /boot/grub2/install.sh -a -x /usr/sbin/detectloader ] && [ "$DURING_INSTALL" != "1" ] ; then
		LOADER=$(/usr/sbin/detectloader)
		[ "$LOADER" = "GRUB2" ] && /boot/grub2/install.sh ||:
		rm -f /boot/grub2/updtrans
   fi
   
# Don't let rpmdrake ask users to shoot themselves in feet! Mga#17263
		rm -f /etc/default/grub.rpm*

%post mageia-theme
# Don't install if updating
if [ $1 -eq 1 ] ; then
# Remove trailing blank lines from /etc/default/grub
sed -i -e :a -e '/^\n*$/{$d;N;};/\n$/ba' %{_sysconfdir}/default/grub
# Check that /etc/default/grub ends in a linefeed
[ "$(tail -n 1 %{_sysconfdir}/default/grub | wc --lines)" = "1" ] || echo >> %{_sysconfdir}/default/grub
# Add theme
echo "GRUB_THEME=/boot/grub2/themes/maggy/theme.txt" >> %{_sysconfdir}/default/grub

# If installing theme outside installer then update menu 
if [ "x${DURING_INSTALL}" != "x1" ]; then
%{name}-mkconfig -o /boot/%{name}/grub.cfg && rm -f /boot/%{name}/grub.cfg.rpmsave
fi
fi

# Copy system default background at correct aspect ratio to grub2 default theme
if [ -h %{_datadir}/mga/backgrounds/default.png ] && [ "$DURING_INSTALL" != "1" ]; then
cp -f %{_datadir}/mga/backgrounds/default.png /boot/%{name}/themes/%{name}-mageia-default.png
fi

%triggerpostun mageia-theme -- %{name}-mageia-theme <  2.02-0.git10463.5.mga6
# Run install.sh to replace /boot/grub2/fonts/unicode.pf2
   if [ -f /boot/grub2/install.sh -a -x /usr/sbin/detectloader ] && [ "$DURING_INSTALL" != "1" ]; then
		LOADER=$(/usr/sbin/detectloader)
		[ "$LOADER" = "GRUB2" ] && /boot/grub2/install.sh ||:
   fi

# If updating from below 2.02-0.git10101.4 then re-make grub.cfg once.
# grub2 dropped ownership of grub.cfg to avoid rpmnew being created.
# Remove rpmnew and after new grub.cfg is created remove rpmsave. Mga#17263
%triggerpostun common -- %{name} < 2.02-0.git10101.4, %{name}-efi < 2.02-0.git10101.4
rm -f /boot/%{name}/grub.cfg.rpmnew
%{name}-mkconfig -o /boot/%{name}/grub.cfg && rm -f /boot/%{name}/grub.cfg.rpmsave
# Take this opportunity to remove some unwanted logs
rm -f /var/log/%{name}_preun.log
rm -f /var/log/%{name}_post.log
rm -f /var/log/%{name}_theme_postun.log

%preun
# Only if uninstalling
if [ $1 -eq 0 ]; then
rm -rf /boot/%{name}/%{pc_arch}
rm -rf /boot/%{name}/locale
fi

%ifnarch %arm
%preun efi
# Only if uninstalling
if [ $1 -eq 0 ]; then
rm -rf /boot/%{name}/%{efi_arch}
rm -rf /boot/%{name}/locale
fi
%endif

%postun mageia-theme
# Only if uninstalling theme
if [ $1 -eq 0 ]; then
# Remove theme from config
sed -i '/GRUB_THEME=\/boot\/grub2\/themes\/maggy\/theme.txt/d' %{_sysconfdir}/default/grub
fi

%ifnarch %arm
%files
%dir %{_libdir}/grub/i386-pc
%{_libdir}/grub/i386-pc/*
%endif

%ifnarch %arm
%files efi 
%doc README.efi
%dir %{_libdir}/grub/%{efi_arch}
%{_libdir}/grub/%{efi_arch}/*
%endif

%ifarch %arm
%files uboot
%dir %{_libdir}/grub/%{efi_arch}
%{_libdir}/grub/%{efi_arch}/*
%endif

%files common -f grub.lang
%doc COPYING NEWS README THANKS TODO README.Mageia
%dir /boot/%{name}
%dir /boot/%{name}/fonts
%dir /boot/%{name}/themes
%{_infodir}/*
%{_bindir}/%{name}-*
%{_bindir}/update-grub
%{_bindir}/update-grub2
%{_sbindir}/%{name}-*
%dir %{_libdir}/grub
%{_datarootdir}/bash-completion/completions/grub
%{_sysconfdir}/grub.d/README
%{_sysconfdir}/grub.d/00_header
%{_sysconfdir}/grub.d/01_users
%{_sysconfdir}/grub.d/10_linux
%{_sysconfdir}/grub.d/20_linux_xen
%{_sysconfdir}/grub.d/20_ppc_terminfo
%{_sysconfdir}/grub.d/30_os-prober
%config(noreplace) %{_sysconfdir}/grub.d/40_custom
%config(noreplace) %{_sysconfdir}/grub.d/41_custom
%config(noreplace) %{_sysconfdir}/default/grub
%{_datadir}/grub/*
%config(noreplace) /boot/%{name}/custom.cfg
%{_mandir}/man1/%{name}-*.1*
%{_mandir}/man8/%{name}-*.8*

%files mageia-theme
/boot/%{name}/themes/*
