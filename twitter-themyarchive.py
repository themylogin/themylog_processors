# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import requests


def process(record):
    if record.application == "twitter":
        urls = record.args.get("urls", [])
        if isinstance(urls, dict):
            urls = urls.values()
        else:
            urls = [url["expanded_url"] for url in urls]

        for url in urls:
            requests.post("http://archive.thelogin.ru/url", json={"url": url}).json()
