import os
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
static_root = '/home/hua/static'
template_root = '/home/hua/xiaoyezi.org/template'
request_root = '/s'
