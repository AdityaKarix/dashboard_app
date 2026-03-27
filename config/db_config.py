import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="10.250.55.124",
        user="karix_dashboard_11",
        password="Karix@2026",
        database="karixdummy"
    )