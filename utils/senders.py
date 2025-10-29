from typing import Dict, Any

import httpx


async def send_telegram_message(
    text: str,
) -> Dict[str, Any]:
    url = f"https://api.telegram.org/bot8061492806:AAFwgOo33AoBtAv6-7SAbSfA6wUEMp9u3rM/sendMessage"

    payload = {
        "chat_id": 5593831038,
        "text": text,
        "parse_mode": "HTML",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
