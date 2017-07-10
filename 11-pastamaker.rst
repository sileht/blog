:title: Automate rebasing and merging of your PR with pastamaker
:date: 2017-07-07 10:01
:category: Gnocchi
:tags: pastamaker, github, gnocchi

The story of pastamaker
=======================

`Gnocchi`_ project recently moved from the OpenStack infrastructure to `GitHub`_.

The OpenStack infrastructure provides a very good set of tools for
managing/reviewing/testing projects. To do so, they use `Gerrit`_ to review
patches and `Zuul`_ to schedule testing and checking jobs. `Zuul`, the gating
system, ensures that no commit failling the unit and functional tests are
merged.

When we moved to `GitHub`_, we obviously switched to the Pull Request system,
instead of using `Gerrit`_. We also switched ot `Travis-CI`_ to run tests. But
the workflow around Pull Request and `Travis-CI`_ is not as good as `Zuul`_
was.

First, `Travis-CI`_ only tests the head of the Pull Request branch whatever the
base branch commit is. The base branch commit of a Pull Request is never the
last commit of your base branch. At this point, if you click on the `GitHub`_
Merge button you can't known if the resulting merge or rebase will pass tests
or not.

`GitHub`_ offers a branch merging protection call: "Require branches to be up
to date before merging". That means that each times a Pull Request is merged,
all Pull Requests must be rebased... But nothing in `GitHub`_ allows to
automate that. They just offer a "Update branch" button you have to click
manually.

For the `Gnocchi`_ project, after some weeks of using `GitHub`_, we realized
that all reviewers had to talk about which PR should be merged next. Then one
of them would have to take care of it, click on "Update branch", then wait ~
30~40 minutes for `Travis-CI`_ to post the new result and click on the Merge
Button. So much time lost, especially when you come from OpenStack
Infrastructure and `Zuul`_ is doing all of that for you.

That why we ended up writing a `GitHub`_ bot to manage this administrative work
for us. It uses new GitHub Apps API. The code is under "Apache License v2" and
it's called `pastamaker`.

How it works
============

Pastamaker in composed of three small apps:

* The engine triggered by GitHub events.
* A REST API.
* A dashboard of ongoing pull requests to merge for all registered projects.

The engine workflow
-------------------

On each GitHub event, Pastamaker looks at the pull request information in the
event to retrieve the GitHub project and branch. Then it builds the list of
open Pull Requests for this branch. For each pull request, it retrieves the CI
status, the reviews, and if the pull request is up to date with the base
branch. With this information it computes a weight. This naturally creates a
priority queue of pull requests to merge. For example, the rule for computing
the weight are "do we have enough core reviewers approvals?", "Does the CI
pass?", "Is the pull request conflicting?", etc.

Some rules are customisable by project/branch with a configuration file, like
the number of required core reviewers.

When the queue is ready, Pastamaker stores it in `Redis`_ so it's accessible
from API and from the dashboard. Then it processes the first element of the
queue. If everything is OK, it merges the patch. If the patch needs to be
rebased, it uses the GitHub "Update branch" button.

The engine could be smarter and just do special action depending on the event
type and the pull request state. But for now, I decided to keep it simple to
avoid any race condition. The queue ordering is stable whatever the order of
events is, whatever are the human interaction on pull requests. `Pastamaker`_
is also designed stateless: everything is built from information given by
GitHub Events and GitHub API.

The REST API
------------

The REST API passes the HTTP `GitHub`_ events to the engine through Redis,
serves all the static files for the dashboard. It allows to retrieve the queues
built by the engine, or to subscribe a stream of the queues update. You can
also trigger the initial built of the queue for all registered projects.

The dashbord
------------

It just displays the pull requests list of all registered projects with the
weight of the Pull Requests. An example of the dashboard:

.. figure:: /static/pastamaker-dashboard.png
   :alt: Pastamaker dasbhoard

Install your own
================

`pastamaker`_ offers helpers to be deployed on `Heroku`. For the `Gnocchi`
project, we currently use only the free services offered by `Travis-CI`,
`Heroku`_ and `GitHub`_ and it works well for the size of our project.

The setup steps are basically:

* Create a GitHub App
* Add your projects to this GitHub App
* Configure branch protection on your project (this may be done automatically
  by `pastamaker`_ one day)
* Install `pastamaker`_ somewhere

You're ready, `pastamaker`_ will start to receive your projects events.

More information can be found `here <https://github.com/sileht/pastamaker/blob/master/README.rst>`_


.. _pastamaker: https://github.com/sileht/pastamaker
.. _gnocchi: https://github.com/gnocchixyz
.. _github: https://github.com
.. _travis-ci: https://travis-ci.org
.. _gerrit: https://www.gerritcodereview.com/
.. _zuul: https://docs.openstack.org/infra/zuul/
.. _redis: https://redis.io/
.. _heroku: https://heroku.com
