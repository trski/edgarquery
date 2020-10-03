import xmltodict
import requests
import re
import sys
from bs4 import BeautifulSoup


BASE_URL = 'https://www.sec.gov'
RSS_URL = BASE_URL + '/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb=&owner=exclude&count={}&output=atom'


def get_rss_url(sym, filing_type, atom_count=500):
    url = RSS_URL.format(sym, filing_type, atom_count)
    return url


def parse_xml(xmltxt):
    d = xmltodict.parse(xmltxt)
    return d


def get_rss(sym, filing_type, **kwargs):
    url = get_rss_url(sym, filing_type, **kwargs)
    res = requests.get(url)
    d = res.text
    rss = parse_xml(d)
    return rss


def get_filing_dates(sym, filing_type, **kwargs):
    rss = get_rss(sym, filing_type, **kwargs)
    dates = []
    for x in rss['feed']['entry']:
        dates.append(x['content']['filing-date'])
    return dates


def get_filing_url(sym, filing_type, tdate, **kwargs):
    rss = get_rss(sym, filing_type, **kwargs)
    for x in rss['feed']['entry']:
        c = x['content']
        d = c['filing-date']
        if d == tdate:
            return c['filing-href']
    return False


def get_xbrl_url(link):
    d = requests.get(link)
    txt = d.text
    m = re.findall(
        r'<table.*?>(.*?)</table>',
        txt,
        flags=re.S | re.IGNORECASE
    )
    if len(m) == 0:
        return False
    found = False
    for x in m:
        n = '<root>{}</root>'.format(x)
        g = BeautifulSoup(n, 'html.parser')
        tds = g.find_all('td')
        for td in tds:
            if found:
                try:
                    href = td.a.attrs['href']
                    return BASE_URL + href
                except Exception as e:
                    sys.stderr.write(str(e))
                return None
            if 'XBRL INSTANCE DOCUMENT' in td.text:
                found = True
    return False


def get_filing(sym, filing_type, tdate, **kwargs):
    filing_url = get_filing_url(sym, filing_type, tdate, **kwargs)
    xbrl_url = get_xbrl_url(filing_url)
    res = requests.get(xbrl_url)
    txt = res.text
    m = xmltodict.parse(txt)
    return m
