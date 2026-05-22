import json
from redis.asyncio import Redis

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.notification import Notification

async def create_and_push(
    db: AsyncSession,
    redis: Redis,
    user_id: int,
    message: str,
) -> Notification:
    
    notif = Notification(
        user_id=user_id,
        message=message,
        is_read=False
    )

    db.add(notif)
    await db.commit()
    await db.refresh(notif)

    await redis.publish(
        f"notification:{user_id}",
        json.dumps({"type": "notification", "message": message})
    )

    return notif