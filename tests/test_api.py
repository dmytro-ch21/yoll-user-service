# tests/test_api.py
import json
import pytest

def test_default_route(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "openapi_docs" in data


def test_add_movie_success(client, monkeypatch):
    from app.repositories.movie_repository import MovieRepository

    def fake_add_movie(data):
        return {
            "id": 1,
            "title": data["title"],
            "genre": data.get("genre"),
            "release_year": data.get("release_year"),
            "user_id": data["user_id"],
        }

    monkeypatch.setattr(MovieRepository, "add_movie", fake_add_movie)
    
    movie_data = {"title": "Test Movie", "user_id": 1, "genre": "Action", "release_year": 2025}
    response = client.post("/movies", json=movie_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Movie"
    assert data["user_id"] == 1

def test_get_movies_success(client, monkeypatch):
    from app.repositories.movie_repository import MovieRepository

    def fake_get_movies_by_user(user_id):
        return [
            {"id": 1, "title": "Test Movie", "genre": "Action", "release_year": 2025}
        ]
    monkeypatch.setattr(MovieRepository, "get_movies_by_user", fake_get_movies_by_user)
    
    response = client.get("/movies?user_id=1")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Test Movie"

# --- TODO ENDPOINTS ---
def test_create_todo_success(client, monkeypatch):
    from app.repositories.todo_repository import TodoRepository

    def fake_create_todo(data):
        return {
            "id": 1,
            "title": data["title"],
            "completed": data.get("completed", False),
            "user_id": data["user_id"],
            "created_at": "2025-02-02T19:42:53"
        }
    monkeypatch.setattr(TodoRepository, "create_todo", fake_create_todo)

    todo_data = {"title": "Test Todo", "user_id": 1}
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 201
    data = response.get_json()
    # Check that the returned todo has the correct fields.
    assert data["title"] == "Test Todo"
    assert data["user_id"] == 1

def test_get_all_todos_success(client, monkeypatch):
    from app.repositories.todo_repository import TodoRepository

    def fake_get_all_todos(user_id):
        return [
            {"id": 1, "title": "Test Todo", "completed": False, "created_at": "2025-02-02T19:42:53"}
        ]
    monkeypatch.setattr(TodoRepository, "get_all_todos", fake_get_all_todos)

    response = client.get("/todos?user_id=1")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["title"] == "Test Todo"

def test_update_todo_success(client, monkeypatch):
    from app.repositories.todo_repository import TodoRepository

    def fake_update_todo(todo_id, user_id, data):
        return {
            "id": todo_id,
            "title": data["title"],
            "completed": data.get("completed", False),
            "created_at": "2025-02-02T19:42:53"
        }
    monkeypatch.setattr(TodoRepository, "update_todo", fake_update_todo)

    update_data = {"title": "Updated Todo", "completed": True}
    response = client.put("/todos/1?user_id=1", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Todo updated successfully"
    assert data["task"]["title"] == "Updated Todo"

def test_delete_todo_success(client, monkeypatch):
    from app.repositories.todo_repository import TodoRepository

    def fake_delete_todo(todo_id, user_id):
        # Return a fake deleted id if successful.
        return 1
    monkeypatch.setattr(TodoRepository, "delete_todo", fake_delete_todo)

    response = client.delete("/todos/1?user_id=1")
    assert response.status_code == 200
    data = response.get_json()
    assert "deleted successfully" in data["message"]

# --- USER ENDPOINTS ---
def test_create_user_success(client, monkeypatch):
    from app.repositories.user_repository import UserRepository

    def fake_create_user(data):
        return {"id": 1, "name": data["name"], "email": data["email"]}
    monkeypatch.setattr(UserRepository, "create_user", fake_create_user)

    user_data = {"name": "Test User", "email": "test@example.com"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"

def test_get_user_success(client, monkeypatch):
    from app.repositories.user_repository import UserRepository

    def fake_get_user_by_id(user_id):
        return {"id": user_id, "name": "Test User", "email": "test@example.com"}
    monkeypatch.setattr(UserRepository, "get_user_by_id", fake_get_user_by_id)

    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Test User"
