## simple makefile - currently *nix like
default: clean all docs tests

clean:
	@echo "   === cleaning	==="
	@python setup.py clean

all: 
	@echo "   === building egg ==="
	@python setup.py bdist_egg 

deploy:
	@echo "   === deploying	==="
	@python setup.py deploy

bounce:
	@echo "   === bouncing	==="
	@python setup.py bounce

docs:
	@echo "   === documentation ==="
	@pydoc -w tracindexserversearch

trac-install: deploy bounce

tests:
	@echo tests - WRITE ME!

