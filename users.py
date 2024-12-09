import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('task_manager.db')
cursor = conn.cursor()

# Query the User table
cursor.execute("SELECT * FROM user")  # Replace with your table name
users = cursor.fetchall()

# Print all records
for user in users:
    print(user)

# Close the connection
conn.close()