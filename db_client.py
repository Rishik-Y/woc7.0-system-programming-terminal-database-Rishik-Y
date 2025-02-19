import socket
import argparse

# Function to send command to the server
def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 5555))  # Connect to the server
        client_socket.send(command.encode('utf-8'))  # Send the command to the server
        response = client_socket.recv(1024).decode('utf-8')  # Receive response
        print(response)  # Print the server's response

# Main function to handle user input
def main():
    parser = argparse.ArgumentParser(description="Client for Key-Value Database Server")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command")
    
    # Command for 'list-db'
    subparsers.add_parser('list-db', help="List all available databases")
    
    # Command for 'create-db'
    create_db_parser = subparsers.add_parser('create-db', help="Create a new database")
    create_db_parser.add_argument('name', type=str, help="Name of the database to create")
    
    # Command for 'switch-db'
    switch_db_parser = subparsers.add_parser('switch-db', help="Switch to a specific database")
    switch_db_parser.add_argument('name', type=str, help="Name of the database to switch to")
    
    # Command for 'create-table'
    create_table_parser = subparsers.add_parser('create-table', help="Create a new table in the current database")
    create_table_parser.add_argument('name', type=str, help="Name of the table to create")
    
    # Command for 'list-tables'
    subparsers.add_parser('list-tables', help="List all tables in the current database")
    
    # Command for 'insert-data'
    insert_data_parser = subparsers.add_parser('insert-data', help="Insert data into a table")
    insert_data_parser.add_argument('table', type=str, help="Table name")
    insert_data_parser.add_argument('key', type=str, help="Key of the entry")
    insert_data_parser.add_argument('value', type=str, help="Value of the entry")
    
    # Command for 'update-data'
    update_data_parser = subparsers.add_parser('update-data', help="Update an entry in a table")
    update_data_parser.add_argument('table', type=str, help="Table name")
    update_data_parser.add_argument('key', type=str, help="Key of the entry")
    update_data_parser.add_argument('value', type=str, help="New value of the entry")
    
    # Command for 'delete-data'
    delete_data_parser = subparsers.add_parser('delete-data', help="Delete an entry from a table")
    delete_data_parser.add_argument('table', type=str, help="Table name")
    delete_data_parser.add_argument('key', type=str, help="Key of the entry")
    
    # Command for 'list-entries'
    list_entries_parser = subparsers.add_parser('list-entries', help="List all entries in a table")
    list_entries_parser.add_argument('table', type=str, help="Table name")

    # Parse the arguments
    args = parser.parse_args()

    # Send the corresponding command to the server based on the input
    if args.command == 'list-db':
        send_command("list-db")
    elif args.command == 'create-db':
        send_command(f"create-db {args.name}")
    elif args.command == 'switch-db':
        send_command(f"switch-db {args.name}")
    elif args.command == 'create-table':
        send_command(f"create-table {args.name}")
    elif args.command == 'list-tables':
        send_command("list-tables")
    elif args.command == 'insert-data':
        send_command(f"insert-data {args.table} {args.key} {args.value}")
    elif args.command == 'update-data':
        send_command(f"update-data {args.table} {args.key} {args.value}")
    elif args.command == 'delete-data':
        send_command(f"delete-data {args.table} {args.key}")
    elif args.command == 'list-entries':
        send_command(f"list-entries {args.table}")
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()

