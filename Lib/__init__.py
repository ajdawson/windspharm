"""Spherical harmonic vector wind analysis."""
# Copyright (c) 2012 Andrew Dawson
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


# List to define the behaviour of imports of the form:
#     from windspharm import *
__all__ = []


try:
    # Import the meta-data interface.
    import metadata
    __all__.append('metadata')
except ImportError:
    # If it fails then only the numpy interface will be available.
    pass


try:
    # Try to import the numpy interface.
    import standard
    __all__.append('standard')
    import tools
    __all__.append('tools')
except ImportError:
    # Failure here indicates a missing requirement (pyspharm).
    raise ImportError('windspharm requires spharm (pyspharm)')

