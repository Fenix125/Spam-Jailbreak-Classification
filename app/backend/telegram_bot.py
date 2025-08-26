from __future__ import annotations

import httpx
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from app.backend.config import settings

AGENT_URL = f"{settings.backend_adress}/agent"


async def call_agent(prompt: str) -> str:
    """
    POST the user's prompt to your FastAPI /api/agent endpoint.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(AGENT_URL, params={"prompt": prompt})
        resp.raise_for_status()
        return resp.json()


async def on_post_init(app: Application) -> None:
    me = await app.bot.get_me()
    print(f"[START] Bot @{me.username} ({me.id}) is up.")
    print(f"[INFO ] Backend agent endpoint: {AGENT_URL}")

async def on_post_shutdown(app: Application) -> None:
    print("[STOP ] Bot shutting down.")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot is running. Send me a message!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or update.message.text is None:
        return

    user = update.effective_user
    chat = update.effective_chat
    text = update.message.text

    print(f"[IN  ] from @{getattr(user, 'username', None)}({user.id}) "
          f"chat={chat.id}: {text}")

    try:
        reply = await call_agent(text)
    except httpx.HTTPStatusError as e:
        reply = f"Backend HTTP {e.response.status_code}"
        print(f"[ERR ] HTTPStatusError: {e} | body={e.response.text!r}")
    except Exception as e:
        reply = f"Backend request failed: {e!s}"
        print(f"[ERR ] {e!r}")
    else:
        preview = reply if not isinstance(reply, str) else (reply[:200] + "…") if len(reply) > 200 else reply
        print(f"[OUT ] to   @{getattr(user, 'username', None)}({user.id}) "
              f"chat={chat.id}: {preview}")

    await update.message.reply_text(reply)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"[ERR ] Unhandled exception: {context.error!r} | update={update!r}")



def main() -> None:
    token = settings.telegram_bot_token
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN in your environment.")

    print("[BOOT] Launching Telegram polling…")

    app: Application = (
        ApplicationBuilder()
        .token(token)
        .post_init(on_post_init)
        .post_shutdown(on_post_shutdown)
        .build()
    )

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
