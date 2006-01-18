
%define plugins_ver 0.80.3
Summary:	Games for children with plugins
Summary(pl):	Gra dla dzieci z wtyczkami
Name:		childsplay
Version:	0.81.1
Release:	1
Group:		X11/Applications/Games
Source0:	http://dl.sourceforge.net/childsplay/%{name}-%{version}.tgz
# Source0-md5:	fc7497ba05c242f7eaf4c8898aff3043
Source1:	http://dl.sourceforge.net/childsplay/%{name}_plugins-%{plugins_ver}.tgz
# Source1-md5:	7ccaffb34f191af3f8cd945c7fbc0652
Patch0:		%{name}-install.patch
License:	GPL v2
URL:		http://childsplay.sourceforge.net/
%pyrequires_eq	python-modules
Requires:	python-pygame >= 1.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Childsplay is a 'suite' of educational games for young children, like
gcompris, but without the overkill of c/c++ and the gnome environ.
Also the use of the SDL libraries makes smooth animation and the
playing of sound very easy.

%description -l pl
Childsplay jest gra edukacyjna dla dzieci podobna do gcompris. Jest
jednak napisana w pythonie, uzywa biblioteki SDL.


%prep
%setup -q -a1
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
SCOREFILE = SCOREDIR + "childsplay.score"
DOCDIR =  "%{_docdir}/childsplay"
MANDIR = "%{_mandir}/man6"
CPDIR = "%{_datadir}/childsplay"
SHAREDIR = CPDIR
BINDIR = "%{_bindir}/games"
LIBDIR = CPDIR + "/lib"
MODULESDIR = LIBDIR
SHARELIBDATADIR = SHAREDIR + "/lib"
SHAREDATADIR = SHAREDIR + "/Data"
RCDIR = SHARELIBDATADIR + "/ConfigData"
CHILDSPLAYRC = "childsplayrc"
HOME_DIR_NAME = ".childsplayrc"
EOF

%build


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}{/%{name}/lib/{ConfigData,MemoryData},locale,assetml} \
	$RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man6,/var/games}

install -Dp childsplay.sh $RPM_BUILD_ROOT%{_bindir}/childsplay
install -Dp man/childsplay.6.gz $RPM_BUILD_ROOT%{_mandir}/man6/childsplay.6.gz

cp -fr Data/childsplay.score $RPM_BUILD_ROOT/var/games/%{name}.score
cp -fr *.py $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -fr Data/ $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -fr lib $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -fr locale $RPM_BUILD_ROOT%{_datadir}/
cp -fr assetml $RPM_BUILD_ROOT%{_datadir}/

cd childsplay_plugins-%{plugins_ver}/
cp -fr lib/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/
cp -fr Data/*.icon.png $RPM_BUILD_ROOT%{_datadir}/%{name}/Data/icons/
cp -fr Data/AlphabetSounds $RPM_BUILD_ROOT%{_datadir}/%{name}/Data/
cp -fr assetml/childsplay $RPM_BUILD_ROOT%{_datadir}/assetml/
%{__python} add-score.py $RPM_BUILD_ROOT/var/games/ "Packid,Numbers"
cd ..

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

find $RPM_BUILD_ROOT%{_datadir} -name "*.py" | xargs rm

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* doc/README* doc/Changelog
%{_mandir}/man6/*
%{_datadir}/%{name}
%{_datadir}/assetml/*
%attr(664,root,games) %config(noreplace) %verify(not md5 mtime size) /var/games/%{name}.score
%attr(2755,root,games) %{_bindir}/childsplay
