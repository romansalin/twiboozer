# TwiBoozer

Simple Markov chain text generator integrated with your Twitter account and based on timeline.

## Requirements

- python (2.7+ or 3.3+)
- pip

## Installation

Install `TwiBoozer` with `pip`:

```bash
sudo pip install twiboozer
```

## Usage

```python
from twiboozer import TwiBot


OAUTH_TOKEN = ''
OAUTH_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

twibot = TwiBot(oauth_token=OAUTH_TOKEN, oauth_secret=OAUTH_SECRET, 
                consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
tweets = twibot.get_timeline(count=500, include_rts=True, include_replies=True)

mc = MarkovChain()
mc.generate_database(tweets)
tweet = mc.generate_string()

twibot.post_tweet(tweet)
```
