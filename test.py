#!/usr/bin/env python

from edgarquery import (
    EdgarQuery,
    us_gaap_factory
)
import json


args = [
    'aapl',
    '10-q',
    '2020-07-31'
]

def test_get_matches():
    eq = EdgarQuery(*args[0:2])
    link = eq.get_filing_url(args[2])
    assert link is not None
    m = eq.get_xbrl_url(link)
    assert len(m) > 0
    print(m)


def test_get_filing_keys():
    eq = EdgarQuery(*args[0:2])
    m = eq.get_filing(args[2])
    assert m is not None
    keys = list(m['xbrl'].keys())
    keys.sort()
    print(json.dumps({'data': keys}))


def test_get_us_gaap_keys():
    eq = EdgarQuery(*args[0:2])
    m = eq.get_filing(args[2])
    assert m is not None
    g = us_gaap_factory(m)
    keys = g.__dict__.keys()
    keys = sorted(keys)
    print(json.dumps({'data': list(keys)}))


def test_get_filing_assets():
    eq = EdgarQuery(*args[0:2])
    m = eq.get_filing(args[2])
    assert m is not None
    d = m['xbrl']
    assets = d['us-gaap:Assets']
    assert assets is not None
    for x in assets:
        print(x['@contextRef'])
        print(x['#text'])
    return True


# test_get_filing_assets()
# test_get_filing_keys()
test_get_us_gaap_keys()
