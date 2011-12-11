# Index Server plugin

## Overview 

This Trac http://trac.edgewall.org plugin maps searches on files in an Index Server catalogue to the files in a Trac environment.
Index Server can handle large indexed volumes 100s of GB of files data and supports a number of interesting query types,
including queries on the metadata properties of Microsoft Office documents (author, keywords etc.).

## Build tasks

These are all implemented as standard or custom commands in setup.py,
there is also a _fairly_ standard makefile to help wrap things up a little.

## Building

```make all``` 

## Installation

The egg simply needs to be copied into the plugins dir of a Trac environment.


```make deploy <Trac Env>```

```make bounce``` 

these are wrapped up in the make target ```install-trac```

TODO - deploy and bounce stub targets exist, but do nothing right now
 



