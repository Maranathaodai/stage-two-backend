# database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# Import MySQL driver only when using a MySQL URL and build SSL connect args if provided
connect_args = {}
if DATABASE_URL.startswith("mysql"):
    import aiomysql  # noqa: F401

    ssl_ca_path = os.getenv("MYSQL_SSL_CA_PATH")
    ssl_ca_inline = os.getenv("MYSQL_SSL_CA")

    # Support inline CA cert: write to a temp path if provided
    if not ssl_ca_path and ssl_ca_inline:
        os.makedirs("cache", exist_ok=True)
        ssl_ca_path = os.path.join("cache", "aiven-ca.pem")
        with open(ssl_ca_path, "w", encoding="utf-8") as f:
            f.write(ssl_ca_inline)

    if ssl_ca_path and os.path.exists(ssl_ca_path):
        connect_args = {"ssl": {"ca": ssl_ca_path}}

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
