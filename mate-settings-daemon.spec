Summary:	MATE Desktop settings daemon
Summary(pl.UTF-8):	Demon ustawień środowiska MATE Desktop
Name:		mate-settings-daemon
Version:	1.20.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.20/%{name}-%{version}.tar.xz
# Source0-md5:	2692c4a2251ff780c4206dc45cc82a04
URL:		http://wiki.mate-desktop.org/mate-settings-daemon
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.1.2
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	dconf-devel >= 0.13.4
BuildRequires:	fontconfig-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	intltool >= 0.50.1
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libmatekbd-devel >= 1.17.0
BuildRequires:	libmatemixer-devel >= 1.10.0
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libtool
BuildRequires:	libxklavier-devel >= 5.2
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.20.0
BuildRequires:	nss-devel >= 3.11.2
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	pulseaudio-devel >= 0.9.16
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXxf86misc-devel
BuildRequires:	xz
Requires:	dbus >= 1.1.2
Requires:	dbus-glib >= 0.74
Requires:	dconf >= 0.13.4
Requires:	glib2 >= 1:2.50.0
Requires:	gsettings-desktop-schemas
Requires:	gtk+3 >= 3.22
Requires:	gtk-update-icon-cache
Requires:	libmatekbd >= 1.17.0
Requires:	libmatemixer >= 1.10.0
Requires:	libnotify >= 0.7.0
Requires:	libxklavier >= 5.2
Requires:	mate-desktop >= 1.20.0
Requires:	mate-icon-theme
Requires:	polkit >= 0.97
Requires:	pulseaudio-libs >= 0.9.16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# NOTE: we must move %{_libexecdir}/mate-settings-daemon out of %{_libdir},
# because it conflicts with %{_libdir}/mate-settings-daemon plugin dir
# (not using %{_libdir}/%{name} not to mess programs with plugins)
%define		_libexecdir %{_libdir}/mate-settings-daemon-exec

%description
MATE Desktop settings daemon. It's a fork of gnome-settings-daemon.

%description -l pl.UTF-8
Demon ustawień środowiska MATE Desktop. Jest to odgałęzienie pakietu
gnome-settings-daemon.

%package devel
Summary:	Development files for mate-settings-daemon
Summary(pl.UTF-8):	Pliki programistyczne pakietu mate-settings-daemon
Group:		Development/Libraries
# doesn't require base
Requires:	dbus-devel >= 1.1.2
Requires:	dbus-glib-devel >= 0.74
Requires:	glib2-devel >= 1:2.50.0

%description devel
Development files for mate-settings-daemon.

%description devel -l pl.UTF-8
Pliki programistyczne pakietu mate-settings-daemon.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-polkit \
	--enable-pulse \
	--enable-smartcard-support \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-static \
	--with-gnu-ld \
	--with-nssdb \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,ku_IQ,pms}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache mate
%glib_compile_schemas

%postun
%update_icon_cache mate
if [ "$1" -eq 0 ]; then
	%glib_compile_schemas
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/mate-settings-daemon
%attr(755,root,root) %{_libexecdir}/msd-datetime-mechanism
%attr(755,root,root) %{_libexecdir}/msd-locate-pointer
%dir %{_libdir}/mate-settings-daemon
%attr(755,root,root) %{_libdir}/mate-settings-daemon/*.so
%{_libdir}/mate-settings-daemon/*.mate-settings-plugin
%{_datadir}/mate-settings-daemon
%{_datadir}/dbus-1/services/org.mate.SettingsDaemon.service
%{_datadir}/dbus-1/system-services/org.mate.SettingsDaemon.DateTimeMechanism.service
%{_datadir}/glib-2.0/schemas/org.mate.SettingsDaemon.plugins.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.SettingsDaemon.plugins.*.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.applications-at.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.font-rendering.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.peripherals-smartcard.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.peripherals-touchpad.gschema.xml
%dir %{_datadir}/mate-control-center
%dir %{_datadir}/mate-control-center/keybindings
%{_datadir}/mate-control-center/keybindings/50-accessibility.xml
%{_datadir}/polkit-1/actions/org.mate.settingsdaemon.datetimemechanism.policy
/etc/dbus-1/system.d/org.mate.SettingsDaemon.DateTimeMechanism.conf
%{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop
%dir %{_sysconfdir}/xrdb
%{_sysconfdir}/xrdb/*.ad
%{_iconsdir}/hicolor/*/apps/msd-xrandr.*
%{_iconsdir}/mate/*/actions/touchpad-*.*
%{_mandir}/man1/mate-settings-daemon.1*
%{_mandir}/man1/msd-datetime-mechanism.1*
%{_mandir}/man1/msd-locate-pointer.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/mate-settings-daemon
%{_pkgconfigdir}/mate-settings-daemon.pc
