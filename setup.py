"""Build and install the windspharm package."""
# Copyright (c) 2012-2018 Andrew Dawson
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
import os.path

from setuptools import setup
import versioneer

packages = ['windspharm',
            'windspharm.examples',
            'windspharm.tests']

package_data = {
    'windspharm.examples': ['example_data/*'],
    'windspharm.tests': ['data/regular/*.npy', 'data/gaussian/*.npy']}

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(name='windspharm',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='vector wind analysis in spherical coordinates',
      author='Andrew Dawson',
      author_email='dawson@atm.ox.ac.uk',
      url='http://ajdawson.github.com/windspharm/',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=packages,
      package_data=package_data,
      install_requires=['numpy', 'pyspharm >= 1.0.8'],)
