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

%CMD% -P %PW% -s "87.9" -e "88.1" --speedx 0.5 -H 0.4 --freeze-at 0.2 --freeze-x2 0.5 --fps 15 %VIDEO% anna_olaf.gif --verbose
