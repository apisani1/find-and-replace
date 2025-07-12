"""Basic tests for find-and-replace."""


def test_import() -> None:
    """Test that the package can be imported."""
    import find_and_replace
    assert hasattr(find_and_replace, '__version__')


def test_version() -> None:
    """Test that version is defined."""
    from find_and_replace import __version__
    assert __version__ is not None
    assert isinstance(__version__, str)
