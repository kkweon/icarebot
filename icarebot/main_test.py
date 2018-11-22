from . import main


def test_get_reddit_instance():
    r = main.get_reddit_instance()
    assert not r.read_only


def test_get_response():
    test1 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. I don't care. Cras nulla libero, scelerisque quis tempus quis, mollis ac augue. Vestibulum tristique varius nisi a imperdiet. Vivamus quis convallis orci. Nunc et faucibus ligula. Cras nec accumsan mauris. Maecenas elementum, ex vitae egestas ultrices, sem massa lacinia urna, in ornare augue ex id mi. Praesent faucibus risus ligula, ac venenatis lacus porta ut. Maecenas egestas quam diam, nec vulputate elit efficitur congue. Praesent euismod libero porta molestie tempor. Phasellus eget urna aliquam, sodales diam eget, vehicula dolor. Suspendisse aliquet diam sed velit convallis tempor. Integer consectetur convallis placerat.
    """
    response = main.get_response(test1)
    assert (
        response
        == """
> ...lit. I don't care. Cra...

I care"""
    )

    test2 = """I don't care"""
    assert (
        main.get_response(test2)
        == """
> I don't care

I care"""
    )

    test3 = """I don't care whatever"""
    assert (
        main.get_response(test3)
        == """
> I don't care what...

I care"""
    )
