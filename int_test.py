from bwikibot.api import Wiki
from bwikibot.path import config

wiki = Wiki()
wiki.session_login(config['endpoint'], config['login'], config['password'])

wiki.page('test').write('hello world', 'test')
