from flask import Flask, render_template
import sqlite3

# create a Flask app instance
app = Flask(__name__)
DATABASE = "recipedatabase.db"

# Helper function to get a database connection 
def get_db_connection(): 
    conn = sqlite3.connect(DATABASE) 
    conn.row_factory = sqlite3.Row 
    return conn

# define a route and a view function
@app.route('/recipe/<int:id>')
def home(id):
    conn = get_db_connection() 
    recipes = conn.execute(f'SELECT id,name FROM recipes where id = {id}').fetchall() 
    conn.close()
    return render_template('index.html', recipes = recipes)

@app.route('/about')
def about():
    
    return render_template('about.html')

# run the app if this file is executed
if __name__ == '__main__':
    app.run(debug=True)