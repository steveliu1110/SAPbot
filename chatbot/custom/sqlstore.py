import sqlite3
import json
from datetime import datetime

# Initialize database connection
conn = sqlite3.connect("SAP.db")
cursor = conn.cursor()

# Create a table for storing scraped data
cursor.execute("""
CREATE TABLE IF NOT EXISTS update_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    last_update TEXT
)
""")

def update_scrapy_data(url):
    late_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO update_state (url, last_update) VALUES (?, ?)", 
       (url, late_update))
    
    conn.commit()
    print("Data saved to database.")

def add_new_site(url):
    cursor.execute("INSERT INTO update_state (url, last_update) VALUES (?, ?)", 
       (url, 'Not Fetched'))
    
    conn.commit()
    print("Data saved to database.")

if __name__ == "__main__":
    update_scrapy_data('www.freelancer.com')
    
    cursor.execute('SELECT * FROM update_state')
    result = cursor.fetchone()
    print(result)