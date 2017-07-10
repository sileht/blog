
SITENAME = "Random thing I work on"
SITESUBTITLE = "From Mehdi Abaakouk (sileht)"
SITEIMAGE = "/images/logo.png"
SITEURL = "https://blog.sileht.net"
AUTHOR = "Mehdi Abaakouk"
TIMEZONE = "Europe/Paris"

ICONS = [
    ('twitter', 'http://twitter.com/sileht'),
    ('github', 'http://github.com/sileht'),
    ('linkedin', 'http://fr.linkedin.com/pub/mehdi-abaakouk/24/9b0/27/'),
    ('envelope', 'mailto:sileht@sileht.net'),
    ('key', 'https://keybase.io/sileht'),
]

# STYLE
THEME = "/var/www/blog.sileht.net/pelican-twitchy"
THEME = "/var/www/blog.sileht.net/pelican-themes/alchemy/alchemy"

HIDE_AUTHORS = True
SUMMARY_MAX_LENGTH = 30
RECENT_POST_COUNT = 10
# BOOTSTRAP_THEME = "sandstone"
PYGMENTS_STYLE = "tango"
DISPLAY_RECENT_POSTS_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_TAGS_ON_MENU = True

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

# SETUP
LOAD_CONTENT_CACHE = False
OUTPUT_PATH = "/var/www/blog.sileht.net/output/dev"
DELETE_OUTPUT_DIRECTORY = True

GOOGLE_ANALYTICS_UNIVERSAL = "UA-4618550-4"
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = "auto"
