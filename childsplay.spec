#
# TODO:	- enable plugins (if possible)
#
%define plugins_ver 0.90
%define plugins_lfc_ver 0.90
Summary:	Games for children with plugins
Summary(pl.UTF-8):	Gry dla dzieci z wtyczkami
Name:		childsplay
Version:	1.5.1
Release:	0.1
License:	GPL v3+
Group:		X11/Applications/Games
Source0:	http://downloads.sourceforge.net/schoolsplay/%{name}-%{version}.tgz
# Source0-md5:	6ed368af17e7e2fd129b0b9c5d4921ec
Source1:	%{name}.desktop
Source2:	pld_setup.py
Patch0:		%{name}-gettext.patch
URL:		http://www.schoolsplay.org/
%pyrequires_eq	python-modules
BuildRequires:	rpm-pythonprov
Requires:	python-SQLAlchemy
Requires:	python-numpy
Requires:	python-pygame >= 1.7
Requires:	python-sqlite >= 1.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Childsplay is a 'suite' of educational games for young children, like
gcompris, but without the overkill of C/C++ and the GNOME environment.
Also the use of the SDL libraries makes smooth animation and the
playing of sound very easy.

%description -l pl.UTF-8
Childsplay to zestaw gier edukacyjnych dla małych dzieci, podobnie do
gcompris. Jest jednak napisana bez narzutu C/C++ i środowiska GNOME -
w Pythonie, z użyciem biblioteki SDL, co czyni animacje płynnymi i
odtwarzanie dźwięku bardzo łatwym.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/{%{name}/alphabetsounds,locale},%{_pixmapsdir},%{_desktopdir}}
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}/childsplay_sp

# use our custom setup.py instead of ugly orginal one
cp %{SOURCE2} setup.py

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

cp -fr lib/CPData $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -fr lib/SPData $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -fr alphabetsounds/en $RPM_BUILD_ROOT%{_datadir}/%{name}/alphabetsounds
cp -fr locale/* $RPM_BUILD_ROOT%{_datadir}/locale

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install bin/childsplay $RPM_BUILD_ROOT%{_bindir}
install lib/SPData/menu/default/logo_cp_64x64.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

#mv $RPM_BUILD_ROOT%{_datadir}/locale/{no,nb}

%find_lang %{name}_sp --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}_sp.lang
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/childsplay
%{_datadir}/%{name}
%{py_sitescriptdir}/childsplay_sp
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
