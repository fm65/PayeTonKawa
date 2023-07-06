import sqlite3

# Connect to the database (create a new one if it doesn't exist)
conn = sqlite3.connect("mydatabase.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (email TEXT PRIMARY KEY, token TEXT, is_admin INTEGER DEFAULT 0 )''')

# Commit the changes and close the connection
conn.commit()
conn.close()
