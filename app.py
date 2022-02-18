# import other dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask Dependency
from flask import Flask, jsonify

# PRECTICING FLASK APP
# Adding first Flask app instance
# app = Flask(__name__)

# # Creating the first route (or root)
# @app.route('/')
# def hello_world():
#     return 'Hello world'

# Set up Database engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()

Base.prepare(engine, reflect = True)

# Save our references to each table as a variable
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)

# Define our Flask app-- create a Flask application called 'app'
app = Flask(__name__)

# # Define the welcome route
@app.route("/")
# # Create a function
def welcome():
     return (
    f'Welcome to the Climate Analysis API!<br/>'
    f'Available Routes:<br/>'
    f'/api/v1.0/precipitation<br/>'
    f'/api/v1.0/stations<br/>'
    f'/api/v1.0/tobs<br/>'
    f'/api/v1.0/temp/start/end'
    )

# Create a route for precipitation data
@app.route("/api/v1.0/precipitation")
# Create the precipitation() function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
         filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


# Create a route for the stations data
@app.route("/api/v1.0/stations")
# Create a function for stations()
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations = stations)


# Create a route for the temperature observation data
@app.route("/api/v1.0/tobs")
# Create a function called temp_monthly()
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps = temps)

# Create route for the statistics info
## We need to create a starting and ending date 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Create a function called stats()
def stats(start = None, end = None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps = temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps= temps)

