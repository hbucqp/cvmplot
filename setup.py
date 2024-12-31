#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jake Cui
# Mail: cqp@cau.edu.cn
# Created Time:  2024-12-31 17:17:50
#############################################

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


requirements = [
    'Bio',
    'pandas >= 2.2.3',
    'setuptools',
    'matplotlib >= 3.9.2',
    'numpy >= 1.26.4',
    'scipy >= 1.14.1',
    'tabulate >= 0.9.0',
    'dask >= 2024.9.1',
    'pygenomeviz >= 1.4.1'
]

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'cvmplot', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)


# Get the long description from the relevant file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="cvmplot",
    version=about['__version__'],
    keywords=["tnseq", "dendrogram", "phylogram", "cgMLST", "wgMLST", "plot"],
    description="SZQ lab data plot function",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(),
    # include_package_data=True,
    package_data={'': ['*']},
    platforms="any",
    install_requires=requirements,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    # entry_points={
    #     'console_scripts': [
    #         'cvmblaster=cvmbalster.cvmblaster:main',
    #     ],
    # },
)
