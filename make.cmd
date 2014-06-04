set makensis="C:\Program Files (x86)\NSIS\makensis.exe"
set python="C:\Python27\python.exe"
set zip7="C:\Program Files\7-Zip\7z.exe"
set upxEXE=C:\Tools\upx\upx.exe

rd /Q /S dist build

%python% setup.py py2exe

goto:mkinst
:: recompression works only with bundle_files = 2 or 3
cd dist
mkdir library

%zip7% x library.zip -aoa -olibrary
del library.zip
cd library
move ..\*.jpg .\

:: %zip7% a -tzip -mx9 "..\library.zip" -r
%zip7% a -tzip "..\library.zip" -r
cd ..

rd /Q /S library

cd ..

:mkinst

cd dist
%upxEXE% --best *.exe 
:: %upxEXE% --best *.dll
cd ..

mkdir Install
%makensis% install.nsi

:eof
