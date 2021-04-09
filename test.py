#!/usr/bin/env python

from edgarquery import (
    EdgarQuery,
    us_gaap_factory
)
import json


args = [
    'AAPL',
    '10-q',
    '2020-07-31'
]

def test_get_matches():
    ed = EdgarQuery(*args[0:2])
    link = ed.get_filing_url(args[2])
    assert link is not None
    m = ed.get_xbrl_url(link)
    assert len(m) > 0
    print(m)


def test_get_filing_keys():
    ed = EdgarQuery(*args[0:2])
    m = ed.get_filing(args[2])
    assert m is not None
    keys = list(m['xbrl'].keys())
    keys.sort()
    print(json.dumps({'data': keys}))


def test_get_us_gaap_keys():
    ed = EdgarQuery(*args[0:2])
    m = ed.get_filing(args[2])
    assert m is not None
    g = us_gaap_factory(m)
    keys = g.__dict__.keys()
    keys = sorted(keys)
    print(json.dumps({'data': list(keys)}))


def test_get_filing_assets():
    ed = EdgarQuery(*args[0:2])
    m = ed.get_filing(args[2])
    assert m is not None
    d = m['xbrl']
    assets = d['us-gaap:Assets']
    assert assets is not None
    for x in assets:
        print(x['@contextRef'])
        print(x['#text'])
    return True


def test_get_filing():
    ed = EdgarQuery(*args[0:2])
    dates = ed.get_filing_dates()
    t = ed.get_filing(dates[0])
    assert t is not None
    return True


test_get_filing()
