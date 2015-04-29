Adding schroot support to piuparts 
##################################################################

:date: 2012-06-11 10:49
:category: Debian
:tags: upstream-university, debian, piuparts

| For my work on the Openstack packages, I have decided to make some tests with piuparts. So I have installed piuparts, read the manual, and made my first test.
| By default, piuparts uses deboostrap to make chroot environment for packages testing. Other methods are pbuilder or lvm snapshot.
|
| But, I have a setup with schroot+aufs to test my Debian packages and piuparts doesn't support it, then I will add it !
|
| After digging into the code, making a first patch, I have contacted the upstream via the bug `#530733 <http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=530733>`_ and followed some advise from my upstream-university curriculum. 
| Upstream review my code very quickly (thanks to it :-)). After some mail exchanges and code fixes, my `patch <http://anonscm.debian.org/gitweb/?p=piuparts/piuparts.git;a=commitdiff;h=8fe2135340df67035d7fc72a2618a320ca5402c3>`_ is now upstream :)
|
