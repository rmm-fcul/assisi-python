'''
A setuptools script that follows recommendations (where relevant) from:
  https://github.com/pypa/sampleproject/blob/master/setup.py
  https://github.com/jeffknupp/sandman/blob/develop/setup.py
  http://pythonhosted.org/setuptools/setuptools.html

Note: to ensure that the description file is available in the target,
(needed when setup.py is executed, either manually or by easy_install/pip)
the MANIFEST.in file is used.
package_data and data_files are ignored by setuptools when compiling
source distributions!

'''


from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # source: https://github.com/jeffknupp/sandman/blob/develop/setup.py
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    # source: https://github.com/jeffknupp/sandman/blob/develop/setup.py
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('DESCRIPTION.rst')

setup(
    name="assisipy",
    version=find_version('assisipy', '__init__.py'),
    packages=find_packages(exclude=["doc"]),

    description="Python API for the ASSISbf project",
    long_description=long_description,

    # The project URL.
    url='https://github.com/larics/assisi-python',

    # Author details
    author='LARICS Laboratory',
    author_email='larics@fer.hr',

    license='LGPL',

    classifiers=[
        'Development status :: 5 - Production/Stable',

        'Intended Audience :: ASSISIbf researchers',
        'Topic :: Collective systems :: Software tools',

        'License :: OSI Approved :: LGPL License',

        'Programming Language :: Python :: 2.7'
    ],

    keywords='assisi, assisibf, collective systems',

    # Run-time dependencies (will be installed by pip)
    install_requires = ['pyzmq','protobuf','pyyaml', 'pygraphviz', 'Fabric'],


)
