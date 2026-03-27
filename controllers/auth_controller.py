from models.user_model import get_user_by_email
from utils.security import hash_password, verify_password
from models.session_model import create_session
from config.db_config import get_connection
import uuid

def login(email, password):

    # Hardcoded admin user (no validation for testing)
    user = {
        "id": 1,
        "name": "Admin",
        "email": "admin@karix.com",
        "level": 1
    }
    hashed_pw = hash_password(password)
    conn = get_connection()
    query = "SELECT id, name, level, is_active FROM users WHERE email=%s AND password=%s AND is_active=1"
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (email, hashed_pw))
    user = cur.fetchone()
    conn.close()

    if user:
        # Create a session
        session_id = str(uuid.uuid4())
        session_token = str(uuid.uuid4())
        conn = get_connection()
        insert = "INSERT INTO user_sessions (session_id, user_id, session_token) VALUES (%s, %s, %s)"
        cur = conn.cursor()
        cur.execute(insert, (session_id, user["id"], session_token))
        conn.commit()
        conn.close()

        # Add session info to user dict
        user["session_id"] = session_id
        user["session_token"] = session_token
        return user
    return None

def validate_session(session_id, session_token):
    conn = get_connection()
    query = "SELECT user_id FROM user_sessions WHERE session_id=%s AND session_token=%s AND is_active=1"
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (session_id, session_token))
    result = cur.fetchone()
    conn.close()
    return result["user_id"] if result else None

def logout(user):
    conn = get_connection()
    update = "UPDATE user_sessions SET is_active=0 WHERE session_id=%s"
    cur = conn.cursor()
    cur.execute(update, (user["session_id"],))
    conn.commit()
    conn.close()