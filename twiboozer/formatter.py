# -*- encoding: utf-8 -*-

import random
import textwrap


class Formatter(object):
    def __init__(self, tweet):
        self.tweet = tweet

    def get_format_tweet(self):
        """Format tweet after generation."""
        max_len = 140
        tweet = self.tweet
        if len(tweet) > max_len:
            tweet = textwrap.wrap(self.tweet, max_len - 1)[0]

        if tweet[-1] not in ".?!":
            tweet += self._get_end_tweet()
        return tweet

    @staticmethod
    def _get_end_tweet():
        """Get random punctuation at the end of the sentence."""
        endings = ('.', '!')
        rate = 0.2
        return endings[random.random() < rate]
