# TO-DO List

This is a simple To-Do List web application built using Flask, SQLAlchemy, and Bootstrap. It allows users to add, delete, and update tasks, as well as mark them as completed.

## Installation

To run this application locally, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/todo-list.git
```

2. Navigate to the project directory:
```bash
cd todo-list
```

3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

4. Set up the Flask application:

```bash
export FLASK_APP=main.py
```

5. Create the database tables:
```bash
flask db upgrade
```

6. Run the Flask application:

```bash
flask run
```

7. Open your web browser and go to http://127.0.0.1:5000 to view the application.
