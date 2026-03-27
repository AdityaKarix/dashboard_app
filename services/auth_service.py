from utils.security import hash_password
from utils.session_utils import create_session, validate_session
from config.db_config import get_connection

def login_user(email, password):
    hashed_pw = hash_password(password)
    conn = get_connection()
    query = "SELECT id, name, level, is_active FROM users WHERE email=%s AND password=%s AND is_active=1"
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (email, hashed_pw))
    user = cur.fetchone()
    conn.close()
    if user:
        session_id, session_token = create_session(user["id"])
        return {
            "user_id": user["id"],
            "name": user["name"],
            "level": user["level"],
            "session_id": session_id,
            "session_token": session_token
        }
    return None