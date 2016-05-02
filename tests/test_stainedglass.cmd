SET LOC=C:\EditImageWithIM
SET PWD=p4s5w0rd

IF EXIST %LOC%\stainedglass.exe (
  SET SG_CMD=%LOC%\stainedglass.exe
) ELSE (
  IF EXIST ..\dist\stainedglass.exe (
    SET SG_CMD=..\dist\stainedglass.exe
  ) ELSE (
    SET SG_CMD=py -2.7-32 ..\stainedglass.py
  )
)

%SG_CMD% -P %PWD% -k random -b 150 -t 1 -r 56 birdofparadise.gif sg_01.gif --verbose
%SG_CMD% -P %PWD% -k hexagon -b 150 -t 1  birdofparadise.gif sg_02.gif --verbose
%SG_CMD% -P %PWD% -k square -b 150 -t 1  birdofparadise.gif sg_03.gif --verbose
%SG_CMD% -P %PWD% -k random -b 150 -t 0 -r 56 birdofparadise.gif sg_04.gif --verbose

%SG_CMD% -P %PWD% -k random -t 1 -r 56 face.jpg sg_face_01.png --verbose
%SG_CMD% -P %PWD% -k hexagon -t 1  face.jpg sg_face_02.png --verbose
%SG_CMD% -P %PWD% -k square -t 1  face.jpg sg_face_03.png --verbose
%SG_CMD% -P %PWD% -k random -t 0 -r 56 face.jpg sg_face_04.png --verbose
