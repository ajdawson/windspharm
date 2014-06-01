"""Build and install the windspharm package."""
from setuptools import setup

for line in open('lib/windspharm/__init__.py').readlines():
    if line.startswith('__version__'):
        exec(line)

packages = ['windspharm',
            'windspharm.examples',
            'windspharm.tests' ]

package_data = {'windspharm.examples': ['example_data/*'],
                'windspharm.tests': ['data/*.npy'],}

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
      package_dir={'':'lib'},
      package_data=package_data,
      use_2to3=True,
      install_requires=['numpy', 'pyspharm >= 1.0.8'],)
