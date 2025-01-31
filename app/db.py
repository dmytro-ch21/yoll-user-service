import psycopg2
from flask import g, current_app  # Use current_app instead of create_app

def get_db():
    """Establish a database connection if one does not exist"""
    if 'db' not in g:
        config = current_app.config['DATABASE']  # Use Flask's global config
        print(config['dbname'])
        print(config['user'])
        print(config['password'])
        print(config['host'])
        print(config['port'])
        g.db = psycopg2.connect(
            dbname=config['dbname'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )
    return g.db

def close_db(exception=None):
    """Close the database connection after request"""
    db = g.pop('db', None)
    if db is not None:
        db.close()