#!/usr/bin/env python

from edgarquery import EdgarQuery
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


test_get_filing_assets()
"""
[OrderedDict([('@contextRef', 'i06d107b9e8124e8f980ce20843670f50_I20200627'), ('@decimals', '-6'), ('@id', 'id3VybDovL2RvY3MudjEvZG9jOjg5NzA4NDI1MzYyZDQ4OTY5NTgwMzU1NGQ4NzY1MzJmL3NlYzo4OTcwODQyNTM2MmQ0ODk2OTU4MDM1NTRkODc2NTMyZl8yMi9mcmFnOmRlNjhmOWE2Y2RkMjQ0Y2NiNmYyNGMzNjNjZmIwMjdiL3RhYmxlOjg5NDBiMDA3NDg0ODQ4Yzk4MDVkOTA2YzU4NjVkMGFmL3RhYmxlcmFuZ2U6ODk0MGIwMDc0ODQ4NDhjOTgwNWQ5MDZjNTg2NWQwYWZfMTYtMS0xLTEtMA_02dc3a32-5087-46e6-8d93-f55885508753'), ('@unitRef', 'usd'), ('#text', '317344000000')]), OrderedDict([('@contextRef', 'i8d2e24f3acf240cfb5fb5e8abd2376b3_I20190928'), ('@decimals', '-6'), ('@id', 'id3VybDovL2RvY3MudjEvZG9jOjg5NzA4NDI1MzYyZDQ4OTY5NTgwMzU1NGQ4NzY1MzJmL3NlYzo4OTcwODQyNTM2MmQ0ODk2OTU4MDM1NTRkODc2NTMyZl8yMi9mcmFnOmRlNjhmOWE2Y2RkMjQ0Y2NiNmYyNGMzNjNjZmIwMjdiL3RhYmxlOjg5NDBiMDA3NDg0ODQ4Yzk4MDVkOTA2YzU4NjVkMGFmL3RhYmxlcmFuZ2U6ODk0MGIwMDc0ODQ4NDhjOTgwNWQ5MDZjNTg2NWQwYWZfMTYtMy0xLTEtMA_65e3b939-2a5b-4b76-ace0-38e492c68dd8'), ('@unitRef', 'usd'), ('#text', '338516000000')])]
"""
