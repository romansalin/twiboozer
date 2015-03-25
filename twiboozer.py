# -*- encoding: utf-8 -*-

# TODO вынести, оформить как package

import os
import datetime
import random

from pymarkovchain import MarkovChain

from twibot import TwiBot


def format_tweet(tweet):
    """Format tweet after generation."""
    if tweet[-1] not in ".?!":
        return "{0}{1}".format(tweet, get_end_tweet())
    return tweet


def get_end_tweet():
    endings = ('.', '!')
    rate = 0.2
    return endings[random.random() < rate]


def train(tweets):
    """Training of model from tweets based on a Markov chain."""
    directory = "db"
    filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = os.path.join(directory, filename)

    model = MarkovChain(path)
    model.generateDatabase("\n".join(tweets).encode("utf-8"))
    return model


def main():
    twibot = TwiBot()
    tweets = twibot.get_timeline(count=200)

    mc = train(tweets)
    tweet = mc.generateString()
    tweet = format_tweet(tweet)

    twibot.post_tweet(tweet)
    print(tweet)


if __name__ == "__main__":
    main()
