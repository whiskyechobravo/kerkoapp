# Changelog

## Latest (unreleased)

*Warning:* Upgrading from version 0.9 or earlier will require that you rebuild
your search index. Use the following commands, then restart the application:

```bash
flask kerko clean index
flask kerko sync index
```

Features:

- Many new configuration settings have been added.

Other changes:

- Add Portuguese translation. Thanks to Gonçalo Cordeiro.
- Update versions of pinned dependencies.

Backwards incompatible changes:

- Rename `kerkoapp.py` to `wsgi.py`, which is a better default that, in many
  cases, makes it unnecessary to set the `FLASK_APP` environment variable. You
  may need to unset or change your `FLASK_APP` environment variable, and/or
  adapt your WSGI server's configuration to refer to the new location of the
  application object, which is now `wsgi.app` instead of `kerkoapp.app`.
- Rename the `app` directory to `kerkoapp` to avoid potential ambiguity with the
  `app` object.
- Remove all uses of the `FLASK_ENV` configuration variable, which Flask 2.3
  stopped supporting. For debug mode, use Flask's `--debug` command line option.

- Move most configuration options from environment variables to settings in TOML
  configuration files: **TODO:config: describe upgrade steps**
    - `KERKO_DATA_DIR` (now optional) → `DATA_DIR` if set in a TOML file, `KERKOAPP_DATA_DIR` if set as an environment variable.
    - `KERKO_BOOTSTRAP_VERSION` → `kerko.assets.bootstrap_version`
    - `KERKO_JQUERY_VERSION` → `kerko.assets.jquery_version`
    - `KERKO_POPPER_VERSION` → `kerko.assets.popper_version`
    - `KERKO_WITH_JQUERY` → `kerko.assets.with_jquery`
    - `KERKO_WITH_POPPER` → `kerko.assets.with_popper`
    - `KERKO_DOWNLOAD_ATTACHMENT_NEW_WINDOW` → `kerko.features.download_attachment_new_window`
    - `KERKO_DOWNLOAD_CITATIONS_LINK` → `kerko.features.download_citations_link`
    - `KERKO_DOWNLOAD_CITATIONS_MAX_COUNT` → `kerko.features.download_citations_max_count`
    - `KERKO_OPEN_IN_ZOTERO_APP` → `kerko.features.open_in_zotero_app`
    - `KERKO_OPEN_IN_ZOTERO_WEB` → `kerko.features.open_in_zotero_web`
    - `KERKO_PRINT_CITATIONS_LINK` → `kerko.features.print_citations_link`
    - `KERKO_PRINT_CITATIONS_MAX_COUNT` → `kerko.features.print_citations_max_count`
    - `KERKO_PRINT_ITEM_LINK` → `kerko.features.print_item_link`
    - `KERKO_RELATIONS_LINKS` → `kerko.features.relations_links`
    - `KERKO_RELATIONS_INITIAL_LIMIT` → `kerko.features.relations_initial_limit`
    - `KERKO_RELATIONS_SORT` → `kerko.features.relations_sort`
    - `KERKO_RESULTS_ABSTRACTS` → `kerko.features.results_abstracts`
    - `KERKO_RESULTS_ABSTRACTS_MAX_LENGTH` → `kerko.features.results_abstracts_max_length`
    - `KERKO_RESULTS_ABSTRACTS_MAX_LENGTH_LEEWAY` → `kerko.features.results_abstracts_max_length_leeway`
    - `KERKO_RESULTS_ABSTRACTS_TOGGLER` → `kerko.features.results_abstracts_toggler`
    - `KERKO_RESULTS_ATTACHMENT_LINKS` → `kerko.features.results_attachment_links`
    - `KERKO_RESULTS_URL_LINKS` → `kerko.features.results_url_links`
    - `KERKO_FEEDS` → `kerko.feeds.formats`
    - `KERKO_FEEDS_FIELDS` → `kerko.feeds.fields`
    - `KERKO_FEEDS_MAX_DAYS` → `kerko.feeds.max_days`
    - `KERKO_FEEDS_REQUIRE_ANY` → `kerko.feeds.require_any`
    - `KERKO_FEEDS_REJECT_ANY` → `kerko.feeds.reject_any`
    - `KERKO_HIGHWIREPRESS_TAGS` → `kerko.meta.highwirepress_tags`
    - `KERKO_TITLE` → `kerko.meta.title`
    - `KERKO_PAGE_LEN` → `kerko.pagination.page_len`
    - `KERKO_PAGER_LINKS` → `kerko.pagination.pager_links`
    - `KERKO_RESULTS_FIELDS` → `kerko.search.result_fields`
    - `KERKO_FULLTEXT_SEARCH` → `kerko.search.fulltext`
    - `KERKO_WHOOSH_LANGUAGE` → `kerko.search.whoosh_language`
    - `KERKO_TEMPLATE_BASE` → `kerko.templates.base`
    - `KERKO_TEMPLATE_LAYOUT` → `kerko.templates.layout`
    - `KERKO_TEMPLATE_SEARCH` → `kerko.templates.search`
    - `KERKO_TEMPLATE_SEARCH_ITEM` → `kerko.templates.search_item`
    - `KERKO_TEMPLATE_ITEM` → `kerko.templates.item`
    - `KERKO_TEMPLATE_ATOM_FEED` → `kerko.templates.atom_feed`
    - `KERKO_CSL_STYLE` → `kerko.zotero.csl_style`
    - `KERKO_ZOTERO_LOCALE` → `kerko.zotero.locale`
    - `KERKO_ZOTERO_BATCH_SIZE` → `kerko.zotero.batch_size`
    - `KERKO_ZOTERO_MAX_ATTEMPTS` → `kerko.zotero.max_attempts`
    - `KERKO_ZOTERO_WAIT` → `kerko.zotero.wait`
    - `KERKOAPP_TAG_INCLUDE_RE` → `kerko.zotero.tag_include_re`
    - `KERKOAPP_TAG_EXCLUDE_RE` → `kerko.zotero.tag_exclude_re`
    - `KERKOAPP_CHILD_INCLUDE_RE` → `kerko.zotero.child_include_re`
    - `KERKOAPP_CHILD_EXCLUDE_RE` → `kerko.zotero.child_exclude_re`
    - `KERKOAPP_MIME_TYPES` → `kerko.zotero.attachment_mime_types`
    - `KERKOAPP_COLLECTION_FACETS` → `kerko.facets.collection_facets`
    - `KERKOAPP_EXCLUDE_DEFAULT_SCOPES`: Default scopes may now be excluded on a per-scope basis, using `kerko.scopes.SCOPE_KEY.enabled = false`.
    - `KERKOAPP_EXCLUDE_DEFAULT_FIELDS`: Default fields may now be excluded on a per-field basis, using `kerko.fields.FIELD_KEY.enabled = false`.
    - `KERKOAPP_EXCLUDE_DEFAULT_FACETS`: Default facets may now be excluded on a per-facet basis, using `kerko.facets.FACET_KEY.enabled = false`.
    - `KERKOAPP_EXCLUDE_DEFAULT_SORTS`: Default sorts may now be excluded on a per-sort option basis, using `kerko.sorts.SORT_KEY.enabled = false`.
    - `KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS`: Default citation formats may now be excluded on a per-citation format basis, using `kerko.citation_formats.CITATION_FORMAT_KEY.enabled = false`.
    - `KERKOAPP_FACET_INITIAL_LIMIT`: Limit must may now be set on a per-facet basis, using `kerko.facets.FACET_KEY.initial_limit = LIMIT`.
    - `KERKOAPP_FACET_INITIAL_LIMIT_LEEWAY`: Limit leeway must may now be set on a per-facet basis, using `kerko.facets.FACET_KEY.initial_limit_leeway = LEEWAY`.


## 0.9 (2022-12-29)

*Warning:* Upgrading from version 0.8.x or earlier will require that you rebuild
your search index. Use the following commands, then restart the application:

```bash
flask kerko clean index
flask kerko sync index
```

Features:

- Add settings to control the initial limit on the number of values to show
  under each facet. When the initial limit is reached, a "show more" button
  allow to user to expand the full list. See `KERKOAPP_FACET_INITIAL_LIMIT` and
  `KERKOAPP_FACET_INITIAL_LIMIT_LEEWAY`.
- Read new settings `KERKO_FEEDS` and `KERKO_FEEDS_MAX_DAYS` from environment
  variables.

Backwards incompatible changes:

- Remove the `KERKO_FACET_COLLAPSING` option.


## 0.8 (2021-11-16)

*Warning:* Upgrading from version 0.7.x or earlier will require that you clean
and re-sync your existing search index. Use the following commands, then restart
the application:

```bash
flask kerko clean index
flask kerko sync
```

Changes:

- Read new settings `KERKO_FULLTEXT_SEARCH`, `KERKO_HIGHWIREPRESS_TAGS`,
  `KERKO_RESULTS_ABSTRACTS_MAX_LENGTH`,
  `KERKO_RESULTS_ABSTRACTS_MAX_LENGTH_LEEWAY`, `KERKO_RELATIONS_LINKS`,
  `KERKO_RESULTS_ATTACHMENT_LINKS`, `KERKO_RESULTS_URL_LINKS`, and
  `GOOGLE_ANALYTICS_ID` from environment variables.
- If full-text search is disabled, remove default scopes and fields that would
  otherwise be irrelevant or redundant.
- Add template for HTTP 503 (Service Unavailable) responses.
- Fix missing info about library groupID in configuration docs. Thanks
  [@drmikeuk](https://github.com/drmikeuk) for reporting the issue.
- Fix missing mandatory variables in instructions for running from Docker.
  Thanks [@amv](https://github.com/amv).

## 0.7 (2021-01-08)

*Warning:* Upgrading from version 0.6 or earlier will require that you clean and
re-sync your existing search index. Use the following commands, then restart the
application:

```bash
flask kerko clean index
flask kerko sync
```

Changes:

- The `Config` class is now instantiated, so the configuration variables are now
  taken from an object rather than a class.
- Replace the `KERKO_RESULTS_ABSTRACT` environment variable with two variables,
  `KERKO_RESULTS_ABSTRACTS` (note the now plural form) and
  `KERKO_RESULTS_ABSTRACTS_TOGGLER`.
- The following environment variable names are deprecated:
  - `KERKOAPP_TAG_WHITELIST_RE` (replaced by `KERKOAPP_TAG_INCLUDE_RE`)
  - `KERKOAPP_TAG_BLACKLIST_RE` (replaced by `KERKOAPP_TAG_EXCLUDE_RE`)
  - `KERKOAPP_CHILD_WHITELIST_RE` (replaced by `KERKOAPP_CHILD_INCLUDE_RE`)
  - `KERKOAPP_CHILD_BLACKLIST_RE` (replaced by `KERKOAPP_CHILD_EXCLUDE_RE`)
- Add environment variables `KERKOAPP_ITEM_INCLUDE_RE`,
  `KERKOAPP_ITEM_EXCLUDE_RE`, and `BABEL_DEFAULT_TIMEZONE`.
- Add German translation. Thanks to [@mmoole](https://github.com/mmoole).
- Use Flask-Babel instead of its fork Flask-BabelEx, now that is has merged the
  translation domain features from Flask-BabelEx.
- Drop support for Python 3.6. Kerko is no longer being tested under Python 3.6.

## 0.6 (2020-06-15)

Changes:

- Allow setting `LOGGING_LEVEL` through an environment variable.
- Set default value for the `KERKOAPP_MIME_TYPES` variable to `['application/pdf']`.
- Fix `.env` file sometimes not read at app startup.
- Add a root logging handler.
- Improve documentation.

## 0.5 (2019-11-19)

*Warning:* Upgrading from version 0.4 or earlier will require that you clean and
re-sync your existing search index. Use the following commands:

```bash
flask kerko clean index
flask kerko sync
```

Changes:

- Upgrade Kerko to version
  [0.5](https://github.com/whiskyechobravo/kerko/blob/master/CHANGELOG.md#05-2019-11-19).
- Read new Kerko configuration variables from the environment.
- Deprecate abandoned environment variables.
- Use new Kerko template name configuration variables.
- Update versions of pinned dependencies.
- Improve documentation of configuration variables.

## 0.4 (2019-09-28)

Changes:

- Upgrade Kerko to version
  [0.4](https://github.com/whiskyechobravo/kerko/blob/master/CHANGELOG.md#04-2019-09-28).
- Update versions of pinned dependencies.
- Improve documentation.

## 0.3 (2019-07-29)

Changes:

- Upgrade Kerko to version
  [0.3](https://github.com/whiskyechobravo/kerko/blob/master/CHANGELOG.md#03-2019-07-29).
- Provide a Docker container with KerkoApp
  ([#6](https://github.com/whiskyechobravo/kerkoapp/pull/6),
  [#7](https://github.com/whiskyechobravo/kerkoapp/pull/7)). Thanks
  [Emiliano Heyns](https://github.com/retorquere).
- Read more Kerko configuration variables from the environment.
- Improve documentation.

## 0.3alpha1 (2019-07-17)

- First PyPI release.
