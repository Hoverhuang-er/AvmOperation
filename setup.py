#!/usr/bin/env python

"""
distutils/setuptools install script.
"""

import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''version\s*=\s*['"]([0-9.]+)['"]''')


def get_version():
    """Extract version from pyproject.toml"""
    with open(os.path.join(ROOT, 'pyproject.toml')) as f:
        content = f.read()
        match = VERSION_RE.search(content)
        if match:
            return match.group(1)
    return '0.1.0'


def get_long_description():
    """Read README for long description"""
    readme_path = os.path.join(ROOT, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, encoding='utf-8') as f:
            return f.read()
    return ''


requires = [
    'requests>=2.31.0',
    'azure-identity>=1.15.0',
    'azure-mgmt-compute>=30.0.0',
]


setup(
    name='avmoperation',
    version=get_version(),
    description='Azure VM operations with webhook notifications',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Hoverhuang',
    url='https://github.com/Hoverhuang-er/AvmOperation',
    scripts=[],
    packages=find_packages(exclude=['tests*', 'docs*']),
    package_data={},
    include_package_data=True,
    install_requires=requires,
    license="MIT",
    python_requires=">= 3.11",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
    ],
    project_urls={
        'Documentation': 'https://github.com/Hoverhuang-er/AvmOperation#readme',
        'Source': 'https://github.com/Hoverhuang-er/AvmOperation',
        'Bug Tracker': 'https://github.com/Hoverhuang-er/AvmOperation/issues',
    },
)
