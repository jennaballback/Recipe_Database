from Main_DataBase import Database

db = Database("recipedatabase.db")

# Add new recipe
recipe_data = ("Pancakes", "Breakfast", "American", None)
recipe_id =db.add_data(recipe_data)

# Add ingredients
db.add_ingredient(recipe_id, "Flour", "1 cup")
db.add_ingredient(recipe_id, "Milk", "1 cup")
db.add_ingredient(recipe_id, "Egg", "1")
db.add_ingredient(recipe_id, "Sugar", "2 tbsp")
db.add_ingredient(recipe_id, "Salt", "1/4 tsp")

# Add instructions
db.add_instruction(recipe_id, 1, "Mix dry ingredients together.")
db.add_instruction(recipe_id, 2, "Add wet ingredients and whisk until smooth.")
db.add_instruction(recipe_id, 3, "Pour batter onto a hot skillet and cook until bubbles form.")
db.add_instruction(recipe_id, 4, "Flip and cook until golden brown.")

# Retrieve and print the recipe with ingredients and instructions
recipe_details = db.get_recipe_with_details(recipe_id)
print("Recipe Details:", recipe_details)