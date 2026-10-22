# Fyyur

Fyyur is a server-rendered booking site where local musical venues and performing artists list themselves, find each other, and publish shows. Venue owners and artists use it to post a profile, search by name, and record a booking with a start time. This repository is the Fyyur project from Udacity's Full Stack Web Developer Nanodegree (`projects/01_fyyur` in the course starter). The starter supplies the Jinja pages and layout. The work here is the PostgreSQL schema, the Flask routes that read and write it, and a production configuration for Vercel.

## Features

- Venues are listed in groups by city and state. Artists are listed by name. Shows are listed with the artist, the venue, and a formatted start time.
- Venues and artists can be created and edited. Forms cover name, city, state, phone, genres, image, website, Facebook link, and whether the listing is seeking talent (venues) or a venue (artists).
- Venue creation runs the `VenueForm` validators: required name, city, state, address, and genres, plus a URL check on the Facebook link. Genres are a fixed multi-select stored as a PostgreSQL string array.
- Venue and artist search accepts a partial name and matches it case-insensitively with SQL `ILIKE`. Results show the match count and the matching names.
- A venue page loads that venue and splits its shows into upcoming and past by comparing `Show.time` with the current time. An artist page renders the same two sections from that artist's shows.
- A show is created from an artist id, a venue id, and a start time.
- `DELETE /venues/<venue_id>` removes a venue. Create, update, and delete flash a success or error message.
- Unknown routes and server errors render the 404 and 500 templates.

## Tech stack

**Backend**

- Python 3.11 (`runtime.txt`)
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5 and PostgreSQL via psycopg2-binary 2.9.7
- Flask-Migrate 4.0.5 (Alembic), initialized with `compare_type=True`
- Flask-WTF 1.1.1 and WTForms 3.0.1
- Babel 2.12.1 and python-dateutil 2.8.2, used by the `datetime` Jinja filter
- Flask-Moment 1.0.5, initialized on the app

**Frontend**

- Jinja2 templates under `templates/`
- Bootstrap 3, jQuery 1.11, Moment.js, Modernizr, and Font Awesome, vendored in `static/`
- Show times rendered with the Babel `datetime` filter (`full` and `medium` patterns, `en` locale)

## Architecture

One Flask app. Models, forms, and routes live in separate modules. `app.py` selects `config_prod` when `VERCEL_ENV` is `production` and `config` otherwise.

| Path | Role |
| --- | --- |
| `app.py` | Routes, error handlers, flash messages, logging to `error.log` when debug is off, and the `datetime` filter. `python app.py` starts the development server. |
| `models.py` | `Venues`, `Artists`, and `Shows`. Genres use `db.ARRAY(db.String())`. Each venue and artist declares a relationship to `Show`. |
| `forms.py` | `VenueForm`, `ArtistForm`, and `ShowForm`. State is a select of US abbreviations. Genres are a multi-select. |
| `config.py` | Local settings, including `SQLALCHEMY_DATABASE_URI` and `DEBUG = True`. |
| `config_prod.py` | Production settings read from the environment. |
| `api/index.py` | Imports the Flask app for Vercel. |
| `vercel.json` | Builds `api/index.py` with `@vercel/python` and routes every path to it. |
| `templates/pages/` | Home, listings, search results, and detail pages. |
| `templates/forms/` | Create and edit forms for venues, artists, and shows. |
| `templates/layouts/` | Shared shell, navigation, and search boxes. |
| `templates/errors/` | 404 and 500 pages. |
| `static/` | CSS, JavaScript, fonts, and images. |

`app2.py` is an unfinished alternate of the venue listing. The running application is `app.py`, which `api/index.py` imports.

A show row stores `artist_id`, `venue_id`, and `time`. Venue and artist models point back at their shows, and the listing and detail handlers join through those relationships to read a name and an image.

## Getting started

### Prerequisites

- Python 3.11
- PostgreSQL
- pip

### Install

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

On Windows, activate the environment with `env\Scripts\activate`.

### Configuration

Local runs read `config.py`. Point `SQLALCHEMY_DATABASE_URI` at a PostgreSQL database you can write to. `SECRET_KEY` is generated with `os.urandom` when the process starts.

`.env.example` names the production variables. This project does not depend on python-dotenv, so a local `.env` file is not loaded. Production reads the environment only after `VERCEL_ENV` selects `config_prod.py`.

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string. A `postgres://` URL is rewritten to `postgresql://` for SQLAlchemy. |
| `SECRET_KEY` | Flask session and form secret. If it is unset, the process generates one. |
| `DEBUG` | `true` turns debug on. Any other value leaves it off. |
| `VERCEL_ENV` | `production` loads `config_prod.py`. |

### Create the schema

`migrations/` is listed in `.gitignore`, so a clone does not include an Alembic revision. After the database exists and `SQLALCHEMY_DATABASE_URI` is set:

```bash
export FLASK_APP=app
flask db init
flask db migrate -m "initial schema"
flask db upgrade
```

### Run

```bash
python app.py
```

The development server listens on `http://127.0.0.1:5000/`.

The model classes in `models.py` are `Venues`, `Artists`, and `Shows`. Most handlers in `app.py` still refer to `Venue`, `Artist`, and `Show`. Show foreign keys reference `artist.id` and `venue.id`, while the table names are `artists` and `venues`. Those names have to agree before the routes can query PostgreSQL.

There is no application test suite in the repository. `fabfile.py` is leftover starter Fabric code whose test modules and Heroku targets are absent here, so it is outside this setup.

## Deployment

The repo is configured for Vercel as a Python serverless function.

- `runtime.txt` selects Python 3.11.
- `vercel.json` sends traffic to `api/index.py`.
- `api/index.py` exposes the Flask `app` object.
- Set `DATABASE_URL`, `SECRET_KEY`, and `DEBUG` on the host. Vercel sets `VERCEL_ENV`.

This repository does not record a live deployment URL. Apply the schema to the database behind `DATABASE_URL` on first deploy, using the Flask-Migrate commands above with production config selected.

## Project status

Coursework, for the Fyyur project in Udacity's Full Stack Web Developer Nanodegree. The pages, layout, form markup, and original assignment notes came with the starter. This repository adds the SQLAlchemy models, the create, edit, list, search, and show handlers, and the Vercel production config.

`.github/workflows/manual.yml` is the course workflow. On an opened pull request it files a Jira ticket. It does not build or test the app.

The assignment's optional extras — artist availability windows, a homepage of the ten newest listings, and search by city and state — are not in this code. Name search is what the `/venues/search` and `/artists/search` handlers implement.

## What this demonstrates

- A booking domain modeled in PostgreSQL: a venue and an artist each carry location, contact details, genres, and a seeking flag, and a show links one artist to one venue at a start time.
- SQLAlchemy relationships and a Postgres array column for multi-valued genres, with Flask-Migrate set up to compare column types when generating migrations.
- Server-rendered list, search, create, and edit flows whose query results match the dictionaries the existing Jinja pages render, including WTForms checks and flash feedback.
- A custom Babel datetime filter so show times render in a readable locale format from stored timestamps.
- Environment-specific configuration, including the `postgres://` to `postgresql://` rewrite, and a thin `api/index.py` entry so the same Flask app is the Vercel WSGI callable.
- Separation of models, forms, and controllers across `models.py`, `forms.py`, and `app.py`.

## License

The starter materials are Udacity educational content. Terms are in `LICENSE.txt`.
