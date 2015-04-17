# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import glob
import math
import PIL.Image
import PIL.ImageStat
import os
import re
import shutil
import subprocess
import tempfile


def process(record):
    if record.application == "theMediaShell" and record.logger == "movie" and record.msg == "end":
        filename = record.args["movie"].replace("/home/themylogin/Storage", "/media/storage")

        i = 1
        length = int(re.search(r"ID_LENGTH=([0-9]+)",
                               subprocess.check_output(["mplayer",
                                                        "-nosound",
                                                        "-vc", ",",
                                                        "-vo", "null",
                                                        "-frames", "0",
                                                        "-identify",
                                                        filename],
                                                       stderr=subprocess.STDOUT)).group(1))
        for ss in range(int(length / 5 + 1), length, int(length / 5 + 1)):
            tmp_dir = str(tempfile.mkdtemp())

            subprocess.call(["mplayer",
                             "-ss", str(ss),
                             "-nosound",
                             "-vc", ",",
                             "-vo", "jpeg:outdir=" + tmp_dir,
                             "-subcp", "enca:ru:cp1251",
                             "-frames", "50",
                             filename])

            max_brightness = -1
            max_brightness_image = None
            for image in glob.glob(os.path.join(tmp_dir, "0000*.jpg")):
                r, g, b = PIL.ImageStat.Stat(PIL.Image.open(image)).mean
                brightness = math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))
                if brightness > max_brightness:
                    max_brightness = brightness
                    max_brightness_image = image

            dir = os.path.join("/home/themylogin/www/thelogin.ru/data/movies",
                               os.path.relpath(filename, "/media/storage/Torrent/downloads"))
            if not os.path.exists(dir):
                os.makedirs(dir)
            shutil.copy(max_brightness_image, os.path.join(dir, "%d.jpg" % i))

            for image in glob.glob(os.path.join(tmp_dir, "0000*.jpg")):
                os.unlink(image)

            os.rmdir(tmp_dir)

            i += 1
