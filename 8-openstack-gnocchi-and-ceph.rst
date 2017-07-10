:title: Writing a Gnocchi storage driver for ceph 
:date: 2015-01-20 17:00
:category: Openstack
:tags: openstack, ceilometer, gnocchi, ceph 
:status: published

`As presented by Julien
Danjou <http://techs.enovance.com/7152/openstack-ceilometer-and-the-gnocchi-experiment>`__,
Gnocchi is designed to store metric metadata into an indexer (usually a
SQL database) and store the metric measurements into another backend.
The default backend creates timeseries using Carbonara (a
`pandas <http://pandas.pydata.org/>`__ based library) and stores them
into Swift.

The storage Gnocchi backend is pluggable, and not all deployments
install Swift, so I have decided to write another backend, I have chosen
Ceph because it’s close to Swift in the way we use it in Gnocchi and
scale well when we have many objects stored too. Now, let’s see what I
need to do to reach this goal.

Storage driver interface
------------------------

The current metric storage driver interface to implement looks like
this:

-  create\_metric(metric, archive\_policy)
-  add\_measures(metric, measures)
-  get\_measures(metric, from\_timestamp=None, to\_timestamp=None,
   aggregation='mean')
-  delete\_metric(metric)
-  get\_cross\_metric\_measures(metrics, from\_timestamp=None,
   to\_timestamp=None, aggregation='mean', needed\_overlap=None)

Cool, not so many methods to implement, we have to:

-  initialize a new metric with the defined archive policy, how many
   point we keep, the frequency, the aggregation methods…
-  add new measures to this metric, a measure is just a timestamp
   associated with a value. The storage driver doesn't care about the
   nature/unit of the metric. This is actually stored into indexer
   database.
-  retrieve the aggregated measurements of a metric This returns a list
   of tuple(timestamp, granularity, value)
-  delete a metric with all its measures
-  get the aggregation acrossmultiple metrics. Theisreturns a list of
   tuple(timestamp, granularity, value), too

By default, the interface doesn't enforce the time series format, so we
are free to store the metric archive policy and the measurements in any
format we want. But actually, timeseries fit well with this interfaces.
This is why it's possible to write a
`OpenTSDB <https://review.openstack.org/#/c/107986/>`__ or a
`InfluxDB <https://review.openstack.org/#/c/103329/>`__ driver.

We currently have a driver for Swift, so let's go to write the driver
for Ceph. It should be pretty straightforward, as it's also a key value
store.

The case of a Carbonara based storage driver
--------------------------------------------

By chance, if the storage driver is a key value store, we don't have to
implement all of these methods. Gnocchi provide an other layer named
`Carbonara <https://github.com/stackforge/gnocchi/blob/master/gnocchi/carbonara.py>`__
that do all the timeseries stuffs for us. The only thing we need to do
is to store a blob for a particular metric and a particular aggregation.

A storage driver that uses
`Carbonara <https://github.com/stackforge/gnocchi/blob/master/gnocchi/carbonara.py>`__
has to inherit from
`gnocchi.storage.\_carbonara.CarbonaraBasedStorage <https://github.com/stackforge/gnocchi/blob/master/gnocchi/storage/_carbonara.py>`__
and to implement these methods:

-  \_create\_metric\_container(metric)
-  \_store\_metric\_measures(metric, aggregation, data)
-  \_get\_measures(metric, aggregation)
-  delete\_metric(self, metric)
-  \_lock(metric, aggregation)

Now, we have:

-  to create a container (\_create\_metric\_container), this method can
   make any initialization for a metric (the Swift driver create a
   container per metric) and raise 'storage.MetricAlreadyExists' is the
   metric already exists.
-  to store the blob created by carbonara for the aggregation of a
   metric, (the Swift driver creates/updates an object named with the
   aggregation method name into the metric container)
-  to return the blob for the aggregation of a metric
-  to delete all blobs associated to a metric
-  lock a Carbonara blob, here, we can just use the
   CarbonaraBasedStorageToozLock class, that use
   `Tooz <https://github.com/openstack/tooz>`__ and do all the locking
   stuffs for us.

Note that we don't care about aggregation across metric, Carbonara does
this for us too.

How will we do that for Ceph? Ceph doesn't have the notion of container,
we just have to choose a format for the object name such as
"gnocchi\_<metric\_name>\_<aggregation\_method>", and then
stats/stores/retrieves/deletes the Carbonara blobs.

How does it look like in Python
-------------------------------

Connect to Ceph with the RADOS protocol, define the object name format,
use the `Tooz <https://github.com/openstack/tooz>`__ lock helper and
create a helper to prepare the Ceph object name.


.. code-block:: python

    import rados
    from gnocchi import storage
    from gnocchi.storage import _carbonara


    class CephStorage(_carbonara.CarbonaraBasedStorage):
        def __init__(self, conf):
            super(CephStorage, self).__init__(conf)
            self.pool = 'my_gnocchi_pool'
            self.rados = rados.Rados(conffile='/etc/ceph/ceph.conf')
            self.rados.connect()
            self._lock = _carbonara.CarbonaraBasedStorageToozLock(conf)

       @staticmethod
       def _get_object_name(metric, aggregation):
            return "gnocchi_%s_%s" % (metric, aggregation)


       def _get_ioctx(self):
            return self.rados.open_ioctx(self.pool)

Then, check if the object already exists or not andraise the appropriate
exception if so (storage.MetricAlreadyExists):


.. code-block:: python

        def _create_metric_container(self, metric):
            aggregation = self.aggregation_types[0]
            name = self._get_object_name(metric, aggregation)
            with self._get_ioctx() as ioctx:
                try:
                    size, mtime = ioctx.stat(name)
                except rados.ObjectNotFound:
                    return
                raise storage.MetricAlreadyExists(metric)

Store the Carbonara blob in a Ceph object named
gnocchi\_<metric\_name>\_<aggregation\_method>


.. code-block:: python

        def _store_metric_measures(self, metric, aggregation, data):
            name = self._get_object_name(metric, aggregation)
            with self._get_ioctx() as ioctx:
                ioctx.write_full(name, data)

Retrieve the Carbonara blob associated with this aggregation and metric:


.. code-block:: python

        def _get_measures(self, metric, aggregation):
            try:
                with self._get_ioctx() as ioctx:
                    name = self._get_object_name(metric, aggregation)
                    offset = 0
                    content = b''
                    while True:
                        data = ioctx.read(name, offset=offset)
                        if not data:
                            break
                        content += data
                        offset += len(content)
                    return content
            except rados.ObjectNotFound:
                raise storage.MetricDoesNotExist(metric)

Delete all stuffs behind a metric:


.. code-block:: python

        def delete_metric(self, metric):
            with self._get_ioctx() as ioctx:
                try:
                    for aggregation in self.aggregation_types:
                        name = self._get_object_name(metric, aggregation)
                        ioctx.remove_object(name)
                except rados.ObjectNotFound:
                    raise storage.MetricDoesNotExist(metric)

Indeed, this is really straightforward, we have just written glue to
create/update/delete object with the blob generated by Carbonara. At
this point we have a working storage driver with ~ 50 lines of code. I'm
pretty sure that writting a `Cassandra <http://cassandra.apache.org/>`__
or a `Riak <http://basho.com/riak/>`__ storage driver would be simple
too.

Carbonara based storage driver lock mechanism.
----------------------------------------------

The update workflow of this driver is: get the timeserie data from the
key/value store update it with the new values store it in the key/value
store.

Since we can deploy multiple Gnocchi API workers,we have to ensure the
consistency of this workflow. To do that, the Carbonara based storage
driver have to lock the timeserie it is updating across all the Gnocchi
API workers. The Swift driver use
`Tooz <https://github.com/openstack/tooz>`__ to do that (and the Ceph
example above too).

But with Ceph we can go deeper and replace the
`Tooz <https://github.com/openstack/tooz>`__ lock helper by the Ceph
object lock.

To do that instead of doing:


.. code-block:: python

    self._lock = _carbonara.CarbonaraBasedStorageToozLock(conf)

I have implemented the '\_lock(metric, aggregation)' method, this method
have to returns a context manager that lock Carbonara blob in
__enter__ and release it in __exit__:

For ceph is looks like this:


.. code-block:: python

    @contextlib.contextmanager
    def _lock(self, metric, aggregation):
        name = self._get_object_name(metric, aggregation)
        with self._get_ioctx() as ctx:
            ctx.lock_exclusive(name, 'lock', 'gnocchi')
            try:
                yield
            finally:
                ctx.unlock(name, 'lock', 'gnocchi')

*Note: the in tree gnocchi code is quite different to support older
version of the Python rados*

Then we have to tweak a bit the \_create\_metric\_container and
\_get\_measures, because creating an object lock on an unexisting object
in Ceph, create the object with no content.

So in \_create\_metric\_container replaces:


.. code-block:: python

    size, mtime = ioctx.stat(name)

by


.. code-block:: python

    size, mtime = ioctx.stat(name)
    if size == 0:
         return

And in \_get\_measures replaces:


.. code-block:: python

    return content

by


.. code-block:: python

    if len(content) == 0:
         raise storage.MetricDoesNotExist(metric)
    return content

With this few additional lines, we now have the ceph storage driver that
use the object locking mechanism of ceph.

The `in tree ceph driver of
gnocchi <https://github.com/stackforge/gnocchi/blob/master/gnocchi/storage/ceph.py>`__
looks like that with some compatibility stuffs for old python-ceph
library and some additional configuration options (ceph
keyring/userid/pool).

Unit tests
----------

To test the driver we don't have to rewrite everything. Gnocchi uses
testscenarios to run a suite of tests on each drivers, so we can just
add the new storage driver to the list.

In
https://github.com/stackforge/gnocchi/blob/master/gnocchi/tests/base.py
we add:


.. code-block:: python

    storage_backends = [
        ('null', dict(storage_engine='null')),
        ('swift', dict(storage_engine='swift')),
    ...
        ('ceph', dict(storage_engine='ceph')),
    ]

Then, we have two solutions:

-  if this is possible, we can create a script to setup the backend,
   like we did for
   `PostgreSQL <https://github.com/stackforge/gnocchi/blob/master/setup-postgresql-tests.sh>`__
   or
   `MySQL <https://github.com/stackforge/gnocchi/blob/master/setup-mysql-tests.sh>`__.
-  if not, we can just mock the underlying Python module, like this is
   done for Swift (that mock python-swiftclient).

For the Ceph driver, I have used the second solution, because installing
and setuping Ceph into the Openstack Infra CI, it not really easy. You
can found the mock of this library
`here <https://github.com/stackforge/gnocchi/blob/master/gnocchi/tests/base.py#L59>`__.

This mocked library is loaded
`here <https://github.com/stackforge/gnocchi/blob/master/gnocchi/tests/base.py#L331>`__
like this:


.. code-block:: python

    self.useFixture(mockpatch.Patch('gnocchi.storage.ceph.rados', FakeRadosModule()))

Nothing else, the driver have unit tests now.

Now test it!
------------

To do it, I setup a devstack VM for swift with the following devstack
configuration:


.. code-block:: shell

    SWIFT_REPLICAS=1
    enable_plugin gnocchi https://github.com/stackforge/gnocchi
    enable_service key,gnocchi-api,s-proxy,s-object,s-container,s-account

And a devstack VM for ceph with:


.. code-block:: shell

    enable_plugin gnocchi https://github.com/stackforge/gnocchi
    enable_service key,gnocchi-api,ceph

And then for each, I run the gnocchi perf\_tools that measures the time
to put/get measurements. I use 10 clients in parallel that POST 100
times a batch of 100 measurements, the value of each measurements is
always 100, to have exactly the same data generated for each backend.

I run this workload with


.. code-block:: shell

    mkdir result_swift
    n=10 parallel --progress -j $n python ./tools/duration_perf_test.py --result result_swift/client{}.. :::  $(seq 0 $n)


And after on my ceph VM:


.. code-block:: shell

    mkdir result_ceph
    n=10 parallel --progress -j $n python ./tools/duration_perf_test.py --result result_ceph/client{}.. :::  $(seq 0 $n)


Take a looks of the result:


.. code-block:: shell

    python ./tools/duration_perf_analyse.py result_swift
    * get_measures:
             Duration
    mean      0.03918
    std       0.02060
    min       0.01000
    max       0.13000
    ...

    * write_measures:
              Duration
    mean     4.058136
    std      2.034822
    min      0.550000
    max      9.350000
    ...


.. code-block:: shell

    python ./tools/duration_perf_analyse.py result_ceph
    * get_measures:
              Duration
    mean      0.037790
    std       0.029531
    min       0.010000
    max       0.310000
    ...

    * write_measures:
              Duration
    mean      5.523090
    std       2.643746
    min       0.500000
    max       9.400000
    ...

The tools also generates csv files that we can use to make some graphs:

.. figure:: /static/7-swift-get.png
   :alt: Swift - GET measurements

.. figure:: /static/7-ceph-get.png
   :alt: Ceph - GET measurements

.. figure:: /static/7-swift-post.png
   :alt: Swift - GET measurements

.. figure:: /static/7-ceph-post.png
   :alt: Ceph - GET measurements

We don’t see a significant difference between swift and ceph here, but
results come from a all-in-one vm, I could be cool to do that on a real
swift/ceph cluster with more clients in parallel and during much times,
to see the limit of each backends. But this is enough to see that the
time to get/write measurements doesn’t change over the times, and that
is good things.
