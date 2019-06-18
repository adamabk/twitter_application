import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Fetch Twitter Data")
    parser.add_argument('-u', '--user', type=str, help="username whose tweets need to be fetched")
    parser.add_argument('--show', dest='show', action='store_true',
                        help="whether to show the 5 recent tweets in cli")

    return parser


def validate_argument(parser):
    if not parser.user:
        print("Please place any username you want to fetch tweets")
        return None

    return parser.user


if __name__ == '__main__':
    from . import create_parser, validate_argument
    from db import init_db
    from resources import twitter_fetcher


    init_db()   # Initialize db

    parser = create_parser()
    args = parser.parse_args()
    username = validate_argument(args)

    if username:
        t = twitter_fetcher.search_by_user(username)
    else:
        print("username was not provided - Fetcher Closing")
    if args.show:
        print(t)
