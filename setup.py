# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 Patrick Martin patrickmmartin@gmail.com 
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from setuptools import setup, find_packages

setup(
    name = 'TracIndexServer', version = '0.2',
    author = 'Patrick Martin', author_email = 'patrickmmartin@gmail.com',
    url = 'about:mozilla',
    description = 'Support for Using MS Index Server in Trac for full-text repository search',
    license = 'BSD',
    packages = find_packages(exclude=['*.tests*']),
    entry_points = {
        'trac.plugins': ['tracindexserversearch = tracindexserversearch']
    }
)
