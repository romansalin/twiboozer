from twitter import Twitter, OAuth, TwitterHTTPError

import config as conf


class TwiBot(object):
    def __init__(self):
        """Create a new twitter API connector."""
        self.t = Twitter(
            auth=OAuth(conf.OAUTH_TOKEN, conf.OAUTH_SECRET, conf.CONSUMER_KEY,
                       conf.CONSUMER_SECRET))

    def get_timeline(self, count=100):
        """Get tweets from timeline."""
        try:
            timeline = self.t.statuses.home_timeline(count=count,
                                                     include_rts=False)
            return [tweet['text'] for tweet in timeline]
        except TwitterHTTPError as e:
            print('Error: ', e)
            return None

    def post_tweet(self, tweet):
        """Post tweet."""
        try:
            self.t.statuses.update(status=tweet)
        except TwitterHTTPError as e:
            print('Error: ', e)

    def search_tweets(self, q, count=100):
        """Search for the latest tweets."""
        return self.t.search.tweets(q=q, result_type='recent', count=count)
