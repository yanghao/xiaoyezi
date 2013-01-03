import os
import logging
import codecs
from webapp2 import RequestHandler, Response
from mako.template import Template
from markdown import markdown
from time import strftime
from time import localtime
from time import time

from view.cache import CacheHandler
from config import mc
from config import static_root
from config import template_root
from config import request_root
from config import app_root
from config import template_lookup

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
NUM_TEXT = 7

class StaticBlog(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def create_left_menu_list(self, lang, path, static_root=static_root):
        full_path = os.path.join(static_root, lang, path)
        items = os.listdir(full_path)
        items.sort()
        items.reverse()
        item_list = []
        for item in items:
            item = item.decode('utf-8')
            if os.path.isdir(os.path.join(full_path, item)):
                continue # ignore folders
            elif item == "README":
                continue # ignore README for now
            elif item[0] == '.':
                continue # ignore vim cache files
            else:
                item_s1, item_s2 = item.split('.')
                unicode_num = 0
                ascii_num = 0
                n = 0
                tmp = ''
                for i in item_s2:
                    if ord(i) > 255:
                        unicode_num += 1
                    else:
                        ascii_num += 1
                    n += 1
                    if (unicode_num + (ascii_num/2.0)) >= NUM_TEXT:
                        break
                if n < len(item_s2):
                    tmp = '..'
                item_list.append([item, item_s2, item_s2[0:n]+tmp, 'leftmenu_normal'])
        return item_list

    def create_top_menu_list(self, lang='en', filename='', static_root=static_root):
        item_list = []
        with codecs.open(os.path.join(static_root, lang, filename), 'r', encoding='utf8') as fd:
            for line in fd.readlines():
                line = line.strip()
                if line[0] == '#': # this is comment
                    continue
                else: # this is an item
                    item = list(line.split(' : '))
                    if len(item) != 2:
                        item = ["Error", "Error"]
                    item.append('menuitem')
                    item_list.append(item)
        return item_list

    def load_markdown(self, lang, category, filename, static_root):
        file_path = os.path.join(static_root, lang, category, filename)
        update_time = ''
        try:
            with codecs.open(file_path, mode='r', encoding="utf8") as fd:
                text = fd.read()
            update_time = strftime(TIME_FORMAT, localtime(os.path.getmtime(file_path)))
        except IOError:
            text = "## Not Found\n### File: %s\n### category: %s\n### root: %s\n" % (filename, category, static_root)
        if text == '': # empty doc
            text = "# Empty Document"
        html = markdown(text, extensions=['codehilite(force_linenos=True)'])
        return html, update_time

    def fetch_get_request(self, lang='', folder='', filename=''):
        start_time = time()
        env = {'request_root':request_root, 'update_time':strftime(TIME_FORMAT)}
        if lang == '': # /blog/
            t = Template(filename=os.path.join(template_root, 'front.html'), lookup=template_lookup)
            env['serve_time'] = '%.6f' % (time() - start_time)
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
            else:
                env['category'] = folder
                category = folder
                for item in menu_list:
                    if item[0] == folder:
                        item[2] = 'menuitem_now'
                if filename == '':  # /blog/lang/folder
                    body,update_time = self.load_markdown(lang, category, 'README', static_root)
                else: # /blog/lang/folder/article
                    for item in leftmenu_list:
                        if item[0] == filename.decode('utf-8'):
                            item[3] = 'leftmenu_now'
                    body,update_time = self.load_markdown(lang, category, filename, static_root)
                env['update_time'] = update_time
            env['body'] = body
            env['serve_time'] = '%.6f' % (time() - start_time)
            return t.render(**env)
        return "req: %s, lang: %s, folder: %s, filename: %s" % (self.request.uri, lang, folder, filename)
