from __future__ import absolute_import, print_function

# import modules
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
from getWeather import get_temperature
import emoji
import sys
import models

#  credentials go here --
consumer_key = "oi8Zn76YmU8tN57OvZTOqlPw3"
consumer_secret = "cWDmBMPFzOjRLv11DyG81aWWkwI5uVTNjk8dHrFc6ERJfpPtzZ"
access_token = "1208572114019770368-4d6RZD2oCYbLLM2au0JlShUxvncG4a"
access_token_secret = "IOdOYWJHehVH6X1WYRWU79TftjIoJjRohaxQA54yPHztS"

class CustomStreamListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_success(self, status):
        print(status.text)
        return True

    def on_status(self, status):
        s = extract_emojis(status.text)
        if s != '':
            print(s)
        return True

    def on_error(self, status_code):
        print('Error: ' + repr(status_code))
        return False



def extract_emojis(str):
  return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)

if __name__ == '__main__':
    zip = '20002'
    if len(sys.argv) == 2:
        zip = sys.argv[1]


    d = get_temperature(zip)
    box_radius = .3
    coords = [d['coord']['lon']-box_radius, d['coord']['lat']-box_radius,d['coord']['lon']+box_radius, d['coord']['lat']+box_radius]
    """
    # oxford coordinates over-write
    p = 51.752022
    q = -1.257677
    coords = [p-box_radius, q-box_radius,p+box_radius, q+box_radius]
    """
    temp_imperial = d['main']['temp']
    #filter = "point_radius:[" + str(coords[0]) + " " + str(coords[1]) +" 25mi]"

    l = CustomStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)

    print("streaming all emojis from: " + d['name'] + ", zip=" + zip)
    stream.filter(locations=coords)
