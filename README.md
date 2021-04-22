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


## Demo site

A [KerkoApp demo site][KerkoApp_demo] is available for you to try. You may also
view the [Zotero library][Zotero_demo] that contains the source data for the
demo site.


## Features

KerkoApp is just a thin container around Kerko. As such, almost all of its
features are inherited from Kerko. See [Kerko's documentation][Kerko] for the
list of features.

The main features added by KerkoApp over Kerko's are:

* Most of Kerko's configuration settings are read from environment variables or
  a `.env` file, adhering to the [Twelve-factor
  App](https://12factor.net/config) methodology.
* Extra environment variables provide quick shortcuts for:
    * defining facets based on Zotero collections;
    * excluding or including tags or child items (notes and attachments) with
      regular expressions;
    * excluding fields, facets, sort options, search scopes, citation download
      formats, or badges from Kerko's defaults.
* Templates for common HTTP errors.


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

2. Copy `dotenv.sample` to `.env`. Open `.env` in a text editor to assign proper
   values to the variables outlined below.

   * `KERKO_TITLE`: The title to display in web pages.
   * `SECRET_KEY`: This variable is required for generating secure tokens in web
     forms. It should have a secure, random value and it really has to be
     secret. For this reason, never add your `.env` file to a code repository.
   * `KERKO_ZOTERO_API_KEY`, `KERKO_ZOTERO_LIBRARY_ID` and
     `KERKO_ZOTERO_LIBRARY_TYPE`: These variables are required for Kerko to be
     able to access your Zotero library. See the **Environment variables**
     section below for details.

3. Have KerkoApp retrieve your data from zotero.org:

   ```bash
   flask kerko sync
   ```

   If you have a large bibliography and/or large file attachments, that command
   may take a while to complete (and there is no progress indicator). In
   production use, that command is usually added to the crontab file for regular
   execution.

4. Run KerkoApp:

   ```bash
   flask run
   ```

5. Open http://localhost:5000/ in your browser and explore the bibliography.

Note that Flask's built-in server is **not suitable for production** as it
doesn’t scale well. You'll want to consider better options, such as the [WSGI
servers suggested in Flask's documentation][Flask_production].


### Running from Docker

This procedure requires that [Docker] is installed on your computer.

1. Copy the `Makefile` and `dotenv.sample` files from [KerkoApp's
   repository][KerkoApp] to an empty directory on your computer.

2. Rename `dotenv.sample` to `.env`. Open `.env` in a text editor to assign
   proper values to the variables outlined below.

   * `KERKO_TITLE`: The title to display in web pages.
   * `SECRET_KEY`: This variable is required for generating secure tokens in web
     forms. It should have a secure, random value and it really has to be
     secret. For this reason, never add your `.env` file to a code repository.
   * `KERKO_ZOTERO_API_KEY`, `KERKO_ZOTERO_LIBRARY_ID` and
     `KERKO_ZOTERO_LIBRARY_TYPE`: These variables are required for Kerko to be
     able to access your Zotero library. See the **Environment variables**
     section below for details.
   * `MODULE_NAME`, `FLASK_APP` and `FLASK_ENV`: These variables should be present
     to configure the base Gunicorn image. `dotenv.sample` should already contain a
     working sample: `kerkoapp`, `kerkoapp.py` and `production`.

   **Do not** assign a value to the `KERKO_DATA_DIR` variable. If you do, the
   volume bindings defined within the `Makefile` won't be of any use to the
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

Keep in mind that the `dotenv.sample` and `Makefile` provide only examples on
how to run the dockerized KerkoApp. Also, **we have not made any special effort
to harden the KerkoApp image for production use**; for such use, you will have
to build an image that is up to your standards. For full documentation on how to
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

The environment variables below are required and have no default values:

* `FLASK_APP`: Specifies the application to load. Normally set to `kerkoapp.py`.
* `FLASK_ENV`: Specifies the environment in which the app should run. Either
  `development` or `production`. Normally set to `production`.
* `KERKO_ZOTERO_API_KEY`: Your API key, as [created on
  zotero.org](https://www.zotero.org/settings/keys/new).
* `KERKO_ZOTERO_LIBRARY_ID`: The identifier of the library to get data from. For
  your personal library this value should be your _userID_, as found on
  https://www.zotero.org/settings/keys (you must be logged-in). For a group
  library this value should be the _groupID_ of the library, as found in the URL
  of that library (e.g., in https://www.zotero.org/groups/2348869/kerko_demo,
  the _groupID_ is `2348869`).
* `KERKO_ZOTERO_LIBRARY_TYPE`: The type of library to get data from, either
  `'user'` for your personal library, or `'group'` for a group library.

The environment variables below are required to run KerkoApp in Docker using
the base Gunicorn image, and have no default values:

* `MODULE_NAME`: Specifies the base module to derive which application module to
  initiate Gunicorn with. Normally set to `kerkoapp`, which causes the base
  Gunicorn docker image to set `APP_MODULE` to `kerkoapp:app`.

The following environment variables are supported by KerkoApp and may be added
to your `.env` file if you wish to override their default values:

* `KERKO_CSL_STYLE`: The citation style to use for formatted references. Can be
  either the file name (without the `.csl` extension) of one of the styles in the
  [Zotero Styles Repository][Zotero_styles] (e.g., `apa`) or the URL of a remote
  CSL file. Defaults to `'apa'`.
* `KERKO_DATA_DIR`: The directory where to store the search index and the file
  attachments. Defaults to `data/kerko`. Subdirectories `index` and
  `attachments` will be created if they don't already exist.
* `KERKO_DOWNLOAD_ATTACHMENT_NEW_WINDOW`: Open attachments in new windows, i.e.,
  add the `target="_blank"` attribute to attachment links. Defaults to `False`.
* `KERKO_DOWNLOAD_CITATIONS_LINK`: Provide a citation download button on search
  results pages. Defaults to `True`.
* `KERKO_DOWNLOAD_CITATIONS_MAX_COUNT`: Limit over which the citation download
  button should be hidden from search results pages. Defaults to `0` (i.e. no
  limit).
* `KERKO_FACET_COLLAPSING`: Allow collapsible facets. Defaults to `False`.
* `KERKO_PAGE_LEN`: The number of search results per page. Defaults to `20`.
* `KERKO_PAGER_LINKS`: Number of pages to show in the pager (not counting the
  current page). Defaults to `4`.
* `KERKO_PRINT_ITEM_LINK`: Provide a print button on item pages. Defaults to
  `False`.
* `KERKO_PRINT_CITATIONS_LINK`: Provide a print button on search results
  pages. Defaults to `False`.
* `KERKO_PRINT_CITATIONS_MAX_COUNT`: Limit over which the print button should
  be hidden from search results pages. Defaults to `0` (i.e. no limit).
* `KERKO_RELATIONS_INITIAL_LIMIT`: Number of related items to show above the
  "view all" link. Defaults to `5`.
* `KERKO_RESULTS_ABSTRACTS`: Determines whether abstracts are displayed on
  search results pages. Defaults to `False` (hidden).
* `KERKO_RESULTS_ABSTRACTS_TOGGLER`: Determines whether the user may toggle the
  display of abstracts on search results pages. Defaults to `True`.
* `KERKO_TITLE`: The title to display in web pages. Defaults to `'Kerko App'`.
* `KERKO_ZOTERO_BATCH_SIZE`: Number of items to request on each call to the
  Zotero API. Defaults to `100` (which is the maximum currently allowed by the
  API).
* `KERKO_ZOTERO_MAX_ATTEMPTS`: Maximum number of tries after the Zotero API
  has returned an error or not responded during indexing. Defaults to `10`.
* `KERKO_ZOTERO_WAIT`: Time to wait (in seconds) between failed attempts to
  call the Zotero API. Defaults to `120`.
* Localization-related variables:
  * `BABEL_DEFAULT_LOCALE`: The default language of the user interface. Defaults
    to `'en'`.
  * `BABEL_DEFAULT_TIMEZONE`: The timezone to use for user facing dates.
    Defaults to `'UTC'`.
  * `KERKO_WHOOSH_LANGUAGE`: The language of search requests. Defaults to
    `'en'`. You may refer to Whoosh's source to get the list of supported
    languages (`whoosh.lang.languages`) and the list of languages that support
    stemming (`whoosh.lang.has_stemmer()`).
  * `KERKO_ZOTERO_LOCALE`: The locale to use with Zotero API calls. This
    dictates the locale of Zotero item types, field names, creator types and
    citations. Defaults to `'en-US'`. Supported locales are listed at
    https://api.zotero.org/schema, under "locales".
* `KERKOAPP_COLLECTION_FACETS`: Defines facets modeled on Zotero collections.
  This variable should be a list of semicolon-delimited triples (collection key,
  facet weight and facet title, separated by colons). Each specified collection
  will appear in Kerko as a facet where subcollections will be represented as
  values within the facet. The weight determines a facet's position relative to
  the other facets. The value of `KERKOAPP_COLLECTION_FACETS` should be defined
  within a single string, on a single line.
* `KERKOAPP_EXCLUDE_DEFAULT_BADGES`: List of badges (identified by key) to
  exclude from those created by default. If that list contains the value '*', no
  badge will be created by default. Please refer to the implementation of
  `kerko.composer.Composer.init_default_badges()` for the list of default
  badges.
* `KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS`: List of citation download formats
  (identified by key) to exclude from those created by default. If that list
  contains the value '*', no citation format will be created by default. Please
  refer to the implementation of
  `kerko.composer.Composer.init_default_citation_formats()` for the list of
  default citation formats.
* `KERKOAPP_EXCLUDE_DEFAULT_FACETS`: List of facets (identified by key) to
  exclude from those created by default. If that list contains the value '*', no
  facet will be created by default. Please refer to the implementation of
  `kerko.composer.Composer.init_default_facets()` for the list of default
  facets.
* `KERKOAPP_EXCLUDE_DEFAULT_FIELDS`: List of fields (identified by key) to
  exclude from those created by default. If that list contains the value '*', no
  field will be created by default. Caution: some default fields are required by
  Kerko or by badges. If required fields are excluded, the application probably
  won't start. Please refer to the implementation of
  `kerko.composer.Composer.init_default_fields()` for the list of default
  fields.
* `KERKOAPP_EXCLUDE_DEFAULT_SCOPES`: List of scopes (identified by key) to
  exclude from those created by default. If that list contains the value '*', no
  scope will be added by default. Caution: most default fields are expecting one
  or more of those scopes to exist. If required scopes are excluded, the
  application probably won't start. Please refer to the implementation of
  `kerko.composer.Composer.init_default_scopes()` for the list of default
  scopes.
* `KERKOAPP_EXCLUDE_DEFAULT_SORTS`: List of sorts (identified by key) to exclude
  from those created by default. Caution: at least one sort must remain for the
  application to start. Please refer to the implementation of
  `kerko.composer.Composer.init_default_sorts()` for the list of default sorts.
* `KERKOAPP_MIME_TYPES`: List of allowed MIME types for attachments. Defaults to
  `"application/pdf"`.
* `KERKOAPP_ITEM_EXCLUDE_RE`: Regex to use to exclude items based on their tags.
  Any object that have a tag that matches this regular expression will be
  excluded. If empty (which is the default), no items will be excluded unless
  `KERKOAPP_ITEM_INCLUDE_RE` is set, in which case items that don't have any tag
  that matches it will be excluded.
* `KERKOAPP_ITEM_INCLUDE_RE`: Regex to use to include items based on their tags.
  Any object which does not have a tag that matches this regular expression will
  be excluded. If empty (which is the default), all items will be included
  unless `KERKOAPP_ITEM_EXCLUDE_RE` is set and causes some to be excluded.
* `KERKOAPP_TAG_EXCLUDE_RE`: Regex to use to exclude tags. The default value
  causes any tag that begins with an underscore ('_') to be ignored by Kerko.
  Note that citation exports (downloads) always include all tags regardless of
  this parameter, which only applies to information displayed by Kerko (exports
  are generated by the Zotero API, not by Kerko).
* `KERKOAPP_TAG_INCLUDE_RE`: Regex to use to include tags. By default, all
  tags are accepted. Note that citation exports (downloads) always include all
  tags regardless of this parameter, which only applies to information displayed
  by Kerko (exports are generated by the Zotero API, not by Kerko).
* `KERKOAPP_CHILD_EXCLUDE_RE`: Regex to use to exclude children (e.g. notes,
  attachments) based on their tags. Any child that have a tag that matches this
  regular expression will be ignored. If empty, no children will be rejected
  unless `KERKOAPP_CHILD_INCLUDE_RE` is set and the tags of those children
  don't match it. By default, any child having at least one tag that begins with
  an underscore ('_') is rejected.
* `KERKOAPP_CHILD_INCLUDE_RE`: Regex to use to include children (e.g. notes,
  attachments) based on their tags. Any child which does not have a tag that
  matches this regular expression will be ignored. If empty, all children will
  be accepted unless `KERKOAPP_CHILD_EXCLUDE_RE` is set and causes some to be
  rejected.
* `LOGGING_LEVEL`: Severity of events to track. Allowed values are `DEBUG`,
  `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Defaults to `DEBUG` if app is running
  in the development environment, and to `WARNING` in the production
  environment.

Note that some of Kerko's variables do not have a corresponding environment
variable in KerkoApp and therefore can only be set in Python from a custom
application.

If you are building your own application, you don't really need the above
environment variables. Instead, you could directly set Kerko variables in your
application's `Config` object and set arguments to `kerko.composer.Composer`'s
init method. In that case, please refer to [Kerko's documentation][Kerko] rather
than KerkoApp's.


## Configuration example

The `.env` file of the [demo site][KerkoApp_demo] looks like the following,
except for the private keys:

```
FLASK_APP=kerkoapp.py
FLASK_ENV=production
SECRET_KEY=XXXXX
KERKO_TITLE=Kerko Demo
KERKO_ZOTERO_API_KEY=XXXXX
KERKO_ZOTERO_LIBRARY_ID=2348869
KERKO_ZOTERO_LIBRARY_TYPE=group
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

- [Deploying KerkoApp on Ubuntu 20.04 with nginx and gunicorn](https://gist.github.com/davidlesieur/e1dafd09636a4bb333ad360e4b2c5d6d)


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
pybabel extract -F babel.cfg -o app/translations/messages.pot --project=KerkoApp --version=CURRENT_VERSION --copyright-holder="Kerko Contributors" app
```

Create a new PO file (for a new locale) based on the POT file. Replace
`YOUR_LOCALE` with the appropriate language code, e.g., `de`, `es`, `it`:

```bash
pybabel init -l YOUR_LOCALE -i app/translations/messages.pot -d app/translations
```

Update an existing PO file based on the POT file:

```bash
pybabel update -l YOUR_LOCALE -i app/translations/messages.pot -d app/translations
```

Compile MO files:

```bash
pybabel compile -l YOUR_LOCALE -d app/translations
```


## Contributing

### Reporting issues

For reporting an issue, please consider the following guidelines:

* Try to identify whether the issue belongs to [KerkoApp] or to [Kerko]. If
  unsure, check the list of features related to each package and try to
  determine which feature is the most related to the issue. Then you may submit
  the issue to [KerkoApp's issue tracker][KerkoApp_issues] if it is related to
  KerkoApp, or to [Kerko's issue tracker][Kerko_issues] otherwise.
* Make sure that the same issue has not already been reported or fixed in the
  repository.
* Describe what you expected to happen.
* If possible, include a minimal reproducible example to help others identify
  the issue.
* Describe what actually happened. Include the full traceback if there was an
  exception.


### Submitting code changes

Pull requests may be submitted against [KerkoApp's repository][KerkoApp]. Please
consider the following guidelines:

* Use [Yapf](https://github.com/google/yapf) to autoformat your code (with
  option `--style='{based_on_style: facebook, column_limit: 100}'`). Many
  editors provide Yapf integration.
* Include a string like "Fixes #123" in your commit message (where 123 is the
  issue you fixed). See [Closing issues using
  keywords](https://help.github.com/en/articles/closing-issues-using-keywords).


### Submitting a translation

Some guidelines:

* The PO file encoding must be UTF-8.
* The header of the PO file must be filled out appropriately.
* All messages of the PO file must be translated.

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

### No such command "kerko" error when running flask

You might have to set the `FLASK_APP` variable. Its value is normally picked up
from the `.env` file in the current working directory, but if that's not the
case you might need to set it directly in the environment.

Under Linux:

```bash
export FLASK_APP=kerkoapp.py
```

Under Windows:

```
set FLASK_APP=kerkoapp.py
```

### Errors when using the `master` version of Kerko

The `master` branch of KerkoApp is meant to work with the latest published
release of Kerko. If you have installed the `master` version of Kerko instead
its latest published release, use the `kerko-head` branch of KerkoApp instead of
`master`.


[Docker]: https://www.docker.com/
[Docker_docs]: https://docs.docker.com/
[Flask]: https://pypi.org/project/Flask/
[Flask_production]: https://flask.palletsprojects.com/en/1.1.x/deploying/
[Kerko]: https://github.com/whiskyechobravo/kerko
[Kerko_email]: mailto:kerko@whiskyechobravo.com
[Kerko_issues]: https://github.com/whiskyechobravo/kerko/issues
[Kerko_variables]: https://github.com/whiskyechobravo/kerko#configuration-variables
[KerkoApp]: https://github.com/whiskyechobravo/kerkoapp
[KerkoApp_demo]: https://demo.kerko.whiskyechobravo.com
[KerkoApp_issues]: https://github.com/whiskyechobravo/kerkoapp/issues
[Python]: https://www.python.org/
[venv]: https://docs.python.org/3.8/tutorial/venv.html
[Zotero]: https://www.zotero.org/
[Zotero_demo]: https://www.zotero.org/groups/2348869/kerko_demo/items
