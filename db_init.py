from app import create_app, get_db

def create_tables():
    """Create database tables using raw SQL if they don't exist."""
    app = create_app()
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='users');")
        if cursor.fetchone()[0]:
            print("✅ Tables already exist, skipping initialization.")
            return

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                genre VARCHAR(100),
                release_year INT,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        db.commit()
        cursor.close()
        db.close()

        print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()