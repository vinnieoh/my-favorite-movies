import pytest
from httpx import AsyncClient
from main import app
from app.config.configs import settings

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url='http://localhost:8000/') as ac:
        response = await ac.post(
            f"{settings.API_V1_STR}/usuario/signup",
            json={
                "firstName": "Test12222",
                "lastName": "User",
                "username": "testuser21222",
                "email": "testuser1212@example.com",
                "senha": "password123"
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(app=app, base_url='http://localhost:8000/') as ac:
        create_response = await ac.post(
            f"{settings.API_V1_STR}/usuario/signup",
            json={
                "firstName": "Test12311",
                "lastName": "User",
                "username": "testuser12311",
                "email": "testuser12345@example.com",
                "senha": "password123"
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        assert create_response.status_code == 201

        auth_response = await ac.post(
            f"{settings.API_V1_STR}/usuario/login",
            data={"username": "testuser12345@example.com", "password": "password123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert auth_response.status_code == 200
        
        user_email = auth_response.json()["email"]
        
        response_email = await ac.get(f"{settings.API_V1_STR}/usuario/usuario-email/{user_email}")
        assert response_email.status_code == 200

        user_id = auth_response.json()["id"]

        response_id = await ac.get(f"{settings.API_V1_STR}/usuario/usuario-id/{user_id}")
        assert response_id.status_code == 200
        
        response_all = await ac.get(f"{settings.API_V1_STR}/usuario/")
        assert response_all.status_code == 200
        

@pytest.mark.asyncio
async def test_put_user():
        async with AsyncClient(app=app, base_url='http://localhost:8000/') as ac:
            create_response = await ac.post(
                f"{settings.API_V1_STR}/usuario/signup",
                json={
                    "firstName": "TestPutUser",
                    "lastName": "User",
                    "username": "testuserputuser",
                    "email": "testuserputuser@example.com",
                    "senha": "password123"
                },
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            assert create_response.status_code == 201

            auth_response = await ac.post(
                f"{settings.API_V1_STR}/usuario/login",
                data={"username": "testuserputuser@example.com", "password": "password123"},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            assert auth_response.status_code == 200

            auth_data = auth_response.json()
            access_token = auth_data["token"]
            headers = {"Authorization": f"Bearer {access_token}"}
    
            user_id = auth_data["id"]
    
            response = await ac.put(
                f"{settings.API_V1_STR}/usuario/{user_id}",
                json={
                    "firstName": "UpdatedFirstName",
                    "lastName": "UpdatedLastName",
                    "username": "updateduserputuser",
                    "email": "updateduserputuser@example.com",
                    "senha": "newpassword123"
                },
                headers=headers
            )
            assert response.status_code == 202

            response = await ac.get(f"{settings.API_V1_STR}/usuario/usuario-id/{user_id}", headers=headers)
            assert response.status_code == 200
            assert response.json()["email"] == "updateduserputuser@example.com"
        
        
@pytest.mark.asyncio
async def test_del_user():
    async with AsyncClient(app=app, base_url='http://localhost:8000/') as ac:
        create_response = await ac.post(
            f"{settings.API_V1_STR}/usuario/signup",
            json={
                "firstName": "TestDel",
                "lastName": "User",
                "username": "testuserDel",
                "email": "testuserDel@example.com",
                "senha": "password123"
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        assert create_response.status_code == 201
        
        auth_response = await ac.post(
            f"{settings.API_V1_STR}/usuario/login",
            data={"username": "testuserDel@example.com", "password": "password123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert auth_response.status_code == 200
        
        auth_data = auth_response.json()
        access_token = auth_data["token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        user_id = auth_data["id"]
        
        response = await ac.delete(f"{settings.API_V1_STR}/usuario/{auth_response.json()['id']}", headers=headers)
        assert response.status_code == 204
        
        response = await ac.get(f"{settings.API_V1_STR}/usuario/usuario-id/{user_id}", headers=headers)
        assert response.status_code == 404
        
        