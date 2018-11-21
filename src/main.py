import praw
import logging

logger = logging.getLogger(__name__)


def get_reddit_instance() -> praw.Reddit:
    reddit = praw.Reddit("icarebot")
    logger.info("got reddit instance {}".format(reddit))
    return reddit


def subscribe_all_subreddits(reddit: praw.Reddit):
    all_subreddits = reddit.subreddit("all")

    for submission in all_subreddits.stream.submissions():
        if should_I_care(submission):
            logger.info(
                "Found a target submission: {} {}".format(
                    submission.title, submission.url
                )
            )
            response = get_response(submission)
            logger.info("Sending a response: {}".format(response))
            comment = submission.reply(response)
            logger.info("Comment was created at {}".format(comment.url))


def should_I_care(submission: praw.models.Submission) -> bool:
    return "I don't care" in submission.title


def get_response(submission: praw.models.Submission) -> str:
    return "I care"


def setup_logger(loglevel: int):
    global logger
    logger.setLevel(loglevel)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def main(args):
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
        "-v", "--verbose", help="set logger to verbose", action="store_true"
    )
    args = parser.parse_args()
    main(args)
