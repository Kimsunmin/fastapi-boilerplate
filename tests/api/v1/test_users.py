import pytest


class TestCreateUser:
    def test_create_user_success(self, client):
        response = client.post("/api/v1/users", json={
            "email": "test@example.com",
            "name": "홍길동"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["email"] == "test@example.com"
        assert data["data"]["name"] == "홍길동"
        assert "id" in data["data"]

    def test_create_user_duplicate_email(self, client):
        client.post("/api/v1/users", json={
            "email": "dup@example.com",
            "name": "A"
        })
        response = client.post("/api/v1/users", json={
            "email": "dup@example.com",
            "name": "B"
        })
        assert response.status_code == 409
        assert response.json()["status"] == "error"


class TestGetUser:
    def test_get_user_success(self, client):
        created = client.post("/api/v1/users", json={
            "email": "get@example.com",
            "name": "조회용"
        }).json()["data"]

        response = client.get(f"/api/v1/users/{created['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["email"] == "get@example.com"

    def test_get_user_not_found(self, client):
        response = client.get("/api/v1/users/9999")
        assert response.status_code == 404
        assert response.json()["status"] == "error"


class TestListUsers:
    def test_list_users_empty(self, client):
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"] == []

    def test_list_users_with_data(self, client):
        client.post("/api/v1/users", json={"email": "a@example.com", "name": "A"})
        client.post("/api/v1/users", json={"email": "b@example.com", "name": "B"})

        response = client.get("/api/v1/users")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 2


class TestUpdateUser:
    def test_update_user_success(self, client):
        created = client.post("/api/v1/users", json={
            "email": "update@example.com",
            "name": "변경전"
        }).json()["data"]

        response = client.patch(f"/api/v1/users/{created['id']}", json={
            "name": "변경후"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == "변경후"
        assert data["data"]["email"] == "update@example.com"

    def test_update_user_duplicate_email(self, client):
        a = client.post("/api/v1/users", json={"email": "a@example.com", "name": "A"}).json()["data"]
        b = client.post("/api/v1/users", json={"email": "b@example.com", "name": "B"}).json()["data"]

        response = client.patch(f"/api/v1/users/{a['id']}", json={
            "email": "b@example.com"
        })
        assert response.status_code == 409
        assert response.json()["status"] == "error"


class TestDeleteUser:
    def test_delete_user_success(self, client):
        created = client.post("/api/v1/users", json={
            "email": "delete@example.com",
            "name": "삭제용"
        }).json()["data"]

        response = client.delete(f"/api/v1/users/{created['id']}")
        assert response.status_code == 204

        get_response = client.get(f"/api/v1/users/{created['id']}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client):
        response = client.delete("/api/v1/users/9999")
        assert response.status_code == 404
        assert response.json()["status"] == "error"
