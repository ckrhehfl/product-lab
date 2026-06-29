from product_lab.health import get_status


def test_get_status_returns_ok():
    """Verify get_status returns the expected 'ok' value."""
    assert get_status() == "ok"


def test_get_status_returns_string():
    """Verify get_status returns a string."""
    assert isinstance(get_status(), str)


def test_get_status_is_non_empty():
    """Verify get_status returns a non-empty value."""
    assert len(get_status()) > 0


def test_get_status_is_idempotent():
    """Verify repeated get_status calls return the same value."""
    assert get_status() == get_status()
