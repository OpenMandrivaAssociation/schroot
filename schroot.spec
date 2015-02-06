Name: schroot
Version: 1.6.3
Release: 3
Summary: Execute commands in a chroot environment
Group: Development/Other
License: GPLv3+
URL: http://packages.debian.org/schroot
Source0: http://ftp.de.debian.org/debian/pool/main/s/schroot/%{name}_%{version}.orig.tar.xz
Patch0: schroot-pam.patch
Patch1: schroot-default-config-path.patch
BuildRequires: pam-devel
BuildRequires: boost-devel
BuildRequires: lockdev-devel
BuildRequires: gettext
BuildRequires: libuuid-devel
BuildRequires: lvm2
BuildRequires: cppunit-devel
BuildRequires: btrfs-progs

Suggests: lvm2
Suggests: btrfs-progs

%description
schroot allows users to execute commands or interactive shells in
different chroots.  Any number of named chroots may be created, and
access permissions given to each, including root access for normal
users, on a per-user or per-group basis.  Additionally, schroot can
switch to a different user in the chroot, using PAM for
authentication and authorisation.  
All operations are logged for security.

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
chroots. Users can move between chroots as necessary. Enhanced functionality 
is available in the next generation tool called schroot.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
%configure2_5x --disable-rpath --disable-static --enable-shared --enable-dchroot || ( cat config.log && exit 1 )
%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_localstatedir}/lib/schroot/session
mkdir -p %{buildroot}%{_sysconfdir}/schroot/chroot.d
/sbin/ldconfig -n %{buildroot}/%{_libdir}

# get rid of uneeded include and library files
rm -rf %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/pkgconfig/sbuild.pc
rm -f %{buildroot}%{_libdir}/libsbuild.la
# rm -f %{buildroot}%{_libdir}/libsbuild.so*
rm -f %{buildroot}%{_libdir}/libsbuild.a

rm -rf %{buildroot}%{_sysconfdir}/schroot/sbuild
rm -rf %{buildroot}%{_bindir}/schroot-sbuild
rm -f  %{buildroot}%{_sysconfdir}/schroot/setup.d/15binfmt

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS ChangeLog HACKING NEWS README THANKS TODO
%config %{_sysconfdir}/bash_completion.d/schroot
%config %{_sysconfdir}/pam.d/schroot
%config(noreplace) %{_sysconfdir}/schroot
%verify(not mode) %attr(4755,root,root) %{_bindir}/schroot
#%#exclude %#{_bindir}/schroot-sbuild
#%#exclude %#{_sysconfdir}/schroot/setup.d/15binfmt
%{_libexecdir}/schroot
%{_localstatedir}/lib/schroot
%{_datadir}/schroot
%{_mandir}/man1/schroot.1.*
%{_mandir}/man5/schroot-script-config.5.*
%{_mandir}/man5/schroot-setup.5.*
%{_mandir}/man5/schroot.conf.5.*
%{_mandir}/man7/schroot-faq.7.*
%{_libdir}/libsbuild.so*

%files -n dchroot
%{_bindir}/dchroot
%{_mandir}/man1/dchroot.1.*
