import requests
import json
from pprint import pprint

from bwikibot.path import config

endpoint = config['endpoint']
login = config['login']
password = config['password']

s = requests.Session()

def get_page():
    r = s.get(endpoint, params=dict(
        format='json',
        action='query',
        titles='Git',
        prop='revisions',
        rvprop='content',
    ))
    pprint(json.loads(r.text))

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
    write_page()
