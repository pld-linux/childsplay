
%define plugins_ver 0.85.2
%define plugins_lfc_ver 0.85.2
Summary:	Games for children with plugins
Summary(pl.UTF-8):	Gry dla dzieci z wtyczkami
Name:		childsplay
Version:	0.85.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/childsplay/%{name}-%{version}.tgz
# Source0-md5:	427ab5f69e12f12a6af8824e5cd92ff9
Source1:	http://dl.sourceforge.net/childsplay/%{name}_plugins-%{plugins_ver}.tgz
# Source1-md5:	015ea52f03614f7b8cf4797d18ff321b
Source2:	http://dl.sourceforge.net/childsplay/%{name}_plugins_lfc-%{plugins_lfc_ver}.tgz
# Source2-md5:	33f15cc131014b15383fd5cfec7e4fdf
Source3:        %{name}.desktop
Patch0:		%{name}-install.patch
URL:		http://childsplay.sourceforge.net/
%pyrequires_eq	python-modules
BuildRequires:	rpm-pythonprov
Requires:	python-pygame >= 1.6
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
%setup -q -a1 -a2
%patch0 -p1

cat <<'EOF' >childsplay.sh
#!/bin/sh
exec python %{_datadir}/childsplay/childsplay.pyc $@
EOF

cat <<'EOF' >BASEPATH.py
BASEPATH = "%{_prefix}"
EXECDIR = "%{_bindir}"
LOCALEDIR = "%{_datadir}/locale"
ASSETMLDIR = "%{_datadir}/assetml"
SCOREDIR = "/var/games/"
SCOREFILE = "/var/games/childsplay.score"
DOCDIR =  "%{_docdir}/childsplay"
MANDIR = "%{_mandir}/man6"
CPDIR = "%{_datadir}/childsplay"
SHAREDIR = "%{_datadir}/childsplay"
BINDIR = "%{_bindir}"
LIBDIR = "%{_datadir}/childsplay/lib"
MODULESDIR = "%{_datadir}/childsplay/lib"
SHARELIBDATADIR = "%{_datadir}/childsplay/lib"
SHAREDATADIR = "%{_datadir}/childsplay/Data"
RCDIR = "%{_datadir}/childsplay/lib/ConfigData"
CHILDSPLAYRC = "childsplayrc"
HOME_DIR_NAME = ".childsplayrc"
EOF

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}{/%{name}/lib/{ConfigData,MemoryData},locale,assetml} \
        $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_mandir}/man6,/var/games}

install -Dp childsplay.sh $RPM_BUILD_ROOT%{_bindir}/childsplay
gzip -dc man/childsplay.6.gz >$RPM_BUILD_ROOT%{_mandir}/man6/childsplay.6

install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install Data/logo_cp_32x32.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

cp -fr Data/childsplay.score $RPM_BUILD_ROOT/var/games/%{name}.score
cp -fr *.py $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -fr Data/ $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -fr lib $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -fr locale $RPM_BUILD_ROOT%{_datadir}
cp -fr assetml $RPM_BUILD_ROOT%{_datadir}

cd childsplay_plugins-%{plugins_ver}
cp -fr lib/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp -fr Data/*.icon.png $RPM_BUILD_ROOT%{_datadir}/%{name}/Data/icons
cp -fr Data/AlphabetSounds $RPM_BUILD_ROOT%{_datadir}/%{name}/Data
cp -fr assetml/childsplay $RPM_BUILD_ROOT%{_datadir}/assetml
%{__python} add-score.py $RPM_BUILD_ROOT/var/games/ "Packid,Numbers"
cd ..

cd childsplay_plugins_lfc-%{plugins_lfc_ver}
cp -fr lib/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lib
cp -fr Data/*.icon.png $RPM_BUILD_ROOT%{_datadir}/%{name}/Data/icons
cp -fr assetml/childsplay $RPM_BUILD_ROOT%{_datadir}/assetml
cd ..


%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

find  $RPM_BUILD_ROOT%{_datadir} -maxdepth 2 -name "*.py" | xargs rm
find  $RPM_BUILD_ROOT%{_datadir}/%{name}/lib -name "*.py[c,o]" | xargs rm

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/BASEPATH.py*
cp BASEPATH.py $RPM_BUILD_ROOT%{_datadir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* doc/README* doc/Changelog
%{_mandir}/man6/*
%{_datadir}/%{name}
# XXX: shared with gcompris
%dir %{_datadir}/assetml
%{_datadir}/assetml/*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%attr(664,root,games) %config(noreplace) %verify(not md5 mtime size) /var/games/%{name}.score
%attr(2755,root,games) %{_bindir}/childsplay
