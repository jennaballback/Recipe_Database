# Recipe_Database

A collection of all the recipes we have found and use as a family.
Organized by "recipe card" that includes the ingredients & measurements, instructions, author, and total time.
The "recipe" table has attributes of Name, Type, Cuisine, Season, Author, and Total Time.
- Type includes Breakfast, Lunch, Dinner, Dessert, etc.
- Cuisine includes Italian, American, Mexican, etc.
- Season (if applicable) includes Autumn, Winter, Spring, and Summer.

The 'ingredients' table and 'instructions' table are children of the parent table 'recipe'.
The 'ingredients' table has attributes of Recipe ID, Ingredients, and Measurements.
- Recipe ID is a unique number that establishes a connection to the 'recipe' table.

The 'instructions' table has attributes of Recipe ID, Step Number, and Instructions.
- Recipe ID is a unique number that establishes a connection to the 'recipe' table.
- Step Number tracks the numerical order of the instructions.
