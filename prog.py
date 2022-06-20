import asyncio
import requests
import time

from lxml.html import parse
from lxml.html import fromstring
from lxml.cssselect import CSSSelector
import operator
import json

URL = 'https://news.ycombinator.com/'
page1 = 'news'
page2 = 'show'
page3 = 'ask'
DEBUG = False

async def get_page(p_url, p_name):
    print('Fetching page: ' + p_name)
    s = time.perf_counter()    
    await asyncio.sleep(1)
    response = requests.get(p_url + p_name)
    print('Fetch DONE: ' + p_name)
    f_name = p_name + '.txt'
    open(f_name, 'wb').write(response.content)
    delta = time.perf_counter() - s
    print(f"Page {f_name} saved in {delta:0.2f} seconds")

def collect_data(f_names):
    all_data = []
    for f_name in f_names:
        with open(f_name + '.txt') as f:
            tree = fromstring(f.read())

        sel_headlines = CSSSelector('.titlelink')
        sel_ranks = CSSSelector('.rank')
        sel_subtext = CSSSelector('.subtext')
        sel_points = CSSSelector('.score')
        sel_author = CSSSelector('.hnuser')
        sel_age = CSSSelector('.age > a')
        sel_ncom = CSSSelector('a:last-child')
        headlines = sel_headlines(tree)
        ranks = sel_ranks(tree)
        i = 0
        for item in sel_subtext(tree):
            t = {}
            t['points'] = 0 if len(sel_points(item)) == 0 else int(sel_points(item)[0].text.split()[0])
            t['title'] = headlines[i].text_content()
            t['rank'] = ranks[i].text_content()
            t['author'] = "No author" if len(sel_author(item)) == 0 else sel_author(item)[0].text
            t['age'] = sel_age(item)[0].text
            t['num_comments'] = sel_ncom(item)[-1].text.split()[0].replace('discuss','0')
            i+=1
            all_data.append(t)
    print('collect_data ENDS!')
    return all_data

def d_print(s):
    if DEBUG:
        print(s)

def print_json(d):
    d_print(json.dumps(d, indent=4))

def sort_list_by_dict_key(p_key, p_list):
    return sorted(p_list, key=operator.itemgetter(p_key), reverse=True)

def save_content_to_file(p_fname, p_list):
    print_json(p_list)
    with open(p_fname, 'w', encoding='utf-8') as fout:
        for i in p_list:
            line = ' '.join(str(e) for e in i.values())
            d_print(line)
            fout.write(line + "\n")

async def main():
    print('Main program starts ...')
    await asyncio.gather(
        get_page(URL, page2),
        get_page(URL, page3),
        get_page(URL, page1))
    files = [page1, page2, page3]
    data = collect_data(files)
    sorted_list = sort_list_by_dict_key('points', data)
    output_fname = 'outputfile.txt'
    save_content_to_file(output_fname, sorted_list)
    print(f"Fetched data saved to file: {output_fname}")

asyncio.run(main())
