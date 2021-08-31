%global __provides_exclude_from	^(%{_libdir}/jitsi/lib/native/.*\\.so|%{_libdir}/jitsi/sc-bundles/.*\\.jar)$
%global debug_package %{nil}
%global java_home /usr/lib/jvm/java-1.8.0-openjdk

%global commit0 bde1701b1c8582a046ab203fa0cfd108fbf3b356
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:		jitsi
Version:	2.11.5633
Release:	5%{dist}
Summary:	Open Source Video Calls And Chat
Group:		Applications/Communications
License:	LGPLv2+
URL:		https://jitsi.org/
Source0:        https://github.com/jitsi/jitsi/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:	jitsi.sh
Source2:	jitsi.desktop
Source3:	org.jitsi.jitsi.metainfo.xml
Source4:	splash.gif

BuildRequires:	ant
BuildRequires:	git
BuildRequires:	java-1.8.0-openjdk-devel
#BuildRequires:	javapackages-tools

#BuildRequires:	pkgconfig(x11)
#BuildRequires:	pkgconfig(xtst)
#BuildRequires:	pkgconfig(dbus-1)
#BuildRequires:	pkgconfig(xscrnsaver)
#BuildRequires:	pkgconfig(gtk+-2.0)
#BuildRequires:	pkgconfig(alsa)

Requires:	java-1.8.0-openjdk
Requires: ffmpeg3-libs

%description
Jitsi is an audio/video Internet phone and instant messenger that
supports some of the most popular instant messaging and telephony protocols
such as SIP, Jabber/XMPP (and hence Facebook and Google Talk), AIM/ICQ,
Yahoo! Messenger, RSS and counting.
Jitsi is completely Open Source / Free Software, and is freely available
under the terms of the GNU Lesser General Public License.


%prep
%autosetup -n jitsi-%{commit0}

%build

# append the build revision to the jitsi version
sed -i "s/0\.build\.by\.SVN/build.%{version}/" src/net/java/sip/communicator/impl/version/NightlyBuildID.java
  
%ant rebuild

%install
  find lib/ lib/bundle/ -maxdepth 1 -type f -exec install -Dm644 {} "%{buildroot}/%{_libdir}/%{name}/"{} \;
  shopt -sq extglob
  CARCH=$(uname -m)
  CARCH=$(sed 's/_/-/g' <<<${CARCH/#*(i?86|x86)/})
  find lib/native/linux${CARCH}/ -maxdepth 1 -type f -execdir install -Dm644 {} "%{buildroot}/%{_libdir}/%{name}/lib/native/"{} \;
  find sc-bundles/{,os-specific/linux/} -maxdepth 1 -type f -execdir install -Dm644 {} "%{buildroot}/%{_libdir}/%{name}/sc-bundles/"{} \;
  install -Dm755 "%{S:1}" "%{buildroot}/%{_bindir}/%{name}"
  install -Dm644 "%{S:2}" "%{buildroot}/%{_datadir}/applications/%{name}.desktop"
  install -Dm644 "%{S:4}" "%{buildroot}/%{_libdir}/%{name}/"

# copy the menu icons
  pushd "resources/install/debian/"
  for _file in *.{svg,xpm}; do
    install -Dm644 "$_file" "%{buildroot}/%{_datadir}/pixmaps/${_file}"
  done
  popd

# copy the documentation
mkdir -p %{buildroot}/%{_mandir}/man1/
mv -f resources/install/debian/jitsi.1.tmpl %{buildroot}/%{_mandir}/man1/jitsi.1

# Appdata
install -Dm 0644 %{S:3} %{buildroot}/%{_metainfodir}/org.jitsi.jitsi.metainfo.xml


%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/org.jitsi.jitsi.metainfo.xml
%{_datadir}/pixmaps/%{name}*
%{_mandir}/man1/%{name}.1.gz


%changelog

* Thu Aug 12 2021 David Va <davidva AT tuta DOT io> 2.11.5633-5
- Launcher improvements and splash activation

* Wed Aug 11 2021 Sérgio Basto <sergio@serjux.com> - 2.11.5633-4
- fix native libraries and  osgi.wiring.package;
  (&(osgi.wiring.package=com.sun.jna)(version>=5.5.0)(\!(version>=6.0.0)))]]
  dropping the last commit

* Sat Jul 17 2021 Sérgio Basto <sergio@serjux.com> - 2.11.5633-3
- Fix build on F34+

* Wed Jun 03 2020 David Va <davidva AT tuta DOT io> 2.11.5633-2
- Added requires ffmpeg3-libs

* Tue Mar 31 2020 David Va <davidva AT tuta DOT io> 2.11.5633-1
- Updated to 2.11.5633

* Fri Mar 27 2020 David Va <davidva AT tuta DOT io> 2.10.5550-9
- Upstream
- Modernized

* Sat Feb 15 2020 umeabot <umeabot> 2.10.5550-8.mga8
+ Revision: 1528457
- Mageia 8 Mass Rebuild

* Tue Aug 20 2019 daviddavid <daviddavid> 2.10.5550-7.mga8
+ Revision: 1430618
- add patch to fix harfbuzz headers path

* Wed Oct 24 2018 daviddavid <daviddavid> 2.10.5550-6.mga7
+ Revision: 1324818
- fix build on armv7hl

* Tue Oct 23 2018 wally <wally> 2.10.5550-5.mga7
+ Revision: 1324696
- remove requires excludes
- enable debug pkgs
- build on all arches again
- add patch to fix native modules build from sources
- add patches from upstream for native module building

* Mon Oct 22 2018 daviddavid <daviddavid> 2.10.5550-4.mga7
+ Revision: 1323685
- build only on ix86 and x86_64

* Sun Sep 23 2018 umeabot <umeabot> 2.10.5550-3.mga7
+ Revision: 1298379
- Mageia 7 Mass Rebuild

* Sat Aug 26 2017 daviddavid <daviddavid> 2.10.5550-2.mga7
+ Revision: 1148189
- disable debug package as debugsourcefiles are empty

* Sat Feb 11 2017 daviddavid <daviddavid> 2.10.5550-1.mga6
+ Revision: 1085760
- new version: 2.10.5550 (stable build)

* Sun Jan 29 2017 daviddavid <daviddavid> 2.9.5545-1.mga6
+ Revision: 1084170
- new version: 2.9.5545 (nightly builds)

* Sun Jan 15 2017 daviddavid <daviddavid> 2.9.5541-1.mga6
+ Revision: 1081764
- new version: 2.9.5541 (nightly builds)

* Sun Oct 30 2016 daviddavid <daviddavid> 2.9.5534-1.mga6
+ Revision: 1064153
- new version: 2.9.5534 (nightly builds)
- rediff patches (P0, P1)
- update description

* Fri May 13 2016 daviddavid <daviddavid> 2.9.5513-1.mga6
+ Revision: 1014522
- new version: 2.9.5513 (nightly builds)

* Mon Apr 25 2016 daviddavid <daviddavid> 2.9.5509-1.mga6
+ Revision: 1006261
- new version: 2.9.5509 (nightly builds)
- rename and rediff all patches
- update description removing unneeded detail of named and versioned package

* Wed Mar 02 2016 umeabot <umeabot> 2.8-4.mga6
+ Revision: 983522
- Rebuild for openssl

* Mon Feb 15 2016 umeabot <umeabot> 2.8-3.mga6
+ Revision: 960724
- Mageia 6 Mass Rebuild

* Mon Jun 22 2015 daviddavid <daviddavid> 2.8-2.mga6
+ Revision: 839117
- add another require excludes

* Sat Jun 20 2015 daviddavid <daviddavid> 2.8-1.mga6
+ Revision: 835881
- new version: 2.8 build 5426 (stable build)
- rename and rediff all patches

* Mon Feb 02 2015 daviddavid <daviddavid> 2.6-1.mga5
+ Revision: 813090
- new version: 2.6 build 5390 (stable build)
- rename and rediff all patches

* Wed Jan 28 2015 daviddavid <daviddavid> 2.5-14.mga5
+ Revision: 812635
- new build version: 5389 (nightly builds)

* Tue Jan 06 2015 daviddavid <daviddavid> 2.5-13.mga5
+ Revision: 808859
- new build version: 5375 (nightly builds)
- exclude all unneeded provides

* Thu Dec 11 2014 daviddavid <daviddavid> 2.5-12.mga5
+ Revision: 802751
- new build version: 5367 (nightly builds)

* Fri Nov 28 2014 daviddavid <daviddavid> 2.5-11.mga5
+ Revision: 799722
- new build version: 5350 (nightly builds)

* Sun Nov 09 2014 daviddavid <daviddavid> 2.5-10.mga5
+ Revision: 796136
- new build version: 5336 (nightly builds)

* Sun Oct 19 2014 daviddavid <daviddavid> 2.5-9.mga5
+ Revision: 791830
- new build version: 5321 (nightly builds)

* Wed Oct 15 2014 umeabot <umeabot> 2.5-8.mga5
+ Revision: 746326
- Second Mageia 5 Mass Rebuild

* Sat Sep 27 2014 wally <wally> 2.5-7.mga5
+ Revision: 730657
- add require excludes

* Sat Sep 27 2014 daviddavid <daviddavid> 2.5-6.mga5
+ Revision: 725987
- new build version: 5306 (nightly builds)

* Tue Sep 16 2014 umeabot <umeabot> 2.5-5.mga5
+ Revision: 680816
- Mageia 5 Mass Rebuild

* Mon Sep 08 2014 daviddavid <daviddavid> 2.5-4.mga5
+ Revision: 673698
- new build version: 5295 (nightly builds)

* Thu Aug 28 2014 daviddavid <daviddavid> 2.5-3.mga5
+ Revision: 669119
- rediff patch 2 (fix_desktop_file_package-name)
- update file list
- new build version: 5290 (nightly builds)

* Sat Aug 16 2014 daviddavid <daviddavid> 2.5-2.mga5
+ Revision: 663984
- new build version: 5277 (nightly builds)

* Thu Aug 07 2014 daviddavid <daviddavid> 2.5-1.mga5
+ Revision: 660799
- rename patches (P0, P1, P2)
- rediff Patch0 to fix new binary file
- improve the description
- add BR on git-core
- add a splash gif file for opening of jitsi
- new version: 2.5 build 5269 (nightly builds)

* Tue Aug 05 2014 luigiwalser <luigiwalser> 2.4-2.mga5
+ Revision: 659861
- switch to java-1.8.0-openjdk

* Sun Mar 16 2014 david-david <david-david> 2.4-1.mga5
+ Revision: 604098
- add patches to remove 'sed' commands (bin, man and desktop files)
- use correct '.jar' files directory
- use correct library files directory
- imported package jitsi

