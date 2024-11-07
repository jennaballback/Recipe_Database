from sqlite3 import Error
import sqlite3 
#test
class Database:
    def __init__(self, recipe_database):
        self.recipe_database = recipe_database
        self.conn = self.create_connection()

        # Create the 'recipes' table
        self.create_table(
            """
            CREATE TABLE recipes(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                Name TEXT, # Name of the recipe
                Type TEXT, # Type of recipe (e.g. breakfast, dinner, dessert)
                Cuisine TEXT, # Cuisine of recipe (e.g. italian, mexican)
                Season TEXT # Seasonal relevance, if any (e.g. winter, summer)
            );
            """
        )

        # Create the 'ingredients' table
        self.create_table(
            """
            CREATE TABLE ingredients(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                recipe_id INTEGER, # integer to identify 
                ingredient_name TEXT, # e.g. flour, sugar, salt
                measurement TEXT, # e.g. cups, tablespoons, teaspoons
                # link 'ingredients' & 'instructions' table to the 'recipes' table
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            );
            """
        )


        # Create the 'instructions' table
        self.create_table(
            """
            CREATE TABLE instructions(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                recipe_id INTEGER, # integer to identify 
                step_name INTEGER, # number for each step 
                instruction TEXT, # contents of directions on how to make
                # link 'ingredients' & 'instructions' table to the 'recipes' table
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            );
            """
        )
    # Method to establish a connection to the SQLite database
    def create_connection(self): 
        try:
            return sqlite3.connect(self.recipe_database) # Attempt to connect to the recipe database
        except Error as e:
            print(e)

    # Method to execute a SQL command to create a new table (if doesn't exist)
    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    # Method to insert a new recipe into the recipes table
    def add_data(self, data):
        sql = "INSERT INTO recipes(Name, Type, Cuisine, Season) VALUES(?,?,?,?);"
        cur = self.conn.cursor() 
        cur.execute(sql, data) 
        self.conn.commit() 
        return cur.lastrowid 
    
    def add_ingredient(self, recipe_id, ingredient_name, measurement):
        sql = "INSERT INTO ingredients(recipe_id, ingredient_name, measurement) VALUES(?, ?, ?);"
        cur = self.conn.cursor()
        cur.execute(sql, (recipe_id, ingredient_name, measurement))
        self.conn.commit()

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

        # Structure and return all details
        return {
            "recipe": recipe,
            "ingredients": ingredients,
            "instructions": instructions
        }
    
