# Changelog

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
