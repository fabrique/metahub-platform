# MetaHub online collection

This is the readme for MetaHub online collection. Use this to get started,
but don't forget to update these instructions when you change and add stuff.

## Setting up this project for development

To get this project up and running locally for development, do the following
in the directory you want the project to be in:

```bash
$ mkdir metahub  # this can be anything you want, it's not in git
$ cd metahub

$ git clone git@bitbucket.org:fabrique/<name-of-repo>.git src

```

> Note: the `src` directory can be called anything you like, but the convention is `src`.
 All other instructions assume `src`.

Next, execute the following commands:
```bash
cd src
python3 bootstrap.py
```
> It doesn't matter which python version you use to run this, it is compatible with both
2.7+ and 3.6+.
The project itself requires Python 3.6+, bootstrap will check this requirement.

This will setup the virtual environment, yarn/webpack, the database and a superuser.

> Powerusers: check the command line options for the bootstrap command and the generated .env file.

Make sure your editor picks up the `.editorconfig` and the `.eslintrc` files.

## Running the project
This project does not use webpack but uses the Design System and Starling. It also makes use of ElasticSearch.

To run the development server on port 8080:
```bash
$ python src/manage.py runserver 0.0.0.0:8080
```

To update and run the Design System frontend:
```bash
$ cd src/frontend
$ yarn
$ node sonic
```

A `.node-version` is present in this folder and if you have nodenv, it should set the right version automatically.
Running `node sonic` will also serve the static templates on port 8000.


In another terminal window, set up ElasticSearch with evm:
```bash
evm 6.4.2
```

> *NOTE*: According to the (https://www.elastic.co/support/matrix#matrix_jvm)[support matrix], 6.4.x only works on OpenJDK10. If you have OpenJDK 11, try `evm 6.5.4`.
> If you have a newer version of OpenJDK, install v11 via `brew tap AdoptOpenJDK/openjdk; brew cask install adoptopenjdk11`, then reinstall the version you have via `brew cask install adoptopenjdkXX` and immediately uninstall the newer version after via `brew cask uninstall adoptopenjdkXX`.

Also make sure that you copy over env.example, it contains the index variable that is needed.
If it's the first time, also build the search index through the manage command:
We do not use the integrated search that comes with Wagtail but elasticsearch-dsl
```bash
$ python src/manage.py search_index --create
```

After a `git pull`, don't forget to run the following command:
```bash
$ python src/manage.py update
```
This will update pip, migrate and compilemessages, bringing the local
environment up to date with the changes you just pulled.


## .gitignore
One of the nice things of not having the git root the same as the project root,
is that most things that are not in git are simply placed outside the git root.
There are exceptions though, like python binary files (`.pyc`) and gettext
`.mo` and `.pot` files.

If you have (IDE) specific files that should end up in git, _don't_ add them
to this `.gitignore`!
Use your local setup to ignore those globally, as explained in
[the git documentation](https://git-scm.com/docs/gitignore).

## Deploying

For deployment, there is a management command.

You can specify the environment (default is `staging`) and the
branch (default is `develop` for staging, `master` for production).

```bash
$ python src/manage.py deploy <environment>
```

For all options, run
```bash
$ python src/manage.py help deploy
```

The environments are managed in the `development.py` settings under `DEPLOY_CONFIGURATION`.

## Project structure
The basic project structure is as follows:

```
    metahub  # this can be anything you want, it's not in git
    ├── assets  # compiled static files
    ├── mail    # development mail folder
    ├── media   # media folder
    ├── ...     # other non-git folders
    ├── src     # this is the git root, name 'src' is recommended but can be anything
    |   ├── conf            # server config
    |   ├── requirements    # requirements for dev and production
    |   ├── frontend        # design system frontend folder
    |   ├──
    |   ├── metahub
    |   |   ├── ...        # apps for this project
    |   |   ├── assets     # uncompiled assets (sass, js, etc.)
    |   |   ├── locale     # labels and translations
    |   |   ├── settings   # settings, split for devevelopment and production
    |   |   ├── static     # ready-to-use assets (fonts, images, etc.)
    |   |   ├── templates  # template folder for all apps in this project
    |   |   ├── wsgi.py
    |   |   └── urls.py
    |   ├── .editorconfig   # activate this in your editor to enforce the right code styles
    |   ├── .eslintrc       # make sure your editor picks this up as well
    |   ├── .gitignore      # don't put IDE specific things in here
    |   ├── env.example     # example .env file to use as a start on the server (or locally)
    |   ├── bootstrap.py    # used to setup project locally
    |   ├── manage.py       # your friend
    |   ├── README.md       # this file
    |   └── ...             # other frontend config files
    ├── venv    # local virtual env (optional, can be outside project)
    ├── .env    # local .env
    └── ...     # other non-git files
```


## Other settings
### `env.example`?
Yes, this is an example file for `django-environ`. On the production server, rename this
file to `.env` and put specific settings in there (passwords etc.).

The idea is that these settings should not be put into version control. Read more about
this at [12-Factor](http://12factor.net/) and [django-environ](https://github.com/joke2k/django-environ)
It is also very explicit about which settings can be changed in which environment.

### Where's my `localsettings.py`?
You probably won't need it, since everyone shares the same development settings
(in `metahub/settings/development.py`).
You can tweak some settings in your local version of the `.env` file (like `DATABASE_URL`).

If you really want to, you can put your local settings in `metahub/settings/local.py`.

This file is ignored by git, and is only included in development settings if it exists.
On the staging and production environment, all local settings should be configured
through the `.env` file.

### Email Server
In development, we don't necessarily want to send e-mails, just check that they contain
the correct information.
This is why by default, sending mail with development settings will use Django's EmailFileBackend.

Development mail is stored in the `/email/` folder (outside git root).

### Sentry
Sentry is enabled by default but only on production. You still need to add the relevant
config to link the server with the client. Add this config in the `env` file on the server.

### Credentials
Don't forget to add all credentials you create (secret key, databases, sentry config, etc.) to
LastPass for future reference. **Never put them in git!**


