async def test_register_success(async_client):
    response = await async_client.post(
        "/api/auth/register",
        json={"email":"admin1@example.com", "username":"admin1", "role":"candidate", "password":"Password@123"}
        )
    assert response.status_code == 201


async def test_register_duplicate_email(async_client):
    await async_client.post(
        "/api/auth/register",
        json={"email":"admin2@example.com", "username":"admin2", "role":"candidate", "password":"Password@123"}
        )
    response = await async_client.post(
        "/api/auth/register",
        json={"email":"admin2@example.com", "username":"admin2", "role":"candidate", "password":"Password@123"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail":"Email id already taken"}

async def test_login_success(async_client):
    await async_client.post(
        "/api/auth/register",
        json={"email":"admin3@example.com", "username":"admin3", "role":"candidate", "password":"Password@123"}
    )
    response = await async_client.post(
        "/api/auth/login",
        json={"email":"admin3@example.com", "password":"Password@123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_login_wrong_password(async_client):
    await async_client.post(
        "/api/auth/register",
        json={"email":"admin4@example.com", "username":"admin4", "role":"candidate", "password":"Password@123"}
    )
    response = await async_client.post(
        "/api/auth/login",
        json={"email":"admin4@example.com", "password":"Password@456"}
    )
    assert response.status_code == 400

async def test_login_inactive_user(async_client):
    await async_client.post(
        "/api/auth/register",
        json={"email":"admin5@example.com", "username":"admin5", "role":"candidate", "password":"Password@123", "is_active": False}
    )
    response = await async_client.post(
        "/api/auth/login",
        json={"email":"admin5@example.com", "password":"Password@123"}
    )
    assert response.status_code == 200