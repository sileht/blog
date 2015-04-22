
OUTPUT_PATH = "/var/www/blog.sileht.net/output/"
PLUGIN_PATHS = ['/var/www/blog.sileht.net/pelican-plugins']
THEME = "/var/www/blog.sileht.net/pelican-twitchy"

AUTHOR="Mehdi ABAAKOUK"

RELATIVE_URLS = True

PLUGINS = [
    'gravatar',
#    'better_code_samples',
    'better_figures_and_images',
#    'extract_toc'
]

RESPONSIVE_IMAGES = True
TYPOGRIFY = True

ARTICLE_URL = '{slug}'
ARTICLE_LANG_URL = '{slug}-{lang}'
PAGE_URL = 'pages/{slug}'
PAGE_LANG_URL = 'pages/{slug}-{lang}'

DELETE_OUTPUT_DIRECTORY = True

MARKUP = ('rst', 'md', 'mkd')
#MD_EXTENSIONS = ['markdown.extensions.extra']
#PDF_GENERATOR = True

SITENAME = "Sileht's Blog"
SITEURL = "http://blog.sileht.net"
AUTHOR = "Mehdi Abaakouk"

DEFAULT_METADATA = (('yeah', 'it is'),)
DEFAULT_CATEGORY = 'misc'
DISPLAY_PAGES_ON_MENU = True
STATIC_PATHS = ['images', 'static']

FEED_ATOM = 'feeds/atom.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

SOCIAL = (
    ('twitter', 'http://twitter.com/sileht'),
    ('github', 'http://github.com/sileht'),
    ('linkedin', 'http://fr.linkedin.com/pub/mehdi-abaakouk/24/9b0/27/'),
    ('ohloh','https://www.ohloh.net/accounts/sileht'),
    ('# irc:   sileht', ''),
    ('launchpad', 'https://launchpad.net/~sileht'),
)
GITHUB_ACTIVITY_FEED = 'http://github.com/sileht.atom'

TIMEZONE = "Europe/Paris"
FALLBACK_ON_FS_DATE = True
