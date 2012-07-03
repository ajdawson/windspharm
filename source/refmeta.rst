Metadata Interface Reference
============================

The `metadata` interface is contained in the module :py:mod:`windspharm.metadata`. It is designed for use with :py:mod:`cdms2` variables. The computations retain meta-data, so coordinate dimensions are preserved and appropriate attributes are set for returned quantities. Computation is done by creating an instance of the class :py:class:`windspharm.metadata.VectorWind`. The :py:class:`~windspharm.metadata.VectorWind` class is initialized with the eastward and northward components of the global wind field.

.. autoclass:: windspharm.metadata.VectorWind
   :members:

