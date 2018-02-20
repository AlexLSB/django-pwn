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

    pip install django-pwn

Then use it in a project::

    import django_pwn

In order to use the application, add `django_pwn` to your INSTALLED_APPS in your project's settings::

    INSTALLED_APPS = (
        ...
        'django_pwn',
        ...
    )

Setup the Open Exchange Rates backend
-------------------------------------

Open an account at https://pwnhealth.com/ if you don't have one already. Then, add this to your project's settings::

    DJANGO_MONEY_RATES = {
        'api_key': 'pwn_api_key',
        'api_token': 'PwNaPiToKeN',
    }

For more information on the PWN API, see https://api-docs-labs-module.pwnhealth.com/


Convert from one currency to another
------------------------------------

Here's an example of converting 10 Euros to Brazilian Reais:

.. code-block:: python

    from django_pwn import PWNCustomer
    customer = PWNCustomer(
        name=
    )
    customer.

Features
--------

* Create an order at PWN
* Get a list of orders
* View details on an order.


TODO List
---------

* Add url to get norifications from PWN
