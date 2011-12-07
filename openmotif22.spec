%define intern_name openMotif

Summary: Open Motif runtime libraries and executables
Name: openmotif22
Version: 2.2.3
Release: 19%{?dist}
License: Open Group Public License
Group: System Environment/Libraries
Source:  %{intern_name}-%{version}.tar.gz
URL: http://www.motifzone.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: /usr/share/X11/XKeysymDB

BuildRequires: flex, byacc, pkgconfig
BuildRequires: libjpeg-devel libpng-devel
BuildRequires: libXft-devel libXmu-devel libXp-devel libXt-devel libXext-devel
BuildRequires: xorg-x11-xbitmaps
BuildRequires: perl

Patch19: openMotif-2.2.3-utf8.patch
Patch22: openMotif-2.2.3-no_demos.patch
Patch23: openMotif-2.2.3-uil_lib.patch
Patch25: openMotif-2.2.3-libdir.patch
Patch26: openMotif-2.2.3-char_not_supported.patch
Patch27: openMotif-2.2.3-pixel_length.patch
Patch28: openMotif-2.2.3-popup_timeout.patch
Patch29: openMotif-2.2.3-acinclude.patch
Patch30: openMotif-2.2.3-autofoo.patch
Patch31: openMotif-2.2.3-CAN-2004-0687-0688.patch
Patch32: openMotif-2.2.3-CAN-2004-0914.patch
Patch33: openMotif-2.2.3-CAN-2004-0914_autofoo.patch
Patch34: openMotif-2.2.3-tmpnam.patch
Patch35: openmotif-2.2.3-CAN-2004-0914_sec8.patch
Patch36: openMotif-2.2.3-vizcount.patch
Patch37: openMotif-2.2.3-long64.patch
Patch38: openMotif-2.2.3-multiscreen.patch
Patch39: openMotif-2.2.3-motifzone_1193.patch
Patch40: openMotif-2.2.3-motifzone_1202.patch
Patch41: openMotif-2.2.3-CAN-2005-0605.patch
Patch42: openMotif-2.2.3-CVE-2005-3964.patch
Patch43: openMotif-2.2.3-xmlist_fix.patch
Patch44: openMotif-2.2.3-overrun.patch
Patch45: openMotif-2.2.3-text_paste.patch
Patch46: openMotif-2.2.3-xim-onthespot.patch
Patch47: openMotif-2.2.3-free_children.patch
Patch48: openMotif-2.2.3-motifzone_1231.patch
Patch49: openMotif-2.2.3-rgbtxt.patch
Patch50: openMotif-2.2.3-mwmrc_dir.patch
Patch51: openMotif-2.2.3-bindings.patch
Patch52: openMotif-2.3.0-no_X11R6.patch
Patch53: openMotif-2.2.3-no_Xaw.patch
Patch54: openMotif-2.2.3-mrm.patch

Conflicts: lesstif <= 0.92.32-6

%description
This is the Open Motif %{version} runtime environment. It includes the
Motif shared libraries, needed to run applications which are dynamically
linked against Motif.

%prep
%setup -q -n %{intern_name}-%{version}
%patch19 -p1 -b .utf8
%patch22 -p1 -b .no_demos
%patch23 -p1 -b .uil_lib
%patch25 -p1 -b .libdir
%patch26 -p1 -b .char_not_supported
%patch27 -p1 -b .pixel_length
%patch28 -p1 -b .popup_timeout
%patch29 -p1 -b .acinclude
%patch30 -p1 -b .autofoo
%patch31 -p1 -b .CAN-2004-0687-0688
%patch32 -p1 -b .CAN-2004-0914
%patch33 -p1 -b .CAN-2004-0914_autofoo
%patch34 -p1 -b .tmpnam
%patch35 -p1 -b .CAN-2004-0914_sec8
%patch36 -p1 -b .vizcount
%patch37 -p1 -b .long64
%patch38 -p1 -b .multiscreen
%patch39 -p1 -b .motifzone_1193
%patch40 -p1 -b .motifzone_1202
%patch41 -p1 -b .CAN-2005-0605
%patch42 -p1 -b .CVE-2005-3964
%patch43 -p1 -b .xmlist_fix
%patch44 -p1 -b .overrun
%patch45 -p1 -b .text_paste
%patch46 -p1 -b .xim-onthespot
%patch47 -p1 -b .free_children
%patch48 -p1 -b .motifzone_1231
%patch49 -p1 -b .mwmrc_dir
%patch50 -p1 -b .no_X11R6
%patch51 -p1 -b .bindings
%patch52 -p1 -b .no_X11R6
%patch53 -p1 -b .no_Xaw
%patch54 -p1 -b .mrm


for i in doc/man/man3/{XmColumn,XmDataField}.3; do
	iconv -f windows-1252 -t utf-8 < "$i" > "${i}_"
	mv "${i}_" "$i"
done

%build
CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fno-strict-aliasing" \
./configure \
   --prefix=%{_prefix} \
   --libdir=%{_libdir} \
   --mandir=%{_datadir}/man \
   --enable-static \
   --enable-xft \
   --enable-jpeg --enable-png

# do not use rpath
perl -pi -e 's|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"-L\\\$libdir\"|g;' libtool

export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make clean
make

%install
rm -rf %{buildroot}

export LD_LIBRARY_PATH=`pwd`/lib/Mrm/.libs:`pwd`/lib/Xm/.libs
make DESTDIR=%{buildroot} prefix=%{_prefix} install

rm -fr %{buildroot}%{_libdir}/*a \
       %{buildroot}%{_libdir}/*.so \
       %{buildroot}%{_datadir}/Xm/doc \
       %{buildroot}%{_bindir} \
       %{buildroot}/etc/X11 \
       %{buildroot}%{_includedir} \
       %{buildroot}%{_datadir}/man \
       %{buildroot}%{_datadir}/X11

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT.MOTIF README RELEASE RELNOTES
%{_libdir}/libMrm.so.*
%{_libdir}/libUil.so.*
%{_libdir}/libXm.so.*

%changelog
* Fri Jun 25 2010 Thomas Woerner <twoerner@redhat.com> 2.2.3-19
- build with -fno-strict-aliasing (rhbz#605095)

* Tue Dec 08 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.2.3-18.1
- Rebuilt for RHEL 6

* Tue Nov 14 2006 Thomas Woerner <twoerner@redhat.com> 2.2.3-18
- readded lost mrm initialization patch from Arjan van de Ven (#211599)

* Wed Jul  5 2006 Thomas Woerner <twoerner@redhat.com> 2.2.3-17
- spec file cleanup
- added no_Xaw patch

* Tue Jun 27 2006 Thomas Woerner <twoerner@redhat.com> 2.2.3-16
- fixed CVE-2005-3964: libUil buffer overflows (#174814)
- fixed XmList out of bound accesses (#167701)
- fixed pasting into TextField (#179549)
- moved mwmrc to /etc/X11/mwm
- moved bindings to /usr/share/X11
- fixed paths in man pages containing /usr/X11R6
- patch for new rgb.txt location (#174210)
  Thanks to Ville Skyttä for the patch

* Fri Nov 18 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-15
- moved man pages to /usr/share/man (#173604)

* Wed Nov 16 2005 Jeremy Katz <katzj@redhat.com> - 2.2.3-14
- X11R6 stuff is gone

* Wed Nov 16 2005 Jeremy Katz <katzj@redhat.com> - 2.2.3-13
- also buildrequire xbitmaps

* Wed Nov 16 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-12
- rebuild for modular X

* Fri Sep  2 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-11
- fixed mrm initialization error in MrmOpenHierarchyPerDisplay (#167094)
  Thanks to Arjan van de Ven for the patch.

* Mon Apr  4 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-10
- fixed possible libXpm overflows (#151642)

* Mon Feb 28 2005 Thomas Woerner <twoerner@redhat.com> 2.2.3-9
- Upstream Fix: Multiscreen mode
- Upstream Fix: Crash when restarting by a session manager (motifzone#1193)
- Upstream Fix: Crash when duplicating a window menu containing f.circle_up
  (motifzone#1202)
- fixed divide by zero error in ComputeVizCount() (#144420)
- Xpmcreate: define LONG64 on 64 bit architectures (#143689)

* Mon Nov 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-8.1
- allow to write XPM files with absolute path names again (#140815)

* Wed Nov 24 2004 Miloslav Trmac <mitr@redhat.com> 2.2.3-8
- Convert man pages to UTF-8

* Mon Nov 22 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-7
- latest Xpm patches: CAN-2004-0914 (#134631)
- new patch for tmpnam in imake (only used for build)

* Thu Sep 30 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-6
- fixed CAN-2004-0687 (integer overflows) and CAN-2004-0688 (stack overflows)
  in embedded Xpm library

* Wed Sep 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5.2
- replaced libtoolize and autofoo* calls with a patch (autofoo)

* Wed Sep 29 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5.1
- use new autofoo

* Wed Sep  1 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-5
- libXp now moved to xorg-x11-deprecated-libs, therefore no compatibility 
  with XFree86 packages anymore.

* Mon Aug 30 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.3
- devel package: added requires for XFree86-devel (#131202)

* Thu Jun 17 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.2
- rebuilt for fc3

* Wed Jun 16 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-4.1
- renamed xmbind script to xmbind.sh (#126116)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-3
- fixed popup menus fail on Tarantella/VNC (#123027)
- fixed character not supported problem (#124960)
- fixed data out of bounds bug (#124961)

* Wed Apr 14 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-2
- 2.2.3 final version

* Tue Mar 23 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-1.9.2
- final CVS version

* Wed Mar 17 2004 Thomas Woerner <twoerner@redhat.com> 2.2.3-1.9.1
- new openmotif 2.2.3 beta version

* Mon Mar  8 2004 Thomas Woerner <twoerner@redhat.com> 2.2.2-17
- fixed popdown problem in ToolTip (#75730)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Thomas Woerner <twoerner@redhat.com> 2.2.2-16.3
- rebuilt

* Thu Dec 18 2003 Thomas Woerner <twoerner@redhat.com>
- added missing BuildRequires for XFree86-devel

* Thu Nov 27 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-16.2
- removed rpath

* Mon Aug 27 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-16
- fixed ToggleBG (#101159)

* Thu Jul 31 2003  <timp@redhat.com> 2.2.2-15.2
- rebuild for RHEL

* Wed Jul 30 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-15
- fixed ToggleB (#101159)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Thomas Woerner <twoerner@redhat.com> 2.2.2-13
- fix for Xmu/EditRes conflict (bug #80777)
- fix for wml and utf-8 (bug #80271)
- fix for Ext18List (bug #74502)

* Thu Nov 14 2002 Than Ngo <than@redhat.com> 2.2.2-12.2
- add buildprereq byacc and flex (bug #77860)

* Fri Nov  8 2002 Than Ngo <than@redhat.com> 2.2.2-12.1
- fix some build problem

* Mon Aug 27 2002 Than Ngo <than@redhat.com> 2.2.2-12
- Fixed a segmentation fault in mkcatdefs (bug #71955)

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 2.2.2-11
- Added missing symlinks (bug #69117)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 2.2.2-10
- build using gcc-3.2-0.1

* Tue Jun 25 2002 Than Ngo <than@redhat.com> 2.2.2-9
- fix to build openmotif (bug #64176)

* Thu Jun 13 2002 Than Ngo <than@redhat.com> 2.2.2-8
- rebuild in new enviroment

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Harald Hoyer <harald@redhat.de> 2.2.2-6
- patched ltmain.sh to link properly

* Wed May 22 2002 Harald Hoyer <harald@redhat.de> 2.2.2-6
- specified libraries by full name in files section 
  (libMrm was missing on alpha)

* Tue Mar 26 2002 Than Ngo <than@redhat.com> 2.2.2-5
- update new 2.2.2 from ICS

* Sun Mar 24 2002 Than Ngo <than@redhat.com> 2.2.2-4
- add missing uil

* Fri Mar 22 2002 Tim Powers <timp@redhat.com>
- rebuilt to try and shake some broken deps in the devel package

* Thu Mar 21 2002 Than Ngo <than@redhat.com> 2.2.2-2
- rebuild

* Thu Mar 21 2002 Than Ngo <than@redhat.com> 2.2.2-1
- update to 2.2.2 release

* Mon Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-3
- conflict with older lesstif

* Mon Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-2
- fix bug #60816

* Fri Feb 22 2002 Than Ngo <than@redhat.com> 2.2.1-1
- update to 2.2.1 release
- remove somme patches, which are included in 2.2.1

* Fri Feb 22 2002 Tim Powers <timp@redhat.com>
- rebuilt in new environment

* Fri Jan 25 2002 Tim Powers <timp@redhat.com>
- don't obsolete lesstif anymore, play nicely together
- rebuild against new toolchain

* Wed Jan 21 2002 Than Ngo <than@redhat.com> 2.1.30-11
- add some patches from Darrell Commander (supporting largefile)
- fix to build on s390

* Thu Jan 17 2002 Than Ngo <than@redhat.com> 2.1.30-10
- rebuild in 8.0

* Wed Sep  6 2001 Than Ngo <than@redhat.com>
- rebuild for ExtraBinge 7.2

* Thu May 03 2001 Than Ngo <than@redhat.com>
- add 3 official motif patches 
- add rm -rf $RPM_BUILD_ROOT in install section
- remove some old patches which are now in official patches

* Fri Dec 29 2000 Than Ngo <than@redhat.com>
- don't build static debug libraries

* Mon Dec 18 2000 Than Ngo <than@redhat.com>
- bzip2 source

* Mon Jul 24 2000 Than Ngo <than@redhat.de>
- rebuilt against gcc-2.96-44

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- rebuilt

* Sun Jun 11 2000 Than Ngo <than@redhat.de>
- fix imake to built with gcc-2.96 (thanks Jakup)
- put bitmaps in /usr/X11R6/include/X11/bitmaps
- put bindings in /usr/X11R6/lib/Xm/bindings
- add define -D_GNU_SOURCE to build Motif
- gzip man pages
- cleanup specfile

* Mon May 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to patchlevel 2
- remove bindings patch, it's included in pl2

* Tue May 16 2000 Matt Wilson <msw@redhat.com>
- use -fPIC on sparc
- fixed Ngo's "fixes"

* Mon May 15 2000 Ngo Than <than@redhat.de>
- added description.
- fixed spec, added uil stuff.

* Mon May 15 2000 Matt Wilson <msw@redhat.com>
- initialization of spec file.
