# -*- coding=utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import operator
import re

from themylog.client import Retriever
from themylog.level import levels
from themylog.record import Record


def get_balance():
    return Retriever().retrieve((operator.eq, lambda k: k("application"), "alfa-bank"), 1)[0].args["balance"]


def parse_amount(s):
    match = re.search("([0-9.,]+) ([A-Z]{3})", s)

    amount = match.group(1)
    if "," in amount and "." in amount:
        amount = amount.replace(",", "", 1)
    amount = amount.replace(",", ".")
    amount = float(amount)

    currency = match.group(2)

    return amount, currency


def process(record):
    if record.application == "sms" and record.logger == "Alfa-Bank":
        if record.explanation.startswith("Uspeshnaja otmena operacii"):
            return None

        args = None
        if record.explanation.count("; ") >= 3:
            args = {}
            args["text"] = record.explanation

            card, operation, tail = args["text"].split("; ", 2)
            if operation in ["Oplata uslug", "Pokupka", "Vydacha nalichnyh"]:
                success, amount, balance, details, datetime_ = tail.split("; ")

                if success == "Uspeshno":
                    args["write_off"], args["write_off_currency"] = parse_amount(amount)

                    args["balance"] = parse_amount(balance)[0]

                    args["details"] = details
            elif operation in ["Postupleniye"]:
                amount, balance, datetime_ = tail.split("; ")

                args["charge"], args["charge_currency"] = parse_amount(amount)

                args["balance"] = parse_amount(balance)[0]                    
            else:
                raise Exception("Neither charge nor write-off match found in '%s'" % args["text"])
        elif "Spisanie so scheta" in record.explanation:
            args = {}
            args["text"] = record.explanation

            match = re.search("Spisanie so scheta (.+), poluchatel platezha (.+); (.+).", args["text"])
            if match:
                args["write_off"], args["write_off_currency"] = parse_amount(match.group(1))

                if args["write_off_currency"] != "RUR":
                    raise Exception("Non-RUR charges are not supported: %s" % args["text"])

                args["balance"] = get_balance() - args["write_off"]

                args["details"] = match.group(2)
            else:
                raise Exception("No charge match found in '%s'" % args["text"])

        if args is not None:
            return Record(application="alfa-bank",
                          logger="root",
                          datetime=record.datetime,
                          level=levels["info"],
                          msg=record.msg,
                          args=args,
                          explanation="")
