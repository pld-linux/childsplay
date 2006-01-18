%define plugins_ver 0.80.3

Summary:	Games for children with plugins
Summary(pl):	Gra dla dzieci z wtyczkami
Name:		childsplay
Version:	0.81.1
Release:	1
Group:		X11/Applications/Games
Source0:        http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tgz
Source1:        http://dl.sourceforge.net/sourceforge/%{name}/%{name}_plugins-%{plugins_ver}.tgz
# Source0-md5:
License:	GPL v2
URL:		http://childsplay.sourceforge.net/
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	libogg-devel
BuildRequires:	python-devel
BuildRequires:	python-pygame-devel
Requires:	python-pygame >= 1.6
Patch0:		%{name}-install.patch
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

### fix python compile error
#perl -pi.orig -e 's|quiet\=1||g' install.py

cat <<'EOF' >childsplay.sh
#!/bin/sh
exec python %{_libdir}/childsplay/childsplay.py $@
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
CPDIR = "%{_prefix}/lib/childsplay"
SHAREDIR = CPDIR
BINDIR = "%{_prefix}/games"
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

install -d 	$RPM_BUILD_ROOT%{_bindir} \
			$RPM_BUILD_ROOT%{_libdir}/childsplay/lib/ConfigData/ \
			$RPM_BUILD_ROOT%{_libdir}/childsplay/lib/MemoryData/ \
			$RPM_BUILD_ROOT%{_mandir}/man6/	\
			$RPM_BUILD_ROOT%{_datadir}/locale \
			$RPM_BUILD_ROOT%{_datadir}/assetml \
			$RPM_BUILD_ROOT/var/games 			


install -Dp childsplay.sh $RPM_BUILD_ROOT%{_bindir}/childsplay
install -Dp man/childsplay.6.gz $RPM_BUILD_ROOT%{_mandir}/man6/childsplay.6.gz

cp -fr Data/childsplay.score $RPM_BUILD_ROOT/var/games/childsplay.score
cp -fr *.py $RPM_BUILD_ROOT%{_libdir}/childsplay/
cp -fr Data/ $RPM_BUILD_ROOT%{_libdir}/childsplay/
cp -fr lib $RPM_BUILD_ROOT%{_libdir}/childsplay/
cp -fr locale $RPM_BUILD_ROOT%{_datadir}/
cp -fr assetml $RPM_BUILD_ROOT%{_datadir}/

### compile bytecode
%{__python} install.py --compile $RPM_BUILD_ROOT%{_libdir}/childsplay/
%{__python} install.py --makedir $RPM_BUILD_ROOT%{_libdir}/childsplay/

### install plugins
cd %{name}_plugins-%{plugins_ver}/
python $RPM_BUILD_ROOT%{_libdir}/childsplay/install.py --compile Lib
cp -fr lib/* $RPM_BUILD_ROOT%{_libdir}/childsplay/lib/
cp -fr Data/*.icon.png $RPM_BUILD_ROOT%{_libdir}/childsplay/Data/icons/
cp -fr Data/AlphabetSounds $RPM_BUILD_ROOT%{_libdir}/childsplay/Data/
cp -fr assetml/%{name} $RPM_BUILD_ROOT%{_datadir}/assetml/
%{__python} add-score.py $RPM_BUILD_ROOT/var/games/ "Packid,Numbers"
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* doc/GPL* doc/README*
%{_libdir}/%{name}/
%{_datadir}/*
%attr(755,root,games) %{_bindir}/*


#%changelog
#* Initial package.
