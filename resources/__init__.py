import os

from .twitter import Twitter


twitter_fetcher = Twitter(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])


__all__ = [twitter_fetcher]
