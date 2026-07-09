def test_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_db(client):
    response = client.get("/db-test")
    assert response.status_code == 200