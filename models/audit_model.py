from config.db_config import get_connection
import json

def log_action(user_id,action,table_name,record_id,old_value,new_value):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs
        (user_id,action,table_name,record_id,old_value,new_value)
        VALUES(%s,%s,%s,%s,%s,%s)
    """,(user_id,action,table_name,record_id,
        json.dumps(old_value),json.dumps(new_value)))

    conn.commit()
    conn.close()