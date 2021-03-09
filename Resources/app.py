import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#############################################################
#Database Setup
#############################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect on existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measure = Base.classes.measurement
Stat = Base.classes.station
# create our session link from python to the DB
session = Session(engine)
########################################################
# Flask Setup
########################################################

app = Flask(__name__)

@app.route('/')
def welcome():
    """List all routes that are available."""
    return (
        f"Welcome to the climate Analysis API!<br/>"
        f"Here are available API routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end>"
        f"/api/v1.0/"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
  
    # Query measurement table to return date and prcp data
    measure_qry = session.query(Measure.date, Measure.prcp).filter(Measure.date>="2016-08-23").all()
    
    prcp_dict = list(np.ravel(measure_qry))
    """ return the precipitation and date dictionary as Json """
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
  
    # Query station table and return list of station
    stat_qry = session.query(Stat.station).all()

    station_lst = list(np.ravel(stat_qry))
    """ return the station list as Json """
    return jsonify(station_lst)

@app.route("/api/v1.0/tobs")
def tobs():
  
    # Query dates and temperature observations for most active station for last year 
    temp_qry = session.query(Measure.station, Measure.tobs, Measure.date ).filter(Measure.station == 'USC00519281').filter(Measure.date >= "2016-08-23").all()

    temp_lst = list(np.ravel(temp_qry))
    """ return the Json list of temperature observation """
    return jsonify(temp_lst)

@app.route("/api/v1.0/temp/<start>")
def start():
    # Query to get minimum, average and maximum temperature for a given start-end range

    temp=session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).filter(Measure.station==activestation[0][0])
    temp[0][0], temp[0][1], temp[0][2]

    """ return the Json list of temperature for a given start-end range"""
    temp_info = start.replace(" ", "").lower()
    for temperature in temp:
        search_temp = temperature["start"].replace(" ", "").lower

        if search_temp == temp_info:
            return jsonify(temperature)

if __name__ == "__main__":
    app.run(debug=True)

