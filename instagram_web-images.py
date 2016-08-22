# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import requests


def process(record):
    if record.application == "instagram_web":
        requests.get("http://thelogin.ru/data/internet/%s" % record.args["display_src"].replace("://", "/"))
        requests.get("http://thelogin.ru/data/internet/%s" % record.args["thumbnail_src"].replace("://", "/"))
