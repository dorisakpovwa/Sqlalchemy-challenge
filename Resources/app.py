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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # create our session link from python to the DB
    session = Session(engine)
    # Query measurement table to return date and prcp data
    measure_qry = session.query(Measure.date, Measure.prcp).filter(Measure.date>="2016-08-23").all()

    session.close()
    #create dictionary to hold the data
    prcp_dict ={}
    for date, prcp in measure_qry:
        prcp_dict[date]=prcp
    """ return the precipitation and date dictionary as Json """
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # create our session link from python to the DB
    session = Session(engine)
    # Query station table and return list of station
    stat_qry = session.query(Stat.station).all()
    
    session.close()
    
    station_lst = list(np.ravel(stat_qry))
    """ return the station list as Json """
    return jsonify(station_lst)

@app.route("/api/v1.0/tobs")
def tobs():
    # create our session link from python to the DB
    session = Session(engine)
    # Query dates and temperature observations for most active station for last year 
    temp_qry = session.query(Measure.station, Measure.tobs, Measure.date ).filter(Measure.station == 'USC00519281').filter(Measure.date >= "2016-08-23").all()
    
    session.close()
    
    temp_lst = list(np.ravel(temp_qry))
    """ return the Json list of temperature observation """
    return jsonify(temp_lst)

    # Query to get minimum, average and maximum temperature for a given start date
@app.route("/api/v1.0/<start>")
def statdate(start):
    # create our session link from python to the DB
    session = Session(engine)
    temp=session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).filter(Measure.date >= start).all()
    
    session.close()
    
    temps={}
    for date in temp:
        
        temps[date[0]]={"min": date[0], "max":round(date[1], 0), "avg": round(date[2], 0)}
    """ return the Json list of min, max and avg temperatures for a given start date"""    
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    # create our session link from python to the DB
    session = Session(engine)
    # Query to get minimum, average and maximum temperature for a given start-end range

    temp2=session.query(func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)).filter(Measure.date >= start, Measure.date <= end).all()
    
    session.close()
    
    temps2={}
    for dat in temp2:

        temps2[dat[0]]={"min": dat[0], "max":round(dat[1], 0), "avg": round(dat[2], 0)}
    """ return the Json list of min, max and avg temperatures for a given start-end range"""  
    return jsonify(temps2)


if __name__ == "__main__":
    app.run(debug=True)

