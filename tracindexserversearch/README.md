# tracindedxserversearch

This is the source dir for the python egg.

## ```__init__.py```

This files simply imports from the main class ```indexserversearch.py```.

## ```indexserversearch.py```

This class implements ISearchSource

The methods delegate to _get_index_server_results_ which yields the search results.
The function calls CoInitialze and CoUninitialize to avoid requiring the hosting process to explicitly or implicitly 
have to initialise COM.


## Configuration


The Trac config needs to have a section _indexserver-search_ _catalogue-root_
Currently the Index Server Catalogue searched must be called "Source Catalogue".
The catalogue root path must map to the root of the repo indexed and searched. 
Files under a directory called .svn are ignored, so the checkout can be a working copy and updated as a result
of a post-commit hook allowing near live search on committed files.



