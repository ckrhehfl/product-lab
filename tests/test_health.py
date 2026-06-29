from product_lab.health import get_status


def test_get_status_returns_ok():
    assert get_status() == "ok"


def test_get_status_returns_string():
    assert isinstance(get_status(), str)


def test_get_status_is_non_empty():
    assert len(get_status()) > 0


def test_get_status_is_idempotent():
    assert get_status() == get_status()
