import logging
import pathlib

from environs import Env
from flask_babelex import lazy_gettext as _

from kerko.composer import Composer
from kerko.specs import CollectionFacetSpec

env = Env()  # pylint: disable=invalid-name
env.read_env()


@env.parser_for('collection_spec')
def collection_spec_parser(value):
    try:
        return [tuple(i.strip() for i in v.split(':', maxsplit=2)) for v in value.split(';')]
    except:  # noqa  # pylint: disable=bare-except
        return value


class Config():
    app_dir = pathlib.Path(env.str('FLASK_APP')).parent.absolute()

    SECRET_KEY = env.str('SECRET_KEY')
    EXPLAIN_TEMPLATE_LOADING = False
    PROXY_FIX = env.bool('PROXY_FIX', False)
    BABEL_DEFAULT_LOCALE = env.str('BABEL_DEFAULT_LOCALE', 'en')

    # Set Kerko variables from the environment. Some are deliberately omitted
    # because it would make more sense to set them in the app's Config object
    # directly.
    KERKO_TITLE = env.str('KERKO_TITLE', _("Kerko App"))
    KERKO_DATA_DIR = env.path('KERKO_DATA_DIR', str(app_dir / 'data' / 'kerko'))
    KERKO_WHOOSH_LANGUAGE = env.str('KERKO_WHOOSH_LANGUAGE', 'en')
    KERKO_ZOTERO_LOCALE = env.str('KERKO_ZOTERO_LOCALE', 'en-US')
    KERKO_ZOTERO_API_KEY = env.str('KERKO_ZOTERO_API_KEY')
    KERKO_ZOTERO_LIBRARY_ID = env.str('KERKO_ZOTERO_LIBRARY_ID')
    KERKO_ZOTERO_LIBRARY_TYPE = env.str('KERKO_ZOTERO_LIBRARY_TYPE')
    KERKO_ZOTERO_MAX_ATTEMPTS = env.int('KERKO_ZOTERO_MAX_ATTEMPTS', 10)
    KERKO_ZOTERO_WAIT = env.int('KERKO_ZOTERO_WAIT', 120)  # In seconds.
    KERKO_ZOTERO_BATCH_SIZE = env.int('KERKO_ZOTERO_BATCH_SIZE', 100)
    KERKO_PAGE_LEN = env.int('KERKO_PAGE_LEN', 20)
    KERKO_PAGER_LINKS = env.int('KERKO_PAGER_LINKS', 4)
    KERKO_CSL_STYLE = env.str('KERKO_CSL_STYLE', 'apa')
    KERKO_RESULTS_ABSTRACT = env.bool('KERKO_RESULTS_ABSTRACT', False)
    KERKO_FACET_COLLAPSING = env.bool('KERKO_FACET_COLLAPSING', False)
    KERKO_PRINT_ITEM_LINK = env.bool('KERKO_PRINT_ITEM_LINK', False)
    KERKO_PRINT_CITATIONS_LINK = env.bool('KERKO_PRINT_CITATIONS_LINK', False)
    KERKO_PRINT_CITATIONS_MAX_COUNT = env.int('KERKO_PRINT_CITATIONS_MAX_COUNT', 0)
    KERKO_DOWNLOAD_CITATIONS_LINK = env.bool('KERKO_DOWNLOAD_CITATIONS_LINK', True)
    KERKO_DOWNLOAD_CITATIONS_MAX_COUNT = env.int('KERKO_DOWNLOAD_CITATIONS_MAX_COUNT', 0)
    KERKO_DOWNLOAD_ATTACHMENT_NEW_WINDOW = env.bool('KERKO_DOWNLOAD_ATTACHMENT_NEW_WINDOW', False)

    if env.str('KERKOAPP_NOTE_WHITELIST_RE', '') or env.str('KERKOAPP_NOTE_BLACKLIST_RE', ''):
        # Obsolete after version 0.4.
        raise SystemExit(
            "ERROR: The 'KERKOAPP_NOTE_WHITELIST_RE' and 'KERKOAPP_NOTE_BLACKLIST_RE'"
            " environment variables are no longer supported. Please use"
            " 'KERKOAPP_CHILD_WHITELIST_RE' and 'KERKOAPP_CHILD_BLACKLIST_RE' instead."
        )

    KERKO_COMPOSER = Composer(
        whoosh_language=KERKO_WHOOSH_LANGUAGE,
        exclude_default_scopes=env.list('KERKOAPP_EXCLUDE_DEFAULT_SCOPES', []),
        exclude_default_fields=env.list('KERKOAPP_EXCLUDE_DEFAULT_FIELDS', []),
        exclude_default_facets=env.list('KERKOAPP_EXCLUDE_DEFAULT_FACETS', []),
        exclude_default_sorts=env.list('KERKOAPP_EXCLUDE_DEFAULT_SORTS', []),
        exclude_default_citation_formats=env.list('KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS', []),
        exclude_default_badges=env.list('KERKOAPP_EXCLUDE_DEFAULT_BADGES', []),
        default_tag_whitelist_re=env.str('KERKOAPP_TAG_WHITELIST_RE', ''),
        default_tag_blacklist_re=env.str('KERKOAPP_TAG_BLACKLIST_RE', r'^_'),
        default_child_whitelist_re=env.str('KERKOAPP_CHILD_WHITELIST_RE', ''),
        default_child_blacklist_re=env.str('KERKOAPP_CHILD_BLACKLIST_RE', r'^_'),
        mime_types=env.list('KERKOAPP_MIME_TYPES', ['application/pdf']),
    )

    # Add collection facets.
    collection_spec = env.collection_spec('KERKOAPP_COLLECTION_FACETS', None)
    if collection_spec:
        for collection_key, weight, title in collection_spec:
            KERKO_COMPOSER.add_facet(
                CollectionFacetSpec(
                    title=title,
                    weight=int(weight),
                    collection_key=collection_key,
                )
            )


class DevelopmentConfig(Config):
    CONFIG = 'development'
    DEBUG = True
    KERKO_ZOTERO_START = env.int('KERKO_ZOTERO_START', 0)
    KERKO_ZOTERO_END = env.int('KERKO_ZOTERO_END', 0)
    LOGGING_LEVEL = env.str('LOGGING_LEVEL', 'DEBUG')


class ProductionConfig(Config):
    CONFIG = 'production'
    DEBUG = False
    LOGGING_HANDLER = env.str('LOGGING_HANDLER', 'syslog')
    LOGGING_ADDRESS = env.str('LOGGING_ADDRESS', '/dev/log')
    LOGGING_LEVEL = env.str('LOGGING_LEVEL', 'WARNING')


CONFIGS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
