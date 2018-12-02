
SITENAME = "Random things I work on"
SITESUBTITLE = "From Mehdi Abaakouk (sileht)"

SITENAME = "Mehdi Abaakouk (sileht)"
SITESUBTITLE = "Random things I work on"

SITEIMAGE = "/images/logo.png"
SITEURL = "https://sileht.net"
AUTHOR = "Mehdi Abaakouk"
TIMEZONE = "Europe/Paris"

ICONS = [
    ('twitter', 'http://twitter.com/sileht'),
    ('github', 'http://github.com/sileht'),
    ('linkedin', 'http://fr.linkedin.com/pub/mehdi-abaakouk/24/9b0/27/'),
    ('envelope', 'mailto:sileht@sileht.net'),
    ('key', 'https://keybase.io/sileht'),
]
LINKS = [
]

# STYLE
THEME = "/var/www/blog.sileht.net/pelican-twitchy"
THEME = "/var/www/blog.sileht.net/pelican-themes/alchemy/alchemy"

HIDE_AUTHORS = True
SUMMARY_MAX_LENGTH = 30
PYGMENTS_STYLE = "tango"

TYPOGRIFY = True
MARKUP = ('rst', 'md', 'mkd')

# PLUGINS
PLUGIN_PATHS = ['/var/www/blog.sileht.net/pelican-plugins']
PLUGINS = [
    'better_code_samples',
    'better_figures_and_images',
    'pelican-bootstrapify',
]
RESPONSIVE_IMAGES = True  # better_figures_and_images

BOOTSTRAPIFY = {
    'table': ['table', 'table-striped', 'table-hover'],
    'img': ['img-fluid'],
    'blockquote': ['blockquote'],
}

STATIC_PATHS = ['images', 'static']

ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
INDEX_SAVE_AS = 'blog.html'

# SETUP
LOAD_CONTENT_CACHE = False
OUTPUT_PATH = "/var/www/blog.sileht.net/output"
DELETE_OUTPUT_DIRECTORY = True

GOOGLE_ANALYTICS_UNIVERSAL = "UA-4618550-4"
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = "auto"
