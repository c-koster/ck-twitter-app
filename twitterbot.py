# import twitter modules
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from dotenv import load_dotenv
import os
# import extras
from getWeather import get_temperature
from models import *
import emoji
from datetime import datetime

#  credentials go here
load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
zip = "11201" # hardcoded zipcode for brooklyn, ny 

class CustomStreamListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_success(self, status):
        print('success!')
        print(status.text)
        return True

    def on_status(self, status):
        """
        """
        s = extract_emojis(status.text)
        if s != '':
            t = Tweet(zipcode=zip,text=s,timestamp=datetime.now())
            # create instance of a Tweet class.
            t.add_self() # tell it to commit into the collection of tweets.
            print(s)
        return True

    def on_error(self, status_code):
        print('Error: ' + repr(status_code))
        # TODO should store errors in sql too, wait (120) seconds and return True
        return False


def extract_emojis(str):
    return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)


def stream():
    """
    I've been running this script indefinitely with a nohup command
    """
    d = get_temperature(zip)
    box_radius = .3
    # define a coordinate box.
    coords = [d['coord']['lon']-box_radius, d['coord']['lat']-box_radius,d['coord']['lon']+box_radius, d['coord']['lat']+box_radius]
    # oxford coordinates over-write -- see below
    #p = 51.752022
    #q = -1.257677
    #coords = [p-box_radius, q-box_radius,p+box_radius, q+box_radius]

    temp_imperial = d['main']['temp']
    #filter = "point_radius:[" + str(coords[0]) + " " + str(coords[1]) +" 25mi]"
    l = CustomStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    print("stream all emojis from: " + d['name'] + ", zip=" + zip)
    stream.filter(locations=coords) # start the stream


if __name__ == '__main__':
    stream()
