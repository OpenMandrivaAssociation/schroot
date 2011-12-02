Name: schroot
Version: 1.4.23
Release: 1
Summary: Execute commands in a chroot environment
Group: Development/Other
License: GPLv3+
Url: http://packages.debian.org/schroot
Source0: http://ftp.de.debian.org/debian/pool/main/s/schroot/%{name}_%{version}.orig.tar.bz2
Patch0: schroot-pam.patch
Patch1: schroot-default-config-path.patch
BuildRequires: pam-devel
BuildRequires: boost-devel
BuildRequires: lockdev-devel
BuildRequires: gettext
BuildRequires: libuuid-devel

%description
schroot allows users to execute commands or interactive shells in
different chroots.  Any number of named chroots may be created, and
access permissions given to each, including root access for normal
users, on a per-user or per-group basis.  Additionally, schroot can
switch to a different user in the chroot, using PAM for
authentication and authorisation.  All operations are logged for
security.

Several different types of chroot are supported, including normal
directories in the filesystem, and also block devices.  Sessions,
persistent chroots created on the fly from files (tar with optional
compression and zip) and LVM snapshots are also supported.

schroot supports kernel personalities, allowing the programs run
inside the chroot to have a different personality.  For example,
running 32-bit chroots on 64-bit systems, or even running binaries
from alternative operating systems such as SVR4 or Xenix.

schroot also integrates with sbuild, to allow building packages with
all supported chroot types, including session-managed chroot types
such as LVM snapshots.

schroot shares most of its options with dchroot, but offers vastly
more functionality.

%package -n dchroot
Group: Development/Other
Summary: Older tool similar to schroot

%description -n dchroot
dchroot allows users to execute commands or interactive shells in different 
chroots. Users can move between chroots as necessary.  Enhanced
functionality is available in the next generation tool called schroot.

%prep

%setup -q 

%patch0 -p0
%patch1 -p0

%build
sed -i '/AM_PATH_CPPUNIT/d' configure.ac

%configure LIBS="-lboost_program_options -lboost_system -lboost_regex" --disable-rpath --enable-static --disable-shared --enable-dchroot || ( cat config.log && exit 1 )
%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_localstatedir}/lib/schroot/session
mkdir -p %{buildroot}%{_sysconfdir}/schroot/chroot.d

# get rid of uneeded include and library files
rm -rf %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/pkgconfig/sbuild.pc
rm -f %{buildroot}%{_libdir}/libsbuild.la
rm -f %{buildroot}%{_libdir}/libsbuild.so*
rm -f %{buildroot}%{_libdir}/libsbuild.a

rm -rf %{buildroot}%{_sysconfdir}/schroot/sbuild
rm -rf %{buildroot}%{_sysconfdir}/schroot/buildd
rm -f %{buildroot}%{_bindir}/schroot-sbuild

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/schroot
%dir %{_sysconfdir}/schroot
%dir %{_sysconfdir}/schroot/desktop
%dir %{_sysconfdir}/schroot/minimal
%dir %{_sysconfdir}/schroot/default
%dir %{_sysconfdir}/schroot/chroot.d
%config(noreplace) %{_sysconfdir}/schroot/schroot.conf
%config(noreplace) %{_sysconfdir}/pam.d/schroot
%dir %{_sysconfdir}/schroot/setup.d
%{_sysconfdir}/bash_completion.d/schroot
%{_sysconfdir}/schroot/default/config
%{_sysconfdir}/schroot/default/copyfiles
%{_sysconfdir}/schroot/default/fstab
%{_sysconfdir}/schroot/default/nssdatabases
%{_sysconfdir}/schroot/desktop/config
%{_sysconfdir}/schroot/desktop/copyfiles
%{_sysconfdir}/schroot/desktop/fstab
%{_sysconfdir}/schroot/desktop/nssdatabases
%{_sysconfdir}/schroot/minimal/config
%{_sysconfdir}/schroot/minimal/copyfiles
%{_sysconfdir}/schroot/minimal/fstab
%{_sysconfdir}/schroot/minimal/nssdatabases
%{_sysconfdir}/schroot/setup.d/00check
%{_sysconfdir}/schroot/setup.d/05btrfs
%{_sysconfdir}/schroot/setup.d/05file
%{_sysconfdir}/schroot/setup.d/05lvm
%{_sysconfdir}/schroot/setup.d/05union
%{_sysconfdir}/schroot/setup.d/10mount
%{_sysconfdir}/schroot/setup.d/15killprocs
%{_sysconfdir}/schroot/setup.d/20copyfiles
%{_sysconfdir}/schroot/setup.d/20nssdatabases
%{_sysconfdir}/schroot/setup.d/50chrootname
%{_sysconfdir}/schroot/setup.d/99check
%dir %{_libexecdir}/schroot
%{_libexecdir}/schroot/schroot-listmounts
%{_libexecdir}/schroot/schroot-mount
%{_libexecdir}/schroot/schroot-releaselock
%dir %{_localstatedir}/lib/schroot
%{_localstatedir}/lib/schroot/session
%{_localstatedir}/lib/schroot/mount
%{_datadir}/%{name}/setup/common-data
%{_datadir}/%{name}/setup/common-functions
%{_mandir}/man1/schroot.1.*
%{_mandir}/man5/schroot-script-config.5.*
%{_mandir}/man5/schroot-setup.5.*
%{_mandir}/man5/schroot.conf.5.*
%{_mandir}/man7/schroot-faq.7.*
%doc COPYING ABOUT-NLS AUTHORS ChangeLog HACKING INSTALL NEWS README THANKS TODO

%files -n dchroot
%{_bindir}/dchroot
%{_mandir}/man1/dchroot.1.*
%doc COPYING ABOUT-NLS AUTHORS ChangeLog HACKING INSTALL NEWS README THANKS TODO
