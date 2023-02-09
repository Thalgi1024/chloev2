import sqlite3

# Setting up the connection
DB_PATH = "data/database.db"
connection = sqlite3.connect(DB_PATH)

# Cursor
cur = connection.cursor()

# Commit changes
def commit():
    connection.commit()

# Execute a command
def execute(command, *values):
    cur.execute(command, tuple(values))
    commit()

# Fetch values from database
def fetch(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchall()