From the tetaneutral.net to a looking glass for bird
##################################################################

:date: 2012-05-31 14:36
:category: Tetaneutral.net
:tags: Tetaneutral.net, bird, looking-glass

During one year of participation in the `tetaneutral.net <http://www.tetaneutral.net/>`_ project,
a French Associative Internet Service Provider and Host Provider,
I have set up a mini cloud with `ganeti <http://code.google.com/p/ganeti/>`_ (~100 virtual machines), 
I have integrated `CheckMK <http://mathias-kettner.de/check_mk.html>`_ for monitoring the ISP infrastructure and I have done some other system administration tasks.


Tetaneutral.net daily uses and promotes opensource softwares, this is why it uses `Bird <http://bird.network.cz/>`_ on its BGP router. So, I have begun to work on a Web Looking Glass for this BGP router: `bird-lg <https://github.com/sileht/bird-lg>`_.


| The software is not ready yet for an easy setup, but it works fine.
| The tool is now in production for tetaneutral.net at this address: `<http://lg.tetaneutral.net/>`_
|
| The main features are the classic  "`show route <http://lg.tetaneutral.net/prefix/gw+h3/ipv4?q=81.20.16.0>`_" and the `bgpmap <http://lg.tetaneutral.net/prefix_bgpmap/gw+h3/ipv4?q=81.20.16.0>`_.
| The technologies used are `Flask <http://flask.pocoo.org>`_, `jQuery <http://jquery.com/>`_ and `Bootstrap <http://twitter.github.com/bootstrap/>`_.
|

