from app import get_db, create_app

def test_connection():
    """Test AWS RDS database connection"""
    app = create_app()

    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print("AWS RDS Connection Successful:", result)
        cursor.close()
        db.close()

if __name__ == "__main__":
    test_connection()