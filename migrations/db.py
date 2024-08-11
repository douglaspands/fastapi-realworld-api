from alembic import op

from app.core.settings import get_settings


def grant():
    settings = get_settings()
    if settings.db_url.scheme == "postgresql+psycopg":
        op.execute("""
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO fastapi_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO fastapi_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO fastapi_user;
               """)
