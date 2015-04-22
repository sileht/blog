First step in my involvement in openstack
#########################################

:date: 2012-05-24 17:30
:category: Openstack
:tags: upstream-university, Openstack, Debian, Munin

Due to a recent interest for the Openstack project, I have begun to test and to do some work around it.

I have started to setup a cluster of four nodes (1 proxy/volume and 3 computes) on Debian by following this `guide <http://wiki.debian.org/OpenStackHowto>`_ (Or `this one <http://wiki.debian.org/OpenStackPuppetHowto>`_ if you love Puppet and if you are in a hurry)

| The next step was to dive into the code, to do so I have updated and created `new Munin plugins for openstack <https://github.com/sileht/openstack-munin>`_ .
| This one can make beautiful graphs about many metrics of Openstack
|
| After some tiny problems encountered with the Debian packaging, I have taken a look on it and started to fix `some of them <http://qa.debian.org/developer.php?login=openstack-devel@lists.alioth.debian.org>`_. 
| To have more chance to see my changes committed to upstream, I have followed some steps:
| - Join the Alioth project teams
| - Subscribe to the mailing list
| - Clone the Debian git repository of Openstack
| - Hack the package (And learn new stuffs about the `Debian Policy <http://www.debian.org/doc/debian-policy/>`_)
| - Commit my changes
| - Contact one of the maintainers of the project on IRC for code reviewing
|

After my code has been reviewed by the upstream maintainer, it was successfully uploaded into the Debian archives.

The Openstack Debian packages now have some code from me :-)

All of this has been done thanks to the useful advises of the course I'm following: the `upstream university <http://redmine.upstream-university.org/projects/general/wiki/Manifesto>`_.



