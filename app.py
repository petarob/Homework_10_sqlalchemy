import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"AVAILABLE API ROUTES:<br/><br/>"
        f"<strong>Find precipitation data here</strong><br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"<strong>Link to list of field stations here</strong><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"<strong>Link to list to last year of temperatures</strong><br/>"
        f"/api/v1.0/tobs<br><br/>"
        f"<strong>Link to minimum, average, and maximum temperatures - but did not incorporate a start date</strong><br/>"
        f"/api/v1.0/start<br><br/>"
        F"<strong>This Link does not work</strong><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all locations of measuring stations across Hawaii"""
    # Query all stations
    session = Session(engine)
    stations = session.query(Station.name).all()
    station_names = list(np.ravel(stations))
    return jsonify(stations)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return rainfall amounts by date"""
    # Query
    session = Session(engine)
    precip = session.query(Measurement.date, Measurement.prcp).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_precip = []
    for date, prcp in precip:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precip.append(precipitation_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperture observation for last year"""
    # Query
    session = Session(engine)
    tobs = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >='2016-08-23').all()
    temps = list(np.ravel(tobs))
       
    return jsonify(tobs)


@app.route("/api/v1.0/start")
def start():
    """Return TMIN TMAX TAVG for all dates from the start date"""
# Query
    session = Session(engine)
    start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date).all()
    various = list(np.ravel(start))

    return jsonify(start)

if __name__ == '__main__':
    app.run(debug=True)