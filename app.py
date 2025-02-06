from flask import Flask, render_template, request, redirect, flash
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Load tasks from JSON file
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
            # Convert date strings back to datetime objects
            tasks = [
                {
                    **task,
                    'due_date': datetime.strptime(task['due_date'], '%Y-%m-%d'),
                    'added_on': datetime.strptime(task['added_on'], '%Y-%m-%d %H:%M:%S')
                }
                for task in tasks
            ]
            # Sort tasks by due date in ascending order
            tasks.sort(key=lambda task: task['due_date'])
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        # Convert datetime objects to strings before saving
        tasks_to_save = [
            {
                **task,
                'due_date': task['due_date'].strftime('%Y-%m-%d'),
                'added_on': task['added_on'].strftime('%Y-%m-%d %H:%M:%S')
            }
            for task in tasks
        ]
        json.dump(tasks_to_save, file, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task']
    due_date = request.form['due_date']
    
    tasks = load_tasks()
    
    # Check for duplicates
    if any(task['task'] == task_name for task in tasks):
        flash("Task already exists!")  # Flash message for duplicate task
    else:
        new_task = {
            'task': task_name,
            'due_date': datetime.strptime(due_date, '%Y-%m-%d'),
            'added_on': datetime.now()
        }
        tasks.append(new_task)
        save_tasks(tasks)

    return redirect('/')

@app.route('/remove_task', methods=['POST'])
def remove_task():
    task_name = request.form['task']
    tasks = load_tasks()
    tasks = [task for task in tasks if task['task'] != task_name]
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  # Change 127.0.0.1 to 0.0.0.0


