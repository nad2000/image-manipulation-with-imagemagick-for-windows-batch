
import os
import hashlib
import subprocess

PW = "p4s5w0rd"

def test_stainedglass(tmpdir):
    output_name = str(tmpdir.join("output.png"))
    #../stainedglass.py -P $PW -k random -b 150 -t 1 -r 56 birdofparadise.gif sg_01.gif 
    #../stainedglass.py -P $PW -k hexagon -b 150 -t 1  birdofparadise.gif sg_02.gif 
    #../stainedglass.py -P $PW -k square -b 150 -t 1  birdofparadise.gif sg_03.gif 
    #../stainedglass.py -P $PW -k random -b 150 -t 0 -r 56 birdofparadise.gif sg_04.gif
    #
    #../stainedglass.py -P $PW -k random -t 1 -r 56 face.jpg sg_face_01.png 
    #../stainedglass.py -P $PW -k hexagon -t 1  face.jpg sg_face_02.png
    #../stainedglass.py -P $PW -k square -t 1  face.jpg sg_face_03.png
    subprocess.call([
        "python", 
        "../stainedglass.py", "-P", PW, "-k", "random", 
        "-t", "0", "-r", "56", "face.jpg",
        output_name, "--verbose"])
    with open(output_name, "rb") as output:
        assert hashlib.sha1(output.read()).hexdigest() == "1f79a0ba04c57753d7178b31703178d9c36243e0"


