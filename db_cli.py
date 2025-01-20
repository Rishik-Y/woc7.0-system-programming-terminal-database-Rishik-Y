import argparse
import os
import json

# Global variable to store the currently selected database
current_db = None
CURRENT_DB_FILE = 'current_db.txt'

class Database:
    def __init__(self, name):
        self.name = name
        self.path = f"databases/{name}"

    def create(self):
        # Check if the database already exists
        if not os.path.exists(self.path):
            os.makedirs(self.path)  # Create a directory for the database
            print(f"Database '{self.name}' created successfully.")
        else:
            print(f"Database '{self.name}' already exists.")

    @staticmethod
    def list_all():
        # List all databases in the 'databases' folder
        if os.path.exists('databases'):
            databases = [f for f in os.listdir('databases') if os.path.isdir(os.path.join('databases', f))]
            if databases:
                print("Available databases:")
                for db in databases:
                    print(f"- {db}")
            else:
                print("No databases found.")
        else:
            print("The 'databases' folder does not exist.")

    @staticmethod
    def switch_db(db_name):
        global current_db

        # Check if the database exists
        if os.path.exists(f"databases/{db_name}"):
            current_db = db_name
            with open(CURRENT_DB_FILE, 'w') as f:
                f.write(current_db)  # Save the selected database to the file
            print(f"Switched to database: {current_db}")
        else:
            print(f"Database '{db_name}' does not exist.")

    @staticmethod
    def create_table(table_name):
        global current_db

        if current_db is None:
            print("No database selected. Please switch to a database first.")
            return

        # Check if table already exists
        table_path = f"databases/{current_db}/{table_name}.json"
        if os.path.exists(table_path):
            print(f"Table '{table_name}' already exists in the '{current_db}' database.")
            return

        # Create a new empty table (JSON file)
        with open(table_path, 'w') as table_file:
            json.dump({}, table_file)  # Initialize with an empty dictionary (key-value store)
        
        print(f"Table '{table_name}' created successfully in the '{current_db}' database.")

    @staticmethod
    def list_tables():
        global current_db

        if current_db is None:
            print("No database selected. Please switch to a database first.")
            return

        # Path to the database folder
        db_path = f"databases/{current_db}"

        # Check if the database folder exists
        if not os.path.exists(db_path):
            print(f"Database '{current_db}' does not exist.")
            return

        # List all files in the current database folder
        tables = [f for f in os.listdir(db_path) if f.endswith('.json')]

        # If no tables are found
        if not tables:
            print(f"No tables found in database '{current_db}'.")
        else:
            print(f"Tables in '{current_db}' database:")
            for table in tables:
                # Remove the .json extension to display the table name
                print(f"- {table[:-5]}")  # Removing the ".json" extension

    @staticmethod
    def insert_data(table_name, key, value):
        global current_db

        if current_db is None:
            print("No database selected. Please switch to a database first.")
            return

        table_path = f"databases/{current_db}/{table_name}.json"

        # Check if the table exists
        if not os.path.exists(table_path):
            print(f"Table '{table_name}' does not exist.")
            return

        # Load the table data
        with open(table_path, 'r') as table_file:
            data = json.load(table_file)

        # Check if the key already exists
        if key in data:
            print(f"Error: Key '{key}' already exists in table '{table_name}'.")
            return

        # Insert the new data
        data[key] = value

        # Save the updated table data
        with open(table_path, 'w') as table_file:
            json.dump(data, table_file)

        print(f"Inserted key '{key}' into table '{table_name}'.")

    @staticmethod
    def update_data(table_name, key, value):
        global current_db

        if current_db is None:
            print("No database selected. Please switch to a database first.")
            return

        table_path = f"databases/{current_db}/{table_name}.json"

        # Check if the table exists
        if not os.path.exists(table_path):
            print(f"Table '{table_name}' does not exist.")
            return

        # Load the table data
        with open(table_path, 'r') as table_file:
            data = json.load(table_file)

        # Check if the key exists
        if key not in data:
            print(f"Error: Key '{key}' does not exist in table '{table_name}'.")
            return

        # Update the entry
        data[key] = value

        # Save the updated table data
        with open(table_path, 'w') as table_file:
            json.dump(data, table_file)

        print(f"Updated key '{key}' in table '{table_name}'.")

    @staticmethod
    def delete_data(table_name, key):
        global current_db

        if current_db is None:
            print("No database selected. Please switch to a database first.")
            return

        table_path = f"databases/{current_db}/{table_name}.json"

        # Check if the table exists
        if not os.path.exists(table_path):
            print(f"Table '{table_name}' does not exist.")
            return

        # Load the table data
        with open(table_path, 'r') as table_file:
            data = json.load(table_file)

        # Check if the key exists
        if key not in data:
            print(f"Error: Key '{key}' does not exist in table '{table_name}'.")
            return

        # Delete the entry
        del data[key]

        # Save the updated table data
        with open(table_path, 'w') as table_file:
            json.dump(data, table_file)

        print(f"Deleted key '{key}' from table '{table_name}'.")

    @staticmethod
    def list_entries(table_name):
        global current_db

        if current_db is None:
            print("No database selected. Please switch to a database first.")
            return

        table_path = f"databases/{current_db}/{table_name}.json"

        # Check if the table exists
        if not os.path.exists(table_path):
            print(f"Table '{table_name}' does not exist.")
            return

        # Load the table data
        with open(table_path, 'r') as table_file:
            data = json.load(table_file)

        # Print all entries in the table
        print(f"Entries in table '{table_name}':")
        for key, value in data.items():
            print(f"- {key}: {value}")

# Function to load the currently selected database from the file
def load_current_db():
    global current_db
    if os.path.exists(CURRENT_DB_FILE):
        with open(CURRENT_DB_FILE, 'r') as f:
            current_db = f.read().strip()  # Load the current database name
            print(f"current_db is: {current_db}")
    else:
        current_db = None

def main():
    global current_db

    # Load the current database when the program starts
    load_current_db()

    parser = argparse.ArgumentParser(description="Key-Value Database CLI")

    # Add subparsers to handle different commands
    subparsers = parser.add_subparsers(dest="command")

    # Command: create-db
    create_db_parser = subparsers.add_parser('create-db', help="Create a new database")
    create_db_parser.add_argument('name', type=str, help="Name of the database to create")

    # Command: list-db
    subparsers.add_parser('list-db', help="List all available databases")

    # Command: switch-db
    switch_db_parser = subparsers.add_parser('switch-db', help="Switch to a specific database")
    switch_db_parser.add_argument('name', type=str, help="Name of the database to switch to")

    # Command: create-table
    create_table_parser = subparsers.add_parser('create-table', help="Create a new table in the current database")
    create_table_parser.add_argument('name', type=str, help="Name of the table to create")

    # Command: list-tables
    subparsers.add_parser('list-tables', help="List all tables in the current database")

    # Command: insert-data
    insert_data_parser = subparsers.add_parser('insert-data', help="Insert data into a table")
    insert_data_parser.add_argument('table', type=str, help="Table name")
    insert_data_parser.add_argument('key', type=str, help="Key of the entry")
    insert_data_parser.add_argument('value', type=str, help="Value of the entry")

    # Command: update-data
    update_data_parser = subparsers.add_parser('update-data', help="Update an entry in a table")
    update_data_parser.add_argument('table', type=str, help="Table name")
    update_data_parser.add_argument('key', type=str, help="Key of the entry")
    update_data_parser.add_argument('value', type=str, help="New value of the entry")

    # Command: delete-data
    delete_data_parser = subparsers.add_parser('delete-data', help="Delete an entry from a table")
    delete_data_parser.add_argument('table', type=str, help="Table name")
    delete_data_parser.add_argument('key', type=str, help="Key of the entry")

    # Command: list-entries
    list_entries_parser = subparsers.add_parser('list-entries', help="List all entries in a table")
    list_entries_parser.add_argument('table', type=str, help="Table name")

    # Parse the arguments
    args = parser.parse_args()

    # Handle commands
    if args.command == 'create-db':
        db = Database(args.name)
        db.create()
    elif args.command == 'list-db':
        Database.list_all()
    elif args.command == 'switch-db':
        Database.switch_db(args.name)
    elif args.command == 'create-table':
        Database.create_table(args.name)
    elif args.command == 'list-tables':
        Database.list_tables()
    elif args.command == 'insert-data':
        Database.insert_data(args.table, args.key, args.value)
    elif args.command == 'update-data':
        Database.update_data(args.table, args.key, args.value)
    elif args.command == 'delete-data':
        Database.delete_data(args.table, args.key)
    elif args.command == 'list-entries':
        Database.list_entries(args.table)

    # Show the current database (if any)
    if current_db:
        print(f"Currently working in database: {current_db}")
    else:
        print("No database selected.")

if __name__ == "__main__":
    main()

