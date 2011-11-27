del updatesearchentries.bat
FOR /F %%E in (searchentries.txt) do gensearchentry %%E & echo regedit /s ISEntry-%%E.reg >> updatesearchentries.bat