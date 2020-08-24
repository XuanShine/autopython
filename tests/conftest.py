import pytest

@pytest.fixture(scope="module")
def test_rpi():
    flask_app = create_app("flask_test.cfg")