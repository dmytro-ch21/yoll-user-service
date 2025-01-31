from app import create_app, get_db

def create_tables():
    """Create database tables using raw SQL."""
    app = create_app()  # Initialize Flask app

    with app.app_context():  # Ensure we're inside an app context
        db = get_db()
        cursor = db.cursor()

        # Create Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """)

        # Create Movies Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                genre VARCHAR(100),
                release_year INT,
                user_id INT REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # Create Todos Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                task TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                user_id INT REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        db.commit()
        cursor.close()
        db.close()

    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()