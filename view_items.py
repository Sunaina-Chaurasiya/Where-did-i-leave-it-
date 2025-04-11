# view_items.py
import sqlite3

def view_saved_items():
    db_path = r"C:\Users\SUNAINA\Desktop\hackathon\items.db"
    print(f"[DEBUG] Connecting to DB at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()

    if rows:
        print("📦 Saved Items:")
        for row in rows:
            print(f"🔹 ID: {row[0]} | Item: {row[1]} | Location: {row[2]} | Time: {row[3]}")
    else:
        print("📭 No items found in the database.")

    conn.close()

if __name__ == "__main__":
    view_saved_items()

