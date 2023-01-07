import json, sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# Home
@app.route('/')
def index():
  return render_template('pages/home.html')



#  Venues

#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # get all aggregate locations
    locations = Venues.query(Venues.city, Venues.state).group_by(Venues.city, Venues.state).all()

    # list of locations and their venues
    group_venues = list()

    for location in locations:
        location_venues = { {   "id": venue.id,
                                "name": venue.name, 
                                "num_upcoming_shows": len(db.session.query(Shows).all())} 
                            for venue in 
                            Venues.query.filter(Venues.state==location.state,Venues.city==location.city).all() }
        group_venues.append({
            'city' : location.city,
            'state' : location.state,
            'venues' : location_venues
        })

    return render_template('/pages/venues.html', areas = group_venues)