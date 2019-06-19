import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Fetch Twitter Data")
    parser.add_argument('-u', '--user', dest='user', type=str, help="username whose tweets need to be fetched")
    parser.add_argument('--show', dest='show', action='store_true',
                        help="whether to show the 5 recent tweets in cli")
    parser.add_argument('--followers', dest='followers', action='store_true',
                        help="whether to store the followers of the said user")

    return parser


def validate_argument(parser):
    if not parser.user:
        print("Please place any username you want to fetch tweets")
        return None

    return parser.user


if __name__ == '__main__':
    import os
    import sys
    from pprint import pprint

    from . import create_parser, validate_argument
    from db import init_db, db_session
    from resources import Twitter, JSONParser


    init_db()   # Initialize db
    twitter_client = Twitter(os.environ['CONSUMER_KEY'],
                             os.environ['CONSUMER_SECRET'])
    json_parser = JSONParser(db_session)

    arg_parser = create_parser()
    args = arg_parser.parse_args()
    username = validate_argument(args)

    if username:
        user_json = twitter_client.search_user(username)
        json_parser.persist_user(user_json)

        tweet_json = twitter_client.search_tweets_by_user(username)
        tweet_list, hashtags_dict = JSONParser.parse_hashtags_from_tweet(tweet_json)

        json_parser.persist_tweets(tweet_list)
        if hashtags_dict:
            json_parser.persist_hashtags(hashtags_dict)

        if args.show:
            # Just to make the show a bit more structured
            print({"username": username})
            pprint({"tweets": [{"created_at": tweet["created_at"],
                               "tweet_text": tweet["text"]} for tweet in tweet_list]})

        if args.followers:
            followers_json = twitter_client.search_followers_by_user(username)
            json_parser.persist_followers(followers_json)

        json_parser.commit()

    else:
        print("username was not provided - Fetcher Closing")
        sys.exit(0)
