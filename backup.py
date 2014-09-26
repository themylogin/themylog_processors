# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import re

from themylog.level import levels
from themylog.record import Record


def parse_amount(s):
    match = re.search("([0-9,]+) (RUR|USD)", s)
    return float(match.group(1).replace(",", ".")), match.group(2)


def process(record):
    if record.application == "backup":
        if record.logger == "root":
            if record.msg == "finish":
                if record.args["free"] < 25e9:
                    return Record(application="backup",
                                  logger="root",
                                  datetime=record.datetime,
                                  level=levels["warning"],
                                  msg="few_space_left",
                                  args={},
                                  explanation="Осталось мало места на диске для резервных копий")
