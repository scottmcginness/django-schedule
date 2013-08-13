#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

dateutil = 'python-dateutil'
if sys.version_info < (3, 0):
    dateutil = 'python-dateutil==2.1'

setup(
    name='django-schedule',
    version='0.7',
    description='A calendaring app for Django.',
    author='Anthony Robert Hauber',
    author_email='thauber@gmail.com',
    url='http://github.com/scottmcginness/django-schedule/tree/master',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    install_requires=['setuptools', 'vobject', dateutil, 'pytz'],
    license='BSD',
    test_suite="schedule.tests",
)
