:: just an example - none of these commands are portable or OS- independent
:: update from SCM
svn update
:: build eg
call build-egg.bat
:: move to the Trac environment
move dist\*.egg E:\Trac\environments\winampremote2\plugins\
:: restart web server
"c:\Program Files\Apache Group\Apache2\bin\Apache.exe" -k restart
:: you should now have your new code deployed