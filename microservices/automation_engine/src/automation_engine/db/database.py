from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from automation_engine.settings import settings

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_hostname}:"
    f"{settings.db_port}/{settings.db_name}",
    echo=settings.debug,
    max_overflow=10,
    pool_size=10,
    pool_pre_ping=True
)

session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
