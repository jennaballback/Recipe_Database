import sqlite3

# Path to your database file
DATABASE_PATH = "C:/Users/Jenna/OneDrive/Documents/Recipe Database (vs code)/Recipe_Database/recipedatabase.db"

try:
    # Connect to the database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Check existing tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = [row[0] for row in cursor.fetchall()]
    print("Existing tables:", existing_tables)

    # List of tables to clear
    tables = ['recipes', 'ingredients', 'instructions', 'connections']

    # Delete all data from each table if it exists
    for table in tables:
        if table in existing_tables:
            cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            print(f"Cleared all data from {table} (deleted {cursor.rowcount} rows).")
        else:
            print(f"Table {table} does not exist, skipping.")

    print("Database cleared successfully.")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    if conn:
        conn.close()
        print("Database connection closed.")