SET VIDEO=frozen_trailer.mp4
IF NOT EXIST %VIDEO% SET VIDEO=..\frozen_trailer.mp4

SET MASK=mask.png
IF NOT EXIST %MASK% SET MASK=test\mask.png

SET PW=p4s5w0rd
REM SET PY=py -3.4
SET PY=py -2

IF EXIST dist\clip.exe. (
	SET CMD=dist\clip.exe
) ELSE (
	SET CMD=%PY% clip.py
)

%CMD% -P %PW% -s 1,38.15 -e 1,38.5 --speedx 0.2 -H 0.5 --fps 15 --fuzz 3 --mask-grad 5 --point 445,20 --point 345,275 %VIDEO% anna_kris.gif --verbose
%CMD% -P %PW% -s 1,38.15 -e 1,38.5 --speedx 0.2 -H 0.5 --fps 15 --fuzz 3 --mask-grad 5 --point 445,20 --point 440,63 --point 400,150 --point 340,275 %VIDEO% anna_kris_poligon.gif --verbose
%CMD% -P %PW% -s 1,38.15 -e 1,38.5 --speedx 0.2 -H 0.5 --fps 15 --fuzz 3 --mask %MASK% %VIDEO% anna_kris_masked.gif --verbose
