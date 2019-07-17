# KerkoApp

[KerkoApp] is a sample web application using [Kerko] to provide a user-friendly
search and browsing interface for sharing a bibliography managed with the
[Zotero] reference manager. Built in [Python] with the [Flask] framework.

This application is meant to serve as an example on how to integrate the Kerko
blueprint in a Flask application. It also shows how to create additional facets
not provided by Kerko, such as facets based on Zotero collections.


## Features

KerkoApp is just a thin container around Kerko. As such, almost all of its
features are inherited from Kerko. See [Kerko's documentation][Kerko] for the
list of features.

The main features added by KerkoApp are:

* Kerko configuration settings are read from environment variables.
* Configuration settings may be stored in a `.env` file. Configuration therefore
  adheres to the [Twelve-factor App](https://12factor.net/config) methodology.
* Templates for common HTTP errors.


## Demo site

A [KerkoApp demo site][KerkoApp_demo] is available for you to try. You may also
view the [Zotero library][Zotero_demo] that contains the source data for the
demo site.


## Requirements

KerkoApp requires Python 3.6 or later.

It has only been tested under Linux (so far). If you run it on other platforms,
(with or without encountering compatibility issues), please [let us
know][KerkoApp_issues].


## Installation

1. The first step is to install the software. As with any Python package, it is
   highly recommended to install it within a [virtualenv].

   ```bash
   git clone https://github.com/whiskyechobravo/kerkoapp.git
   cd kerkoapp
   pip install -r requirements/run.txt
   ```

   This will install many packages required by Kerko or KerkoApp.

2. In the same directory (the one that contains `kerkoapp.py`), create a `.env`
   file with the desired settings. For example:

   ```
   FLASK_APP=kerkoapp.py
   FLASK_ENV=development
   SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   KERKO_ZOTERO_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
   KERKO_ZOTERO_LIBRARY_ID=9999999
   KERKO_ZOTERO_LIBRARY_TYPE=group
   KERKO_TITLE="My bibliography"
   ```

   The `SECRET_KEY` variable is required for generating secure tokens in web
   forms. It should be a secure, random value and it really has to be secret.
   Never add your `.env` file to a code repository.

   The `KERKO_ZOTERO_API_KEY`, `KERKO_ZOTERO_LIBRARY_ID` and
   `KERKO_ZOTERO_LIBRARY_TYPE` variables are required for Kerko to be able to
   access your Zotero library. See [Kerko's documentation on configuration
   variables][Kerko_variables] for more details. See also the **Example
   configuration** section below.

3. Have Kerko retrieve your bibliographic data from zotero.org. If you have a
   large bibliography, this may take a while (and there is no progress
   indicator):

   ```bash
   flask kerko index
   ```

   In production use, that command is usually added to the crontab file for
   regular execution.

4. Run your application:

   ```bash
   flask run
   ```

5. Open http://127.0.0.1:5000/ in your browser and explore the bibliography.


## Example configuration

The `.env` file of the [demo site][KerkoApp_demo] looks like the following,
except for the private keys:

```
FLASK_APP=kerkoapp.py
FLASK_ENV=production
SECRET_KEY=XXXXX
KERKO_TITLE="Kerko Demo"
KERKO_ZOTERO_API_KEY=XXXXX
KERKO_ZOTERO_LIBRARY_ID=2348869
KERKO_ZOTERO_LIBRARY_TYPE=group
KERKO_CSL_STYLE=apa
KERKO_PRINT_ITEM_LINK=True
KERKO_PRINT_CITATIONS_LINK=True
KERKOAPP_EXCLUDE_DEFAULT_FACETS=facet_tag,facet_link
KERKOAPP_COLLECTION_FACETS="KY3BNA6T:110:Topic; 7H2Q7L6I:120:Field of study; JFQRH4X2:130:Type of contribution"
```

The variables prefixed with `KERKO_` are described in [Kerko's
documentation][Kerko_variables], while those prefixed with `KERKOAPP_` are
specific to KerkoApp.

KerkoApp variables can be used in the `.env` file to exclude elements from
Kerko's default scopes (`KERKOAPP_EXCLUDE_DEFAULT_SCOPES`), fields
(`KERKOAPP_EXCLUDE_DEFAULT_FIELDS`), facets (`KERKOAPP_EXCLUDE_DEFAULT_FACETS`)
or sort options (`KERKOAPP_EXCLUDE_DEFAULT_SORTS`). Please refer to the
implementation of `kerko.composer.Composer` for more details on the defaults;
changing the default scopes and fields, in particular, should be done with care.
In the above example, `KERKOAPP_EXCLUDE_DEFAULT_FACETS` is used to exclude the
`'facet_tag'` and `'facet_link'` facets that Kerko would normally build by
default.

Another KerkoApp variable, `KERKOAPP_COLLECTION_FACETS`, may be used in the
`.env` file to define facets modeled on Zotero collections. It takes a list of
semicolon-delimited triples (collection key, facet weight and facet title,
separated by colons). Each specified collection is then represented as a facet
where subcollections are represented as values within the facet.

These variables cause changes to Kerko's search index. Changing any of those
values require that you rebuild Kerko's search index and restart your
application. To rebuild the index:

```bash
flask kerko clean
flask kerko index
```

KerkoApp variables are just shortcuts for those who wish to use KerkoApp as is,
without changing any Python code. If you are building your own Kerko
application, you don't really need those variables. Instead, you may directly
specify arguments when instanciating the `kerko.composer.Composer` class, or
directly call `kerko.composer.Composer.add_facet()` on the instance to specify
additional facets.



[Flask]: https://pypi.org/project/Flask/
[Kerko]: https://github.com/whiskyechobravo/kerko
[Kerko_variables]: https://github.com/whiskyechobravo/kerko#configuration-variables
[KerkoApp]: https://github.com/whiskyechobravo/kerkoapp
[KerkoApp_demo]: https://demo.kerko.whiskyechobravo.com
[KerkoApp_issues]: https://github.com/whiskyechobravo/kerkoapp/issues
[Python]: https://www.python.org/
[Zotero]: https://www.zotero.org/
[Zotero_demo]: https://www.zotero.org/groups/2348869/kerko_demo/items
