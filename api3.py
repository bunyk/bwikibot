# coding=utf-8

import json
from pprint import pprint
from itertools import islice
from time import sleep

import requests # pip install requests
import mwparserfromhell # pip install mwparserfromhell

endpoint = 'http://uk.wikipedia.org/w/api.php'

s = requests.Session()

def request(**kwargs):
    ''' Зробити запит до Wiki '''
    sleep(0.5) # почекати пів секунди, аби за надто активні запити не забанили IP
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
        eititle=name,
        list='embeddedin',
        eilimit='10',
        einamespace='0', # брати лише сторінки в основному просторі імен
    )
    cont = dict(embeddedin={})
    while cont:
        params.update(cont['embeddedin'])
        res = request(**params)
        for l in res['query']['embeddedin']:
            yield l['title']
        cont = res.get('query-continue')

def get_film_params(page_text):
    ''' Отримати словник з параметрами фільму з сторінки '''
    code = mwparserfromhell.parse(page_text)
    params = {}
    for template in code.filter_templates():
        get_value = lambda name: template.get(name).value.strip()
        if template.name.matches('Infobox film'):
            params['uk_title'] = get_value('українська назва')
            params['title'] = get_value('name')
            params['director'] = get_value('director')
            params['budget'] = get_value('budget')
        if template.name.matches('Фільм'):
            params['uk_title'] = get_value('українська назва')
            params['title'] = get_value('оригінальна назва')
            params['director'] = get_value('режисер')
            params['budget'] = get_value('бюджет')
    return params

if __name__ == '__main__':
    for page in islice(pages_that_use_template('Шаблон:Фільм'), 5): 
        for pv in get_film_params(get_page(page)).items():
            print('%s = %s' % pv)
        print()

