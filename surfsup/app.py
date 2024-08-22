# Import the dependencies.

from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from today
    last_year = dt.datetime.now() - dt.timedelta(days=365)

    # Query the precipitation data for the last year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

    # Create a dictionary with date as the key and precipitation as the value
    precip_data = {date: prcp for date, prcp in results}

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    # Query all the stations from the database
    results = session.query(Station.station).all()

    # Convert the results into a list
    stations_list = [station for station, in results]

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 1 year ago from today
    last_year = dt.datetime.now() - dt.timedelta(days=365)

    # Query the temperature observations (tobs) for the most active station for the last year
    results = session.query(Measurement.date, Measurement.tobs).filter(
    Measurement.station == 'USC00519281').filter(Measurement.date >= last_year).all()

    # Create a list of dictionaries for each observation
    tobs_data = {date: tobs for date, tobs in results}

    return jsonify(tobs_data)


if __name__ == '__main__':
    app.run(debug=True)