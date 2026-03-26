import psycopg2
import sys

DATABASE_URL = "postgresql://postgres.hrbndnvadhqfyncbryxw:Zz9oaKB2z5jUUPpC@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres?pgbouncer=true"

# Note: The bracket syntax `[password]` might literally contain brackets or they were added for emphasis.
# If the literal password is [Zz9oaKB2z5jUUPpC], we need to URL encode the brackets if psycopg2 complains.
# Usually, psycopg2 parses standard postgresql strings, but if it has unencoded brackets it might fail.

def create_tables():
    # Attempt to remove literal brackets since users often leave them in from the UI template.
    safe_db_url = DATABASE_URL.replace("[", "").replace("]", "")
    
    try:
        conn = psycopg2.connect(safe_db_url)
        cur = conn.cursor()
        
        # Create Users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            phone TEXT UNIQUE NOT NULL,
            platform TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Create Messages table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            phone TEXT REFERENCES users(phone),
            message TEXT,
            response TEXT,
            platform TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Create Leads table with a generic schema
        cur.execute("DROP TABLE IF EXISTS leads;")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id TEXT,
            main_category TEXT,
            sub_category TEXT,
            answers JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Database tables created successfully!")
        
    except Exception as e:
        print(f"Failed to connect or create tables: {e}")
        
if __name__ == "__main__":
    create_tables()
