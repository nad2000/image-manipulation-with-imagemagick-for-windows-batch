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
    sha1 = hashlib.sha1()
    with open(file_name, "r") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1


@pytest.mark.parametrize("kind, thick, rseed, expected", [
    ("random",  "1", "56", "14c0523fd102ebd6e2f74c557c87a2f831d29937"),
    ("hexagon", "1", None, "6f98de8d48fb82d60098d8e93cce2408ea898952"),
    ("square",  "1", None, "5dc0781c61face607d682aee72ae8ac12c83c398"),
    ("random",  "0", "56", "ee42638e4792d58f99627447ceb1015baab7f87e"),
])    
def test_birdofparadise(kind, thick, rseed, expected):
    output_name = tempfile.mktemp(suffix=".gif")
    input_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "birdofparadise.gif")

    sg.process(kind=kind, thick=thick, rseed=rseed, infile=input_name, outfile=output_name, bright="150")
    assert file_sha1(output_name).hexdigest() == expected

    
@pytest.mark.parametrize("kind, thick, rseed, expected", [
    ("random",  "1", "0",  "6708ea33106f75ddffc4d867839f1161e4652e70"),
    ("hexagon", "1", None, "124723898918cbce159785fc804b03e1a2b94706"),
    ("square",  "1", None, "57d12019b31b56322c12a2c5391b4a9c2c6c919a"),
    ("random",  "0", "0",  "41cb8438007c80bccf46a19ff6a5fac531810787"),
])    
def test_face(kind, thick, rseed, expected):
    output_name = tempfile.mktemp(suffix=".png")
    input_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "face.jpg")

    sg.process(kind=kind, thick=thick, rseed=rseed, infile=input_name, outfile=output_name)
    assert file_sha1(output_name).hexdigest() == expected


