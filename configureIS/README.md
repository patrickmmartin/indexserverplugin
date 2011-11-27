# configureIS

## Overview

Indexing of text files is controlled through registry entries. 
In order for some extensions to be treated appropriately, the registry data needs to be created.

These scripts demonstrate that process.

dfmsearch.reg and passearch.reg are the final registry entries needed for 2 Delphi file types.

The entire process is automated through populating searchentries.txt, and running gensearchentries, which will in generate input .reg files and populate updatesearchentries.bat.
Running updatesearchentries.bat will set the appropriate properties for those extensions and then the Index Server catalogue can be rebuilt for existing files, and new files will be indexed correctly.


