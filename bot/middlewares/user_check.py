from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.repository import UserRepository
from bot.utils.messages import BANNED_MESSAGE


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data.get("session")
        if not session:
            return await handler(event, data)

        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None

        if not user_id:
            return await handler(event, data)

        repo = UserRepository(session)
        user, _ = await repo.get_or_create(
            user_id,
            username=getattr(
                getattr(event, "from_user", None), "username", None
            ),
        )

        if user.is_banned:
            if isinstance(event, Message):
                await event.answer(BANNED_MESSAGE)
            elif isinstance(event, CallbackQuery):
                await event.answer(BANNED_MESSAGE, show_alert=True)
            return

        data["user"] = user
        data["user_repo"] = repo
        return await handler(event, data)
