from flask import Flask, render_template
from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField, ForeignKeyField, BooleanField
from datetime import datetime
from flask import request, redirect, url_for 
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash  
from flask import Flask, render_template, redirect, url_for, request, flash
from peewee import ForeignKeyField
from functools import wraps
from flask_login import current_user, login_required
import re  # For email format validation        

# Initialize Flask-Login
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
db = SqliteDatabase('task_manager.db')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))

def unauthenticated_user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # Redirect logged-in users to the task list
            return redirect(url_for('list_user_tasks'))
        return func(*args, **kwargs)
    return decorated_function

# User model
class User(UserMixin, Model):  # Add UserMixin
    name = CharField()
    email = CharField(unique=True)
    password = CharField()  # Add a password field

    class Meta:
        database = db

# Task model
class Task(Model):
    title = CharField()
    description = CharField()
    due_date = DateTimeField()
    priority = CharField()
    assigned_to = ForeignKeyField(User, backref='tasks')  # Link task to a user
    completed = BooleanField(default=False) # type: ignore
    
    class Meta:
        database = db

@app.route('/register', methods=['GET', 'POST'])
@unauthenticated_user_required 
def register():
    email = request.args.get('email', '')  # Pre-filled email from login page

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists
        if User.get_or_none(User.email == email):
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for('login'))

        # Hash the password before saving to database
        hashed_password = generate_password_hash(password)
        User.create(name=name, email=email, password=hashed_password)

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', email=email)

@app.route('/login', methods=['GET', 'POST'])
@unauthenticated_user_required 
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists
        user = User.get_or_none(User.email == email)

        if user is None:
            # Redirect to the register page with a helpful flash message
            flash("User does not exist. Please register first.", "warning")
            return redirect(url_for('register', email=email))

        # Verify the password
        if not check_password_hash(user.password, password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for('login'))

        # Log in the user if credentials are correct
        login_user(user)
        flash("Logged in successfully!", "success")
        return redirect(url_for('list_user_tasks'))

    return render_template('login.html')

@app.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']

        # Regular expression to allow only letters and spaces
        pattern = r'^[a-zA-Z\s]+$'

        # Validate title
        if not re.match(pattern, title):
            flash("Task name should only contain letters and spaces.", "danger")
            return redirect(url_for('create_task'))

        # Validate description
        if not re.match(pattern, description):
            flash("Task description should only contain letters and spaces.", "danger")
            return redirect(url_for('create_task'))

        # Save task if validation passes
        Task.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            assigned_to=current_user.id
        )
        flash('Task created successfully!', 'success')
        return redirect(url_for('list_user_tasks'))

    return render_template('create_task.html')

@app.route('/tasks')
@login_required
def list_user_tasks():
    tasks = Task.select().where(Task.assigned_to == current_user.id)
    return render_template('tasks.html', tasks=tasks)

@app.route('/task/update/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.get_or_none(Task.id == task_id)
    if not task or task.assigned_to.id != current_user.id:
        flash("Task not found or access denied.", "danger")
        return redirect(url_for('list_user_tasks'))

    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.priority = request.form.get('priority')  
    
    due_date = request.form.get('due_date')  
    due_time = request.form.get('due_time') 
    if due_date and due_time:
        task.due_date = datetime.strptime(f"{due_date} {due_time}", "%Y-%m-%d %H:%M")
    
    task.save()
    flash("Task updated successfully!", "success")
    return redirect(url_for('list_user_tasks'))

@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    # Fetch the task by ID and verify ownership
    task = Task.get_or_none(Task.id == task_id)
    if not task or task.assigned_to.id != current_user.id:
        flash("Task not found or access denied.", "danger")
        return redirect(url_for('list_user_tasks'))

    if request.method == 'POST':
        # Update task attributes from the form
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        
        # Combine due date and time into a single datetime object
        due_date = request.form.get('due_date')  # Date input
        due_time = request.form.get('due_time')  # Time input
        if due_date and due_time:
            task.due_date = datetime.strptime(f"{due_date} {due_time}", "%Y-%m-%d %H:%M")
        
        # Save changes to the task
        task.save()
        flash("Task updated successfully!", "success")
        return redirect(url_for('list_user_tasks'))

    return render_template('edit_task.html', task=task)

@app.route('/task/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.get_or_none(Task.id == task_id)
    if task and task.assigned_to.id == current_user.id:
        task.completed = not task.completed
        task.save()
        flash("Task updated successfully!", "success")
    else:
        flash("Task not found or access denied.", "danger")
    return redirect(url_for('list_user_tasks'))

@app.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    # Retrieve the task associated with the current user
    task = Task.get_or_none((Task.id == task_id) & (Task.assigned_to == current_user.id))
    
    # If the task exists and belongs to the user, delete it
    if task:
        task.delete_instance()
        flash("Task deleted successfully!", "success")
    else:
        flash("Task not found or access denied.", "danger")
    
    return redirect(url_for('list_user_tasks'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))  

@app.route('/')
@unauthenticated_user_required  # Optional if you use the decorator
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
