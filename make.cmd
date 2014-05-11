SET makensis="C:\Program Files (x86)\NSIS\makensis.exe"
SET python="C:\Python27\python.exe"

rmdir /Q /S dist build

%python% setup.py py2exe

mkdir Install
%makensis% install.nsi
