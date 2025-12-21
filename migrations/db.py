from alembic import op


def grant():
    op.execute("""
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO fastapi_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO fastapi_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO fastapi_user;
               """)
