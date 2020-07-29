Hello all.
This project's purpose is to see if I can predict the weather in Brooklyn based upon emojis originating from there.
Here is how it works:
1. I use the Twitter API modules (Tweepy) to continuously stream data into a psql database. Tweets are stored with zipcode, eemoji, and . Currently I let this run forever using a nohup command with (twitterbot.py).

2. Next I compile tweets into an 'examples' table on an 8 hour interval, and delete them from the 'tweets' table to save space. Each time I compile an examplee, I also collect the weather into a 'weather' tablee. I store both into my database using the same id. This is done by using crontab on the (schedule.py) script. --See also (models.py) to have a look at how I interact with my psql database using an ORM.

3. Lastly, I query for all my examples, join by timestamp/id with the weather table, and build matrices for linear and logistic regressin. These bits of code are found in (predict.py)

xoxo hope this helps
