# KerkoApp

[KerkoApp] is a web application that uses [Kerko] to provide a user-friendly
search and browsing interface for sharing a bibliography managed with the
[Zotero] reference manager. It is built in [Python] with the [Flask] framework.

Although this application may be deployed as is on a web server, it is primarily
meant to serve as an example on how to integrate Kerko into a Flask application.

Basic configuration options can be set with environment variables, but for more
advanced customizations one should consider building a custom application
(possibly using KerkoApp as a starting point), and configuring Kerko through its
Python interface.

Contents:

- [KerkoApp](#kerkoapp)
  - [Demo site](#demo-site)
  - [Features](#features)
  - [Getting started](#getting-started)
    - [Standard installation](#standard-installation)
    - [Running from Docker](#running-from-docker)
  - [Environment variables](#environment-variables)
  - [Configuration example](#configuration-example)
  - [Deploying KerkoApp in production](#deploying-kerkoapp-in-production)
  - [Translating KerkoApp](#translating-kerkoapp)
  - [Contributing](#contributing)
    - [Reporting issues](#reporting-issues)
    - [Submitting code changes](#submitting-code-changes)
    - [Submitting a translation](#submitting-a-translation)
    - [Supporting the project](#supporting-the-project)
  - [Changelog](#changelog)
  - [Troubleshooting](#troubleshooting)
    - [Conflicting package versions with standard installation](#conflicting-package-versions-with-standard-installation)
    - [No such command "kerko" error when running Flask](#no-such-command-kerko-error-when-running-flask)
    - [Errors when using the `master` version of Kerko](#errors-when-using-the-master-version-of-kerko)

## Demo site

A [KerkoApp demo site][KerkoApp_demo] is available for you to try. You may also
view the [Zotero library][Zotero_demo] that contains the source data for the
demo site.


## Features

KerkoApp is just a thin container around Kerko. As such, almost all of its
features are inherited from Kerko. See [Kerko's documentation][Kerko] for the
list of features.

The main features added by KerkoApp over Kerko's are:

**TODO:config: Update this description!**

- Read most configuration from environment variables or a `.env` file, adhering
  to the [Twelve-factor App](https://12factor.net/config) methodology.
- Provide extra environment variables for:
    - defining facets based on Zotero collections;
    - excluding or including tags or child items (notes and attachments) with
      regular expressions;
    - excluding fields, facets, sort options, search scopes, record download
      formats, or badges from Kerko's defaults.
- Provide templates for common HTTP errors.
- Load user interface translations based on the configured locale.


## Getting started

This section presents two approaches to getting started with KerkoApp: running
from a standard installation of KerkoApp, or running from a Docker container
pre-built with KerkoApp. You may choose the one you are most comfortable with.


### Standard installation

This procedure requires Python 3.7 or later.

1. The first step is to install the software. As with any Python package, it is
   highly recommended to install it within a [virtual environment][venv].

   ```bash
   git clone https://github.com/whiskyechobravo/kerkoapp.git
   cd kerkoapp
   pip install -r requirements/run.txt
   ```

   This will install many packages required by Kerko or KerkoApp.

2. Copy the `sample.env` file to `.env`. Open `.env` in a text editor to assign
   proper values to the variables outlined below.

   - `KERKOAPP_SECRET_KEY`: This variable is required for generating secure tokens in web
     forms. It should have a secure, random value and it really has to be
     secret. For this reason, never add your `.env` file to a code repository.
   - `KERKOAPP_ZOTERO_API_KEY`, `KERKOAPP_ZOTERO_LIBRARY_ID` and
     `KERKOAPP_ZOTERO_LIBRARY_TYPE`: These variables are required for Kerko to be
     able to access your Zotero library. See [Environment
     variables](#environment-variables) for details.

3. Have KerkoApp retrieve your data from zotero.org:

   ```bash
   flask --debug kerko sync
   ```

   If you have a large bibliography and/or large file attachments, that command
   may take a while to complete (and there is no progress indicator). In
   production use, that command is usually added to the crontab file for regular
   execution.

   The `--debug` switch is optional. If you use it, some messages will give you
   an idea of the sync process' progress. If you omit it, the command will run
   silently unless there are warnings or errors.

4. Run KerkoApp:

   ```bash
   flask --debug run
   ```

5. Open http://localhost:5000/ in your browser and explore the bibliography.

Note that Flask's built-in server is **not suitable for production** as it
doesn’t scale well. You'll want to consider better options, such as the [WSGI
servers suggested in Flask's documentation][Flask_production].


### Running from Docker

This procedure requires that [Docker] is installed on your computer.

1. Copy the `Makefile` and `sample.env` files from [KerkoApp's
   repository][KerkoApp] to an empty directory on your computer.

2. Rename `sample.env` to `.env`. Open `.env` in a text editor to assign proper
   values to the variables outlined below.

   - `KERKOAPP_SECRET_KEY`: This variable is required for generating secure tokens in web
     forms. It should have a secure, random value and it really has to be
     secret. For this reason, never add your `.env` file to a code repository.
   - `KERKOAPP_ZOTERO_API_KEY`, `KERKOAPP_ZOTERO_LIBRARY_ID` and
     `KERKOAPP_ZOTERO_LIBRARY_TYPE`: These variables are required for Kerko to be
     able to access your Zotero library. See [Environment
     variables](#environment-variables) for details.
   - `MODULE_NAME`: This variable is required for running the application with
     the provided Docker image. See `sample.env` for the proper value.

   **Do not** assign a value to the `KERKOAPP_DATA_DIR` variable. If you do, the
   volume bindings defined within the `Makefile` will not be of any use to the
   application running within the container.

3. Pull the latest KerkoApp Docker image. In the same directory as the
   `Makefile`, run the following command:

   ```bash
   docker pull whiskyechobravo/kerkoapp
   ```

4. Have KerkoApp retrieve your bibliographic data from zotero.org:

   ```bash
   make kerkosync
   ```

   If you have a large bibliography, this may take a while (and there is no
   progress indicator).

   Kerko's index will be stored in the `data` subdirectory.

5. Run KerkoApp:

   ```
   make run
   ```

6. Open http://localhost:8080/ in your browser and explore the bibliography.

Keep in mind that the `sample.env` and `Makefile` provide only examples on how
to run the dockerized KerkoApp. Also, **we have not made any special effort to
harden the KerkoApp image for production use**; for such use, you will have to
build an image that is up to your standards. For full documentation on how to
run Docker containers, including the port mapping and volume binding required to
run containers, see the [Docker documentation][Docker_docs].


## Environment variables

KerkoApp supports a number of environment variables which may be useful to those
who wish to use KerkoApp as is, without touching any Python code.

Many of these variables cause changes to the structure of Kerko's search index.
Changing them require that you rebuild Kerko's search index and restart the
application. To rebuild the index:

```bash
flask kerko clean index
flask kerko sync
```

**TODO:config: Cleanup redundancies: these variables are explained in 3 different places in this file!**

**TODO:config: Clarify that the following may be set as environment variables or .env variables but with the KERKOAPP_ prefix**

The environment variables below are required and have no default values:

- `KERKOAPP_SECRET_KEY`: This variable is required for generating secure tokens in web
  forms. It should have a secure, random value and it really has to be secret.
  For this reason, never add your `.env` file to a code repository.
- `KERKOAPP_ZOTERO_API_KEY`: Your API key, as [created on
  zotero.org](https://www.zotero.org/settings/keys/new).
- `KERKOAPP_ZOTERO_LIBRARY_ID`: The identifier of the library to get data from. For
  your personal library this value should be your _userID_, as found on
  https://www.zotero.org/settings/keys (you must be logged-in). For a group
  library this value should be the _groupID_ of the library, as found in the URL
  of that library (e.g., in https://www.zotero.org/groups/2348869/kerko_demo,
  the _groupID_ is `2348869`).
- `KERKOAPP_ZOTERO_LIBRARY_TYPE`: The type of library to get data from, either
  `'user'` for your personal library, or `'group'` for a group library.

The environment variable below is required to run KerkoApp with the provided
Docker image, and has no default value:

- `MODULE_NAME`: Specifies the Python module to be imported by Gunicorn.
  Normally set to `wsgi`, which causes Gunicorn to run with `APP_MODULE` set
  to `wsgi:app`.

**TODO:config: Optional env variables**

- `KERKOAPP_CONFIG_FILE`: **TODO:config: document this!**
- `KERKOAPP_DATA_DIR`: The directory where to store the search index and the
  file attachments. This may be an absolute path or a relative path; a relative
  path will be resolved from the application's directory. Under the data
  directory, subdirectories `cache`, `index` and `attachments` will be created
  if they do not already exist.

**TODO:config: Refer to Kerko documentation for Kerko configuration settings.**

- `KERKOAPP_COLLECTION_FACETS`: Defines facets modeled on Zotero collections.
  This variable should be a list of semicolon-delimited triples (collection key,
  facet weight and facet title, separated by colons). Each specified collection
  will appear in Kerko as a facet where subcollections will be represented as
  values within the facet. The weight determines a facet's position relative to
  the other facets. The facet title will be displayed by Kerko and, if desired,
  may be different from the collection's name in Zotero (you could use this to
  differentiate the names of collections made publicly available in Kerko
  through facets from those used internally in your Zotero library). Note that
  for a collection-based facet to appear in the search interface, all of the
  following conditions must be met:
  - The specified collection key corresponds to a top-level collection in the
    Zotero library.
  - The specified collection has at least one subcollection that contains at
    least one item that is not excluded by Kerko (meaning the item is not
    excluded by other settings such as `KERKOAPP_ITEM_EXCLUDE_RE` or
    `KERKOAPP_ITEM_INCLUDE_RE`).
  - The value of `KERKOAPP_COLLECTION_FACETS` should be defined within a single
    string, on a single line.
- `KERKOAPP_EXCLUDE_DEFAULT_BADGES`: List of badges (identified by key) to
  exclude from those created by default. If that list contains the value '*', no
  badge will be created by default. Please refer to the implementation of
  `kerko.composer.Composer.init_default_badges()` for the list of default
  badges.
- `KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS`: List of record download formats
  (identified by key) to exclude from those created by default. If that list
  contains the value '*', no format will be created by default. Please refer to
  the implementation of
  `kerko.composer.Composer.init_default_citation_formats()` for the list of
  default formats.
- `KERKOAPP_EXCLUDE_DEFAULT_FACETS`: List of facets (identified by key) to
  exclude from those created by default. If that list contains the value '*', no
  facet will be created by default. Please refer to the implementation of
  `kerko.composer.Composer.init_default_facets()` for the list of default
  facets.
- `KERKOAPP_EXCLUDE_DEFAULT_FIELDS`: List of fields (identified by key) to
  exclude from those created by default. If that list contains the value '*', no
  field will be created by default. Caution: some default fields are required by
  Kerko or by badges. If required fields are excluded, the application will
  probably not start. Please refer to the implementation of
  `kerko.composer.Composer.init_default_fields()` for the list of default
  fields. Note that if `kerko.search.fulltext` is `False`, the `'text_docs'`
  field, which otherwise would contain the full-text, is excluded by default.
- `KERKOAPP_EXCLUDE_DEFAULT_SCOPES`: List of scopes (identified by key) to
  exclude from those created by default. If that list contains the value '*', no
  scope will be added by default. Caution: most default fields are expecting one
  or more of those scopes to exist. If required scopes are excluded, the
  application will probably not start. Please refer to the implementation of
  `kerko.composer.Composer.init_default_scopes()` for the list of default
  scopes. Note that if `kerko.search.fulltext` is `False`, the `'metadata'` ("In
  all fields") and `'fulltext'` ("In documents") scopes are excluded by default.
- `KERKOAPP_EXCLUDE_DEFAULT_SORTS`: List of sorts (identified by key) to exclude
  from those created by default. Caution: at least one sort must remain for the
  application to start. Please refer to the implementation of
  `kerko.composer.Composer.init_default_sorts()` for the list of default sorts.
- `KERKOAPP_FACET_INITIAL_LIMIT`: Limits the number of facet values initially
  shown on search results pages. If more values are available, a "show more"
  button will let the user expand the list. Defaults to `0` (i.e. no limit).
- `KERKOAPP_FACET_INITIAL_LIMIT_LEEWAY`: If the number of facet values exceeds
  `KERKOAPP_FACET_INITIAL_LIMIT` by this tolerance margin or less, all values
  will be initially shown. Defaults to `0` (i.e. no tolerance margin).
- `KERKOAPP_MIME_TYPES`: List of allowed MIME types for attachments. Defaults to
  `"application/pdf"`.
- `KERKOAPP_ITEM_EXCLUDE_RE`: Regex to use to exclude items based on their tags.
  Any object that have a tag that matches this regular expression will be
  excluded. If empty (which is the default), no items will be excluded unless
  `KERKOAPP_ITEM_INCLUDE_RE` is set, in which case items that do not have any
  tag that matches it will be excluded.
- `KERKOAPP_ITEM_INCLUDE_RE`: Regex to use to include items based on their tags.
  Any item which does not have a tag that matches this regular expression will
  be ignored. If this value is empty (which is the default), all items will be
  accepted unless `KERKOAPP_ITEM_EXCLUDE_RE` is set which can cause some items
  to be rejected.
- `KERKOAPP_TAG_EXCLUDE_RE`: Regex to use to exclude tags. The default value
  causes any tag that begins with an underscore ('_') to be ignored by Kerko.
  Note that record exports (downloads) always include all tags regardless of
  this parameter, which only applies to information displayed by Kerko (exports
  are generated by the Zotero API, not by Kerko).
- `KERKOAPP_TAG_INCLUDE_RE`: Regex to use to include tags. By default, all tags
  are accepted. Note that record exports (downloads) always include all tags
  regardless of this parameter, which only applies to information displayed by
  Kerko (exports are generated by the Zotero API, not by Kerko).
- `KERKOAPP_CHILD_EXCLUDE_RE`: Regex to use to exclude children (e.g. notes,
  attachments) based on their tags. Any child that have a tag that matches this
  regular expression will be ignored. If empty, no children will be rejected
  unless `KERKOAPP_CHILD_INCLUDE_RE` is set and the tags of those children do
  not match it. By default, any child having at least one tag that begins with
  an underscore ('_') is rejected.
- `KERKOAPP_CHILD_INCLUDE_RE`: Regex to use to include children (e.g. notes,
  attachments) based on their tags. Any child which does not have a tag that
  matches this regular expression will be ignored. If this value is empty (which
  is the default), all children will be accepted unless
  `KERKOAPP_CHILD_EXCLUDE_RE` is set and causes some to be rejected.
- `LOGGING_LEVEL`: Severity of events to track. Allowed values are `DEBUG`,
  `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Defaults to `DEBUG` if app is running
  in debug mode, and to `WARNING` otherwise.

Note that some of Kerko's variables do not have a corresponding environment
variable in KerkoApp and therefore can only be set in Python from a custom
application.

If you are building your own application, you do not really need the above
environment variables. Instead, you could directly set Kerko variables in your
application's `Config` object and set arguments to `kerko.composer.Composer`'s
init method. In that case, please refer to [Kerko's documentation][Kerko] rather
than KerkoApp's.


## Configuration example

The `.env` file of the [demo site][KerkoApp_demo] looks like the following,
except for the private keys:

**TODO:config: Update this example!**

```
KERKOAPP_SECRET_KEY=XXXXX
KERKOAPP_ZOTERO_API_KEY=XXXXX
KERKOAPP_ZOTERO_LIBRARY_ID=2348869
KERKOAPP_ZOTERO_LIBRARY_TYPE=group
KERKO_TITLE=Kerko Demo
KERKO_CSL_STYLE=apa
KERKO_PRINT_ITEM_LINK=True
KERKO_PRINT_CITATIONS_LINK=True
KERKOAPP_EXCLUDE_DEFAULT_FACETS=facet_tag,facet_link
KERKOAPP_COLLECTION_FACETS=KY3BNA6T:110:Topic; 7H2Q7L6I:120:Field of study; JFQRH4X2:130:Contribution
```

In this example, `KERKOAPP_EXCLUDE_DEFAULT_FACETS` is used to exclude the
`'facet_tag'` and `'facet_link'` facets that Kerko would normally build by
default.

Also in this example, `KERKOAPP_COLLECTION_FACETS` defines three facets. The
first one, represented by `KY3BNA6T:110:Topic`, is based on a Zotero collection
whose key is _KY3BNA6T_. Its weight is _110_, which will position it under
facets that have a lighter weight (smaller number), and above those that have a
heavier weight (larger number). And its title is _Topic_. The other two facets
are titled _Field of study_ and _Contribution_.


## Deploying KerkoApp in production

As there are many different systems and environments, setting up KerkoApp for
use in production is out of scope for this guide. The procedures will be the
same as for any Flask application, but you will have consider features that are
more specific to KerkoApp, e.g., the `.env` file, the data directory, the
regular synchronization of data from zotero.org.

You might find the following guide useful:

- [Deploying KerkoApp on Ubuntu 20.04 or 22.04 with nginx and gunicorn](https://gist.github.com/davidlesieur/e1dafd09636a4bb333ad360e4b2c5d6d)


## Translating KerkoApp

Note that Kerko and KerkoApp have separate translation files and that most
messages actually come from Kerko. For translating Kerko's messages, please
refer to [Kerko's documentation][Kerko].

KerkoApp can be translated with [Babel](http://babel.pocoo.org).

The following commands should be executed from the directory that contains
`babel.cfg`, and the appropriate [virtual environment][venv] must have been
activated beforehand.

Create or update the PO file template (POT). Replace `CURRENT_VERSION` with your
current KerkoApp version:

```bash
pybabel extract -F babel.cfg -o kerkoapp/translations/messages.pot --project=KerkoApp --version=CURRENT_VERSION --copyright-holder="Kerko Contributors" kerkoapp
```

Create a new PO file (for a new locale) based on the POT file. Replace
`YOUR_LOCALE` with the appropriate language code, e.g., `de`, `es`, `it`:

```bash
pybabel init -l YOUR_LOCALE -i kerkoapp/translations/messages.pot -d kerkoapp/translations
```

Update an existing PO file based on the POT file:

```bash
pybabel update -l YOUR_LOCALE -i kerkoapp/translations/messages.pot -d kerkoapp/translations
```

Compile MO files:

```bash
pybabel compile -l YOUR_LOCALE -d kerkoapp/translations
```


## Contributing

### Reporting issues

For reporting an issue, please consider the following guidelines:

- Try to identify whether the issue belongs to [KerkoApp] or to [Kerko]. If
  unsure, check the list of features related to each package and try to
  determine which feature is the most related to the issue. Then you may submit
  the issue to [KerkoApp's issue tracker][KerkoApp_issues] if it is related to
  KerkoApp, or to [Kerko's issue tracker][Kerko_issues] otherwise.
- Make sure that the same issue has not already been reported or fixed in the
  repository.
- Describe what you expected to happen.
- If possible, include a minimal reproducible example to help others identify
  the issue.
- Describe what actually happened. Include the full traceback if there was an
  exception.


### Submitting code changes

Pull requests may be submitted against [KerkoApp's repository][KerkoApp]. Please
consider the following guidelines:

- Use [Yapf](https://github.com/google/yapf) to autoformat your code (with
  option `--style='{based_on_style: facebook, column_limit: 100}'`). Many
  editors provide Yapf integration.
- Include a string like "Fixes #123" in your commit message (where 123 is the
  issue you fixed). See [Closing issues using
  keywords](https://help.github.com/en/articles/closing-issues-using-keywords).


### Submitting a translation

Some guidelines:

- The PO file encoding must be UTF-8.
- The header of the PO file must be filled out appropriately.
- All messages of the PO file must be translated.

Please submit your translation as a pull request against [KerkoApp's
repository][KerkoApp], or by [e-mail][Kerko_email], with the PO file included as
an attachment (**do not** copy the PO file's content into an e-mail's body,
since that could introduce formatting or encoding issues).


### Supporting the project

Nurturing an open source project such as Kerko, following up on issues and
helping others in working with the system is a lot of work, but hiring the
original developers of Kerko can do a lot in ensuring continued support and
development of the project.

If you need professional support related to Kerko, have requirements not
currently implemented in Kerko, want to make sure that some Kerko issue
important to you gets resolved, or if you just like our work and would like to
hire us for an unrelated project, please [e-mail us][Kerko_email].


## Changelog

For a summary of changes by release version, see the [changelog](CHANGELOG.md).


## Troubleshooting

### Conflicting package versions with standard installation

The `requirements/run.txt` file specifies a precise version for each required
package, ensuring consistent results with the last environment KerkoApp was
tested with. If some of these packages are already present in your Python
environment, their versions are likely to be different and some Python code
outside KerkoApp might require those versions. In that case, try replacing
`run.txt` with `run.in` in the install command:

```bash
pip install -r requirements/run.in
```

Requirements in `run.in` are more flexible regarding the versions. If you still
have version conflicts with those requirements, you'll have to decide which
version to use and verify that it is compatible with both KerkoApp and your
other Python code.

### No such command "kerko" error when running Flask

Make sure you are trying to run the `flask` command from the application's
directory, where the `wsgi.py` file is found. To run it from other directories,
you might need to use Flask's `--app` option, or to set the `FLASK_APP`
environment variable.

### Errors when using the `master` version of Kerko

The `master` branch of KerkoApp is meant to work with the latest published
release of Kerko. If you have installed the `master` version of Kerko instead
its latest published release, use the `kerko-head` branch of KerkoApp instead of
`master`.


[Docker]: https://www.docker.com/
[Docker_docs]: https://docs.docker.com/
[Flask]: https://pypi.org/project/Flask/
[Flask_production]: https://flask.palletsprojects.com/en/latest/deploying/
[Kerko]: https://github.com/whiskyechobravo/kerko
[Kerko_email]: mailto:kerko@whiskyechobravo.com
[Kerko_issues]: https://github.com/whiskyechobravo/kerko/issues
[Kerko_variables]: https://github.com/whiskyechobravo/kerko#configuration-variables
[KerkoApp]: https://github.com/whiskyechobravo/kerkoapp
[KerkoApp_demo]: https://demo.kerko.whiskyechobravo.com
[KerkoApp_issues]: https://github.com/whiskyechobravo/kerkoapp/issues
[Python]: https://www.python.org/
[pytz]: https://pypi.org/project/pytz/
[venv]: https://docs.python.org/3.11/tutorial/venv.html
[Zotero]: https://www.zotero.org/
[Zotero_demo]: https://www.zotero.org/groups/2348869/kerko_demo/items
