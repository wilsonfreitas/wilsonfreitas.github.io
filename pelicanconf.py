#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Wilson Freitas'
# MAINQUOTE = u'And in the end, the love you take is equal to the love you make.'
MAINQUOTE = u'Data analysis is a mix of belief and evidence'
SITENAME = u'AboutWilson.net'
SITEURL = 'http://localhost:8000'
# SITEURL = 'http://blog.aboutwilson.net'

GOOGLE_ANALYTICS = True
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'pt'
DEFAULT_DATE_FORMAT = u'%Y-%m-%d'
DATE_FORMATS = {
    'pt': '%d/%m/%Y',
    'en': '%Y-%m-%d',
}

# ARTICLE_URL = 'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}/'
# ARTICLE_SAVE_AS = 'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}/index.html'
ARTICLE_URL = 'posts/{date:%Y}-{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}-{date:%m}/{slug}/index.html'
ARTICLE_LANG_URL = 'posts/{date:%Y}-{date:%m}/{slug}/'
ARTICLE_LANG_SAVE_AS = 'posts/{date:%Y}-{date:%m}/{slug}/index.html'
DEFAULT_PAGINATION = 5

MENUITEMS = [('archive',     'archives.html'),
             ('user',         'pages/about.html'),
             ('tags',         'tags.html')]

FEED_DOMAIN = SITEURL
FEED_ALL_RSS = 'feeds/rss.xml'
TAG_FEED_RSS = 'feeds/%s.rss.xml'

DISQUS_SITENAME = 'aboutwilson'
# GITHUB_URL = 'https://github.com/wilsonfreitas'

STATIC_PATHS = ['figure', 'datasets']

THEME = 'aboutwilson'

MARKUP = ('md', 'Rmd', 'rmd')

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ('lib/pelican-plugins', )

PLUGINS = ['sitemap', 'summary', 'liquid_tags.img',
    'liquid_tags.video', 'liquid_tags.include_code', 'liquid_tags.notebook',
    'liquid_tags.literal', 'rmd_reader', 'render_math']

# sitemap
SITEMAP = {
        'format': 'xml',
        'priorities': {
            'articles': 1.0,
            'indexes': 0.7,
            'pages': 0.5
        },
        'changefreqs': {
            'articles': 'monthly',
            'indexes': 'monthly',
            'pages': 'monthly'
        }
    }

# notebook
NOTEBOOK_DIR = ''
NOTEBOOK_HEADER_SAVED = True
EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100