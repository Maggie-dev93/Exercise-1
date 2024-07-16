# Python for Web Developers Course - Exercise 1.2

## Objective
This exercise focuses on creating and manipulating data structures in Python to store recipes.

## Steps

### 1. Create `recipe_1`
```python
recipe_1 = {
    "name": "Tea",
    "cooking_time": 5,
    "ingredients": ["Tea leaves", "Sugar", "Water"]
}

I chose to use a dictionary for the recipe_1 structure because it allows for easy access to named attributes like the recipe's name, cooking time, and ingredients. Each key-value pair can be quickly retrieved and modified as needed.

### 2. Create all_recipes
A list is chosen for all_recipes because it allows for sequential storage of multiple recipes. Lists are dynamic and can easily accommodate the addition and removal of recipes.

### 3. Generate Additional Recipes
-Create four more recipes (recipe_2, recipe_3, recipe_4, and recipe_5) and add them to all_recipes.

recipe_2 = {
    "name": "Coffee",
    "cooking_time": 10,
    "ingredients": ["Coffee beans", "Sugar", "Water"]
}

recipe_3 = {
    "name": "Pancakes",
    "cooking_time": 20,
    "ingredients": ["Flour", "Milk", "Eggs", "Sugar", "Butter"]
}

recipe_4 = {
    "name": "Salad",
    "cooking_time": 15,
    "ingredients": ["Lettuce", "Tomatoes", "Cucumbers", "Olive oil"]
}

recipe_5 = {
    "name": "Omelette",
    "cooking_time": 10,
    "ingredients": ["Eggs", "Milk", "Salt", "Pepper", "Butter"]
}

all_recipes.extend([recipe_2, recipe_3, recipe_4, recipe_5])


### 4. Print Ingredients
-Print the ingredients of each recipe as five different lists inside the IPython shell.
for recipe in all_recipes:
    print(recipe["ingredients"])





