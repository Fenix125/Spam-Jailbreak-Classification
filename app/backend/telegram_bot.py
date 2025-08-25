import httpx
from telegram import Update
from telegram.ext import (Application, ApplicationBuilder,
                          ContextTypes, MessageHandler, filters)
from app.backend.config import settings

async def call_agent(prompt: str, backend_url: str) -> str:
    """
    Send the prompt to the backend /agent endpoint and return the reply.
    """
    url = backend_url + "/agent"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, params={"prompt": prompt})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return f"HTTP error from backend: {exc.response.status_code}"
        except Exception as exc:
            return f"Request failed: {exc}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return
    prompt = update.message.text
    answer = await call_agent(prompt, settings.backend_adress)
    await update.message.reply_text(answer)


def main() -> None:
    """
    Starts the Telegram bot
    """
    token = settings.telegram_bot_token
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN in your environment.")

    application: Application = ApplicationBuilder().token(token).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()