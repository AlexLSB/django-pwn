=============================
django-pwn
=============================

.. image:: https://badge.fury.io/py/django-pwn.png
    :target: http://badge.fury.io/py/django-pwn
    
.. image:: https://travis-ci.org/evonove/django-pwn.png?branch=master
        :target: https://travis-ci.org/evonove/django-pwn


.. image:: https://coveralls.io/repos/evonove/django-pwn/badge.png
  :target: https://coveralls.io/r/evonove/django-pwn

.. image:: https://pypip.in/d/django-pwn/badge.png
        :target: https://crate.io/packages/django-pwn?version=latest


Django integration with PWN API

Documentation
-------------

The full documentation is at https://django-pwn.readthedocs.io/.

Quickstart
----------

Install django-pwn::

    pip install git+https://github.com/AlexLSB/django-pwn.git

Then use it in a project::

    import django_pwn

In order to use the application, add `django_pwn` to your INSTALLED_APPS in your project's settings::

    INSTALLED_APPS = (
        ...
        'django_pwn',
        ...
    )

Settings
-------------------------------------

Open an account at https://pwnhealth.com/ if you don't have one already. Then, add this to your project's settings::

    DJANGO_MONEY_RATES = {
        'API_KEY': 'pwn_api_key',
        'API_TOKEN': 'PwNaPiToKeN',
        'PWN_HOST': 'staging_or_prod_PWNHost',
        'PWN_API': '52.XX.XX.XX',
    }

For more information on the PWN API, see https://api-docs-labs-module.pwnhealth.com/


Convert from one currency to another
------------------------------------

Here's an example of creating an order:

.. code-block:: python

    from django_pwn.models import PWNOrder

    pwn_order = PWNOrder(
        first_name= ... ,
        last_name= ... ,
        gender= ... ,
        dob= ... ,
        state= ... ,
        test_types= ... ,
        work_phone= ... ,
        city= ... ,
        zip_code= ... ,
        address= ... ,
        email= ... ,
        order_id= ... ,
    )
    pwn_order.create()

And getting the result when it's ready:

.. code-block:: python

    from django_pwn.models import PWNOrder

    pwn_order = PWNOrder.objects.get( ... )
    results = pwn_order.fetch_results()


To get a list of orders:

.. code-block:: python

    from django_pwn import PWNClient

    cli = PWNClient()

    orders = cli.get_customers()


Features
--------

* Create an order at PWN
* Get a list of orders
* View details on an order.


TODO List
---------

* Add url to get norifications from PWN
