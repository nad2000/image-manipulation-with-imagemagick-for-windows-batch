SET VIDEO=frozen_trailer.mp4
IF NOT EXIST %VIDEO% SET VIDEO=..\frozen_trailer.mp4
SET PW=p4s5w0rd
REM SET PY=py -3.4
SET PY=py -2

IF EXIST dist\clip.exe. (
	SET CMD=dist\clip.exe
) ELSE (
	SET CMD=%PY% clip.py
)

%CMD% -P %PW% -s "1,22.65" -e "1,23.2" -H 0.3 %VIDEO% use_your_head.gif
%CMD% -P %PW% -s "1,13.4" -e "1,13.9" -H 0.5 --x1=145 --x2=400 %VIDEO% kris_sven.gif
