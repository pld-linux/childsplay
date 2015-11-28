Summary:	Educational games for children
Summary(pl.UTF-8):	Gry edukacyjne dla dzieci
Name:		childsplay
Version:	1.6
Release:	1
License:	GPL v3+
Group:		X11/Applications/Games
Source0:	http://downloads.sourceforge.net/schoolsplay/%{name}-%{version}.tgz
# Source0-md5:	d113ca45424f48e5f8fee6df04ffa7a1
Source1:	%{name}.desktop
Source2:	pld_setup.py
Patch0:		%{name}-gettext.patch
URL:		http://www.schoolsplay.org/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.112
%pyrequires_eq	python-modules
Requires:	python-SQLAlchemy
Requires:	python-numpy
Requires:	python-pygame >= 1.7
Requires:	python-pygtk-gtk >= 1:2.0
Requires:	python-sqlite >= 1.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Childsplay is a 'suite' of educational games for young children, like
gcompris, but without the overkill of C/C++ and the GNOME environment.
Also the use of the SDL libraries makes smooth animation and the
playing of sound very easy.

%description -l pl.UTF-8
Childsplay to zestaw gier edukacyjnych dla małych dzieci, podobnych do
gier z zestawu gcompris. Jest jednak napisana bez narzutu C/C++ i
środowiska GNOME - w Pythonie, z użyciem biblioteki SDL, co czyni
animacje płynnymi i odtwarzanie dźwięku bardzo łatwym.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/{games/%{name}/alphabetsounds,locale},%{_pixmapsdir},%{_desktopdir}}
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}/childsplay_sp

# use our custom setup.py instead of ugly orginal one
cp %{SOURCE2} setup.py

%py_install

cp -fr lib/CPData $RPM_BUILD_ROOT%{_datadir}/games/%{name}
cp -fr lib/SPData $RPM_BUILD_ROOT%{_datadir}/games/%{name}
cp -fr alphabetsounds/en $RPM_BUILD_ROOT%{_datadir}/games/%{name}/alphabetsounds
cp -fr locale/* $RPM_BUILD_ROOT%{_datadir}/locale

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install bin/childsplay $RPM_BUILD_ROOT%{_bindir}
install lib/SPData/menu/default/logo_cp_64x64.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%py_comp $RPM_BUILD_ROOT%{_datadir}/games/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/games/%{name}

%find_lang %{name}_sp --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}_sp.lang
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/childsplay
%{_datadir}/games/%{name}
%{py_sitescriptdir}/childsplay_sp
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/childsplay_sp-*.egg-info
%endif
