from . import main


def test_get_reddit_instance():
    """Test account should be read only"""
    r = main.get_reddit_instance()
    assert r.read_only
