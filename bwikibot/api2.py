
import requests
import json
from pprint import pprint
import time

from bwikibot.path import config

LIST_LIMIT = 400

class Wiki(object):
    def __init__(self, endpoint=None, throttle=1):
        ''' Create wiki client for given endpoint addres.  '''
        self._tokens = {}
        self.endpoint = endpoint
        self.throttle = throttle

        self.session = requests.Session()

        if endpoint:
            self.get_namespaces()

    def get_namespaces(self):
        ''' Init two maps for namespaces:
        namespaces_names: from id to localised name 
        namespaces_ids: from canonical name to id
        '''
        # TODO: refactor to some class like two way dict
        res = self.query(
            meta='siteinfo',
            siprop='namespaces',
        )
        self.namespaces_names = {}
        self.namespaces_ids = {}
        for ns in res['namespaces'].values():
            self.namespaces_names[ns['id']] = ns['*']
            self.namespaces_ids[ns.get('canonical')] = ns['id']

        self.init_namespaces()

    def init_namespaces(self):
        ''' Set some constants '''
        def ns_name(canonical):
            return self.namespaces_names[self.namespaces_ids[canonical]]

        self.USER_NS_NAME = ns_name('User')
        self.USER_TALK_NS_NAME = ns_name('User talk')
        self.CATEGORY_NS_NAME = ns_name('Category')
        self.FILE_NS_NAME = ns_name('File')

    def get_cookies_dict(self):
        # http://stackoverflow.com/a/13031628/816449
        return requests.utils.dict_from_cookiejar(
            self.sessioncookies
        )

    def set_cookies_dict(self, d):
        self.session = requests.session(
            cookies=requests.utils.cookiejar_from_dict(d)
        )

    def do_request(self, method, **params):
        if self.throttle:
            time.sleep(self.throttle)

        p = dict(format='json')
        p.update(params)

        r = getattr(self.session, method)(self.endpoint, params=p)
        return json.loads(r.text)

    def post(self, **params):
        return self.do_request('post', **params)

    def get(self, **params):
        return self.do_request('get', **params)

    def login(self, login, password):
        self.user = login

        r = self.post(
            action='login',
            lgname=login,
            lgpassword=password,
        )
        res = r['login']
        if res['result'] == 'NeedToken':
            token = res['token']
            self.post(
                action='login',
                lgname=login,
                lgpassword=password,
                lgtoken=token,
            )

    def query(self, **params):
        ''' Get query to the API. '''
        params['action'] = 'query'
        content = self.get(**params)
        return content['query']

    def query_cont(self, **params):
        ''' Get query to the API for lists.

        Returns pair of responce and continue query params.
        '''
        params['action'] = 'query'
        content = self.get(**params)
        return content['query'], content.get('query-continue')

    def get_pages(self,
        from_name=None, to_name=None,
        prefix=None, prop=None,
        namespace=None
    ):
        q = {
            'list': 'allpages',
            'aplimit': LIST_LIMIT,
        }
        if from_name:
            q['apfrom'] = from_name
        if to_name:
            q['apto'] = to_name
        if prefix:
            q['apprefix'] = prefix
        if namespace:
            q['apnamespace'] = namespace

        res, cont = self.query_cont(**q)
        for page in res['allpages']:
            yield Page(self, page['title'])

        while cont:
            q.update(cont['allpages'])
            res, cont = self.query_cont(**q)
            for page in res['allpages']:
                yield Page(self, page['title'])

    def page(self, title):
        return Page(self, title)

    def __str__(self):
        return 'Wiki("%s")' % self.endpoint

class Page(object):
    def __init__(self, wiki, title):
        self.wiki = wiki
        self.title = title
        self.pageid = None
        self.missing = None
        self.text = None

    def read(self):
        ''' Returns page text, and remembers page meta info, 
        such as namespace, normalized title, is page missing,
        and page id.
        '''
        if self.text:
            return self.text
        res = self.wiki.query(
            prop='revisions',
            rvprop='content',
            titles=self.title,
        )
        page = list(res['pages'].values())[0]
        self.namespace = page['ns']
        self.title = page['title']
        if 'missing' in page:
            self.missing = True
            return None
        else:
            self.missing = False
            self.pageid = page['pageid']
        self.text = page['revisions'][0]['*']
        return self.text

    def __str__(self):
        return '%s.page("%s")' % (self.wiki, self.title)
