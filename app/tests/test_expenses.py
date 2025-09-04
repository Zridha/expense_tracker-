def test_add_expense(client):
    # Register + login user
    client.post("/auth/register", json={
        "username": "expenseuser",
        "password": "password123"
    })
    login = client.post("/auth/login", data={
        "username": "expenseuser",
        "password": "password123"
    })
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/expenses/", json={
        "amount": 500,
        "category": "Food",
        "date": "2025-09-01",
        "note": "Pizza dinner"
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 500
    assert data["category"] == "Food"


def test_monthly_report(client):
    # Register + login user
    client.post("/auth/register", json={
        "username": "reportuser",
        "password": "password123"
    })
    login = client.post("/auth/login", data={
        "username": "reportuser",
        "password": "password123"
    })
    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Add some expenses
    client.post("/expenses/", json={
        "amount": 1000, "category": "Travel", "date": "2025-09-02", "note": "Cab"
    }, headers=headers)

    client.post("/expenses/", json={
        "amount": 200, "category": "Food", "date": "2025-09-02", "note": "Snacks"
    }, headers=headers)

    # Get report
    response = client.get("/expenses/report/2025/9", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "Travel" in data
    assert "Food" in data
    assert data["Travel"] == 1000
    assert data["Food"] == 200
