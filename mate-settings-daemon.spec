# TODO
# - do implicit list of deps?
#mate-settings-daemon-1.5.4-0.2.i686 marks libmatekbd-1.5.0-0.1.i686 (cap libmatekbd.so.4)

Summary:	MATE Desktop settings daemon
Name:		mate-settings-daemon
Version:	1.6.2
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	551b2c2204b67ee2ffc9d49051d35efb
URL:		http://wiki.mate-desktop.org/mate-settings-daemon
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	dconf-devel >= 0.13
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.17.3
BuildRequires:	gtk+2-devel >= 2:2.24.0
BuildRequires:	intltool >= 0.37.1
BuildRequires:	libmatekbd-devel >= 1.6.1
BuildRequires:	libnotify-devel
BuildRequires:	libxklavier-devel >= 5.0
BuildRequires:	mate-common
BuildRequires:	mate-desktop-devel >= 1.5.0
BuildRequires:	nss-devel
#BuildRequires:	pkgconfig(clutter-gst-1.0)
#BuildRequires:	pkgconfig(mate-conf)
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	pulseaudio-devel >= 0.9.16
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.26.0
Requires:	gsettings-desktop-schemas
Requires:	gtk-update-icon-cache
Requires:	mate-icon-theme
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# makefiles and this spec gets confused if %{_libdir} == %{_libexecdir}
%define		_libexecdir %{_libdir}/%{name}

%description
MATE Desktop settings daemon

%package devel
Summary:	Development files for mate-settings-daemon
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for mate-settings-daemon

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--disable-static \
	--with-x  \
	--enable-gstreamer  \
	--enable-polkit  \
	--disable-schemas-compile  \
	--with-gnu-ld  \
	--with-x  \
	--with-nssdb  \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-settings-daemon.convert

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache mate
%glib_compile_schemas

%postun
/sbin/ldconfig
%update_icon_cache mate
if [ "$1" -eq 0 ]; then
	%glib_compile_schemas
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
/etc/dbus-1/system.d/org.mate.SettingsDaemon.DateTimeMechanism.conf
%{_sysconfdir}/xdg/autostart/mate-settings-daemon.desktop
%{_datadir}/dbus-1/services/org.mate.SettingsDaemon.service
%{_datadir}/dbus-1/system-services/org.mate.SettingsDaemon.DateTimeMechanism.service
%{_iconsdir}/mate/*/*/*.*
%{_datadir}/mate-settings-daemon
%{_datadir}/glib-2.0/schemas/org.mate.*.xml
%{_datadir}/polkit-1/actions/org.mate.settingsdaemon.datetimemechanism.policy

%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/mate-settings-daemon
%attr(755,root,root) %{_libexecdir}/msd-datetime-mechanism
%attr(755,root,root) %{_libexecdir}/msd-locate-pointer
%attr(755,root,root) %{_libexecdir}/*.so
%{_libexecdir}/*-plugin

%files devel
%defattr(644,root,root,755)
%{_includedir}/mate-settings-daemon
%{_pkgconfigdir}/mate-settings-daemon.pc
