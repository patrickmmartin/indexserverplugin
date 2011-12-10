## simple makefile - currently *nix like
default: clean all docs tests

clean:
	@echo "   === cleaning	==="
	@rm -rf build
	@rm -rf dist
	@rm -rf TracIndexServer.egg-info 

all: 
	@echo "   === building egg ==="
	@python setup.py bdist_egg 

docs:
	@echo "   === documentation ==="
	@pydoc -w tracindexserversearch

tests:
	@echo tests - WRITE ME!
