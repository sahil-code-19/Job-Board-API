async def test_list_job_success(async_client):
    response = await async_client.get("/api/jobs/all")
    assert response.status_code == 200

# async def test_get_single_job_success(async_client):
#     response = await async_client.get("/api/jobs/{1}")
#     assert response.status_code == 200

async def test_create_job_as_employeer(async_client, employer_token, company_id):
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
    assert response.status_code == 201


async def test_create_job_as_candidate_forbidden(async_client, candidate_token, company_id):
    response = await async_client.post("/api/jobs/create", json={
        "title" : "Software Engineer",
        "description" : "We are looking for passinoate software engineer",
        "salary_range" : "5L-10L/A",
        "job_type" : "Full-time",
        "job_category" : "Software development",
        "company_id" : company_id,
        "company_website" : "www.you.com",
        "company_description" : "We are ...."
    }, headers={"Authorization": f"Bearer {candidate_token}"})
    assert response.status_code == 403



async def test_create_job_missing_field(async_client, employer_token):
    # Title is missing, No company id given
    response = await async_client.post("/api/jobs/create", json={
        "description" : "We are looking for passinoate software engineer",
        "salary_range" : "5L-10L/A",
        "job_type" : "Full-time",
        "job_category" : "Software development",
        "company_id" : None,
        "company_website" : "www.you.com",
        "company_description" : "We are ...."
    },  headers={"Authorization": f"Bearer {employer_token}"})
    assert response.status_code == 422