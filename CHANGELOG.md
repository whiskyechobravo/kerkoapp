# Changelog

## Unreleased

Other changes:

- Add `help`, `requirements`, `dependencies-upgrade`, and `upgrade` targets to
  `Makefile`. These are helpers for KerkoApp development.
- Add pre-commit hooks. Run Ruff and other code checks on pre-commit.


## 1.0.0 (2023-07-24)

Bug fixes:

- Fix Gunicorn not exiting if the application cannot start because of runtime
  errors (such as configuration errors). Exit with the `errno.EINTR` error code.
- Fix duplicate log entries with syslog logging handler.

Backwards incompatible changes:

- Rename parameters in `sample.config.toml` following changes in Kerko.

Other changes:

- Add instance configuration file example, `sample.instance.toml`.
- Replace the base Docker image with the official Python 3.11 image, and update
  Docker setup for Kerko 1.0.x.
- Improve the `Makefile` for an easier first-time experience using the Docker
  image.
- Improve the `Makefile` for a simpler and more reliable Docker image building
  process.
- Compile KerkoApp translations when building Docker image.


## 1.0.0alpha2 (2023-07-12)

Changes:

- Add parameters to `sample.config.toml`.


## 1.0.0alpha1 (2023-06-29)

Changes:

- Rename parameters in `sample.config.toml`.
- Print loaded configuration file paths in debug mode only.
- Rename the default branch of the repository from 'master' to 'main'. If you
  have cloned the repository with Git and were using the `master` branch, use
  the following commands to rename your local branch:

    ```bash
    git branch -m master main
    git fetch origin
    git branch -u origin/main main
    git remote set-head origin -a
    ```


## 1.0.0alpha0 (2023-06-26)

*Warning:* Upgrading from version 0.9 or earlier will require that you adapt
your installation and configuration files (see changes descriptions below),
rebuild your search index using the following commands, and then restart the
application:

```bash
flask kerko clean index
flask kerko sync index
```

Features:

- TOML files are now the preferred way of configuring KerkoApp. Since the
  configuration structure has also greatly changed, it is recommended that you
  review all your settings from `.env` files and migrate them to TOML files.
  Please refer to the Kerko documentation on configuration.
- Add many new configuration parameters. Consequently, many more customizations
  are now possible without having to replace KerkoApp with a custom application.
  Please refer to Kerko's documentation for the full list of options.

Other changes:

- Restructure and expand documentation into a unified documentation site for
  both Kerko and KerkoApp.
- Add Portuguese translation. Thanks to Gonçalo Cordeiro.
- Update the versions of pinned dependencies.

Backwards incompatible changes:

- Rename `kerkoapp.py` to `wsgi.py`, which is a more convenient default that, in
  many cases, makes it unnecessary to set the `FLASK_APP` environment variable
  or the `--app` command line option. You may need to unset or change your
  `FLASK_APP` environment variable, and/or adapt your WSGI server's
  configuration to refer to the new location of the application object, which is
  now `wsgi.app` instead of `kerkoapp.app`.
- Rename the `app` directory to `kerkoapp` to avoid potential name ambiguity
  with the `app` object.
- Remove all uses of the `FLASK_ENV` configuration variable, which Flask 2.3
  stopped supporting. For debug mode, use Flask's `--debug` command line option.
- The data directory has a new default location relative to the instance path.
  Please check the documentation for the `DATA_PATH` and `INSTANCE_PATH`
  configuration parameters. You may need to set one or both of those parameters,
  and/or move your existing data directory.
- Almost all configuration parameters have been renamed and/or moved into a
  hierarchical structure. Hierarchical parameters are referred to using
  path-like, dot-separated parameter names, and may conveniently be set with the
  `kerko.config_helpers.config_set()` function. Here is a mapping of the changed
  parameters that are specific to KerkoApp (please check also Kerko's changelog
  for other parameter changes):
    - `KERKOAPP_CHILD_EXCLUDE_RE` → `kerko.zotero.child_exclude_re`
    - `KERKOAPP_CHILD_INCLUDE_RE` → `kerko.zotero.child_include_re`
    - `KERKOAPP_COLLECTION_FACETS` → `kerko.facets.*`. See sub-parameters `type`
      (set it to `"collection"`), `collection_key`, and `title`.
    - `KERKOAPP_EXCLUDE_DEFAULT_BADGES`: Removed, with no replacement since no
      default badges are provided at this point.
    - `KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS` → `kerko.citation_formats.*`.
      See sub-parameter `enable`.
    - `KERKOAPP_EXCLUDE_DEFAULT_FACETS` → `kerko.facets.*`. See sub-parameter
      `enable`.
    - `KERKOAPP_EXCLUDE_DEFAULT_FIELDS` → `kerko.search_fields.*`. See
      sub-parameter `enable`.
    - `KERKOAPP_EXCLUDE_DEFAULT_SCOPES` → `kerko.scopes.*`. See sub-parameter
      `enable`.
    - `KERKOAPP_EXCLUDE_DEFAULT_SORTS` → `kerko.sorts.*`. See sub-parameter
      `enable`.
    - `KERKOAPP_FACET_INITIAL_LIMIT_LEEWAY` →
      `kerko.facets.*.initial_limit_leeway`. This is now set individually for
      each facet, and there is no longer a global parameter.
    - `KERKOAPP_FACET_INITIAL_LIMIT` → `kerko.facets.*.initial_limit`. This is
      now set individually for each facet, and there is no longer a global
      parameter.
    - `KERKOAPP_ITEM_EXCLUDE_RE` → `kerko.zotero.item_exclude_re`
    - `KERKOAPP_ITEM_INCLUDE_RE` → `kerko.zotero.item_include_re`
    - `KERKOAPP_MIME_TYPES` → `kerko.zotero.attachment_mime_types`
    - `KERKOAPP_TAG_EXCLUDE_RE` → `kerko.zotero.tag_exclude_re`
    - `KERKOAPP_TAG_INCLUDE_RE` → `kerko.zotero.tag_include_re`
    - `PROXY_FIX` → `kerkoapp.proxy_fix.*`


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
