import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False
    )


def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE,
                    time TIME,
                    name VARCHAR(255),
                    amount INT,
                    category VARCHAR(100),
                    notes TEXT
                )
            """)
        conn.commit()


def fetch_all_expenses():
    with get_db_connection() as conn:
        query = "SELECT id, date, time, name, amount, category, notes FROM expenses"
        df = pd.read_sql(query, conn)

    if not df.empty:
        df["Date"] = df["date"].apply(lambda x: x.strftime("%d-%b-%Y") if x else "")
        df["Time"] = df["time"].apply(lambda x: str(x).split()[-1][:5] if x else "")
        # Here time is a Timedelta object like Timedelta('0 days 14:56:00').
        # We only want "14:56".

        df = df.rename(columns={
            "name": "Name",
            "amount": "Amount",
            "category": "Category",
            "notes": "Notes"
        })

        df = df[["Date", "Time", "Name", "Amount", "Category", "Notes", "id"]]

    else:
        df = pd.DataFrame(columns=["Date", "Time", "Name", "Amount", "Category", "Notes", "id"])

    return df


def insert_expense(date, time, name, amount, category, notes):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO expenses (date, time, name, amount, category, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (date, time, name, amount, category, notes)
            cursor.execute(query, values)
        
        conn.commit()


def delete_expense(expense_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = "DELETE FROM expenses WHERE id = %s"
            cursor.execute(query, (expense_id,))  # SQL expects a tuple/list

        conn.commit()


def clear_all_expenses():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE expenses")

        conn.commit()