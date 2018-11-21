"""
MAIN CLI APP
"""
import logging

import praw

LOGGER = logging.getLogger(__name__)


def get_reddit_instance() -> praw.Reddit:
    """Returns a Reddit instance"""
    try:
        reddit = praw.Reddit("icarebot")
        LOGGER.info("got reddit instance %s", reddit)
    except KeyError:
        import os

        client_id = os.environ.get("client_id", "")
        client_secret = os.environ.get("client_secret", "")
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret)
    return reddit


def subscribe_all_subreddits(reddit: praw.Reddit):
    """Subscribe to all subreddit"""
    all_subreddits = reddit.subreddit("all")

    for comment in all_subreddits.stream.comments():
        if should_I_care(comment.body):
            try:
                LOGGER.info(
                    "Found a target: %s %s",
                    comment.body[:10],
                    "https://reddit.com" + comment.permalink,
                )
                response = get_response()
                LOGGER.info("Sending a response: %s", response)
                reply = comment.reply(response)
                LOGGER.info("Comment was created at %s", reply.permalink)

            except Exception as e:
                LOGGER.fatal("Error occurred: %s", e)


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
