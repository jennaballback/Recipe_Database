from sqlite3 import Error
import sqlite3 

class Database:
    def __init__(self, recipe_database):
        self.recipe_database = recipe_database
        self.conn = self.create_connection()

        # Create the 'recipes' table
        self.create_table(
            """
            CREATE TABLE IF NOT EXISTS recipes(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                type TEXT, 
                cuisine TEXT, 
                season TEXT DEFAULT NULL,
                author TEXT,
                total_time TEXT,
                yield TEXT,
                image TEXT
            );
            """
        )

        # Create the 'ingredients' table
        self.create_table(
            """
            CREATE TABLE ingredients(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                recipe_id INTEGER, 
                ingredient_name TEXT, 
                measurement TEXT,
                UNIQUE (recipe_id, ingredient_name),
                FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
            );
            """
        )


        # Create the 'instructions' table
        self.create_table(
            """
            CREATE TABLE instructions(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                recipe_id INTEGER, 
                step_number INTEGER, 
                instruction TEXT, 
                UNIQUE (recipe_id, step_number),
                FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
            );
            """
        )


         # Create the 'connections' table
        self.create_table(
            """
            CREATE TABLE connections(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                step_number INTEGER,
                ingredient_name TEXT,
                measurement TEXT, 
                FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
                FOREIGN KEY (recipe_id, step_number) REFERENCES instructions (recipe_id, step_number) ON DELETE CASCADE,
                FOREIGN KEY (ingredient_name) REFERENCES ingredients (ingredient_name) ON DELETE CASCADE
            );
            """
        )

   # Method to establish a connection to the SQLite database
    def create_connection(self): 
        try:
            # Establish the connection
            conn = sqlite3.connect(self.recipe_database)
        
            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON;")
        
            return conn
        except Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    # Method to execute a SQL command to create a new table (if doesn't exist)
    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    # Method to insert a new recipe into the recipes table
    def add_data(self, data):
        sql = "INSERT INTO recipes(name, type, cuisine, season, author, total_time) VALUES(?,?,?,?,?,?);"
        cur = self.conn.cursor() 
        cur.execute(sql, data) 
        self.conn.commit() 
        return cur.lastrowid 
    
    # Method to add a new ingredient for a recipe in the 'ingredients' table
    def add_ingredient(self, recipe_id, ingredient_name, measurement):
        sql = "INSERT INTO ingredients(recipe_id, ingredient_name, measurement) VALUES(?, ?, ?);"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (recipe_id, ingredient_name, measurement))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error adding ingredient: {e}")

    # Method to add an instruction step for a recipe in the 'instructions' table
    def add_instruction(self, recipe_id, step_number, instruction):
        sql = "INSERT INTO instructions(recipe_id, step_number, instruction) VALUES(?, ?, ?);"
        cur = self.conn.cursor()
        cur.execute(sql, (recipe_id, step_number, instruction))
        self.conn.commit()
    

    # Method to retrieve all records from the recipes table
    def get_recipe_with_details(self, recipe_id):
        # Fetch recipe basic information
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        recipe = cur.fetchone()

        # Fetch ingredients for the recipe
        cur.execute("SELECT ingredient_name, measurement FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        ingredients = cur.fetchall()

        # Fetch instructions for the recipe
        cur.execute("SELECT step_number, instruction FROM instructions WHERE recipe_id = ? ORDER BY step_number", (recipe_id,))
        instructions = cur.fetchall()

        # Fetch connections (linking ingredients and instructions)
        cur.execute("""
        SELECT i.step_number, c.ingredient_name, c.measurement
        FROM connections c
        INNER JOIN instructions i ON c.step_number = i.step_number
        WHERE c.recipe_id = ?
        """, (recipe_id,))
        connections = cur.fetchall()

        # Structure and return all details
        return {
            "recipe": recipe,
            "ingredients": ingredients,
            "instructions": instructions,
            "connections": connections
        }
    
