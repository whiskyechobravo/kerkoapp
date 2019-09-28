# KerkoApp

[KerkoApp] is a web application using [Kerko] to provide a user-friendly
search and browsing interface for sharing a bibliography managed with the
[Zotero] reference manager. Built in [Python] with the [Flask] framework.

Although this application may be deployed as is on a web server, it is primarily
meant to serve as an example on how to integrate the Kerko blueprint in a Flask
application.

Basic configuration options can be set with environment variables, but for more
advanced customizations one should consider using Kerko's Python interface.


## Features

KerkoApp is just a thin container around Kerko. As such, almost all of its
features are inherited from Kerko. See [Kerko's documentation][Kerko] for the
list of features.

The main features added by KerkoApp are:

* Kerko configuration settings are read from environment variables or a `.env`
  file, adhering to the [Twelve-factor App](https://12factor.net/config)
  methodology.
* Extra environment variables provide quick shortcuts for:
    * defining facets based on Zotero collections;
    * filtering tags and notes (regular expressions for blacklisting and/or
      whitelisting);
    * excluding fields, facets, sort options or search scopes from Kerko's
      defaults.
* Templates for common HTTP errors.


## Demo site

A [KerkoApp demo site][KerkoApp_demo] is available for you to try. You may also
view the [Zotero library][Zotero_demo] that contains the source data for the
demo site.


## Getting started

This section presents two approaches to getting started with KerkoApp: running
from a standard installation of KerkoApp, or running from a Docker container
pre-built with KerkoApp. You may choose the one you are most comfortable with.


### Standard installation

This procedure requires Python 3.6 or later.

1. The first step is to install the software. As with any Python package, it is
   highly recommended to install it within a [virtualenv].

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
     able to access your Zotero library. See [Kerko's documentation on
     configuration variables][Kerko_variables] for details on how to properly
     set these variables.

   The **Example configuration** section below might give you additional tips.

4. Have KerkoApp retrieve your bibliographic data from zotero.org:

   ```bash
   flask kerko index
   ```

   If you have a large bibliography, this may take a while (and there is no
   progress indicator). In production use, that command is usually added to the
   crontab file for regular execution.

5. Run KerkoApp:

   ```bash
   flask run
   ```

6. Open http://localhost:5000/ in your browser and explore the bibliography.

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
     able to access your Zotero library. See [Kerko's documentation on
     configuration variables][Kerko_variables] for details on how to properly
     set these variables.

   The **Example configuration** section below might give you additional tips.

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
   make index
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


## Example configuration

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

The variables prefixed with `KERKO_` are described in [Kerko's
documentation][Kerko_variables], while those prefixed with `KERKOAPP_` are
specific to KerkoApp.

KerkoApp variables can be used in the `.env` file to exclude elements from
Kerko's default scopes (`KERKOAPP_EXCLUDE_DEFAULT_SCOPES`), fields
(`KERKOAPP_EXCLUDE_DEFAULT_FIELDS`), facets (`KERKOAPP_EXCLUDE_DEFAULT_FACETS`),
sort options (`KERKOAPP_EXCLUDE_DEFAULT_SORTS`) or citation download links
(`KERKOAPP_EXCLUDE_DEFAULT_CITATION_FORMATS`). Please refer to the
implementation of `kerko.composer.Composer` for more details on the defaults;
changing the default scopes and fields, in particular, should be done with care.
In the above example, `KERKOAPP_EXCLUDE_DEFAULT_FACETS` is used to exclude the
`'facet_tag'` and `'facet_link'` facets that Kerko would normally build by
default.

Another KerkoApp variable, `KERKOAPP_COLLECTION_FACETS`, may be used in the
`.env` file to define facets modeled on Zotero collections. It takes a list of
semicolon-delimited triples (collection key, facet weight and facet title,
separated by colons). Each specified collection is then represented as a facet
where subcollections are represented as values within the facet. The weight
determines a facet's position relative to the other facets. In the above
example, "7H2Q7L6I:120:Field of study" defines a facet based on the collection
whose key on zotero.org is _7H2Q7L6I_. That facet is given a weight of _120_,
which will position it under facets that have a lighter weight (smaller number),
and above those that have a heavier weight (larger number). The facet is also
given the title _Field of study_. The value of `KERKOAPP_COLLECTION_FACETS` is
defined within a single string that will be parsed by KerkoApp.

These variables cause changes to Kerko's search index. Changing any of those
values require that you rebuild Kerko's search index and restart your
application. To rebuild the index:

```bash
flask kerko clean
flask kerko index
```

Environment variables are just shortcuts for those who wish to use KerkoApp as
is, without changing any Python code. If you are building your own Kerko
application, you don't really need those variables. Instead, you may directly
specify arguments when instanciating the `kerko.composer.Composer` class, and
call `add_facet()` on the instance to specify additional facets.


## Translating KerkoApp

Note that Kerko and KerkoApp have separate translation files and that most
messages actually come from Kerko. For translating Kerko's messages, please
refer to [Kerko's documentation][Kerko].

KerkoApp can be translated with [Babel](http://babel.pocoo.org).

The following commands should be executed from the directory that contains
`babel.cfg`, and the appropriate [virtualenv] must have been activated
beforehand.

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

If you need professionnal support related to Kerko, have requirements not
currently implemented in Kerko, want to make sure that some Kerko issue
important to you gets resolved, or if you just like our work and would like to
hire us for an unrelated project, please [e-mail us][Kerko_email].


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

### Errors when using the HEAD version of Kerko

The `master` branch of KerkoApp is meant to work with the latest published
release of Kerko. If you have installed the HEAD version of Kerko, use the
`kerko-head` branch of KerkoApp instead of `master`.


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
[virtualenv]: https://virtualenv.pypa.io/en/latest/
[Zotero]: https://www.zotero.org/
[Zotero_demo]: https://www.zotero.org/groups/2348869/kerko_demo/items
