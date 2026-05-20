import os
import httpx

from ..core.config import get_settings

settings = get_settings()

async def send_email(to_email: str, subject: str, body: str):
    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {settings.resend_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": "onboarding@resend.dev",
        "to": [to_email],
        "subject": subject,
        "html": f"<p>{body}</p>",
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload)