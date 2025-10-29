
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")


connect_args = {}
if DATABASE_URL.startswith("mysql"):
    import aiomysql  # noqa: F401

    ssl_ca_path = os.getenv("MYSQL_SSL_CA_PATH")
    ssl_ca_inline = os.getenv("MYSQL_SSL_CA")
    # If set to "false", skip CA verification (SSL still enabled, just not verified)
    skip_ssl_verify = os.getenv("MYSQL_SKIP_SSL_VERIFY", "false").lower() == "true"

    if ssl_ca_path and os.path.exists(ssl_ca_path):
        connect_args = {"ssl": {"ca": ssl_ca_path}}
    elif ssl_ca_inline:
        # Write inline CA to temp file
        os.makedirs("cache", exist_ok=True)
        ssl_ca_path = os.path.join("cache", "aiven-ca.pem")
        with open(ssl_ca_path, "w", encoding="utf-8") as f:
            f.write(ssl_ca_inline)
        connect_args = {"ssl": {"ca": ssl_ca_path}}
    elif skip_ssl_verify:
        # Use SSL but skip CA verification (simpler, less secure but still encrypted)
        connect_args = {"ssl": {"check_hostname": False, "verify_mode": False}}
    # If DATABASE_URL has ssl=true but no CA provided, use basic SSL
    elif "ssl=true" in DATABASE_URL.lower() or "ssl_mode=required" in DATABASE_URL.lower():
        connect_args = {"ssl": {}}

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
