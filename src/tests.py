'''TODO: まともなテストを書く'''

import time
import unittest

import model
import admonitor
import commands


class ConditionTest(unittest.TestCase):
    vuln = admonitor.VulnInfo({
        'title': 'TITLE',
        'summary': 'SUMMARY',
        'sec_cpe': {
            'vendor': 'VENDOR',
            'product': 'PRODUCT'
        },
        'sec_cvss': {
            'severity': 'SEVERITY',
            'score': '8'
        },
        'link': 'LINK'
    })

    def test_hit_vendor(self):
        condition = model.Condition()
        condition.channel = ''
        condition.vendor = 'VENDOR'
        condition.product = ''
        condition.cvss = 0
    
        hit = condition.hit(self.vuln)
        self.assertTrue(hit)

        condition = model.Condition()
        condition.channel = ''
        condition.vendor = 'HOGE'
        condition.product = ''
        condition.cvss = 0

        hit = condition.hit(self.vuln)
        self.assertFalse(hit)

    def test_hit_product(self):
        condition = model.Condition()
        condition.channel = ''
        condition.vendor = ''
        condition.product = 'PRODUCT'
        condition.cvss = 0
    
        hit = condition.hit(self.vuln)
        self.assertTrue(hit)

        condition = model.Condition()
        condition.channel = ''
        condition.vendor = ''
        condition.product = 'HOGE'
        condition.cvss = 0

        hit = condition.hit(self.vuln)
        self.assertFalse(hit)

    def test_hit_cvss(self):
        condition = model.Condition()
        condition.channel = ''
        condition.vendor = ''
        condition.product = ''
        condition.cvss = 7
    
        hit = condition.hit(self.vuln)
        self.assertTrue(hit)

        condition = model.Condition()
        condition.channel = ''
        condition.vendor = ''
        condition.product = ''
        condition.cvss = 10

        hit = condition.hit(self.vuln)
        self.assertFalse(hit)

    def test_str(self):
        # TODO
        condition = model.Condition()
        condition.id = '1'
        condition.channel = 'CHANNEL'
        condition.vendor = 'VENDOR'
        condition.product = 'PRODUCT'
        condition.cvss = 7

        expect = '''ベンダー名：VENDOR を含む
製品名：PRODUCT を含む
CVSS：7 以上\n'''

        actual = str(condition)
        # self.assertEqual(expect, actual)


class VulnInfoTest(unittest.TestCase):
    vuln = admonitor.VulnInfo({
        'title': 'TITLE',
        'summary': 'SUMMARY',
        'sec_cpe': {
            'vendor': 'VENDOR',
            'product': 'PRODUCT'
        },
        'sec_cvss': {
            'severity': 'SEVERITY',
            'score': '8'
        },
        'link': 'LINK'
    })
    
    def test_str(self):
        # TODO

        expect = '''*TITLE*
SUMMARY

*製品情報*
ベンダー名：VENDOR
製品名：PRODUCT

*緊急度*
緊急度：SEVERITY
CVSS：8.0

LINK
'''

        actual = str(self.vuln)
        # self.assertEqual(expect, actual)

class RSSTest(unittest.TestCase):
    feeds = {
        'bozo': 0,
 'encoding': 'utf-8',
 'entries': [{'id': 'https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-YYYY.html',
              'link': 'https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-YYYY.html',
              'links': [{'href': 'https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-YYYY.html',
                         'rel': 'alternate',
                         'type': 'text/html'}],
              'published': '9999-12-31T23:59+09:00',
              'published_parsed': '',
              'sec_cpe': {'product': '製品',
                          'vendor': 'プロダクト',
                          'version': '2.2'},
              'sec_cvss': {'score': '9.8',
                           'severity': 'Critical',
                           'type': 'base',
                           'vector': 'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
                           'version': '3.0'},
              'sec_identifier': 'JVNDB-2019-324',
              'sec_references': {'id': 'CWE-918',
                                 'title': 'タイトル'},
              'summary': 'サマリー',
              'summary_detail': {'base': 'http://localhost:8000/main.rdf',
                                 'language': 'ja',
                                 'type': 'text/html',
                                 'value': 'サマリー'},
              'title': 'タイトル',
              'title_detail': {'base': 'http://localhost:8000/main.rdf',
                               'language': 'ja',
                               'type': 'text/plain',
                               'value': 'タイトル'},
              'updated': '9999-12-31T23:59+09:00',
              'updated_parsed': ''},
              {
              'id': 'https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-XXXX.html',
              'link': 'https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-XXXX.html',
              'links': [{'href': 'https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-XXXX.html',
                         'rel': 'alternate',
                         'type': 'text/html'}],
              'published': '1970-01-01T00:00+09:00',
              'published_parsed': '',
              'sec_cpe': {'product': '製品',
                          'vendor': 'プロダクト',
                          'version': '2.2'},
              'sec_cvss': {'score': '9.8',
                           'severity': 'Critical',
                           'type': 'base',
                           'vector': 'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
                           'version': '3.0'},
              'sec_identifier': 'JVNDB-2019-324',
              'sec_references': {'id': 'CWE-918',
                                 'title': 'タイトル'},
              'summary': 'サマリー',
              'summary_detail': {'base': 'http://localhost:8000/main.rdf',
                                 'language': 'ja',
                                 'type': 'text/html',
                                 'value': 'サマリー'},
              'title': 'タイトル',
              'title_detail': {'base': 'http://localhost:8000/main.rdf',
                               'language': 'ja',
                               'type': 'text/plain',
                               'value': 'タイトル'},
              'updated': '1970-01-01T00:00+09:00',
              'updated_parsed': ''}
              
            ]}

    def test_split_updated(self):
        rss = admonitor.VulnInfoRSS()
        vulns = rss.split_updated(self.feeds)

        for vuln in vulns:
            vuln = admonitor.VulnInfo(vuln)
            self.assertTrue('https://jvndb.jvn.jp/ja/contents/2019/JVNDB-2019-XXXX.html', vuln.link)


class CommandTest(unittest.TestCase):
    cmd = commands.Command('vendor: VENDOR, cvss: 10, product: PRODUCT')
    
    def test_init(self):
        self.assertEqual('PRODUCT', self.cmd.product)
        self.assertEqual('VENDOR', self.cmd.vendor)
        self.assertEqual(10.0, self.cmd.cvss)

    def test_generate_condition(self):
        condition = self.cmd.generate_condition('CHANNEL')

        self.assertEqual('CHANNEL', condition.channel)
        self.assertEqual('VENDOR', condition.vendor)
        self.assertEqual('PRODUCT', condition.product)
        self.assertEqual(10.0, condition.cvss)


if __name__ == "__main__":
    unittest.main()