Running the test suite
======================

The package comes with a comprehensive set of tests to make sure it is working correctly.
The tests can be run against an installed version of `eofs` or against the current source tree.
Testing against the source tree is handy during development when quick iteration is required, but for most other cases testing against the installed version is more suitable.

Running the test suite requires pytest_ to be installed.
The test suite will function as long as the minimum dependencies for the package are installed, but some tests will be skipped if they require optional dependencies that are not present.
To run the full test suite you need to have the optional dependencies `cdms2` (from UV-CDAT_), iris_, and xarray_ installed.

Testing against the current source tree
---------------------------------------

Testing the current source is straightforward, from the source directory run::

    pytest

This will perform verbose testing of the current source tree and print a summary at the end.


Testing an installed version
----------------------------

First you need to install `windspharm` into your current Python environment::

    cd windspharm/
    python setup.py install

Then create a directory somewhere else without any Python code in it and run ``pytest`` from there giving the package name ``windspharm``::

    mkdir $HOME/windspharm-test-dir && cd $HOME/windspharm-test-dir
    pytest --pyargs windspharm

This will run the tests on the version of `windspharm` you just installed.
This also applies when `windspharm` has been installed by another method (e.g., pip or conda).

.. _pytest: https://docs.pytest.org

.. _UV-CDAT: http://uv-cdat.llnl.gov

.. _iris: http://scitools.org.uk/iris

.. _xarray: http://xarray.pydata.org
