"""Build and install the windspharm package."""
from distutils.core import setup

for line in open('lib/windspharm/__init__.py').readlines():
    if line.startswith('__version__'):
        exec(line)

packages = ['windspharm']

setup(name='windspharm',
      version=__version__,
      description='vector wind analysis in spherical coordinates',
      author='Andrew Dawson',
      author_email='dawson@atm.ox.ac.uk',
      url='http://ajdawson.github.com/windspharm/',
      long_description="""
      windspharm provides a simple interface for doing calculations on
      vector wind fields (e.g., computing streamfunction) in spherical
      geometry using spherical harmonics
      """,
      packages=packages,
      package_dir={'':'lib'},)
