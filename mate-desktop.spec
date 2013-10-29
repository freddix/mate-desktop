Summary:	Mate desktop library
Name:		mate-desktop
Version:	1.6.1
Release:	4
License:	LGPL
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	540936afdcd5d0a694569af9a2cac132
Patch0:		%{name}-freddix.patch
URL:		http://wiki.mate-desktop.org/mate-desktop
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libunique-devel
BuildRequires:	mate-doc-utils
BuildRequires:	pkg-config
BuildRequires:	startup-notification-devel
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	rarian
Requires:	fonts-TTF-droid
Requires:	gtk+-theme-greybird
Requires:	mate-backgrounds-desktop
Requires:	xorg-theme-xcursor-OpenZone
Suggests:	gtk+3-theme-greybird
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE desktop library.

%package libs
Summary:	mate-desktop library
Group:		Development/Libraries

%description libs
This package contains mate-desktop library.

%package devel
Summary:	MATE desktop includes
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
MATE desktop header files.

%package apidocs
Summary:	mate-desktop API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
mate-desktop API documentation.

%prep
%setup -q
%patch0 -p1

# kill mate common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__gtkdocize}
%{__intltoolize}
%{__gnome_doc_prepare}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-desktop-docs		\
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,en@shaw,ig,ug,yo}

%find_lang %{name} --with-mate --with-omf

%clean
rm -fr $RPM_BUILD_ROOT

%post
%update_gsettings_cache
%scrollkeeper_update_post

%postun
%update_gsettings_cache
%scrollkeeper_update_postun

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-about
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_datadir}/mate-about
%{_datadir}/libmate-desktop
%{_desktopdir}/mate-about.desktop
%{_mandir}/man1/mate-about.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libmate-desktop-2.so.??
%attr(755,root,root) %{_libdir}/libmate-desktop-2.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-desktop-2.so
%{_includedir}/mate-desktop-2.0
%{_pkgconfigdir}/mate-desktop-2.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-desktop
