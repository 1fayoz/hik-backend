import datetime
import io
from typing import Dict, Any

import httpx


async def send_telegram_message(
    text: str,
    max_text_length: int = 4000,
) -> Dict[str, Any]:
    url = f"https://api.telegram.org/bot8061492806:AAFwgOo33AoBtAv6-7SAbSfA6wUEMp9u3rM/sendMessage"
    user_id = 5593831038

    async with httpx.AsyncClient(timeout=20.0) as client:
        if len(text) <= max_text_length:
            payload = {
                "chat_id": user_id,
                "text": text,
                "parse_mode": "HTML",
            }
            response = await client.post(url, json=payload)
        else:
            url = f"https://api.telegram.org/bot8061492806:AAFwgOo33AoBtAv6-7SAbSfA6wUEMp9u3rM/sendDocument"

            file_data = io.BytesIO(text.encode("utf-8"))
            file_data.name = f"message-{datetime.datetime.now()}.txt"

            form = {
                "chat_id": str(user_id),
                "caption": "📄 Xabar juda uzun bo‘lgani uchun fayl sifatida yuborildi.",
            }

            files = {"document": (file_data.name, file_data, "text/plain")}
            response = await client.post(url, data=form, files=files)

        data = response.json()

        if response.status_code != 200:
            print("❌ Telegram error:", data)
        else:
            print("✅ Xabar muvaffaqiyatli yuborildi")
        return data
