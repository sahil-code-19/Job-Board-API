from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from io import BytesIO
from unittest.mock import AsyncMock

from app.main import app
from app.database import get_db
from app.core.limiter import limiter
from app.websockets.manager import ConnectionManager

import os
import pytest
import uuid
import random

load_dotenv()

app.state.manager = ConnectionManager()
app.state.redis = AsyncMock()
app.state.redis.publish = AsyncMock()
app.state.metrics = {
    "total_requests": 0,
    "total_errors": 0,
    "total_latency_ms": 0.0
}
limiter.enabled = False

DATABASE_URL = os.getenv("TEST_DATABASE_URI")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_test_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

@pytest.fixture(scope="session")
async def setup_db():
    await create_db_and_tables()

@pytest.fixture(scope="function")
async def db_session(setup_db):
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture(scope="function")
async def async_client(db_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        app.dependency_overrides[get_db] = get_test_db
        yield client
        app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def employer_token(async_client):
    unique_hex = uuid.uuid4().hex[:8]
    await async_client.post("/api/auth/register", json={
        "email": f"employee_{unique_hex}@example.com",
        "username": f"employee_{unique_hex}",
        "role": "employer",
        "password":"Password@123"
    })

    response = await async_client.post("/api/auth/login", json={
        "email": f"employee_{unique_hex}@example.com",
        "password": "Password@123"
    })
    print(f"######################{response.json()}")
    yield response.json()['access_token']

@pytest.fixture(scope="function")
async def candidate_token(async_client):
    unique_hex = uuid.uuid4().hex[:8]
    await async_client.post("/api/auth/register", json={
        "email": f"candidate_{unique_hex}@example.com",
        "username": f"candidate_{unique_hex}",
        "role": "candidate",
        "password":"Password@123"
    })

    response = await async_client.post("/api/auth/login", json={
        "email": f"candidate_{unique_hex}@example.com",
        "password": "Password@123"
    })

    yield response.json()['access_token']

@pytest.fixture(scope="function")
async def user_token(async_client):
    role = ["candidate", "employer"]
    
    unique_hex = uuid.uuid4().hex[:8]
    await async_client.post("/api/auth/register", json={
        "email": f"user_{unique_hex}@example.com",
        "username": f"user_{unique_hex}",
        "role": random.choice(role),
        "password":"Password@123",
    })
    response = await async_client.post("/api/auth/login", json={
        "email": f"user_{unique_hex}@example.com",
        "password": "Password@123"
    })
    tokens = {
        "access_token": response.json()['access_token'], 
        "refresh_token": response.json()['refresh_token']
    }
    yield tokens

@pytest.fixture(scope="function")
async def company_id(async_client, employer_token):

    response = await async_client.post("/api/company/create", json={
        "name": f"Company_{uuid.uuid4().hex[:8]}",
        "description": "Giga company is AI company",
        "website": "www.giga.com"
    }, headers={"Authorization": f"Bearer {employer_token}"})

    yield response.json()['owner_id']

@pytest.fixture(scope="function")
async def job_id(async_client, employer_token, company_id):
    response = await async_client.post("/api/jobs/create", json={
        "title" : "Software Engineer",
        "description" : "We are looking for passinoate software engineer",
        "salary_range" : "5L-10L/A",
        "job_type" : "Full-time",
        "job_category" : "Software development",
        "company_id" : company_id,
        "company_website" : "www.you.com",
        "company_description" : "We are ...."
    }, headers={"Authorization": f"Bearer {employer_token}"})

    yield response.json()['id']

@pytest.fixture(scope="function")
async def application_id(async_client, candidate_token, job_id):
    response = await async_client.post("/api/application/apply", data={
        "job_id": job_id,
        "cover_letter": "Hellow I am applying!"
    }, files={"file": ("cv.pdf", BytesIO(b"fake pdf content"), "application/pdf")}, 
    headers={"Authorization": f"Bearer {candidate_token}"})
    
    yield response.json()['id']