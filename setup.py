"""Build and install the windspharm package.

"""
from distutils.core import setup


setup(
    name="windspharm",
    version="1.1.0",
    description="Vector wind analysis in spherical coordinates.",
    author="Andrew Dawson",
    author_email="dawson@atm.ox.ac.uk",
    packages=["windspharm"],
    package_dir={"windspharm":"lib"}
)

