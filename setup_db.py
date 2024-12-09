from app import db, User, Task  # Import db and models from app.py

db.connect()
db.create_tables([Task])
db.close()
print("Tables created successfully!")