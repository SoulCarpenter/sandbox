import asyncio
import requests

from pyquery import PyQuery
from lxml.html import parse
from lxml.html import fromstring

host = 'https://news.ycombinator.com/'
page = 'show'
URL = host + page

def requ():
    response = requests.get(URL)
    open('testi.txt','wb').write(response.content)

def req_pyquery():
    data_html = open('testi.txt', 'r').read()
    obj = PyQuery(data_html)
    print (obj('head').text())
    print (obj('td').text())

def req_etree():
    info = parse('testi.txt').getroot()
    for x in info.cssselect('td'):
        print(x.text_content())

import urllib
def req_etree2():
    #content = urllib.urlopen(URL).read()
    content = open('testi.txt', 'r').read()
    doc = fromstring(content)
    doc.make_links_absolute(URL)
    print("DOC: " + doc.text_content())
    for x in doc.find_class('subtext'):
        print(x.text_content())

async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World! ' + URL)

#asyncio.run(main())
#req_pyquery()
#req_etree()
req_etree2()
