from io import BytesIO

async def test_apply_job(async_client, candidate_token, job_id):
    response = await async_client.post("/api/application/apply", data={
        "job_id": job_id,
        "cover_letter": "Hellow I am applying!"
    }, files={"file": ("cv.pdf", BytesIO(b"fake pdf content"), "application/pdf")}, 
    headers={"Authorization": f"Bearer {candidate_token}"})
    assert response.status_code == 201

async def test_change_status_application_success(async_client, application_id):
    response = await async_client.post(f"/api/application/{application_id}/status", json={
        "status" : "reviewed"
    })
    assert response.status_code == 200