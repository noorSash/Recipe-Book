from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'recipes.db')

# Initialize the database
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS recipes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        ingredients TEXT NOT NULL,
                        instructions TEXT NOT NULL,
                        category TEXT NOT NULL)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

# Fetch all recipes from the database
def get_recipes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM recipes')
    recipes = c.fetchall()
    conn.close()
    return recipes

# Delete a recipe from the database
def delete_recipe_from_db(recipe_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error deleting recipe: {e}")

# Home route: display all recipes
@app.route('/')
def home():
    recipes = get_recipes()
    return render_template('index.html', recipes=recipes)

# Route to delete a recipe
@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    delete_recipe_from_db(recipe_id)
    return redirect(url_for('home'))

# Route to add a new recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        category = request.form['category']
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO recipes (title, ingredients, instructions, category) VALUES (?, ?, ?, ?)', 
                  (title, ingredients, instructions, category))
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))
    
    return render_template('add_recipe.html')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
















