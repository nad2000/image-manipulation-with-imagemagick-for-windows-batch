# -*- coding: utf-8 -*-

from __future__ import print_function

import subprocess
import os
import sys
import tempfile
from docopt import docopt
from io import StringIO
from functools import partial
from math import sqrt
import platform
import time

import conf

start_ts = time.time()

MY_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))


def show_timing():
    global verbose, start_ts

    if verbose:
        if start_ts > 0:
            print("*** Executed in: %.2fs" % (time.time() - start_ts))

        start_ts = time.time()


def log(line):
    global verbose, start_ts

    if verbose:
        print('#' * 80)
        print(
            ' '.join([os.path.basename(line[0]).replace(".exe", '')] + line[1:]))


def find_command(cmd, version=None):
    if os.name == 'nt':
        ret = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), "shared",
                                           cmd + ("64" if platform.machine().endswith("64") else "32") + ".exe"))
        if not os.path.exists(ret):

            shared_dir = "shared32"
            if cmd == "convert" and version is not None:
                shared_dir += ("-" + version)
            # to run .EXE from dist directory:
            if not os.path.exists(shared_dir):
                shared_dir = os.path.join("..", shared_dir)

            ret = os.path.abspath(os.path.join(
                os.path.dirname(sys.argv[0]),
                shared_dir,
                cmd + ".exe"))
            if not os.path.exists(ret):
                ret = os.path.abspath(os.path.join(shared_dir, cmd + ".exe"))
                if not os.path.exists(ret):
                    import distutils.spawn
                    ret = distutils.spawn.find_executable(cmd)
                    if ret is None and cmd == 'avconv':
                        ret = find_command('ffmpeg')
        return ret
    else:
        return cmd

IM_CMD = find_command('convert')
COMPOSITE_CMD = find_command('coposite')
FFMPEG_CMD = find_command('ffmpeg')
AVCONV_CMD = find_command('avconv')

# Variable settings for Imageio:
if os.name == 'nt':
    os.environ['IMAGEIO_FFMPEG_EXE'] = FFMPEG_CMD
    FREEIMAGE_LIB = "freeimage-3.15.4-win32.dll"

    lib_path = os.path.join(MY_DIR, "shared32", FREEIMAGE_LIB)
    if not os.path.exists(lib_path):
        lib_path = os.path.join("shared32", FREEIMAGE_LIB)
    os.environ["IMAGEIO_FREEIMAGE_LIB"] = lib_path
    #os.environ["IMAGEIO_FREEIMAGE_LIB"] = "shared32"

verbose = False


def get_args(usage):

    global verbose

    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")

    # if -P option is absent, exit quietly
    if "-P" not in sys.argv:
        sys.exit(-1)

    o = docopt(usage)
    if verbose:
        print("Options:\n========")
        for item in o.items():
            print("{}: {}".format(*item))

        print("*** MY_DIR: ", MY_DIR)
        print("*** ImageMagick: ", IM_CMD)
        print("*** FFMPEG: ", FFMPEG_CMD)
        print("*** COMPOSITE_CMD: ", COMPOSITE_CMD)

        if os.name == 'nt':
            print("*** FREEIMAGE_LIB: ", FREEIMAGE_LIB)
            print("*** IMAGEIO_FREEIMAGE_LIB: ",
                  os.environ["IMAGEIO_FREEIMAGE_LIB"])

    if o['-P'] != conf.PASSWORD:
        # raise Exception("Wrong password! Access denied!")
        print("Wrong password! Access denied!")
        sys.exit(-1)

    return o

#%%
im_version = None


def get_im_version():
    global im_version
    if im_version is None:
        version = run_im('-list', 'configure')
        version = version[version.find('LIB_VERSION_NUMBER'):]
        version = version[:version.find('\n')]
        if version == '':
            version = run_im('-version')
            version = version[version.find(
                'Version: ImageMagick ') + len('Version: '):]
            version = version[:version.find('\n')]
            version = version.replace('.', ',').replace('-', ',')
        version = version.split()[1]
        version = ''.join(
            ['0' + n if len(n) == 1 else n for n in version.split(',')])
        im_version = version
    return im_version


def get_file_colorspace(file_name):

    return run_im(file_name, '-ping', '-format', '%[colorspace]', 'info:').strip()

#%%


def color_num(file_name):

    return int(run_im(file_name, '-format', '"%k"', 'info:').strip('"\' \t\n\r'))


def get_dim(file_name):

    out = run_im(file_name, '-format', '"%wx%h"', 'info:')

    return tuple(
        map(int, run_im(file_name, '-format', '"%wx%h"', 'info:').strip('"\' \t\n\r').split('x')))


def hsl_to_cspace(tinthue, tintsaturation, tintlightness, cspace):

    tinthue, tintsaturation, tintlightness = [str(s) if type(
        s) is str else s for s in [tinthue, tintsaturation, tintlightness]]
    return run_im("-size", "1x1", 'xc:hsl({}%,{}%,{}%)'.format(tinthue, tintsaturation, tintlightness),
                  "-colorspace", cspace, "-format", '%[pixel:u.p{0,0}]', "info:")


def hsl_to_srgb(tinthue, tintsaturation, tintlightness):

    return hsl_to_cspace(tinthue, tintsaturation, tintlightness, "sRGB")


def get_cspace_option():
    """
    colorspace RGB and sRGB swapped between 6.7.5.5 and 6.7.6.7
    though probably not resolved until the latter
    then -colorspace gray changed to linear between 6.7.6.7 and 6.7.8.2
    then -separate converted to linear gray channels between 6.7.6.7 and 6.7.8.2,
    though probably not resolved until the latter
    so -colorspace HSL/HSB -separate and -colorspace gray became linear
    but we need to use -set colorspace RGB before using them at appropriate times
    so that results stay as in original script
    The following was determined from various version tests using nightvision.
    with IM 6.7.4.10, 6.7.6.10, 6.8.3.2
    """
    version = get_im_version()

    if (version < "06070607" or version > "06070707") and version <= "06080504":
        return ['-set', 'colorspace', 'RGB']
    else:
        return []


def get_cspace():
    """
    colorspace RGB and sRGB swapped between 6.7.5.5 and 6.7.6.7
    though probably not resolved until the latter
    then -colorspace gray changed to linear between 6.7.6.7 and 6.7.8.2
    then -separate converted to linear gray channels between 6.7.6.7 and 6.7.8.2,
    though probably not resolved until the latter
    so -colorspace HSL/HSB -separate and -colorspace gray became linear
    but we need to use -set colorspace RGB before using them at appropriate times
    so that results stay as in original script
    The following was determined from various version tests using nightvision.
    with IM 6.7.4.10, 6.7.6.10, 6.8.3.2
    """
    version = get_im_version()

    if (version < "06070607" or version > "06070707") and version <= "06080504":
        return 'RGB'
    else:
        return 'sRGB'

#%%


def flatten_list(tree):
    """
    flattens a hirachical strtucture and alos exclued emplty (None) elements
    """
    thelist = []
    for e in tree:
        if e is None or (type(e) is str and e.strip() == ''):
            continue

        if not isinstance(e, (list, tuple)):
            thelist += [e]
        else:
            thelist += flatten_list(e)
    return thelist


def composite(*args, **kwargs):

    cmd = [COMPOSITE_CMD]
    cmd += flatten_list(args)
    log(cmd)

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, **kwargs)

    return proc


def open_im(*args, **kwargs):

    cmd = [IM_CMD]
    cmd += flatten_list(args)
    log(cmd)

    if 'stdout' in kwargs:
        proc = subprocess.Popen(cmd, **kwargs)
    else:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, **kwargs)

    return proc


def run_im(*args, **kwargs):
    """
    Run IamgeMagic convert command
    """

    global verbose

    cmd = [IM_CMD]
    cmd += flatten_list(args)
    log(cmd)

    output = None

    if 'stdout' in kwargs:
        retcode = subprocess.call(cmd, **kwargs)
        if retcode != 0 and verbose:
            print("Last command %s RC=%s" % (cmd, retcode))
    else:
        try:
            output = subprocess.check_output(cmd, **kwargs)
        except subprocess.CalledProcessError as e:
            # ignore the return code and carry on
            output = e.output
        #output = subprocess.check_call(cmd, **kwargs)
        if output:
            output = output.strip()

        if verbose and output:
            print('-' * 80)
            print(output)

    show_timing()
    return str(output, "utf-8") if sys.version[0] == 3 else str(output).encode("utf-8")


def ffmpeg(*args, **kwargs):
    """
    Run FFMPEG command
    """

    global verbose

    cmd = [FFMPEG_CMD]
    cmd += flatten_list(args)
    log(cmd)

    if 'stdout' in kwargs:
        subprocess.check_call(cmd, **kwargs)
        return None
    else:
        output = subprocess.check_output(cmd, **kwargs)
        #output = subprocess.check_call(cmd, **kwargs)
        if output:
            output = output.strip()

        if verbose and output:
            print('-' * 80)
            print(output)

        return output


def avconv(*args, **kwargs):
    """
    Run AVCONV command
    """

    global verbose

    cmd = [AVCONV_CMD]
    cmd += flatten_list(args)
    log(cmd)

    if 'stdout' in kwargs:
        subprocess.check_call(cmd, **kwargs)
        return None
    else:
        output = subprocess.check_output(cmd, **kwargs)
        #output = subprocess.check_call(cmd, **kwargs)
        if output:
            output = output.strip()

        if verbose and output:
            print('-' * 80)
            print(output)

        return output


def get_colors(file_name):

    with open_im(file_name, '-alpha', 'off', '-depth', '8', '-format', '%c',
                 '-define', 'histogram:unique-colors=true', 'histogram:info:-').stdout as lines:

        return [list(map(
            int,
            l[l.find('(') + 1:l.find(')')].replace(' ', '').split(','))) for l in lines if '(' in l]


def delete_tmp_files(*files):

    for f in files:
        try:
            os.remove(f)
        except:
            pass


def rgb_dist(c, m):
    return sqrt(sum((_[0] - _[1]) ** 2 for _ in zip(c, m)))


def lum(color):
    R, G, B = color
    return 0.299 * R + 0.587 * G + 0.114 * B


def rgbl_dist(c, m):
    c_R, c_G, c_B = c
    m_R, m_G, m_B = m
    return sqrt(
        (0.299 * ((c_R - m_R) ** 2)
         + 0.587 * ((c_G - m_G) ** 2)
         + 0.114 * ((c_B - m_B) ** 2)) * 0.75
        + (lum(c) - lum(m)) ** 2)


def setup_vignette(file_name, vignetteshape, vignettesize, vignetterounding):
    """setup vignette"""

    ww, hh = get_dim(file_name)

    vignetteshape = vignetteshape.lower()[0]
    if vignetteshape in ["v", "h"]:  # "vertical", "horizontal"

        run_im("-size", str(ww) + 'x' + str(hh), "xc:black", "-crop",
               "100x" + vignettesize + "+0+0%" if vignetteshape == "v" else vignettesize + "x100+0+0%",
               "+repage", "-background", "white", "-gravity", "center", "-extent", str(
            ww) + 'x' + str(hh),
            "-morphology", "distance", "euclidean:4", "-auto-level", "-negate", file_name)

    elif vignetteshape == "r":  # "roundrectangle"

        xc, yc = ww / 2., hh / 2.
        ww2, hh2 = str(int(vignettesize) * ww /
                       200.), str(int(vignettesize) * hh / 200.)
        rounding = str(min(ww, hh) * int(vignetterounding) / 100.)
        run_im("-size", str(ww) + 'x' + str(hh), "xc:white", "-fill", "black",
               "-draw", "translate {},{} roundrectangle -{},-{} {},{} {},{}".format(
               xc, yc, ww2, hh2, ww2, hh2, rounding, rounding),
               "-alpha", "off", "-morphology", "Distance", "Euclidean:4", "-auto-level", "-negate", file_name)


def add_vignette(file_name, vignette, vignettelighten):
    """add vignette"""

    run_im(file_name, '(', vignette, "+level", vignettelighten + "x100%", "-blur", "0x5", ')',
           "-compose", "multiply", "-composite", file_name)


def make_pached(input_file, output_file, color_map_file):

    global verbose

    version = get_im_version()
    ww, hh = get_dim(input_file)
    process_test = "getColors" in run_im("-list", "module")

    if version >= "06080310":

        with open_im(input_file, "(", "-background", "black", color_map_file, ")", "-alpha", "off",
                     "-compose", "copy_opacity", "-composite", "sparse-color:-").stdout as out:
            run_im("-size", "{}x{}".format(ww, hh), "xc:", "-sparse-color",
                   "voronoi", "@-", output_file, stdin=out)

    elif version < "06060210" or not process_test:

        with open_im(input_file, "(", "-background", "black", color_map_file, ")", "-alpha", "off",
                     "-compose", "copy_opacity", "-composite", "-monitor", "txt:-").stdout as out:

            cmd = [IM_CMD, "-size", "{}x{}".format(ww, hh), "xc:", "-sparse-color", "voronoi",
                   "@-", "+monitor", output_file]
            log(cmd)

            p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            print("\nProgress:\n")

            pipe = p.stdin
            for line in out:
                line = line.strip()
                if line and line[0] != '#' and " 0) " not in line:
                    print(line[:line.find(':')] + ',' +
                          line[line.rfind(" ") + 1:], file=pipe)

            pipe.close()
            p.wait()

    else:
        run_im(input_file, "(", "-background", "black", color_map_file, ")", "-alpha", "off",
               "-compose", "copy_opacity", "-composite", input_file)
        with open_im(input_file, "-alpha", "on", "-process", "getColors", "null:").stdout as out:
            run_im("-size", "{}x{}".format(ww, hh), "xc:",
                   "-sparse-color", "voronoi", "@-", output_file, stdin=out)


def remove_meta(input_name, output_name):
    run_im(input_name, "-define", 'profile:skip="*"', "-strip", output_name)


def num_val(string_val):
    """ Retruns eithe int or float"""

    if string_val is None:
        return None
    else:
        return float(string_val) if '.' in string_val else int(string_val)
