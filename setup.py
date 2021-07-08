#!/usr/bin/env python

#  Copyright 2020 Invana
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http:www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from setuptools import setup, find_packages
from invana_engine.default_settings import __VERSION__

setup(
    name='invana-engine',
    version=__VERSION__,
    description='GraphQL API for Apache TinkerPop supported graph databases.',
    author='Ravi Raja Merugu',
    author_email='ravi@invana.io',
    url='https://github.com/invanalabs/invana-engine',
    packages=find_packages(
        exclude=("dist", "docs", "tests", "scripts", "experiments")
    ),
    install_requires=[
        'gremlinpython==3.5.0'
    ],
    entry_points={
        'console_scripts': [
            'invana-engine-start = invana_engine.server_start:server_start',
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
