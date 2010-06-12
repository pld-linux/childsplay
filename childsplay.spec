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
#Source1:	http://dl.sourceforge.net/childsplay/%{name}_plugins-%{plugins_ver}.tgz
# Source1-md5:	2abd77c938ce4297c3a6190637833ca5
#Source2:	http://dl.sourceforge.net/childsplay/%{name}_plugins_lfc-%{plugins_lfc_ver}.tgz
# Source2-md5:	123b24a0af50cda07f8c6869d6f939ff
Source3:	%{name}.desktop
Source4:	pld_setup.py
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
#%%setup -q -a1 -a2
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/alphabetsounds,%{_datadir}/locale,%{py_sitescriptdir}/childsplay_sp}

cp -fr lib/CPData $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -fr lib/SPData $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -fr alphabetsounds/en $RPM_BUILD_ROOT%{_datadir}/%{name}/alphabetsounds
cp -fr locale/* $RPM_BUILD_ROOT%{_datadir}/locale

install bin/childsplay $RPM_BUILD_ROOT%{_bindir}

# use our custom setup.py instead of ugly orginal one
cp %{SOURCE4} setup.py

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

#install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
#install lib/SPData/menu/default/logo_cp_32x32.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.xpm

#cd childsplay_plugins-%{plugins_ver}
#cp -fr lib/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
#cp -fr Data/*.icon.png $RPM_BUILD_ROOT%{_datadir}/%{name}/Data/icons
#cp -fr Data/AlphabetSounds $RPM_BUILD_ROOT%{_datadir}/%{name}/Data
#cp -fr assetml/childsplay $RPM_BUILD_ROOT%{_datadir}/assetml
#%%{__python} add-score.py $RPM_BUILD_ROOT/var/games/ "Packid,Numbers"
#cd ..

#cd childsplay_plugins_lfc-%{plugins_lfc_ver}
#cp -fr lib/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
#cp -fr Data/*.icon.png $RPM_BUILD_ROOT%{_datadir}/%{name}/Data/icons
#cp -fr assetml/childsplay $RPM_BUILD_ROOT%{_datadir}/assetml
#cd ..

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

#mv $RPM_BUILD_ROOT%{_datadir}/locale/{no,nb}

%find_lang %{name}_sp --all-name

%clean
rm -rf $RPM_BUILD_ROOT

#%%files -f %{name}_sp.lang
%files -f %{name}_sp.lang
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/childsplay
%{_datadir}/%{name}
%{py_sitescriptdir}/childsplay_sp
#%%{_desktopdir}/%{name}.desktop
#%%{_pixmapsdir}/%{name}.xpm
