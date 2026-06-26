"""Test environment defaults so the app imports without real secrets/DB."""
import os

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://book:book@localhost:5432/booktv")
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("OPENAI_API_KEY", "test-openai")
os.environ.setdefault("SUPABASE_URL", "http://localhost")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "test-supabase")
os.environ.setdefault("CORS_ORIGIN", "http://localhost:5173")
