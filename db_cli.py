import argparse
import os

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


def main():
    parser = argparse.ArgumentParser(description="Key-Value Database CLI")

    # Add subparsers to handle different commands
    subparsers = parser.add_subparsers(dest="command")

    # Command: create-db
    create_db_parser = subparsers.add_parser('create-db', help="Create a new database")
    create_db_parser.add_argument('name', type=str, help="Name of the database to create")

    # Parse the arguments
    args = parser.parse_args()

    # Handle the create-db command
    if args.command == 'create-db':
        db = Database(args.name)
        db.create()

if __name__ == "__main__":
    main()

