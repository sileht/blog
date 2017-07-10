:title: Automate rebasing and merging of your PR with pastamaker
:date: 2017-07-07 10:01
:category: Gnocchi
:tags: pastamaker, github, gnocchi
:status: draft

The story of pastamaker
=======================

`Gnocchi`_ project recently moved from the Openstack infrastructure to `Github`_.

The Openstack infrastructure provides a very good set of tools for
managing/reviewing/testing projects. To do so, they use `Gerrit`_ and `Zuul`_.
`Zuul`, the gating system, ensures that we don't merge commit that doesn't pass
tests.

When we moved to `Github`_, we obviously use the Pull Request system to replace
`Gerrit`_ and use `Travis-CI`_ to run tests. But the workflow around Pull Request
and `Travis-CI`_ is not as good as `Zuul`_ was.

First, about `Travis-CI`_, it tests only the head of the Pull Request branch
whatever the base branch commit is. The base branch commit of a Pull Request is
never the last commit of your base branch. At this point, if you click on the
`Github`_ Merge Button you can't known if the result merge or rebase will pass
tests or not.

`Github`_ now offers a branch merging protection call: "Require branches to be
up to date before merging". But, each times a Pull Request is merged, all Pull
Requests must be rebased... and nothing in `Github`_ allow to automate that.
They just offer a manual "Update branch" button.

On `Gnocchi`_ project after some weeks of using `Github`_, all cores was passed
many times to talk about which PR we will merge next, one of them have to take
care of it, click on "Update branch", then wait ~ 30~40 minutes for
`Travis-CI`_ to post the new result and click on the Merge Button. So many
times lost, especially when you come from Openstack Infrastructure and `Zuul`_
is doing all of that for you.

That why we end up to write a `Github`_ Bot to manage this administrative work
for us. It uses new Github Apps API, the code is under "Apache License v2" and
it's called `pastamaker`_.

How does it works
=================

Pastamaker in composed three small apps:

* The engine triggered by Github events.
* A REST API
* A dashboard of ongoing pull requests to merge for all registered projects

The engine workflow
-------------------

On each Github event, we looks at the pull request information in the event to
retrieve the github project and branch. Then we build the list of open Pull
Requests for this branch. For each pull request, we retrieve the CI status, the
reviews, and if the pull is update to date with the base branch. With these
informations we compute a weight. This naturally created a priority queue of
pull request to merge. For example, the rule for computing the weight are "do
we have enough core reviewers approvals ?", "Does the CI pass ?", "Is the pull
request conflict ?", ...

Some rules are customisable by project/branch with a configuration file, like
the number of required core reviewers.

When the queue is ready, we store it in `Redis`_ for the API and
dashboard. Then we process the first element of the queue. If everything is
OK, we merge. If it need to be rebased, we use the Github "Update branch"
button.

The engine could be smarter and just do special action depending on the event
type and the pull request state. But for now, I decide to keep it simple to
avoid any race. The queue ordering is stable whatever the order of events, and
the human interaction on pull request. And we don't manage any state on
`pastamaker`_ side, everything is built from informations from Github Events
and Github API.

The REST API
------------

It passes the HTTP `Github`_ events to the engine through `Redis`_, serves all the
static files for the Dashboard, allows to retrieve the queues built by the
engine, or to subscribe a stream of the queues update. Also you can trigger the
initial built of the queue of all registered projects.

The dashbord
------------

It just displays the pull requests list of all registered projects with the
weight of the Pull Requests. An example of the dashboard:

.. figure:: /static/pastamaker-dashboard.png
   :alt: Pastamaker dasbhoard

Install your own
================

`pastamaker`_ offers all helpers to be deployed on `Heroku`_. For the
`Gnocchi`_ project, we currently use only free service of `Travis-CI`_,
`Heroku`_ and `Github`_ and it works well for our load.

The setup steps are basically:

* Create a Github App
* Add your projects to this Github App
* Configure branch protection on your project (This may be done automatically
  by `pastamaker`_ one day)
* Install `pastamaker`_ somewhere

Your ready, `pastamaker`_ will start to receive your projects events.

More information can be found `here <https://github.com/sileht/pastamaker/blob/master/README.rst>`_


.. _pastamaker: https://github.com/sileht/pastamaker
.. _gnocchi: https://github.com/gnocchixyz
.. _github: https://github.com
.. _travis-ci: https://travis-ci.org
.. _gerrit: https://www.gerritcodereview.com/
.. _zuul: https://docs.openstack.org/infra/zuul/
.. _redis: https://redis.io/
.. _heroku: https://heroku.com

