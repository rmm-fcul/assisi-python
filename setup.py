# The package setup file
# Based on: https://github.com/pypa/sampleproject/blob/master/setup.py

from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

# Read the version number from a source file
def find_version(*file_paths):
    # Open in Latin-1 to avoid encoding errors
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)

    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Get the long description from the relevant file
with codecs.open('DESCRIPTION.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="assispy",
    version=find_version('assisipy', '__init__.py'),
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

    packages=find_packages(exclude=["doc"]),

    # Run-time dependencies (will be installed by pip)
    install_requires = ['pyzmq','protobuf','pyyaml'],

    # Additional files to be installed
    #package_data={
    #    'sample': ['package_data.dat'],
    #},

    # Provide executable scripts
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)

    
