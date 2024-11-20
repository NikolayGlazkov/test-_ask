from fastapi import FastAPI, Query
from typing import Optional
import sqlite3
from datetime import datetime

app = FastAPI()


def get_db_connection():
    conn = sqlite3.connect("traffic_data.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/traffic")
def get_traffic(
    customer_id: Optional[int] = Query(None, description="ID клиента"),
    start_date: Optional[str] = Query(None, description="Начальная дата (формат: YYYY-MM-DD HH:MM:SS)"),
    end_date: Optional[str] = Query(None, description="Конечная дата (формат: YYYY-MM-DD HH:MM:SS)"),
    ip: Optional[str] = Query(None, description="IP-адрес")
):
    """
    Получить суммарный трафик за весь период по клиентам, с поддержкой фильтров:
    - По ID клиента
    - По диапазону дат (start_date, end_date)
    - По IP-адресу
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    
    query = """
    SELECT c.id as customer_id, c.name as customer_name, SUM(t.received_traffic) as total_traffic
    FROM traffic t
    JOIN customers c ON t.customer_id = c.id
    WHERE 1=1
    """
    params = []

    if customer_id:
        query += " AND c.id = ?"
        params.append(customer_id)
    if start_date:
        query += " AND t.date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND t.date <= ?"
        params.append(end_date)
    if ip:
        query += " AND t.ip = ?"
        params.append(ip)


    query += " GROUP BY c.id"

  
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

   
    return [
        {
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "total_traffic": row["total_traffic"]
        }
        for row in results
    ]


# uvicorn main:app --reload
