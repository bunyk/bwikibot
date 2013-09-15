import os

import appdirs

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

DATA_DIR = appdirs.user_data_dir('bwikibot')
ensure_dir(DATA_DIR)

def data_file(name):
    return os.path.join(DATA_DIR, name)

def here(name):
    return os.path.join(os.path.dirname(__file__), name)

RC_FILE = os.path.join(os.path.expanduser("~"), '.bwikibotrc')

def get_config():
    res = {}
    with open(RC_FILE) as f:
        code = compile(f.read(), RC_FILE, 'exec')
        exec(code, res)
    return res

config = get_config()

SESSION_FILE = data_file('cli.session')
SECONDARY_SESSION_FILE = data_file('cli_secondary.session')
