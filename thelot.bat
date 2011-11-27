svn update
call build-egg.bat
move dist\*.egg E:\Trac\environments\winampremote2\plugins\
"c:\Program Files\Apache Group\Apache2\bin\Apache.exe" -k restart