# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import requests


def process(record):
    if record.application == "twitter":
        for url in record.args.get("urls", {}).values():
            requests.post("http://archive.thelogin.ru/url", json={"url": url}).json()
