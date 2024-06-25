import pytest
from httpx import AsyncClient
from main import app
from app.config.configs import settings

BASE_URL = "http://localhost:8000/"

@pytest.mark.asyncio
async def test_create_comment():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # First, create a user to use for creating a comment
        response = await ac.post(
            f"{settings.API_V1_STR}/usuario/signup",
            json={
                "firstName": "Test",
                "lastName": "User",
                "username": "testusercomment",
                "email": "testusercomment@example.com",
                "senha": "password123"
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        assert response.status_code == 201

        # Login to get the token
        auth_response = await ac.post(
            f"{settings.API_V1_STR}/usuario/login",
            data={"username": "testusercomment@example.com", "password": "password123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert auth_response.status_code == 200
        auth_data = auth_response.json()
        access_token = auth_data["token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Create a comment
        response = await ac.post(
            f"{settings.API_V1_STR}/comentario/comentarios",
            json={
                "media_id": 76479,
                "media_type": "movie",
                "content": "This is a test comment",
                "likes": 0,
                "username": "testusercomment"
            },
            headers=headers
        )
        assert response.status_code == 201
        
@pytest.mark.asyncio
async def test_get_comments():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Create a user and a comment first
        response = await ac.post(
            f"{settings.API_V1_STR}/usuario/signup",
            json={
                "firstName": "Test",
                "lastName": "User",
                "username": "testusergetcomment",
                "email": "testusergetcomment@example.com",
                "senha": "password123"
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        assert response.status_code == 201

        # Login to get the token
        auth_response = await ac.post(
            f"{settings.API_V1_STR}/usuario/login",
            data={"username": "testusergetcomment@example.com", "password": "password123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert auth_response.status_code == 200
        auth_data = auth_response.json()
        access_token = auth_data["token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Create a comment
        response = await ac.post(
            f"{settings.API_V1_STR}/comentario/comentarios",
            json={
                "media_id": 76479,
                "media_type": "movie",
                "content": "This is a test comment for get",
                "likes": 0
            },
            headers=headers
        )
        assert response.status_code == 201

        # Get comments by media_id
        response = await ac.get(f"{settings.API_V1_STR}/comentario/comentarios/1", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_update_comment():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Create a user and a comment first
        response = await ac.post(
            f"{settings.API_V1_STR}/usuario/signup",
            json={
                "firstName": "Test",
                "lastName": "User",
                "username": "testuserupdatecomment",
                "email": "testuserupdatecomment@example.com",
                "senha": "password123"
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        assert response.status_code == 201

        # Login to get the token
        auth_response = await ac.post(
            f"{settings.API_V1_STR}/usuario/login",
            data={"username": "testuserupdatecomment@example.com", "password": "password123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert auth_response.status_code == 200
        auth_data = auth_response.json()
        access_token = auth_data["token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Create a comment
        response = await ac.post(
            f"{settings.API_V1_STR}/comentario/comentarios",
            json={
                "media_id": 76479,
                "media_type": "movie",
                "content": "This is a test comment for update",
                "likes": 0
            },
            headers=headers
        )
        assert response.status_code == 201
        comment_id = response.json()["id"]

        # Update the comment
        response = await ac.put(
            f"{settings.API_V1_STR}/comentario/comentarios/{comment_id}",
            json={
                "media_id": 76479,
                "media_type": "movie",
                "content": "Updated comment content",
                "likes": 10
            },
            headers=headers
        )
        assert response.status_code == 202

        # Get the updated comment
        response = await ac.get(f"{settings.API_V1_STR}/comentario/comentarios/1", headers=headers)
        assert response.status_code == 200
        comments = response.json()
        assert any(comment["id"] == comment_id and comment["content"] == "Updated comment content" for comment in comments)

@pytest.mark.asyncio
async def test_delete_comment():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Create a user and a comment first
        response = await ac.post(
            f"{settings.API_V1_STR}/usuario/signup",
            json={
                "firstName": "Test",
                "lastName": "User",
                "username": "testuserdeletecomment",
                "email": "testuserdeletecomment@example.com",
                "senha": "password123"
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        assert response.status_code == 201

        # Login to get the token
        auth_response = await ac.post(
            f"{settings.API_V1_STR}/usuario/login",
            data={"username": "testuserdeletecomment@example.com", "password": "password123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert auth_response.status_code == 200
        auth_data = auth_response.json()
        access_token = auth_data["token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Create a comment
        response = await ac.post(
            f"{settings.API_V1_STR}/comentario/comentarios",
            json={
                "media_id": 1,
                "media_type": "movie",
                "content": "This is a test comment for delete",
                "likes": 0
            },
            headers=headers
        )
        assert response.status_code == 201
        comment_id = response.json()["id"]

        # Delete the comment
        response = await ac.delete(f"{settings.API_V1_STR}/comentario/comentarios/{comment_id}", headers=headers)
        assert response.status_code == 204

        # Verify deletion
        response = await ac.get(f"{settings.API_V1_STR}/comentario/comentarios/1", headers=headers)
        assert response.status_code == 200
        comments = response.json()
        assert not any(comment["id"] == comment_id for comment in comments)
