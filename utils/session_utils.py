import uuid
from config.db_config import get_connection

def create_session(user_id):
    conn = get_connection()
    session_id = str(uuid.uuid4())
    session_token = str(uuid.uuid4())
    query = """
        INSERT INTO user_sessions (session_id, user_id, session_token)
        VALUES (%s, %s, %s)
    """
    cur = conn.cursor()
    cur.execute(query, (session_id, user_id, session_token))
    conn.commit()
    conn.close()
    return session_id, session_token

def validate_session(session_id, session_token):
    conn = get_connection()
    query = """
        SELECT user_id, is_active
        FROM user_sessions
        WHERE session_id=%s AND session_token=%s AND is_active=1
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (session_id, session_token))
    user_session = cur.fetchone()
    conn.close()
    return user_session["user_id"] if user_session else None

def logout_session(session_id):
    conn = get_connection()
    query = "UPDATE user_sessions SET is_active=0 WHERE session_id=%s"
    cur = conn.cursor()
    cur.execute(query, (session_id,))
    conn.commit()
    conn.close()