# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import requests


def process(record):
    if record.application == "twitter":
        for media in record.args.get("media", []):
            if media["type"] == "photo":
                if "media_url" in media:
                    requests.get("http://thelogin.ru/data/internet/%s" % media["media_url"].replace("://", "/"))
                if "media_url_https" in media:
                    requests.get("http://thelogin.ru/data/internet/%s" % media["media_url_https"].replace("://", "/"))

        requests.get("http://thelogin.ru/data/internet/%s" % record.args["user"]["profile_image_url"].replace("://", "/"))

        if "retweeted_status" in record.args:
            requests.get("http://thelogin.ru/data/internet/%s" % record.args["retweeted_status"]["user"]["profile_image_url"].replace("://", "/"))
