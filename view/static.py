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
from config import app_root
from config import template_lookup

class StaticBlog(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def create_left_menu_list(self, lang, path, static_root=static_root):
        full_path = os.path.join(static_root, lang, path)
        items = os.listdir(full_path)
        items.sort()
        item_list = []
        for item in items:
            if os.path.isdir(os.path.join(full_path, item)):
                continue # ignore folders
            elif item == "README":
                continue # ignore README for now
            elif item[0] == '.':
                continue # ignore vim cache files
            else:
                item_list.append((item, item.split('.')[1]))
        return item_list

    def create_top_menu_list(self, lang='en', filename='', static_root=static_root):
        item_list = []
        with codecs.open(os.path.join(static_root, lang, filename), 'r', encoding='utf8') as fd:
            for line in fd.readlines():
                line = line.strip()
                if line[0] == '#': # this is comment
                    continue
                else: # this is an item
                    item = line.split(' : ')
                    if len(item) != 2:
                        item = ["Error", "Error"]
                    item_list.append(item)
        return item_list

    def load_markdown(self, lang, category, filename, static_root):
        try:
            with codecs.open(os.path.join(static_root, lang, category, filename), mode='r', encoding="utf8") as fd:
                text = fd.read()
        except IOError:
            text = "## Not Found\n### File: %s\n### category: %s\n### root: %s\n" % (filename, category, static_root)
        if text == '': # empty doc
            text = "# Empty Document"
        html = markdown(text, extensions=['codehilite(force_linenos=True)'])
        return html

    def fetch_get_request(self, lang='', folder='', filename=''):
        env = {'request_root':request_root}
        if lang == '': # /blog/
            t = Template(filename=os.path.join(template_root, 'front.html'), lookup=template_lookup)
            return t.render(**env)
        else:
            t = Template(filename=os.path.join(template_root, 'base.html'), lookup=template_lookup)
            menu_list = self.create_top_menu_list(lang, 'README', static_root)
            leftmenu_list = self.create_left_menu_list(lang, folder, static_root)
            env['menu_list'] = menu_list
            env['leftmenu_list'] = leftmenu_list
            env['lang'] = lang
            if folder == '': # /blog/lang/
                category = ''
                env['category'] = category
                body = ''
                env['body'] = body
                return t.render(**env)
            else:
                env['category'] = folder
                category = folder
                if filename == '':  # /blog/lang/folder
                    body = self.load_markdown(lang, category, 'README', static_root)
                    env['body'] = body
                    return t.render(**env)
                else: # /blog/lang/folder/article
                    body = self.load_markdown(lang, category, filename, static_root)
                    env['body'] = body
                    return t.render(**env)
        return "req: %s, lang: %s, folder: %s, filename: %s" % (self.request.uri, lang, folder, filename)
