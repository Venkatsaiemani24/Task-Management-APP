# # Task-Management-APP

## Project Overview: 
The **Task Management Application** is a web-based platform designed to help users efficiently manage their tasks.
It allows users to:
- Create, update, delete, and reorder tasks.
- Assign priorities and due dates to tasks.
- Securely log in and manage tasks with personalized dashboards.

## Steps to Set Up and Run the Code: 

### 1. Clone the Repository
Clone this repository to your local machine:
git clone https://github.com/veerareddy143/Task-Management-APP.git 
cd Task-Management-Application

### 2. Set Up a Virtual Environment
python -m venv task_manager_env
source task_manager_env/bin/activate  # For macOS/Linux
task_manager_env\Scripts\activate    # For Windows

### 3. Install Dependencies
Use the below command: 
pip install -r requirements.txt

### 4. Configure the Database
from app import db, User, Task
db.connect()
db.create_tables([User, Task])

### 5. Run the Application 
Use the below command in new terminal in the same directory
python app.py

The Web Page will run at http://127.0.0.1:5000

## Dependencies and Prerequisites

### Prerequisites
Python: Version 3.7 or later.
SQLite: Included with Python installations.
Browser: Any modern browser to access the web application.

### Dependencies
The required dependencies are listed in the requirements.txt file. Key dependencies include:
Flask: For backend routing and server-side logic.
Flask-Login: For user authentication.
Flask-WTF: For form handling.
Peewee: For ORM-based database management.

## Main Files

1. app.py
The main file for the application.
Contains route definitions for handling user requests (e.g., login, register, create tasks).
Implements core logic for task management and user authentication.

2. models.py (if applicable)
Defines the database models for User and Task using Peewee ORM.

3. templates/
Contains all HTML templates for the application:
base.html: Main layout template with navigation bar and footer.
home.html: Landing page for the application.
login.html and register.html: Templates for user authentication.
tasks.html: Task dashboard for viewing and managing tasks.
create_task.html and edit_task.html: Forms for creating and editing tasks.

4. static/
styles.css: Custom styles for the application.

5. requirements.txt
Lists all the Python dependencies required to run the project.
"# Task-Management-APP" 
