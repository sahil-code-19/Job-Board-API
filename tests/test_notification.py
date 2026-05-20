async def test_unread_notifications(async_client, user_token):
    response = await async_client.get("/api/notifications", headers={"Authorization": f"Bearer {user_token["access_token"]}"})
    assert response.status_code == 200

async def test_mark_notification_read(async_client, user_token, db_session):
    print(f"#######################################{user_token['access_token']}")
    user_response = await async_client.get("/api/auth/me", headers={"Authorization": f"Bearer {user_token["access_token"]}"})
    user = user_response.json()
    user_id = user["id"]

    from app.models.notification import Notification
    if user["role"] == "candidate":
        notification = Notification(
            user_id = user_id,
            message = "Hi You have applied for this company",
            is_read = False
        )
    else:
        notification = Notification(
            user_id = user_id,
            message = "Hi Someone applied for your job",
            is_read = False
        )
    db_session.add(notification)
    await db_session.commit()
    await db_session.refresh(notification)

    response = await async_client.post(f"/api/mark-read?id={notification.id}", headers={"Authorization": f"Bearer {user_token["access_token"]}"})
    assert response.status_code == 200