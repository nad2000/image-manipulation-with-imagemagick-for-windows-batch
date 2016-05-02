"""
Usage examples:

    py -2.7-32 -m py.test
    py -2.7-32 -m py.test -k face
    py -2.7-32 -m py.test -k bird
"""

import os
import hashlib
import subprocess
import pytest
import tempfile

import stainedglass as sg
#sg.utl.verbose = True
if sg.utl.os.name == 'nt':
    sg.utl.IM_CMD = sg.utl.find_command('convert', version="6.8.9-3")

BUF_SIZE = 65536  # 64kb chunks    
def file_sha1(file_name):
    # remove all meta data (so that hash gets calculated based on only image data):
    no_profile_name = "_noprofile".join(os.path.splitext(file_name))
    sg.utl.remove_meta(file_name, no_profile_name)
    
    sha1 = hashlib.sha1()
    with open(no_profile_name, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1


@pytest.mark.parametrize("kind, thick, rseed, expected", [
    ("random",  "1", "56", "1a01a0f5511e2d73784edf490a7d04b5f9286de1"),
    ("hexagon", "1", None, "c0a2a3211f16ea632f3494eb1df422da2b711960"),
    ("square",  "1", None, "07eb027ee4fc57039f22c1784a8787b075c9692e"),
    ("random",  "0", "56", "dcc9bf6ddde7371a0929422b91b93b079a21ce84"),
])    
def test_birdofparadise(kind, thick, rseed, expected):
    output_name = tempfile.mktemp(suffix=".gif")
    input_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "birdofparadise.gif")

    sg.process(kind=kind, thick=thick, rseed=rseed, infile=input_name, outfile=output_name, bright="150")
    assert file_sha1(output_name).hexdigest() == expected

    
@pytest.mark.parametrize("kind, thick, rseed, expected", [
    ("random",  "1", "0",  "26c3c064a9b12b07f814afceb878704528f58c8f"),
    ("hexagon", "1", None, "2f2199ae77ddd30bef9b2fd2d135fba8f96126f9"),
    ("square",  "1", None, "ef603e740bf8c26a56c4600b6776d5923e9960ac"),
    ("random",  "0", "0",  "e630713be1e13523c0fe08f5435a952516712101"),
])    
def test_face(kind, thick, rseed, expected):
    output_name = tempfile.mktemp(suffix=".png")
    input_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "face.jpg")

    sg.process(kind=kind, thick=thick, rseed=rseed, infile=input_name, outfile=output_name)
    assert file_sha1(output_name).hexdigest() == expected


