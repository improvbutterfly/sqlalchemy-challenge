import numpy as np
import datetime as dt

# Import regular expression package to check date in search
import re

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

@app.route("/api/v1.0/<start>")
def date_begin(start):
	session = Session(engine)

	# Get last date in database
	get_last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	last_date = get_last_date.date

	# Get first date in database
	get_first_date = session.query(Measurement.date).order_by(Measurement.date).first()
	first_date = get_first_date.date

	session.close()

	# Check if start is actually a date. 
	if re.fullmatch(r'\d\d\d\d-\d\d-\d\d',start):
		# Check if start is within the dates in the database
		if (dt.datetime.strptime(start, "%Y-%m-%d") >= dt.datetime.strptime(first_date, "%Y-%m-%d")) and \
		(dt.datetime.strptime(start, "%Y-%m-%d") <= dt.datetime.strptime(last_date, "%Y-%m-%d")):
			# Now we can perform the search in the databse. Start a new session.
			session = Session(engine)
			results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
			filter(Measurement.date >= start).all()
			session.close()

			# Put results in dictionary
			tobs_data = []
			for min_temp, max_temp, avg_temp in results:
				tobs_dict = {}
				tobs_dict["start date"] = start
				tobs_dict["end date"] = last_date
				tobs_dict["min temp"] = min_temp
				tobs_dict["max temp"] = max_temp
				tobs_dict["avg temp"] = avg_temp
				tobs_data.append(tobs_dict)

			return jsonify(tobs_data)
#			return start

		# If start not in database date range, return an error.
		return jsonify({"error": f"{start} is not in database date range. Must be between {first_date} and {last_date}"}), 404


	# If start not a date or correct format, return an error.
	return jsonify({"error": f"{start} is not a date or in correct format. Date should be YYYY-MM-DD"}), 404


@app.route("/")
def welcome():
	session = Session(engine)

	# Get last date in database
	get_last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	last_date = get_last_date.date

	# Get first date in database
	get_first_date = session.query(Measurement.date).order_by(Measurement.date).first()
	first_date = get_first_date.date

	session.close()

	return (f'<h1>Available Routes</h1>'
    	f'<p><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br />'
    	f'<ul><li>Queries precipitation by date</li></ul></p>'
    	f'<p><a href="/api/v1.0/stations">/api/v1.0/stations</a><br />'
    	f'<ul><li>Queries station data</li></ul></p>'
    	f'<p><a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br />'
    	f'<ul><li>Queries temperature data over the last year in the database at the most popular station</li></ul></p>'
    	f'<p>/api/v1.0/&lt;date&gt;<br />'
    	f'<ul><li>Date parameter must be in format YYYY-MM-DD to return a result. Return a JSON list of the \
    	minimum temperature, the average temperature, and the max temperature for a given start start date. \
    	Date range in database is {first_date} to {last_date}</li></ul></p>'

    )


if __name__ == "__main__":
	app.run(debug=True)
