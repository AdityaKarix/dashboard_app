import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="db.karix.in",
        user="karix_dashboard_11",
        password="Karix@2026",
        database="karixdummy"
    )