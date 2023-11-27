from sqlalchemy import create_engine, text
import pymysql

def create_database_and_users_table(db_name, db_user, db_password, db_host, db_port):
    # Connection string for initial connection (without database name)
    initial_connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}"

    # Create an initial engine without specifying the database
    initial_engine = create_engine(initial_connection_string)

    # SQL command to create the database if it doesn't exist
    # Use backticks around the database name to handle special characters
    create_db_command = text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")

    # Execute the SQL command to create the database
    with initial_engine.connect() as connection:
        connection.execute(create_db_command)
        print(f"Database '{db_name}' created (if it didn't exist already).")

    # Connection string for the new database
    db_connection_string = f"{initial_connection_string}/{db_name}"

    # Create a database engine for the new database
    db_engine = create_engine(db_connection_string)

    create_schema_command = text(f"CREATE SCHEMA IF NOT EXISTS `{db_name}`;")

    with db_engine.connect() as connection:
        connection.execute(create_schema_command)
        print("Schema micro1 created (if it didn't exist already).")

    # SQL command to create the users table if it doesn't exist
    create_table_command = text("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Execute the SQL command to create the table
    with db_engine.connect() as connection:
        connection.execute(create_table_command)
        print("Users table created (if it didn't exist already).")

# Example usage
create_database_and_users_table('micro1', 'root', '', 'localhost', 3306)
