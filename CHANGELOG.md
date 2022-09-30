# Changelog

## Latest (unreleased)

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

* Read new settings `KERKO_FULLTEXT_SEARCH`, `KERKO_HIGHWIREPRESS_TAGS`,
  `KERKO_RESULTS_ABSTRACTS_MAX_LENGTH`,
  `KERKO_RESULTS_ABSTRACTS_MAX_LENGTH_LEEWAY`, `KERKO_RELATIONS_LINKS`,
  `KERKO_RESULTS_ATTACHMENT_LINKS`, `KERKO_RESULTS_URL_LINKS`, and
  `GOOGLE_ANALYTICS_ID` from environment variables.
* If full-text search is disabled, remove default scopes and fields that would
  otherwise be irrelevant or redundant.
* Add template for HTTP 503 (Service Unavailable) responses.
* Fix missing info about library groupID in configuration docs. Thanks
  [@drmikeuk](https://github.com/drmikeuk) for reporting the issue.
* Fix missing mandatory variables in instructions for running from Docker.
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

* The `Config` class is now instantiated, so the configuration variables are now
  taken from an object rather than a class.
* Replace the `KERKO_RESULTS_ABSTRACT` environment variable with two variables,
  `KERKO_RESULTS_ABSTRACTS` (note the now plural form) and
  `KERKO_RESULTS_ABSTRACTS_TOGGLER`.
* The following environment variable names are deprecated:
  * `KERKOAPP_TAG_WHITELIST_RE` (replaced by `KERKOAPP_TAG_INCLUDE_RE`)
  * `KERKOAPP_TAG_BLACKLIST_RE` (replaced by `KERKOAPP_TAG_EXCLUDE_RE`)
  * `KERKOAPP_CHILD_WHITELIST_RE` (replaced by `KERKOAPP_CHILD_INCLUDE_RE`)
  * `KERKOAPP_CHILD_BLACKLIST_RE` (replaced by `KERKOAPP_CHILD_EXCLUDE_RE`)
* Add environment variables `KERKOAPP_ITEM_INCLUDE_RE`,
  `KERKOAPP_ITEM_EXCLUDE_RE`, and `BABEL_DEFAULT_TIMEZONE`.
* Add German translation. Thanks [@mmoole](https://github.com/mmoole).
* Use Flask-Babel instead of its fork Flask-BabelEx, now that is has merged the
  translation domain features from Flask-BabelEx.
* Drop support for Python 3.6. Kerko is no longer being tested under Python 3.6.

## 0.6 (2020-06-15)

Changes:

* Allow setting `LOGGING_LEVEL` through an environment variable.
* Set default value for the `KERKOAPP_MIME_TYPES` variable to `['application/pdf']`.
* Fix `.env` file sometimes not read at app startup.
* Add a root logging handler.
* Improve documentation.

## 0.5 (2019-11-19)

*Warning:* Upgrading from version 0.4 or earlier will require that you clean and
re-sync your existing search index. Use the following commands:

```bash
flask kerko clean index
flask kerko sync
```

Changes:

* Upgrade Kerko to version
  [0.5](https://github.com/whiskyechobravo/kerko/blob/master/CHANGELOG.md#05-2019-11-19).
* Read new Kerko configuration variables from the environment.
* Deprecate abandoned environment variables.
* Use new Kerko template name configuration variables.
* Update versions of pinned dependencies.
* Improve documentation of configuration variables.

## 0.4 (2019-09-28)

Changes:

* Upgrade Kerko to version
  [0.4](https://github.com/whiskyechobravo/kerko/blob/master/CHANGELOG.md#04-2019-09-28).
* Update versions of pinned dependencies.
* Improve documentation.

## 0.3 (2019-07-29)

Changes:

* Upgrade Kerko to version
  [0.3](https://github.com/whiskyechobravo/kerko/blob/master/CHANGELOG.md#03-2019-07-29).
* Provide a Docker container with KerkoApp
  ([#6](https://github.com/whiskyechobravo/kerkoapp/pull/6),
  [#7](https://github.com/whiskyechobravo/kerkoapp/pull/7)). Thanks
  [Emiliano Heyns](https://github.com/retorquere).
* Read more Kerko configuration variables from the environment.
* Improve documentation.

## 0.3alpha1 (2019-07-17)

* First PyPI release.
