"""
MAIN CLI APP
"""
import logging

import praw

LOGGER = logging.getLogger(__name__)


def get_reddit_instance() -> praw.Reddit:
    """
    >>> reddit = get_reddit_instance()
    >>> reddit.read_only
    False
    """
    reddit = praw.Reddit("icarebot")
    LOGGER.info("got reddit instance %s", reddit)
    return reddit


def subscribe_all_subreddits(reddit: praw.Reddit):
    """Subscribe to all subreddit"""
    all_subreddits = reddit.subreddit("all")

    for comment in all_subreddits.stream.comments():
        if should_I_care(comment.body):
            LOGGER.info("Found a target: %s %s", comment.body, comment.url)
            response = get_response()
            LOGGER.info("Sending a response: %s", response)
            reply = reply.reply(response)
            LOGGER.info("Comment was created at %s", reply.url)


def should_I_care(text) -> bool:
    """
    >>> should_I_care("I don't care")
    True
    """
    return "i don't care" in text.lower()


def get_response() -> str:
    """Returns a bot's response"""
    return "I care"


def setup_logger(loglevel: int):
    """Setup logger"""
    global LOGGER  # pylint: disable=global-statement
    LOGGER.setLevel(loglevel)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    LOGGER.addHandler(ch)


def main(args):
    """Main function"""
    loglevel = logging.WARNING

    if args.verbose:
        loglevel = logging.DEBUG

    setup_logger(loglevel)
    reddit = get_reddit_instance()
    subscribe_all_subreddits(reddit)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v", "--verbose", help="set LOGGER to verbose", action="store_true"
    )
    main(parser.parse_args())
