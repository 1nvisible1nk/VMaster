import contextlib
import sqlite3

conn = sqlite3.connect("testing.db")
c = conn.cursor()

c.execute(
    """
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id INTEGER PRIMARY KEY
    )
""",
)

with contextlib.suppress(sqlite3.OperationalError):
    c.execute(
        """
        ALTER TABLE guilds
        ADD COLUMN channel_id INTEGER
    """,
    )
    
with contextlib.suppress(sqlite3.OperationalError):
    c.execute(
        """
        ALTER TABLE guilds
        ADD COLUMN role_id INTEGER
        """,
    )

def set_channel_id(guild_id: int, channel_id: int):
    print(f"Setting channel ID {channel_id} for guild {guild_id}")
    c.execute(
        "INSERT into guilds(channel_id, guild_id) VALUES (?, ?) ON CONFLICT DO UPDATE SET channel_id = ? WHERE guild_id = ?",
        (channel_id, guild_id, channel_id, guild_id),
    )
    conn.commit()
    print("Changes committed")

def get_channel_id(guild_id: int) -> int:
    c.execute("SELECT channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
    result = c.fetchone()
    return result[0] if result else None

def set_role_id(guild_id: int, role_id: int):
    print(f"Setting role ID {role_id} for guild {guild_id}")
    c.execute(
        "UPDATE guilds SET role_id = ? WHERE guild_id = ?",
        (role_id, guild_id),
    )
    conn.commit()
    print("Changes committed")

def get_role_id(guild_id: int) -> int:
    c.execute("SELECT role_id FROM guilds WHERE guild_id = ?", (guild_id,))
    result = c.fetchone()
    return result[0] if result else None


def add_guild_if_not_exists(guild_id: int):
    c.execute(
        "INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)",
        (guild_id,),
    )
    conn.commit()