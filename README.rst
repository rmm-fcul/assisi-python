assisi-python
=============

Python API for the ASSISI|bf project.

Building the Python package and uploading it to PyPy
----------------------------------------------------

Assuming you have `~/.pypirc` already set up:

::

   python setup.py sdist
   twine upload dist/assisipy-x.y.z.tar.gz -p password


Installing the development version
----------------------------------

Local changes to the repo will be immediatelly visible in the
installed package (need to check this).

::

   sudo pip install -e .


To uninstall the development version:

::

   sudo python setup.py develop --uninstall


For more info see
http://python-packaging-user-guide.readthedocs.org/en/latest/distributing
