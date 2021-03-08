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
measure = Base.classes.measurement
stat = Base.classes.station

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
        f"/api/v1.0/measurement<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/measurement")
def measurement():
    # create our session link from python to the DB
    session = Session(engine)
    # Query all measurement
    measure_qry = session.query(measure).all()

    session.close()

    measure_lst = list(np.ravel(measure_qry))
    return jsonify(measure_lst)

@app.route("/api/v1.0/prcp")
def prcp():
    # create our session link from python to the DB
    session = Session(engine)
    # Query all measurement
    prcp_qry = session.query(measure.prcp).all()

    session.close()

    prcp_lst = list(np.ravel(prcp_qry))
    return jsonify(prcp_lst)


@app.route("/api/v1.0/station")
def station():
    # create our session link from python to the DB
    session = Session(engine)
    # Query all station
    station_qry = session.query(stat).all()

    session.close()

    station_lst = list(np.ravel(station_qry))
    return jsonify(station_lst)

@app.route("/api/v1.0/tobs")
def tobs():
    # create our session link from python to the DB
    session = Session(engine)
    # Query all station
    temp_qry = session.query(tobs).all()

    session.close()

    temp_lst = list(np.ravel(temp_qry))
    return jsonify(temp_lst)

if __name__ == "__main__":
    app.run(debug=True)
