# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 Patrick Martin patrickmmartin@gmail.com 
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from setuptools import setup, find_packages

from distutils.cmd import Command
from distutils.errors import *
import os
import shutil

class CustomCommand(Command):
    user_options = []
    def initialize_options(self):
		None;
    def finalize_options(self):
		None;

class CleanCommand(CustomCommand):
    description = "custom clean command that forcefully removes dist/build directories"
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def removedir(self, dirname):
		# note the delete race condition: not handled by design:
		if os.path.exists(dirname):
			shutil.rmtree(dirname)
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        self.removedir("build")	
        self.removedir("dist")	
        self.removedir("TracIndexServer.egg-info")	

		
class DeployCommand(CustomCommand):
    description = "custom command to update a Trac environment"
    def run(self):
		# TODO assert we have a valid location
		print 'deploying the build ...'
		# TODO copy the build to the environment plugins location
		print 'deploy done'

class BounceCommand(CustomCommand):
    description = "custom command to bounce Apache"
    def run(self):
		# execute the bounce command
		print 'bouncing the server ...'
		# TODO execute the relevant apache graceful restart
		print 'bounce done'

		
		
setup(
    name = 'TracIndexServer', version = '0.2',
    author = 'Patrick Martin', author_email = 'patrickmmartin@gmail.com',
    url = 'https://github.com/patrickmmartin',
    description = 'Adds MS Index Server to Trac environment search',
	long_description = 'Adds Support for using MS Index Server in Trac environments for full-text repository search.',
    license = 'BSD',
    packages = find_packages(exclude=['*.tests*']),
	cmdclass = {'clean': CleanCommand, 'deploy': DeployCommand, 'bounce': BounceCommand},
    entry_points = {
        'trac.plugins': ['tracindexserversearch = tracindexserversearch'],	
    }

)

