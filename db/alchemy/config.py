from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from supabase_config import SUPABASE_URL_POOL


engine = create_engine(SUPABASE_URL_POOL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
