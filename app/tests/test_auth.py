def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["username"] == "testuser"


def test_login_user(client):
    # First register
    client.post("/auth/register", json={
        "username": "testuser2",
        "password": "password123"
    })

    # Then login
    response = client.post("/auth/login", data={
        "username": "testuser2",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
