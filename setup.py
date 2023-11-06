#!/usr/bin/env python
from setuptools import setup, find_packages
from invana_engine2.settings import __VERSION__
from pip._internal.req import parse_requirements
from pip._internal.network.session import PipSession
import os


def get_install_requires():
    requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'),
                                      session=PipSession())
    return [str(requirement.requirement) for requirement in requirements]


print(get_install_requires())
setup(
    name='invana-engine',
    version=__VERSION__,
    description='Opensource GraphQL API for graph data',
    author='Ravi Raja Merugu',
    author_email='ravi@invana.io',
    url='https://github.com/invanalabs/invana-engine',
    packages=find_packages(
        exclude=("dist", "docs", "tests", "scripts", "experiments")
    ),
    install_requires=get_install_requires(),
    entry_points={
        'console_scripts': [
            'invana-engine-start = invana_engine.server.server:server_start',
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
