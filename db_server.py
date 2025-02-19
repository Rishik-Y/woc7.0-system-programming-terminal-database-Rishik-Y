import socket
import threading
import json
import os

# Global variable to store the currently selected database
current_db = None
CURRENT_DB_FILE = 'current_db.txt'

# Database class to handle the operations (same as before)
class Database:
    def __init__(self, name):
        self.name = name
        self.path = f"databases/{name}"

    def create(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            return f"Database '{self.name}' created successfully."
        else:
            return f"Database '{self.name}' already exists."

    @staticmethod
    def list_all():
        if os.path.exists('databases'):
            databases = [f for f in os.listdir('databases') if os.path.isdir(os.path.join('databases', f))]
            if databases:
                print("Available databases:")
                for db in databases:
                    print(f"- {db}")
            else:
                return "No databases found."
        else:
            return "The 'databases' folder does not exist."

    @staticmethod
    def switch_db(db_name):
        global current_db

        if os.path.exists(f"databases/{db_name}"):
            current_db = db_name
            with open(CURRENT_DB_FILE, 'w') as f:
                f.write(current_db)
            return f"Switched to database: {current_db}"
        else:
            return f"Database '{db_name}' does not exist."

    @staticmethod
    def create_table(table_name):
        global current_db
        if current_db is None:
            return "No database selected. Please switch to a database first."
        table_path = f"databases/{current_db}/{table_name}.json"
        if os.path.exists(table_path):
            return f"Table '{table_name}' already exists in the '{current_db}' database."
        with open(table_path, 'w') as table_file:
            json.dump({}, table_file)
        return f"Table '{table_name}' created successfully in the '{current_db}' database."

    @staticmethod
    def list_tables():
        global current_db
        if current_db is None:
            return "No database selected. Please switch to a database first."
        db_path = f"databases/{current_db}"
        if not os.path.exists(db_path):
            return f"Database '{current_db}' does not exist."
        tables = [f for f in os.listdir(db_path) if f.endswith('.json')]
        if not tables:
            return f"No tables found in database '{current_db}'."
        else:
            print(f"Tables in '{current_db}' database:")
            for table in tables:
                # Remove the .json extension to display the table name
                print(f"- {table[:-5]}")  # Removing the ".json" extension

    @staticmethod
    def insert_data(table_name, key, value):
        global current_db
        if current_db is None:
            return "No database selected. Please switch to a database first."
        table_path = f"databases/{current_db}/{table_name}.json"
        if not os.path.exists(table_path):
            return f"Table '{table_name}' does not exist."
        with open(table_path, 'r') as table_file:
            data = json.load(table_file)
        if key in data:
            return f"Error: Key '{key}' already exists in table '{table_name}'."
        data[key] = value
        with open(table_path, 'w') as table_file:
            json.dump(data, table_file)
        return f"Inserted key '{key}' into table '{table_name}'."

    @staticmethod
    def update_data(table_name, key, value):
        global current_db
        if current_db is None:
            return "No database selected. Please switch to a database first."
        table_path = f"databases/{current_db}/{table_name}.json"
        if not os.path.exists(table_path):
            return f"Table '{table_name}' does not exist."
        with open(table_path, 'r') as table_file:
            data = json.load(table_file)
        if key not in data:
            return f"Error: Key '{key}' does not exist in table '{table_name}'."
        data[key] = value
        with open(table_path, 'w') as table_file:
            json.dump(data, table_file)
        return f"Updated key '{key}' in table '{table_name}'."

    @staticmethod
    def delete_data(table_name, key):
        global current_db
        if current_db is None:
            return "No database selected. Please switch to a database first."
        table_path = f"databases/{current_db}/{table_name}.json"
        if not os.path.exists(table_path):
            return f"Table '{table_name}' does not exist."
        with open(table_path, 'r') as table_file:
            data = json.load(table_file)
        if key not in data:
            return f"Error: Key '{key}' does not exist in table '{table_name}'."
        del data[key]
        with open(table_path, 'w') as table_file:
            json.dump(data, table_file)
        return f"Deleted key '{key}' from table '{table_name}'."

    @staticmethod
    def list_entries(table_name):
        global current_db
        if current_db is None:
            return "No database selected. Please switch to a database first."
        table_path = f"databases/{current_db}/{table_name}.json"
        if not os.path.exists(table_path):
            return f"Table '{table_name}' does not exist."
        with open(table_path, 'r') as table_file:
            data = json.load(table_file)
        if not data:
            return f"No entries found in table '{table_name}'."
        entries = "\n".join([f"- {key}: {value}" for key, value in data.items()])
        return f"Entries in table '{table_name}':\n{entries}"

# Function to load the currently selected database from the file
def load_current_db():
    global current_db
    if os.path.exists(CURRENT_DB_FILE):
        with open(CURRENT_DB_FILE, 'r') as f:
            current_db = f.read().strip()
            print(f"current_db is: {current_db}")
    else:
        current_db = None

# Function to handle each client request
def handle_client(client_socket):
    try:
        while True:
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break
            print(f"Received command: {command}")
            command_parts = command.split(' ')
            # Parse the command and call appropriate method on the Database class
            if command_parts[0] == "create-db":
                db = Database(command_parts[1])
                response = db.create()
            elif command_parts[0] == "list-db":
                response = Database.list_all()
            elif command_parts[0] == "switch-db":
                response = Database.switch_db(command_parts[1])
            elif command_parts[0] == "create-table":
                response = Database.create_table(command_parts[1])
            elif command_parts[0] == "list-tables":
                response = Database.list_tables()
            elif command_parts[0] == "insert-data":
                response = Database.insert_data(command_parts[1], command_parts[2], command_parts[3])
            elif command_parts[0] == "update-data":
                response = Database.update_data(command_parts[1], command_parts[2], command_parts[3])
            elif command_parts[0] == "delete-data":
                response = Database.delete_data(command_parts[1], command_parts[2])
            elif command_parts[0] == "list-entries":
                response = Database.list_entries(command_parts[1])
            else:
                response = "Unknown command"
            # Send the response to the client
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Start the server to listen for connections
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(5)
    print("Server listening on port 5555...")

    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Run the server
if __name__ == "__main__":
    load_current_db()  # Load the current database on server startup
    start_server()

