import mysql.connector
import os

# ==========================================
# 1. DATABASE CONFIGURATION & INITIALIZATION (Aiven.io MySQL)
# ==========================================
def get_db_connection():
    db_host = os.environ.get("DB_HOST", "localhost")
    
    # Aiven strictly requires SSL connections.
    # We enforce SSL but disable strict cert verification so you don't 
    # have to manually upload Aiven's ca.pem file to Render.
    ssl_args = {"ssl_disabled": False, "ssl_verify_cert": False} if db_host != "localhost" else {}
    
    return mysql.connector.connect(
        host=db_host,
        port=int(os.environ.get("DB_PORT", 3306)), # Aiven uses a custom 5-digit port
        user=os.environ.get("DB_USER", "avnadmin"), # Aiven's default user
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "defaultdb"), # Aiven's default database
        **ssl_args
    )

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create table if it doesn't exist. MySQL uses DECIMAL for grades.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                grade DECIMAL(5, 2) NOT NULL,
                section VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
