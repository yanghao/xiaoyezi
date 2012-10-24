import os
import codecs
from webapp2 import RequestHandler, Response
from mako.template import Template
from markdown import markdown

from view.cache import CacheHandler
from config import mc
from config import static_root
from config import template_root
from config import request_root

def create_top_menu_list(filename, static_root=static_root):
    item_list = []
    with open(os.path.join(static_root, filename), 'r') as fd:
        for line in fd.readlines():
            line = line.strip()
            if line[0] == '#': # this is comment
                continue
            else: # this is an item
                item = line.split(' : ')
                if len(item) != 3:
                    item = ["Error", "Error", "Error"]
                item_list.append(item)
    return item_list

def create_left_menu_list(path, static_root=static_root):
    full_path = os.path.join(static_root, path)
    items = os.listdir(full_path)
    items.sort()
    item_list = []
    for item in items:
        if os.path.isdir(os.path.join(full_path, item)):
            continue # ignore folders
        elif item == "README":
            continue # ignore README for now
        else:
            item_list.append((item, item.split('.')[1]))
    return item_list

def load_markdown(category, filename, static_root):
    try:
        with codecs.open(os.path.join(static_root, category, filename), mode='r', encoding="utf8") as fd:
            text = fd.read()
    except IOError:
        text = "## Not Found\n### File: %s\n### category: %s\n### root: %s\n" % (filename, category, static_root)
    if text == '': # empty doc
        text = "# Empty Document"
    html = markdown(text, extensions=['codehilite(force_linenos=True)'])
    return html

class StaticReadme(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def fetch_get_request(self, folder=''):
        t = Template(filename=os.path.join(template_root, 'base.html'))
        menu_list = create_top_menu_list('README', static_root)
        leftmenu_list = create_left_menu_list('home', static_root)
        category = 'home'
        body = load_markdown(category, 'README', static_root)
        return t.render(menu_list=menu_list, category=category, leftmenu_list=leftmenu_list, request_root=request_root, body=body)

class StaticFolder(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def fetch_get_request(self, folder=''):
        t = Template(filename=os.path.join(template_root, 'base.html'))
        menu_list = create_top_menu_list('README', static_root)
        leftmenu_list = create_left_menu_list(folder, static_root)
        category = folder
        body = load_markdown(category, 'README', static_root)
        return t.render(menu_list=menu_list, category=category, leftmenu_list=leftmenu_list, request_root=request_root, body=body)

class StaticMarkdown(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def fetch_get_request(self, folder='', filename=''):
        t = Template(filename=os.path.join(template_root, 'base.html'))
        menu_list = create_top_menu_list('README', static_root)
        leftmenu_list = create_left_menu_list(folder, static_root)
        category = folder
        body = load_markdown(category, filename, static_root)
        return t.render(menu_list=menu_list, category=category, leftmenu_list=leftmenu_list, request_root=request_root, body=body)
