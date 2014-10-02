# coding=utf-8

import requests
import json
from pprint import pprint
from itertools import islice

endpoint = 'http://uk.wikipedia.org/w/api.php'

s = requests.Session()

def request(**kwargs):
    ''' Зробити запит до Wiki '''
    params = dict(format='json')
    params.update(kwargs)
    r = s.get(endpoint, params=params)
    return json.loads(r.text)

def get_page(name):
    ''' Отримати текст сторінки за іменем '''
    res = request(
        action='query',
        titles=name,
        prop='revisions',
        rvprop='content',
    )
    pages = res['query']['pages']
    page = list(pages.values())[0]['revisions'][0]['*']
    return page

def pages_that_use_template(name):
    ''' Згенерувати послідовність сторінок що використовують шаблон '''
    params = dict(
        action='query',
        bltitle=name,
        list='alltransclusions',
        atlimit='10',
        atnamespace='0', # брати лише сторінки в основному просторі імен
    )
    cont = dict(alltransclusions={})
    while cont:
        params.update(cont['alltransclusions'])
        res = request(**params)
        for l in res['query']['alltransclusions']:
            yield l['title']
        cont = res.get('query-continue')

if __name__ == '__main__':
    for page in islice(pages_that_use_template('Шаблон:Фільм'), 5): 
        print(repr(page))
        # print(get_page(page))

