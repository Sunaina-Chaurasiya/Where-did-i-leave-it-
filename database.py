import sqlite3
import os
from datetime import datetime

# Path to the database
db_path = r"C:\Users\SUNAINA\Desktop\hackathon\items.db"

# Create the table if it doesn't exist
def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        location TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Database and 'items' table created successfully.")

# Save an item to the database
def save_item_to_db(item, location):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO items (item, location, timestamp)
        VALUES (?, ?, ?)
    """, (item, location, timestamp))
    conn.commit()
    conn.close()
    print(f"✅ Saved: {item} at {location} on {timestamp}")

# Run this only if script is executed directly
if __name__ == "__main__":
    initialize_database()
# Add this to database.py

def get_item_location(item_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT location, timestamp FROM items 
        WHERE item = ? 
        ORDER BY timestamp DESC 
        LIMIT 1
    """, (item_name,))
    result = cursor.fetchone()
    conn.close()
    return result  # returns (location, timestamp) or None
