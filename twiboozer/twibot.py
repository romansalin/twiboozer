# -*- encoding: utf-8 -*-

import sys
import re

from twitter import Twitter, OAuth, TwitterHTTPError

from .formatter import Formatter


class TwiBot(Twitter):
    def __init__(self, **kwargs):
        """Create a new twitter API connector."""
        auth = OAuth(kwargs.get('oauth_token'), kwargs.get('oauth_secret'),
                     kwargs.get('consumer_key'), kwargs.get('consumer_secret'))
        super(TwiBot, self).__init__(auth=auth)

    def get_timeline(self, count=200, include_rts=False, include_replies=False):
        """Get tweets from timeline."""
        try:
            timeline = self.statuses.home_timeline(count=count, include_rts=include_rts)
        except TwitterHTTPError as e:
            sys.stderr.write(e.message)
            raise SystemExit(1)

        tweets = []
        for t in timeline:
            if include_replies or (
                    t['in_reply_to_user_id'] is None and
                    t['in_reply_to_status_id'] is None and
                    t['in_reply_to_screen_name'] is None):
                tweets.append(self._clean_tweet(t['text']))
        return "\n".join(tweets).encode("utf-8")

    def search_tweets(self, q, count=200, result_type="recent"):
        """Search for the latest tweets."""
        try:
            results = self.search.tweets(q=q, result_type=result_type, count=count)
        except TwitterHTTPError as e:
            sys.stderr.write(e.message)
            raise SystemExit(1)
        # TODO filtering tweets same before
        return "\n".join(results).encode("utf-8")

    def post_tweet(self, tweet):
        """Post tweet."""
        formatter = Formatter(tweet)
        try:
            self.statuses.update(status=formatter.get_format_tweet())
        except TwitterHTTPError as e:
            sys.stderr.write(e.message)
            raise SystemExit(1)

    @staticmethod
    def _clean_tweet(tweet):
        """Tweet cleanup."""
        # TODO more robust cleanup
        clean_re = re.compile(r'(https?://.+?|@.+?)(\s|$)|RT',
                              flags=re.IGNORECASE)
        return clean_re.sub('', tweet)
