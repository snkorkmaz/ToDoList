import os
from flask import Flask, render_template, jsonify, url_for, redirect, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

# Create Flask app instance
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

Bootstrap5(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///list_entry.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications to improve performance

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define database model
class ListEntry(db.Model):
    """
    Represents an entry in the to-do list.

    Attributes:
        id (int): The unique identifier for the entry (Primary Key).
        title (str): The title of the entry.
        done (bool): Indicates whether the task associated with the entry is completed (True) or not (False).
    """
    __tablename__ = "list_entry"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)


# Function to create a new row in the database
# def create_row(title, done):
#     """
#     Creates a new row in the database with the specified title and completion status. Then returns a message indicating
#     the success of the operation
#     """
#     # Create a new row in the database
#     new_row = ListEntry(title=title, done=done)
#
#     # Add the new row to the session
#     with app.app_context():
#         db.session.add(new_row)
#
#         # Commit the session to persist the changes to the database
#         db.session.commit()
#
#     return 'New row created successfully!'


@app.route('/', methods=["GET"])
def get_all_entries():
    """
    Retrieves all entries from the ListEntry table in the database and returns HTTP response with the rendered 'index.html' template,
    passing the retrieved entries as context data.
    """
    rows = ListEntry.query.all()

    # Convert each row into a dictionary representation
    data = []
    for row in rows:
        row_dict = {
            'id': row.id,
            'title': row.title,
            'done': row.done
        }
        data.append(row_dict)

    return render_template("index.html", all_entries=data)


@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    """
    Deletes a specific entry from the to-do list.

    This function retrieves and deletes an entry with the specified ID from the ListEntry table which is passed as a
    parameter, commits the changes to the database session, and redirects the user to the root URL to display the
    updated list of entries.
    """
    entry_to_delete = ListEntry.query.get_or_404(entry_id)
    db.session.delete(entry_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_entries'))


@app.route("/add", methods=["POST"])
def add_entry():
    """
    Adds a new entry to the to-do list.

    Retrieves data from the input field named "form3" in the request form.
    Creates a new entry with the retrieved data and a default value for the "done" field (set to False).
    Adds the new entry to the database session, Commits the changes to the database and Redirects the user to the route
    associated with the "get_all_entries" function.
    """
    # Retrieve data from the input field
    input_data = request.form.get('form3')

    # Save to database
    new_entry = ListEntry(title=input_data, done=False)
    db.session.add(new_entry)
    db.session.commit()

    # Redirect or render a response
    return redirect(url_for("get_all_entries"))


@app.route('/update_entry/<int:entry_id>', methods=['POST'])
def update_entry(entry_id):
    """
    Updates the status of an entry in the to-do list.

    Retrieves the entry with the specified ID from the database. If the entry is not found, returns a 404 error.
    Retrieves the new value of the checkbox from the form submission.
    Updates the "done" field of the entry based on the checkbox value.
    Commits the changes to the database and Redirects the user to the route associated with the "get_all_entries"
    function.
    """
    entry = ListEntry.query.get(entry_id)
    if not entry:
        return "Entry not found", 404

    # Get the new value of the checkbox from the form submission
    done = request.form.get('done')
    if done == 'on':  # 'on' is sent by default when checkbox is checked
        entry.done = True
    else:
        entry.done = False

    db.session.commit()
    return redirect(url_for('get_all_entries'))


if __name__ == '__main__':
    app.run(debug=True)
