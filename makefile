## simple makefile - currently *nix like
default: clean all docs tests

clean:
	@echo "   === cleaning	==="
	@python setup.py clean

all: 
	@echo "   === building egg ==="
	@python setup.py bdist_egg 

docs:
	@echo "   === documentation ==="
	@pydoc -w tracindexserversearch

tests:
	@echo tests - WRITE ME!
