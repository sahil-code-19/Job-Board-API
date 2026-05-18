import httpx

RESEND_API_KEY = "re_eMxFw6Fr_KeZiSCL4n2NvC1fT4AW62twc"

async def send_email(to_email: str, subject: str, body: str):
    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
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