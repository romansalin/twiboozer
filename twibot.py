# -*- encoding: utf-8 -*-

import re

from twitter import Twitter, OAuth, TwitterHTTPError

import config as conf


class TwiBot(Twitter):
    def __init__(self):
        """Create a new twitter API connector."""
        auth = OAuth(conf.OAUTH_TOKEN, conf.OAUTH_SECRET, conf.CONSUMER_KEY,
                     conf.CONSUMER_SECRET)
        super(TwiBot, self).__init__(auth=auth)

    def get_timeline(self, count=200, include_rts=False):
        """Get tweets from timeline."""
        try:
            timeline = self.statuses.home_timeline(
                count=count, include_rts=include_rts)
        except TwitterHTTPError as e:
            print("Error: ", e)
            raise SystemExit(1)
        return [self._clean_tweets(t['text']) for t in timeline
                if t['in_reply_to_user_id'] is None
                and t['in_reply_to_status_id'] is None
                and t['in_reply_to_screen_name'] is None]

    def search_tweets(self, q, count=200, result_type="recent"):
        """Search for the latest tweets."""
        try:
            return self.search.tweets(
                q=q, result_type=result_type, count=count)
        except TwitterHTTPError as e:
            print("Error: ", e)
            raise SystemExit(1)

    def post_tweet(self, tweet):
        """Post tweet."""
        try:
            self.statuses.update(status=tweet)
        except TwitterHTTPError as e:
            print("Error: ", e)
            raise SystemExit(1)

    def _clean_tweets(self, tweets):
        # TODO clean needless symbols
        return re.sub(r'(https?:\/\/.+?|@.+?)(\s|$)|RT', '', tweets,
                      flags=re.IGNORECASE)
