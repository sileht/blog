:title: Configuring CORS for Gnocchi and Keystone
:date: 2015-09-02 11:03
:category: Openstack
:tags: openstack, ceilometer, gnocchi, grafana 

In some case `Cross-origin resource sharing (CORS) <https://en.wikipedia.org/wiki/Cross-origin_resource_sharing>`
is required on some REST API to work with certain applications.

For example, if you to use `Grafana <http://grafana.org/>` with the `Gnocchi <http://docs.openstack.org/developer/gnocchi/`> 
datasource, some setup are required on the Gnocchi and Keystone side to allow grafana UI to access 
to Gnocchi REST API.

I will show you how to do this configuration:

All of this configuration have been done with the Liberty version of Openstack and was
not yet supported in previous version.

Since Liberty, we can use the oslo.middleware CORS middleware without waiting it's integration into
a Openstack application.

Note that on my example, my Grafana server is http://my-grafana-ipdomain:3000.

So, we will start with keystone.

Add a new filter to the paste configuration in /etc/keystone/keystone-paste.ini::

    [filter:cors]
    paste.filter_factory = oslo_middleware.cors:CORS.factory
    oslo_config_project = keystone
    # This should be not required, see: https://bugs.launchpad.net/oslo.middleware/+bug/1491293
    allowed_origin = http://my-grafana-ipdomain:3000

And for each pipelines add 'cors' at the beginning, on my setup I have::

    [pipeline:public_api]
    pipeline = cors sizelimit url_normalize request_id build_auth_context token_auth admin_token_auth json_body ec2_extension user_crud_extension public_service

    [pipeline:admin_api]
    pipeline = cors sizelimit url_normalize request_id build_auth_context token_auth admin_token_auth json_body ec2_extension s3_extension crud_extension admin_service

    [pipeline:api_v3]
    pipeline = cors sizelimit url_normalize request_id build_auth_context token_auth admin_token_auth json_body ec2_extension_v3 s3_extension simple_cert_extension revoke_extension federation_extension oauth1_extension endpoint_filter_extension service_v3

    [pipeline:public_version_api]
    pipeline = cors sizelimit url_normalize public_version_service

    [pipeline:admin_version_api]
    pipeline = cors sizelimit url_normalize admin_version_service

Then you can configure the middleware in /etc/keystone/keystone.conf::

    [cors]
    allowed_origin = http://my-grafana-ipdomain:3000
    allow_methods = GET,POST,PUT,DELETE,OPTIONS
    allow_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma,X-Auth-Token,X-Subject-Token
    expose_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma,X-Auth-Token,X-Subject-Token


On Gnocchi side now, we just have to add the following in /etc/gnocchi/gnocchi.conf::

    [api]
    # Ordering here in important
    middlewares = oslo_middleware.cors.CORS
    middlewares = keystonemiddleware.auth_token.AuthProtocol

    [cors]
    allowed_origin = http://my-grafana-ipdomain:3000
    allow_methods = GET,POST,PUT,DELETE,OPTIONS,HEAD
    allow_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma,X-Auth-Token,X-Subject-Token
    expose_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma


That's all! you can now use to Gnocchi Datasource with Grafana.
