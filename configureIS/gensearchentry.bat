@echo off
setlocal
echo. Windows Registry Editor Version 5.00 > ISentry-%1.reg
echo. >> ISentry-%1.reg
echo. [HKEY_CLASSES_ROOT\.%1] >> ISentry-%1.reg
echo. "Content Type"="text/plain" >> ISentry-%1.reg
echo. "PerceivedType"="text" >> ISentry-%1.reg
echo. @="%1 file" >> ISentry-%1.reg
echo. >> ISentry-%1.reg
echo. [HKEY_CLASSES_ROOT\.%1\PersistentHandler] >> ISentry-%1.reg
echo. @="{5e941d80-bf96-11cd-b579-08002b30bfeb}" >> ISentry-%1.reg
endlocal