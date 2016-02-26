"""Build and install the windspharm package."""
# Copyright (c) 2012-2016 Andrew Dawson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from setuptools import setup

for line in open('lib/windspharm/__init__.py').readlines():
    if line.startswith('__version__'):
        exec(line)

packages = ['windspharm',
            'windspharm.examples',
            'windspharm.tests']

package_data = {
    'windspharm.examples': ['example_data/*'],
    'windspharm.tests': ['data/regular/*.npy', 'data/gaussian/*.npy']}

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
      package_dir={'': 'lib'},
      package_data=package_data,
      install_requires=['numpy', 'pyspharm >= 1.0.8'],)
