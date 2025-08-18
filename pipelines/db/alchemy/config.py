from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from supabase_config import supabase_pool_url


engine = create_engine(supabase_pool_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
