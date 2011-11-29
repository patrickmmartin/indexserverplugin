if exist build rmdir /S /Q build
if exist dist rmdir /S /Q dist
if exist TracIndexServer.egg-info rmdir /S /Q TracIndexServer.egg-info

:: assuming the python location
c:\python27\python setup.py bdist_egg