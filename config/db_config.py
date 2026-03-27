import mysql.connector
import traceback

def get_connection():
    try:
        return mysql.connector.connect(
            host="db.karix.in",
            user="karix_dashboard_11",
            password="your_password",
            database="karixdummy",
            port=3306
        )
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        raise