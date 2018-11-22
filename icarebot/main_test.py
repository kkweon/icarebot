from . import main


def test_get_reddit_instance():
    r = main.get_reddit_instance()
    assert not r.read_only


def test_get_response():
    assert main.get_response() == "I care"
