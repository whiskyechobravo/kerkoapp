import pathlib

from environs import Env
from flask_babel import lazy_gettext as _

from kerko.composer import Composer
from kerko.specs import CollectionFacetSpec

# pylint: disable=invalid-name

env = Env()
env.read_env()


@env.parser_for('collection_spec')
def collection_spec_parser(value):
    try:
        return [tuple(i.strip() for i in v.split(':', maxsplit=2)) for v in value.split(';')]
    except:  # noqa  # pylint: disable=bare-except
        return value


class Config:

    def __init__(self):
        app_dir = pathlib.Path(env.str('FLASK_APP')).parent.absolute()

        self.check_deprecated_options()

        self.SECRET_KEY = env.str('SECRET_KEY')
        self.EXPLAIN_TEMPLATE_LOADING = False
        self.PROXY_FIX = env.bool('PROXY_FIX', False)
        self.BABEL_DEFAULT_LOCALE = env.str('BABEL_DEFAULT_LOCALE', 'en')
        self.BABEL_DEFAULT_TIMEZONE = env.str('BABEL_DEFAULT_TIMEZONE', 'UTC')

        # Set Kerko variables from the environment. Some are deliberately omitted
        # because it would make more sense to set them in the app's Config object
        # directly.
        self.KERKO_TITLE = env.str('KERKO_TITLE', _("Kerko App"))
        self.KERKO_DATA_DIR = env.path('KERKO_DATA_DIR', str(app_dir / 'data' / 'kerko'))
        self.KERKO_WHOOSH_LANGUAGE = env.str('KERKO_WHOOSH_LANGUAGE', 'en')
        self.KERKO_ZOTERO_LOCALE = env.str('KERKO_ZOTERO_LOCALE', 'en-US')
        self.KERKO_ZOTERO_API_KEY = env.str('KERKO_ZOTERO_API_KEY')
        self.KERKO_ZOTERO_LIBRARY_ID = env.str('KERKO_ZOTERO_LIBRARY_ID')
        self.KERKO_ZOTERO_LIBRARY_TYPE = env.str('KERKO_ZOTERO_LIBRARY_TYPE')
        self.KERKO_ZOTERO_MAX_ATTEMPTS = env.int('KERKO_ZOTERO_MAX_ATTEMPTS', 10)
        self.KERKO_ZOTERO_WAIT = env.int('KERKO_ZOTERO_WAIT', 120)  # In seconds.
        self.KERKO_ZOTERO_BATCH_SIZE = env.int('KERKO_ZOTERO_BATCH_SIZE', 100)
        self.KERKO_PAGE_LEN = env.int('KERKO_PAGE_LEN', 20)
        self.KERKO_PAGER_LINKS = env.int('KERKO_PAGER_LINKS', 4)
        self.KERKO_CSL_STYLE = env.str('KERKO_CSL_STYLE', 'apa')
        self.KERKO_RESULTS_ABSTRACTS = env.bool('KERKO_RESULTS_ABSTRACTS', False)
        self.KERKO_RESULTS_ABSTRACTS_TOGGLER = env.bool('KERKO_RESULTS_ABSTRACTS_TOGGLER', True)
        self.KERKO_RESULTS_ATTACHMENT_LINKS = env.bool('KERKO_RESULTS_ATTACHMENT_LINKS', True)
        self.KERKO_RESULTS_URL_LINKS = env.bool('KERKO_RESULTS_URL_LINKS', True)
        self.KERKO_FACET_COLLAPSING = env.bool('KERKO_FACET_COLLAPSING', False)
        self.KERKO_FULLTEXT_SEARCH = env.bool('KERKO_FULLTEXT_SEARCH', True)
        self.KERKO_PRINT_ITEM_LINK = env.bool('KERKO_PRINT_ITEM_LINK', False)
        self.KERKO_PRINT_CITATIONS_LINK = env.bool('KERKO_PRINT_CITATIONS_LINK', False)
        self.KERKO_PRINT_CITATIONS_MAX_COUNT = env.int('KERKO_PRINT_CITATIONS_MAX_COUNT', 0)
        self.KERKO_DOWNLOAD_CITATIONS_LINK = env.bool('KERKO_DOWNLOAD_CITATIONS_LINK', True)
        self.KERKO_DOWNLOAD_CITATIONS_MAX_COUNT = env.int('KERKO_DOWNLOAD_CITATIONS_MAX_COUNT', 0)
        self.KERKO_DOWNLOAD_ATTACHMENT_NEW_WINDOW = env.bool(
            'KERKO_DOWNLOAD_ATTACHMENT_NEW_WINDOW', False
        )
        self.KERKO_RELATIONS_INITIAL_LIMIT = env.int('KERKO_RELATIONS_INITIAL_LIMIT', 5)
        self.KERKO_RELATIONS_LINKS = env.bool('KERKO_RELATIONS_LINKS', False)

        self.KERKO_COMPOSER = Composer(
            whoosh_language=self.KERKO_WHOOSH_LANGUAGE,
            exclude_default_scopes=env.list(
                'KERKOAPP_EXCLUDE_DEFAULT_SCOPES',
                [] if self.KERKO_FULLTEXT_SEARCH else ['fulltext', 'metadata']
                # The 'metadata' scope does the same as the 'all' scope when
                # full-text search is disabled, hence its removal in that case.
            ),
            exclude_default_fields=env.list(
                'KERKOAPP_EXCLUDE_DEFAULT_FIELDS',
                [] if self.KERKO_FULLTEXT_SEARCH else ['text_docs']
            ),
            exclude_default_facets=env.list('KERKOAPP_EXCLUDE_DEFAULT_FACETS', []),
            exclude_default_sorts=env.list('KERKOAPP_EXCLUDE_DEFAULT_SORTS', []),
            exclude_default_citation_formats=env.list(
                'KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS', []
            ),
            exclude_default_badges=env.list('KERKOAPP_EXCLUDE_DEFAULT_BADGES', []),
            default_item_include_re=env.str('KERKOAPP_ITEM_INCLUDE_RE', ''),
            default_item_exclude_re=env.str('KERKOAPP_ITEM_EXCLUDE_RE', ''),
            default_tag_include_re=env.str(
                'KERKOAPP_TAG_INCLUDE_RE', env.str('KERKOAPP_TAG_WHITELIST_RE', '')
            ),
            default_tag_exclude_re=env.str(
                'KERKOAPP_TAG_EXCLUDE_RE', env.str('KERKOAPP_TAG_BLACKLIST_RE', r'^_')
            ),
            default_child_include_re=env.str(
                'KERKOAPP_CHILD_INCLUDE_RE', env.str('KERKOAPP_CHILD_WHITELIST_RE', '')
            ),
            default_child_exclude_re=env.str(
                'KERKOAPP_CHILD_EXCLUDE_RE', env.str('KERKOAPP_CHILD_BLACKLIST_RE', r'^_')
            ),
            mime_types=env.list('KERKOAPP_MIME_TYPES', ['application/pdf']),
        )

        # Add collection facets.
        collection_spec = env.collection_spec('KERKOAPP_COLLECTION_FACETS', None)
        if collection_spec:
            for collection_key, weight, title in collection_spec:
                self.KERKO_COMPOSER.add_facet(
                    CollectionFacetSpec(
                        title=title,
                        weight=int(weight),
                        collection_key=collection_key,
                    )
                )

    @staticmethod
    def check_deprecated_options():
        if env.str('KERKOAPP_TAG_WHITELIST_RE', '') or env.str('KERKOAPP_TAG_BLACKLIST_RE', ''):
            # Deprecated after version 0.6.
            print(
                "WARNING: The 'KERKOAPP_TAG_WHITELIST_RE' and 'KERKOAPP_TAG_BLACKLIST_RE' "
                "environment variables are deprecated. Please use 'KERKOAPP_TAG_INCLUDE_RE' "
                "and 'KERKOAPP_TAG_EXCLUDE_RE' instead."
            )
        if env.str('KERKOAPP_CHILD_WHITELIST_RE', '') or env.str('KERKOAPP_CHILD_BLACKLIST_RE', ''):
            # Deprecated after version 0.6.
            print(
                "WARNING: The 'KERKOAPP_CHILD_WHITELIST_RE' and 'KERKOAPP_CHILD_BLACKLIST_RE' "
                "environment variables are deprecated. Please use 'KERKOAPP_CHILD_INCLUDE_RE' "
                "and 'KERKOAPP_CHILD_EXCLUDE_RE' instead."
            )
        if env.str('KERKOAPP_NOTE_WHITELIST_RE', '') or env.str('KERKOAPP_NOTE_BLACKLIST_RE', ''):
            # Deprecated after version 0.4.
            raise SystemExit(
                "ERROR: The 'KERKOAPP_NOTE_WHITELIST_RE' and 'KERKOAPP_NOTE_BLACKLIST_RE' "
                "environment variables are no longer supported. Please use "
                "'KERKOAPP_CHILD_INCLUDE_RE' and 'KERKOAPP_CHILD_EXCLUDE_RE' instead."
            )


class DevelopmentConfig(Config):

    def __init__(self):
        super().__init__()

        self.CONFIG = 'development'
        self.DEBUG = True
        self.KERKO_ZOTERO_START = env.int('KERKO_ZOTERO_START', 0)
        self.KERKO_ZOTERO_END = env.int('KERKO_ZOTERO_END', 0)
        self.LOGGING_LEVEL = env.str('LOGGING_LEVEL', 'DEBUG')


class ProductionConfig(Config):

    def __init__(self):
        super().__init__()

        self.CONFIG = 'production'
        self.DEBUG = False
        self.LOGGING_HANDLER = env.str('LOGGING_HANDLER', 'syslog')
        self.LOGGING_ADDRESS = env.str('LOGGING_ADDRESS', '/dev/log')
        self.LOGGING_LEVEL = env.str('LOGGING_LEVEL', 'WARNING')


CONFIGS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
