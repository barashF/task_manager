from .config import load_config
import asyncpg
from contextlib import asynccontextmanager

import os
from pathlib import Path


env_path = Path.cwd() / ".env"

config = load_config(str(env_path))


pool = None


async def init_db():
    global pool
    print(f"Connecting to DB: host={config.db.database_host}, port={config.db.database_port}, user={config.db.database_user}, db={config.db.database_name}")
    pool = await asyncpg.create_pool(
        host=config.db.database_host,
        port=config.db.database_port,
        user=config.db.database_user,
        password=config.db.database_password,
        database=config.db.database_name
    )

    async with pool.acquire() as conn:
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

        try:
            await conn.execute('''
                CREATE TYPE task_status AS ENUM ('created', 'in_progress', 'completed')
            ''')
        except asyncpg.DuplicateObjectError:
            pass

        await conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status task_status NOT NULL DEFAULT 'created',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    
        await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
            ''')


@asynccontextmanager
async def get_db():
    if pool is None:
        await init_db()
    
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)


async def get_db_connection():
    async with get_db() as conn:
        yield conn