SET LOC=C:\EditImageWithIM


%LOC%\stainedglass.exe -P p4s5w0rd -k random -b 150 -t 1 -r 56 birdofparadise.gif sg_01.gif --verbose
%LOC%\stainedglass.exe -P p4s5w0rd -k hexagon -b 150 -t 1  birdofparadise.gif sg_02.gif --verbose
%LOC%\stainedglass.exe -P p4s5w0rd -k square -b 150 -t 1  birdofparadise.gif sg_03.gif --verbose
%LOC%\stainedglass.exe -P p4s5w0rd -k random -b 150 -t 0 -r 56 birdofparadise.gif sg_04.gif --verbose

%LOC%\stainedglass.exe -P p4s5w0rd -k random -t 1 -r 56 face.jpg sg_face_01.png --verbose
%LOC%\stainedglass.exe -P p4s5w0rd -k hexagon -t 1  face.jpg sg_face_02.png --verbose
%LOC%\stainedglass.exe -P p4s5w0rd -k square -t 1  face.jpg sg_face_03.png --verbose
%LOC%\stainedglass.exe -P p4s5w0rd -k random -t 0 -r 56 face.jpg sg_face_04.png --verbose
