#!/usr/bin/env bash
PW=p4s5w0rd 
../stainedglass.py -P $PW -k random -b 150 -t 1 -r 56 birdofparadise.gif sg_01.gif 
../stainedglass.py -P $PW -k hexagon -b 150 -t 1  birdofparadise.gif sg_02.gif 
../stainedglass.py -P $PW -k square -b 150 -t 1  birdofparadise.gif sg_03.gif 
../stainedglass.py -P $PW -k random -b 150 -t 0 -r 56 birdofparadise.gif sg_04.gif

../stainedglass.py -P $PW -k random -t 1 -r 56 face.jpg sg_face_01.png 
../stainedglass.py -P $PW -k hexagon -t 1  face.jpg sg_face_02.png
../stainedglass.py -P $PW -k square -t 1  face.jpg sg_face_03.png
../stainedglass.py -P $PW -k random -t 0 -r 56 face.jpg sg_face_04.png
