import argparse
import os

# Global variable to store the currently selected database
current_db = None

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
            print(f"Switched to database: {current_db}")
        else:
            print(f"Database '{db_name}' does not exist.")


def main():
    global current_db

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

    # Show the current database (if any)
    if current_db:
        print(f"Currently working in database: {current_db}")
    else:
        print("No database selected.")

if __name__ == "__main__":
    main()

