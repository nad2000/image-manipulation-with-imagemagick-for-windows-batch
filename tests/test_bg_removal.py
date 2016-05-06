"""
Usage examples:

    py -2.7-32 -m py.test
    py -2.7-32 -m py.test -k stamps
"""

import os
from subprocess import call
import pytest
import tempfile

from bg_removal import process, utl
from conf import PASSWORD

utl.verbose = True
if os.name == 'nt':
    utl.IM_CMD = utl.find_command('convert', version="6.8.9-3")
    
POSTMARKS_FN = os.path.join(os.path.dirname(os.path.realpath(__file__)), "stamps.jpg")
EXE = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "dist", "bg_removal.exe"))
TEST_PARAMS = [
    ("0", "100", False, False, False, "black", "1e81c3307358f9d9f0777c371139becc17cdd1da"),
    ("10", "90", False, False, False, "black", "f1cc698525db9570387992580fe9b916d0727d36"),
    ("0", "100", True,  False, False, "black", "e36dc647c4a3e421b79b0ded6f309c756d117761"),
    #("0", "100", False, False, False, "green", "8c6f9c110dc2e21cdf781892d60a4e7cd57ad9cb"),
    ("0", "100", False, True,  False, "black", "1e81c3307358f9d9f0777c371139becc17cdd1da"),
    ("0", "100", False, False, True,  "black", "142d548bce95f7dbd78adaffbe80cfcb000c48f3"),
]

@pytest.mark.parametrize("fuzz_out, fuzz_in, additive, showmasks, replace, background, expected", TEST_PARAMS)    
def test_stamps(fuzz_out, fuzz_in, additive, showmasks, replace, background, expected):
    output_name = tempfile.mktemp(suffix=".png")

    process(
        fuzz_out=fuzz_out, fuzz_in=fuzz_in, additive=additive,
        background=background, showmasks=showmasks, replace=replace,
        image=POSTMARKS_FN, image_out=output_name)
        
    assert utl.file_sha1(output_name).hexdigest() == expected

        
@pytest.mark.parametrize("fuzz_out, fuzz_in, additive, showmasks, replace, background, expected", TEST_PARAMS)    
def test_exe(fuzz_out, fuzz_in, additive, showmasks, replace, background, expected):

    if os.path.exists(EXE):
    
        cmd = [EXE, "-P", PASSWORD, "--verbose"]
        if additive:
            cmd.append("-a")
            
        if showmasks:
            cmd.append("-m")
            
        if replace:
            cmd.append("-r")
            
        if background != "black":
            cmd.extend(["-b", background])
            
        output_name_cmd = tempfile.mktemp(suffix=".png")
        cmd.extend([POSTMARKS_FN, fuzz_out, fuzz_in, output_name_cmd])

        call(cmd)
        
        assert utl.file_sha1(output_name_cmd).hexdigest() == expected
        
