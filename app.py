import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask dependencies
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
	# Create our session from Python to the DB
	session = Session(engine)

    # Get precipitation info from DB
	results = session.query(Measurement.date, Measurement.prcp).all()

	session.close()

	precipitation = []
	for date, prcp in results:
		prcp_dict = {}
		prcp_dict[date] = prcp
		precipitation.append(prcp_dict)

	return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
	session = Session(engine)

    # Get precipitation info from DB
	results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.id, 
		Station.elevation).all()

	session.close()

	station_data = []
	for station, name, latitude, longitude, id, elevation in results:
		station_dict = {}
		station_dict["station"] = station
		station_dict["name"] = name
		station_dict["latitude"] = latitude
		station_dict["longitude"] = longitude
		station_dict["id"] = id
		station_dict["elevation"] = elevation
		station_data.append(station_dict)

	return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
	session = Session(engine)

	# Get last date in database
	get_last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	last_date = get_last_date.date

	# Get a year earlier
	year_before = dt.date.fromisoformat(last_date) - dt.timedelta(days=365)


	results = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(
		func.count(Measurement.id).desc()).first()
	station = results.station

	results = session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.station == station).filter(Measurement.date >= year_before).all()

	session.close()

	tobs_data = []
	for date, tobs, station in results:
		tobs_dict = {}
		tobs_dict["date"] = date
		tobs_dict["tobs"] = tobs
		tobs_dict["station"] = station
		tobs_data.append(tobs_dict)

	return jsonify(tobs_data)

@app.route("/")
def welcome():
    return (f'<h1>Available Routes</h1>'
    	f'<p><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br />'
    	f'<ul><li>Queries precipitation by date</li></ul></p>'
    	f'<p><a href="/api/v1.0/stations">/api/v1.0/stations</a><br />'
    	f'<ul><li>Queries station data</li></ul></p>'
    	f'<p><a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br />'
    	f'<ul><li>Queries temperature data over the last year in the database at the most popular station</li></ul></p>'

    )


if __name__ == "__main__":
	app.run(debug=True)
