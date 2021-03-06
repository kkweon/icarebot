"""
MAIN CLI APP
"""
import logging
import sys
from configparser import NoSectionError
from typing import Optional

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


def with_reddit_prefix(url: str) -> str:
    return "https://reddit.com" + url


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
                        with_reddit_prefix(comment.permalink),
                    )
                    response = get_response()
                    LOGGER.info("Sending a response: %s", response)
                    reply = comment.reply(response)
                    LOGGER.info(
                        "Comment was created at %s", with_reddit_prefix(reply.permalink)
                    )
                elif is_reply(comment):
                    LOGGER.info(
                        "Found a response by human: %s",
                        with_reddit_prefix(comment.permalink),
                    )
                    reply_response = get_reply_response(comment.body)
                    if reply_response:
                        reply = comment.reply(reply_response)
                        LOGGER.info("[Success] %s", with_reddit_prefix(reply.permalink))
            except KeyboardInterrupt:
                print("Bye")
                sys.exit(0)
            except Exception as e:
                LOGGER.error("Error occurred: %s", e)


def should_I_care(text: str) -> bool:
    """
    >>> should_I_care("I don't care")
    True
    """
    return "i don't care" in text.lower()


def is_reply(comment: praw.models.Comment) -> bool:
    if comment.is_root:
        return False

    text = comment.body.lower()

    if text in ("good bot", "bad bot"):
        parent = comment.parent()
        return (
            isinstance(parent, praw.models.Comment)
            and parent.author
            and parent.author.name == "icarebot"
        )
    return False


def get_reply_response(message: str) -> Optional[str]:
    if message.lower() == "good bot":
        return "Thank you, kind human being"
    elif message.lower() == "bad bot":
        return "I am sorry human being :("

    return None


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
