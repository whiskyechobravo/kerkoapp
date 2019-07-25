import logging

from environs import Env
from flask_babelex import lazy_gettext as _

from kerko.composer import Composer
from kerko.specs import CollectionFacetSpec

env = Env()  # pylint: disable=invalid-name


@env.parser_for('collection_spec')
def collection_spec_parser(value):
    try:
        return [tuple(i.strip() for i in v.split(':', maxsplit=2)) for v in value.split(';')]
    except:  # pylint: disable=bare-except
        return value


class Config():
    SECRET_KEY = env.str('SECRET_KEY')
    LOGGING_HANDLER = 'default'
    EXPLAIN_TEMPLATE_LOADING = False
    PROXY_FIX = env.bool('PROXY_FIX', False)
    BABEL_DEFAULT_LOCALE = env.str('BABEL_DEFAULT_LOCALE', 'en')
    KERKO_TITLE = env.str('KERKO_TITLE', _("Kerko App"))
    KERKO_WHOOSH_LANGUAGE = env.str('KERKO_WHOOSH_LANGUAGE', 'en')
    KERKO_ZOTERO_LOCALE = env.str('KERKO_ZOTERO_LOCALE', 'en-US')
    KERKO_ZOTERO_API_KEY = env.str('KERKO_ZOTERO_API_KEY')
    KERKO_ZOTERO_LIBRARY_ID = env.str('KERKO_ZOTERO_LIBRARY_ID')
    KERKO_ZOTERO_LIBRARY_TYPE = env.str('KERKO_ZOTERO_LIBRARY_TYPE')
    KERKO_PRINT_ITEM_LINK = env.bool('KERKO_PRINT_ITEM_LINK', False)
    KERKO_PRINT_CITATIONS_LINK = env.bool('KERKO_PRINT_CITATIONS_LINK', False)
    KERKO_PAGE_LEN = env.int('KERKO_PAGE_LEN', 20)
    KERKO_PAGER_LINKS = env.int('KERKO_PAGER_LINKS', 4)
    KERKO_CSL_STYLE = env.str('KERKO_CSL_STYLE', 'apa')
    KERKO_RESULTS_ABSTRACT = env.bool('KERKO_RESULTS_ABSTRACT', False)
    KERKO_FACET_COLLAPSING = env.bool('KERKO_FACET_COLLAPSING', False)

    KERKO_COMPOSER = Composer(
        whoosh_language=KERKO_WHOOSH_LANGUAGE,
        exclude_default_scopes=env.list('KERKOAPP_EXCLUDE_DEFAULT_SCOPES', []),
        exclude_default_fields=env.list('KERKOAPP_EXCLUDE_DEFAULT_FIELDS', []),
        exclude_default_facets=env.list('KERKOAPP_EXCLUDE_DEFAULT_FACETS', []),
        exclude_default_sorts=env.list('KERKOAPP_EXCLUDE_DEFAULT_SORTS', []),
        exclude_default_citation_formats=env.list('KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS', []),
        default_tag_whitelist_re=env.str('KERKOAPP_TAG_WHITELIST_RE', ''),
        default_tag_blacklist_re=env.str('KERKOAPP_TAG_BLACKLIST_RE', ''),
        default_note_whitelist_re=env.str('KERKOAPP_NOTE_WHITELIST_RE', ''),
        default_note_blacklist_re=env.str('KERKOAPP_NOTE_BLACKLIST_RE', '')
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


class ProductionConfig(Config):
    CONFIG = 'production'
    DEBUG = False
    LOGGING_HANDLER = 'syslog'
    LOGGING_ADDRESS = '/dev/log'
    LOGGING_LEVEL = logging.WARNING
    LOGGING_FORMAT = '%(name)s %(asctime)s %(levelname)s: %(message)s'


CONFIGS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
