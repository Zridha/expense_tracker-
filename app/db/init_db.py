from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.base import Base
from app.models import user, expense

async def init_models(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        