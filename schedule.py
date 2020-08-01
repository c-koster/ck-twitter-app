"""
This script to be run using crontab, every (8) hours.

This should happen at each time interval:
 1 pull tweets out of the tweets table and create an example for each unique zipcode found (1).
 2 record temperature in weather table
"""

from models import *
from getWeather import get_temperature
from datetime import datetime,timedelta


def compile_example(time_now,zip):
    """
    Create an entry in weather table and examples table
    """
    t = get_temperature(zip)
    # use flask's ORM to create the two data rows
    eight_hours_ago = time_now - timedelta(hours = 8)
    w = Weather(zipcode=zip,recorded_at=time_now,description=t['weather'][0]['main'],temperature=t['main']['temp'])
    e = Example(zipcode=zip,t1=time_now,t2=eight_hours_ago)

    # insert both into database
    db.session.add(w)
    db.session.add(e)
    db.session.commit()
    e.fill_text()

if __name__== "__main__":
    #db.session.add(e)
    #db.session.commit()
    compile_example(time_now=datetime.utcnow(),zip="11201")
