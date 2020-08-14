from starlette.testclient import TestClient
from example.hello import app

# get test client
client = TestClient(app)


def test_read_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"text": "hello world"}


def test_read_create_example_data():
    response = client.post(
        "/post", json={"name": "hoge", "emails": ["test@example.com"]}
    )
    assert response.status_code == 200
    assert response.json() == {
        "text": "hello, hoge, None, ['test@example.com']"
    }
