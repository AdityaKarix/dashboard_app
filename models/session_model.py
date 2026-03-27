import uuid
from config.db_config import get_connection

def create_session(user_id,ip,user_agent):

    session_id=str(uuid.uuid4())
    token=str(uuid.uuid4())

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO user_sessions
        (session_id,user_id,session_token,ip_address,user_agent)
        VALUES(%s,%s,%s,%s,%s)
    """,(session_id,user_id,token,ip,user_agent))

    conn.commit()
    conn.close()

    return token


def logout_session(token):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        UPDATE user_sessions
        SET logout_time=NOW(), is_active=0
        WHERE session_token=%s
    """,(token,))

    conn.commit()
    conn.close()