import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud.user import get_user_by_email
from app.database import get_db_session
from app.models.user import UserDB
from app.utils.auth import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db(session: AsyncSession) -> None:
    user = await get_user_by_email(session, settings.FIRST_SUPERUSER)
    if not user:
        superuser = UserDB(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER,
            first_name="Admin",
            last_name="User",
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            is_active=True,
        )
        session.add(superuser)
        await session.commit()
        await session.refresh(superuser)
        logger.info("Superuser created.")
    else:
        logger.info("Superuser already exists.")


async def main() -> None:
    logger.info("Creating initial data...")
    async for session in get_db_session():
        await init_db(session)
    logger.info("Initial data created.")


if __name__ == "__main__":
    asyncio.run(main())
