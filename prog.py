import asyncio
import requests
import time

from lxml.html import parse
from lxml.html import fromstring
from lxml.cssselect import CSSSelector

URL = 'https://news.ycombinator.com/'
page1 = 'news'
page2 = 'show'
page3 = 'ask'

async def get_page(p_url, p_name):
#def get_page(p_url, p_name):
    print('Fetching page: ' + p_name)
    print('DONE -DEBUGGING')
    return 0

    s = time.perf_counter()    
    #response = requests.get(p_url + p_name)
    #try:
    #    response = asyncio.wait_for(requests.get(p_url + p_name), timeout=200.0)
    #except asyncio.TimeoutError:
    #    print(f"Timeout! {p_name}")
    await asyncio.sleep(1)
    response = requests.get(p_url + p_name)
    print('Fetch DONE: ' + p_name)
    f_name = p_name + '.txt'
    open(f_name, 'wb').write(response.content)
    delta = time.perf_counter() - s
    print(f"Page {f_name} saved in {delta:0.2f} seconds")
    #return response.content

def req_etree():
    info = parse('testi.txt').getroot()
    for x in info.cssselect('td'):
        print(x.text_content())

import urllib
def req_etree2():
    #content = urllib.urlopen(URL).read()
    content = open('testi.txt', 'r').read()
    doc = fromstring(content)
    #doc.make_links_absolute(URL)
    print("DOC: " + doc.text_content())
    for x in doc.find_class('subtext'):
        print(x.text_content())

def collect_data(f_names):
    for f_name in f_names:
        content = open(f_name + '.txt', 'r').read()
        tree = fromstring(content)
        #print('TREE: ' + tree.text_content())
        ranks = tree.xpath('//span[@class="rank"]/text()')
        print('RANKS: ' + str(ranks))
        sel_headlines = CSSSelector('.titlelink')
        sel_ranks = CSSSelector('.rank')
        sel_subtext = CSSSelector('.subtext')
        sel_points = CSSSelector('.score')
        sel_author = CSSSelector('.hnuser')
        sel_age = CSSSelector('.age > a')
        sel_ncom = CSSSelector('a:last-child')
        #[e.get('id') for e in sel(tree)]
        print('SEL PATH: ' + str(sel_headlines.path))
        print('OUTPUT ITEMS')
        headlines = sel_headlines(tree)
        ranks = sel_ranks(tree)
        i = 0
        for item in sel_subtext(tree):
            t = {}
            print('TITLE: ' + str(headlines[i].text_content()) + ' ITEM: ' + str(item.text_content()))
            t['title'] = headlines[i].text_content()
            t['rank'] = ranks[i].text_content()
            t['points'] = "0 points" if len(sel_points(item)) == 0 else sel_points(item)[0].text
            t['author'] = "No author" if len(sel_author(item)) == 0 else sel_author(item)[0].text
            t['age'] = sel_age(item)[0].text
            t['num_comments'] = sel_ncom(item)[-1].text.split()[0]
            print('T: ' + str(t)) 
            i+=1
    print('collect_data ENDS!')

async def main():
    print('Hello ...')
    await asyncio.gather(
        get_page(URL, page2),
        get_page(URL, page3),
        get_page(URL, page1))
    #task1 = asyncio.create_task(get_page(URL, page1))
    #task2 = asyncio.create_task(get_page(URL, page2))
    #task3 = asyncio.create_task(get_page(URL, page3))
    #done, pending = await asyncio.wait(task)
    #await asyncio.gather(
    #    asyncio.to_thread(task1),
    #    asyncio.to_thread(task2),
    #    asyncio.to_thread(task3))
    #files = [page1, page2, page3]
    files = [page1]
    collect_data(files)
    print('... World! ' + URL)

asyncio.run(main())
#req_etree()

