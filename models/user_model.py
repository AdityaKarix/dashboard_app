from config.db_config import get_connection

def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM users
        WHERE email=%s AND is_active=1
        LIMIT 1
    """, (email,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def create_user(name,email,password,level):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO users(name,email,password,level)
        VALUES(%s,%s,%s,%s)
    """,(name,email,password,level))

    conn.commit()
    conn.close()