import xmltodict
import requests
import re
import sys
from bs4 import BeautifulSoup


BASE_URL = 'https://www.sec.gov'
RSS_URL = (
    '{}/cgi-bin/browse-edgar?action=getcompany'
    '&CIK={}&type={}&dateb=&owner=exclude'
    '&count={}&output=atom'
)


class Bunch(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class EdgarQuery(object):
    def __init__(self, sym, filing_type):
        self.sym = sym
        self.filing_type = filing_type
        self.raw_xml = dict()

    def get_rss_url(self, atom_count=500):
        url = RSS_URL.format(
            BASE_URL,
            self.sym,
            self.filing_type,
            atom_count
        )
        return url

    def parse_xml(self, xmltxt):
        d = xmltodict.parse(xmltxt)
        return d

    def get_rss(self, **kwargs):
        url = self.get_rss_url(**kwargs)
        res = requests.get(url)
        d = res.text
        rss = self.parse_xml(d)
        return rss

    def get_filing_dates(self, **kwargs):
        rss = self.get_rss(**kwargs)
        dates = []
        for x in rss['feed']['entry']:
            dates.append(x['content']['filing-date'])
        return dates

    def get_filing_url(self, tdate, **kwargs):
        rss = self.get_rss(**kwargs)
        for x in rss['feed']['entry']:
            c = x['content']
            d = c['filing-date']
            if d == tdate:
                return c['filing-href']
        return False

    def get_xbrl_url(self, link):
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

    def get_filing(self, tdate, **kwargs):
        filing_url = self.get_filing_url(
            tdate,
            **kwargs
        )
        xbrl_url = self.get_xbrl_url(filing_url)
        res = requests.get(xbrl_url)
        txt = res.text
        m = xmltodict.parse(txt)
        self.raw_xml = dict(m)
        return m
