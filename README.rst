p7magma
=======

.. image:: https://img.shields.io/travis/bfontaine/p7magma.png
   :target: https://travis-ci.org/bfontaine/p7magma
   :alt: Build status

.. image:: https://img.shields.io/coveralls/bfontaine/p7magma/master.png
   :target: https://coveralls.io/r/bfontaine/p7magma?branch=master
   :alt: Coverage status

.. image:: https://img.shields.io/pypi/v/p7magma.png
   :target: https://pypi.python.org/pypi/p7magma
   :alt: Pypi package

A Python interface for the Paris Diderot CS departement students results
website.

Note: this project is useless for you if you’re not a CS student at Paris
Diderot.

Install
-------

.. code-block::

    [sudo] pip install p7magma

The library works with both Python 2.x and 3.x.

Usage
-----

.. code-block::

    from magma.base import Student
    s = Student("M2", "john", "smith", "topsecret")

    print s.courses.desc()                # print all courses
    print s.courses.followed().desc()     # print all followed courses
    print s.courses.with_results().desc() # print all courses with results
