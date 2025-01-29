from flask import Flask, render_template, request, redirect
import sqlite3

# create a Flask app instance
app = Flask(__name__)
DATABASE = "recipedatabase.db"

# Helper function to get a database connection 
def get_db_connection(): 
    conn = sqlite3.connect(DATABASE) 
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

    # Insert into the database
    conn = get_db_connection()
    cur = conn.cursor()
    conn.execute(
        """
        INSERT INTO recipes (name, type, cuisine, season, author, total_time, yield, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (name, category, cuisine, None, author, time, yield_value, photo)
    )
    recipe_id = cur.lastrowid  # Get the ID of the inserted recipe

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
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchall() 
    # Fetch ingredients for the recipe
    ingredients = conn.execute('SELECT ingredient_name, measurement FROM ingredients WHERE recipe_id = ?', (id,)).fetchall()

    # Fetch instructions for the recipe
    instructions = conn.execute('SELECT step_number, instruction FROM instructions WHERE recipe_id = ? ORDER BY step_number', (id,)).fetchall()
    conn.close()
    return render_template('index.html', recipe=recipe, ingredients=ingredients, instructions=instructions)

@app.route('/<string:category>')
def category_recipes(category):
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes WHERE type = ?', (category.capitalize(),)).fetchall()
    conn.close()
    return render_template('category.html', recipes=recipes, category=category.capitalize())



# run the app if this file is executed
if __name__ == '__main__':
    app.run(debug=True)