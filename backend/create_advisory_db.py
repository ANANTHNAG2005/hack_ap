# create_advisory_db.py
import sqlite3

conn = sqlite3.connect("advisory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS advisories (
    disease_name TEXT PRIMARY KEY,
    advice TEXT
)
""")

advisories = [
    ("Apple___scab", "Use organic fungicide and maintain leaf hygiene."),
    ("Tomato___Bacterial_spot", "Remove infected leaves, use copper-based sprays."),
    ("Tomato___healthy", "No disease detected. Keep monitoring your crop."),
    ("Apple___healthy", "No disease detected. Keep monitoring your crop."),
]

cursor.executemany(
    "INSERT OR REPLACE INTO advisories (disease_name, advice) VALUES (?, ?)",
    advisories
)
conn.commit()
conn.close()
print("[INFO] Database created successfully!")
