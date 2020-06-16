"""
Use ORM to build tweet objects/events, and store them in postgres
"""
class GeoModel:
    """
    Let's build a model from an hour of geocoded tweets, and see what kind of
    shit we can predict/determine
    Methods:
    """
    def __init__(self,zip):
        self.zip = zip
        self.location = self.getCoordinates()

        self.date = datetime.date(now)
        self.tweets = [] # to contain tweet objects


    def convertTraningExample(self):

        for t in self.tweets:
            pass
        return


    def getCoordinates(self):
        """

        """
        d = weatherReader.get_temperature(self.zip)
        return (d['coord']['lon'], d['coord']['lat'])



    def __str__(self):
        s = "Geo(" + self.zip + ",numTweets: " + str(len(self.tweets))+")"
        return s
    def __repr__(self):
        return "Twitter data object intialized at " + str(self.date)


class Tweet:
    """
    Basic storage abstraction with text attribute.
    Should contain methods for evaluation and storage of self.
    """
    def __init__(self,text):
        self.text = text
