import os
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
static_root = '/home/hua/static'
template_root = '/home/hua/uwsgi/blog/template'
request_root = '/blog'
app_root = '/home/hua/uwsgi/blog'
