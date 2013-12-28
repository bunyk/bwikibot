# coding=utf-8
import requests
import json
from pprint import pprint

from bwikibot.path import config
import re

endpoint = config['endpoint']
login = config['login']
password = config['password']

s = requests.Session()

def get_page():
    r = s.get(endpoint, params=dict(
        format='json',
        action='query',
        titles='Ленін Володимир Ілліч',
        prop='revisions',
        rvprop='content',
    ))
    pages = json.loads(r.text)['query']['pages']
    page = list(pages.values())[0]['revisions'][0]['*']
    lines = page.splitlines()
    for line in lines:
        if 'зображення' in line:
            print(line)

def write_page():
    r = s.post(endpoint, params=dict(
        format='json',
        action='login',
        lgname=login,
        lgpassword=password,
    ))
    res = json.loads(r.text)['login']
    if res['result'] == 'NeedToken':
        token = res['token']
        r = s.post(endpoint, params=dict(
            format='json',
            action='login',
            lgname=login,
            lgpassword=password,
            lgtoken=token,
        ))
    r = s.get(endpoint, params=dict(
        format='json',
        action='query',
        prop='info|revisions',
        intoken='edit',
        titles='test'
    ))
    res = json.loads(r.text)['query']['pages']
    edittoken = next(iter(res.values()))['edittoken']
    r = s.post(endpoint, params=dict(
        format='json',
        action='edit',
        title='test',
        summary='test',
        text='hello world 2',
        token=edittoken
    ))
    pprint(json.loads(r.text))


if __name__ == '__main__':
    from bwikibot.api2 import Wiki
    wiki = Wiki(endpoint)
    wiki.login(login, password)
    print(wiki.page('Євромайдан').read())
