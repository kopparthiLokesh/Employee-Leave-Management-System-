import sqlite3
import csv

conn = sqlite3.connect("leave_management.db")

for table in ("employees", "leave_requests"):
    cursor = conn.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    with open(f"{table}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"Exported {table}: {len(rows)} rows")

conn.close()