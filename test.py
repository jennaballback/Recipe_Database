from flask import Flask, render_template, request, redirect
import sqlite3
import os

# create a Flask app instance
app = Flask(__name__)
DATABASE = "recipedatabase.db"

# Helper function to get a database connection 
def get_db_connection(): 
    db_path = os.path.abspath(DATABASE)
    print("Using Database FIle:", db_path)

    # conn = sqlite3.connect(DATABASE) 
    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row 
    return conn

# define a route for the root URL
@app.route("/")
def index():
    return render_template('home.html')

@app.route('/add')
def add():
    
    return render_template('add.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form.get('name')
    category = request.form.get('category')
    cuisine = request.form.get('cuisine')
    author = request.form.get('author')
    time = request.form.get('time')
    yield_value = request.form.get('yield')
    photo = request.form.get('photo')

    if not name or not category or not time:
        return "Error: Missing required fields", 400

    # Insert into the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO recipes (name, type, cuisine, season, author, total_time, yield, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (name, category, cuisine, None, author, time, yield_value, photo)
    )
    conn.commit()
    print("Recipe inserted, lastrowid: ", cur.lastrowid)
    recipe_id = cur.lastrowid  # Get the ID of the inserted recipe

    print("Recipe inserted, lastrowid: ", cur.lastrowid)
    # Verify recipe_id
    if not recipe_id:
        print("ERROR: lastrowid is NULL - Checking database")
        cur.execute("SELECT * FROM recipes;")
        print("Existing Recipes:", cur.fetchall())  # Print current recipes
        return "Error: Recipe ID is NULL after insert", 500
    
    print("Recipe ID:", recipe_id)

    # Add ingredients
    ingredient_names = request.form.getlist('ingredient_name[]')
    measurements = request.form.getlist('measurement[]')
    for ingredient_name, measurement in zip(ingredient_names, measurements):
        cur.execute(
            """
            INSERT INTO ingredients (recipe_id, ingredient_name, measurement)
            VALUES (?, ?, ?)
            """,
            (recipe_id, ingredient_name, measurement)
        )

    # Add instructions
    instructions = request.form.getlist('instruction[]')
    for step_number, instruction in enumerate(instructions, start=1):
        cur.execute(
            """
            INSERT INTO instructions (recipe_id, step_number, instruction)
            VALUES (?, ?, ?)
            """,
            (recipe_id, step_number, instruction)
        )

    conn.commit()
    conn.close()

    # Redirect to all recipes page
    return redirect('/all-recipes')

# view all the recipes
@app.route('/all-recipes')
def all_recipes():
    conn = get_db_connection() 
    recipes = conn.execute(f'SELECT * FROM recipes').fetchall() 
    conn.close()
    return render_template('all.html', recipes = recipes)

# define a route and a view function
@app.route('/all-recipes/<int:id>')
def recipe_details(id):
    conn = get_db_connection() 
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()  # Use fetchone() instead of fetchall()
    ingredients = conn.execute('SELECT ingredient_name, measurement FROM ingredients WHERE recipe_id = ?', (id,)).fetchall()
    instructions = conn.execute('SELECT step_number, instruction FROM instructions WHERE recipe_id = ? ORDER BY step_number', (id,)).fetchall()
    conn.close()
    return render_template('index.html', recipe=recipe, ingredients=ingredients, instructions=instructions)

@app.route('/<string:category>')
def category_recipes(category):
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes WHERE type = ?', (category.capitalize(),)).fetchall()
    conn.close()
    return render_template('category.html', recipes=recipes, category=category.capitalize())

# delete a recipe
@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        conn.commit()
        if cur.rowcount == 0:
            return f"No recipe found with ID {recipe_id}.", 404
        else:
            return f"Recipe with ID {recipe_id} deleted successfully.", 200
    except sqlite3.Error as e:
        conn.rollback()
        return f"Error deleting recipe: {e}", 500
    finally:
        conn.close()



# run the app if this file is executed
if __name__ == '__main__':
    app.run(debug=True)