from sqlite3 import Error
import sqlite3 #what is sqlite3

class Database:
    def __init__(self, recipe_database):
        self.recipe_database = recipe_database
        self.conn = self.create_connection()

        self.create_table(
            CREATE TABLE recipes(
                id INTEGER PRIMARY KEY AUTOINCREMENT, #what does this do
                Name TEXT,
                Type TEXT,
                Cuisine TEXT,
                Season TEXT
            );
        )

    def create_connection(self): #is this connecting the python code to the database?
        try:
            return sqlite3.connect(self.recipe_database)
        except Error as e:
            print(e)

    
    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def add_data(self, data):
        sql = INSERT INTO recipes(Name, Type, Cuisine, Season) VALUES("Test", "Test", "Test", "Test");
        cur = self.conn.cursor()
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid
    
    def get_all_data(self):
        sql = SELECT * FROM recipes
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    