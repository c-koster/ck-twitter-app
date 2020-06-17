"""
Application Program Interface -- refresher
Culton Koster
Wednesday 6/12
"""
import sys
import urllib.request
import json


def run():
    if len(sys.argv) < 2:
        # print usage statement if improper number of args
        print("usage: python weather_reader.py <zip_code>")
    else:
        # run the program with extra command line args
        zip = sys.argv[1]
        d = get_temperature(zip)
        print(d['name'] + ' weather in Farenheit:')
        print(d)


def get_temperature(zip_code):
    url = 'http://api.openweathermap.org/data/2.5/weather?zip=' + zip_code + ',us&APPID=9838b264525602b46f0b2ef8c191eef8&units=imperial'
    with urllib.request.urlopen(url) as webpage:
        contents = webpage.read().decode('utf-8')
    d = json.loads(contents)
    #print(d)
    # create a dictionary from this API grab, using the json module
    temp_imperial = d['main']['temp']

    return d


# Call main function on startup
if __name__ == '__main__':
    run()
