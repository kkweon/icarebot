"""
MAIN CLI APP
"""
import logging
from configparser import NoSectionError

import praw

LOGGER = logging.getLogger(__name__)


def get_reddit_instance() -> praw.Reddit:
    """Returns a Reddit instance"""
    try:
        reddit = praw.Reddit("icarebot")
        LOGGER.info("got reddit instance %s", reddit)
    except NoSectionError:
        import os

        LOGGER.warning("Please create a praw.ini with [icarebot] section")

        client_id = os.environ.get("client_id", "")
        client_secret = os.environ.get("client_secret", "")
        username = os.environ.get("username", "")
        password = os.environ.get("password", "")
        user_agent = os.environ.get("user_agent", "")
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent,
        )
    return reddit


def subscribe_all_subreddits(reddit: praw.Reddit):
    """Subscribe to all subreddit"""
    all_subreddits = reddit.subreddit("all")

    for comment in all_subreddits.stream.comments():
        if is_not_icarebot(comment):
            try:
                if should_I_care(comment.body):
                    LOGGER.info(
                        "Found a target: %s %s",
                        comment.body[:10],
                        "https://reddit.com" + comment.permalink,
                    )
                    response = get_response()
                    LOGGER.info("Sending a response: %s", response)
                    reply = comment.reply(response)
                    LOGGER.info("Comment was created at %s", reply.permalink)
                elif comment.body.lower() == "f":
                    LOGGER.info("Found F %s", "https://reddit.com" + comment.permalink)
                    reply = comment.reply(comment.body)
                    LOGGER.info("Comment was created at %s", reply.permalink)
            except Exception as e:
                LOGGER.error("Error occurred: %s", e)


def should_I_care(text: str) -> bool:
    """
    >>> should_I_care("I don't care")
    True
    """
    return "i don't care" in text.lower()


def get_response() -> str:
    """Returns a bot's response"""
    return "I care"


def is_not_icarebot(comment: praw.models.Comment) -> bool:
    author = comment.author

    if author:
        return author.name != "icarebot"

    return True


def setup_logger(loglevel: int):
    """Setup logger"""
    global LOGGER  # pylint: disable=global-statement
    LOGGER.setLevel(loglevel)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    fh = logging.FileHandler("/tmp/icarebot.log")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    LOGGER.addHandler(ch)
    LOGGER.addHandler(fh)


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
