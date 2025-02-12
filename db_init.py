from app import create_app, get_db


def create_tables():
    """Create database tables using raw SQL if they don't exist."""
    app = create_app()
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='users');"
        )
        if cursor.fetchone()[0]:
            print("✅ Tables already exist, skipping initialization.")
            return

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                genre VARCHAR(100),
                release_year INT,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                full_name VARCHAR(255) NOT NULL,
                phone_number VARCHAR(50),
                email VARCHAR(255),
                street VARCHAR(255),
                city VARCHAR(100),
                state VARCHAR(100),
                postal_code VARCHAR(20),
                country VARCHAR(100),
                additional_info TEXT,
                instagram_link VARCHAR(255),
                facebook_link VARCHAR(255),
                x_link VARCHAR(255),
                base64_image TEXT,
                created_at BIGINT DEFAULT (EXTRACT(EPOCH FROM CURRENT_TIMESTAMP))::BIGINT,
                is_favorite BOOLEAN DEFAULT FALSE
            );
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                contact_id INT REFERENCES contacts(id) ON DELETE CASCADE,
                PRIMARY KEY (user_id, contact_id)
            );
        """
        )

        db.commit()
        cursor.close()
        db.close()

        print("✅ Database tables created successfully!")


if __name__ == "__main__":
    create_tables()
