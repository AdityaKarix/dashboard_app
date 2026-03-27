import pandas as pd
from config.db_config import get_connection

def get_usecase_data():

    conn=get_connection()

    df=pd.read_sql("SELECT * FROM usecase WHERE is_active=1",conn)

    conn.close()

    return df


def insert_usecase(data):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO usecase
        (waba_number,keyword,mobile_number,recommend,impact,efficacy,performance,teaming,improve,correlation_id)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,tuple(data.values()))

    conn.commit()
    conn.close()