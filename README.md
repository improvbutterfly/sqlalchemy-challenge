# sqlalchemy-challenge
Climate Analysis and Exploration and app

## Climate Analysis and Exploration

View [climate.ipynb](climate.ipynb) for the full climate analysis and exploration.

The notebook created the following graphs:

### Precipitation by Date for last year in the database
![Precipitation by Date for last year in the database](images/precip_by_date.png)

### Temperature histogram for station with most observations for last year in the database
![Temperature histogram for station with most observations for last year in the database](images/temperature_histogram.png)

## Climate App

[app.py](app.py) Is a Flask API to return JSON data from the [hawaii.sqlite](Resources/hawaii.sqlite) database.

### Available Routes

/api/v1.0/precipitation
* Queries precipitation by date

/api/v1.0/stations
* Queries station data

/api/v1.0/tobs
* Queries temperature data over the last year in the database at the most popular station

/api/v1.0/<start_date>
* Date parameter must be in format YYYY-MM-DD to return a result. Returns a JSON list of the minimum temperature, the average temperature, and the max temperature between a given start date and last date in database. Date range in database is 2010-01-01 to 2017-08-23

/api/v1.0/<start_date>/<end_date>
* Date parameters must be in format YYYY-MM-DD to return a result. Returns a JSON list of the minimum temperature, the average temperature, and the max temperature between a given start date and end date. Date range in database is 2010-01-01 to 2017-08-23

N.B.: Date range and station with most observations are variable should more data be added to the database.