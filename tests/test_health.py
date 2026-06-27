from product_lab.health import get_status


def test_get_status_returns_ok():
    assert get_status() == "ok"
