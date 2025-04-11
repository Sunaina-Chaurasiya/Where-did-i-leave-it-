import sqlite3
import os

# Make sure the path is absolute and consistent
db_path = r"C:\Users\SUNAINA\Desktop\hackathon\items.db"
print(f"[DEBUG] Connecting to DB at: {db_path}")

# Safety check
if not os.path.exists(db_path):
    print("❌ ERROR: Database not found!")
    exit()

# Connect and clear items
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Delete all records from the items table
    cursor.execute("DELETE FROM items")
    conn.commit()
    print("✅ All items have been deleted.")

    # Optional: reclaim DB file size
    cursor.execute("VACUUM")
    print("✅ Database vacuumed.")

    # Reset the auto-increment counter for the ID column
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'items'")
    print("✅ Auto-increment counter reset to 0.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    conn.close()

