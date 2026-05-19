from io import BytesIO

async def test_apply_job(async_client, candidate_token, job_id):
    response = await async_client.post("/api/application/apply", data={
        "job_id": job_id,
        "cover_letter": "Hellow I am applying!"
    }, files={"file": ("cv.pdf", BytesIO(b"fake pdf content"), "application/pdf")}, 
    headers={"Authorization": f"Bearer {candidate_token}"})
    assert response.status_code == 201