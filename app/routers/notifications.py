from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends, HTTPException

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..auth.jwt import decode_token
from ..auth.dependencies import get_current_user
from ..models.user import User
from ..models.notification import Notification

router = APIRouter(tags=["Notifications"])

@router.websocket("/ws/notifications")
async def ws_notifications(
    websocket: WebSocket,
    token: str
):
    user = decode_token(token)

    if not user:
        await websocket.close(code=1008)
        return
    
    manager = websocket.app.state.manager
    user_id = int(user["sub"])
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)

@router.get("/notifications")
async def unread_notificaftions(
    current_user: User = Depends(get_current_user),
    db : AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .where(Notification.is_read == False)
        .order_by(Notification.created_at.desc())
    )

    return result.scalars().all()

@router.post("/mark-read")
async def mark_read(
    id : int,
    current_user : User = Depends(get_current_user),
    db : AsyncSession = Depends(get_db)
):
    notif = await db.get(Notification, id)

    if not notif or notif.user_id != current_user.id:
        raise HTTPException(status_code=404)
    
    notif.is_read = True
    await db.commit()
    await db.refresh(notif)

    return {"ok": True}