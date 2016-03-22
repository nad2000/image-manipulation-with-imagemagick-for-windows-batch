SET makensis="C:\Program Files (x86)\NSIS\makensis.exe"
SET zip7="C:\Program Files\7-Zip\7z.exe"
SET upxEXE=%CD%\tools\upx391w\upx.exe

RD /Q /S Install

MKDIR Install
%makensis% install.nsi

:eof
