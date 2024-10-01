# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



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
#Start at the homepage.
#List all the available routes.
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<start><br/>"
        f"/api/v1.0/start<start>/end<end>"

    )

#Convert the query results from your precipitation analysis     
    # (i.e. retrieve only the last 12 months of data) to a  
    # dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)    
    one_year_data =session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= one_year_prior).all()
    precipitation_dict = {}
    for date, prcp in one_year_data:
       precipitation_dict[date] = prcp
    return jsonify(precipitation_dict)


#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station_list():
    station = session.query(Station.station).all()
    
    station_list = list(np.ravel(station))
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
#Query the dates and temperature observations of the    
    # most-active station for the previous year of data.
#Return a JSON list of temperature observations for the     
    # previous year.
def most_active():  
    one_year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)
    one_year_prior
    most_active = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= one_year_prior)
    most_active_data= []
    for date, tobs in most_active: 
        most_active_dict = {}
        most_active_dict["date"]= date
        most_active_dict["temperature"]= tobs
        most_active_data.append(most_active_dict)
    session.close()
    return jsonify(most_active_data)
    
       

@app.route("/api/v1.0/<start>")
#Return a JSON list of the minimum temperature, the average temperature,    
    # and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the  
    # dates greater than or equal to the start date.
def temp_start (start):
    results = session.query(    
        func.min(Measurement.tobs).label('TMIN'),   
        func.avg(Measurement.tobs).label('TAVG'),
        func.max(Measurement.tobs).label('TMAX')

    ).filter(Measurement.date >= start).all()
    temperature_data = {    
        'TMIN': results[0].TMIN, 
        'TAVG': results[0].TAVG,
        'TMAX': results[0].TMAX
    }
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>/<end>")
#Return a JSON list of the minimum temperature, the average temperature,    
    # and the maximum temperature for a specified start or start-end range.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX    
    # for the dates from the start date to the end date, inclusive.
def temp_start_end (start, end):
    results = session.query(    
        func.min(Measurement.tobs).label('TMIN'),   
        func.avg(Measurement.tobs).label('TAVG'),
        func.max(Measurement.tobs).label('TMAX')

    ).filter(Measurement.date >= start, Measurement.date <= end).all()
    temperature_data = {    
        'TMIN': results[0].TMIN, 
        'TAVG': results[0].TAVG,
        'TMAX': results[0].TMAX
    }
    return jsonify(temperature_data)

session.close()
if __name__ == "__main__":
    app.run(debug=True)