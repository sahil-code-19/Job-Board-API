async def test_list_job_success(async_client):
    response = await async_client.get("/api/jobs/all")
    assert response.status_code == 200

async def test_get_single_job_success(async_client, job_id):
    response = await async_client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200

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

async def test_delete_job_success(async_client, job_id):
    response = await async_client.delete(f"/api/jobs/delete/{job_id}")
    assert response.status_code == 200

async def test_edit_job_success(async_client, job_id):
    response = await async_client.patch(f"/api/jobs/edit/{job_id}", json={
        "title" : "Software/AI/ML Engineer",
        "description" : "We are looking for passinoate software/AI engineer",
        "job_category" : "Software development/ AI-ML developement",
    })
    assert response.status_code == 200

async def test_full_edit_job_success(async_client, company_id, job_id):
    response = await async_client.put(f"/api/jobs/full-edit/{job_id}", json={
        "title" : "DevOPs Engineer",
        "description" : "We are looking for passinoate DevOps engineer",
        "salary_range" : "12L-15L/A",
        "job_type" : "remote",
        "job_category" : "cloud development",
        "company_id" : company_id,
        "company_website" : "www.decops.com",
        "company_description" : "We are lookin for ...."
    })
    assert response.status_code == 200
