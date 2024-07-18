# Initialize empty lists
recipes_list = []
ingredients_list = []

# Function to take recipe input
def take_recipe():
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter the ingredients, separated by commas: ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]  # Remove any extra spaces
    
    # Store the values in a dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    
    return recipe

# Main section
# Initial user prompt
n = int(input("How many recipes would you like to enter? "))

# Iterates through number of given recipes
for i in range(n):
    recipe = take_recipe()
    
    # Checks whether an ingredient should be added to a given ingredient list
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    # Determine recipe difficulty
    if recipe["cooking_time"] <= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] <= 15 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] > 15 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 20 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"
    else:
        recipe["difficulty"] = "Undefined"  # Catch-all case for recipes that do not fit above conditions
    
    recipes_list.append(recipe)

# Iterates through recipes_list to display their information
for recipe in recipes_list:
    print("\nRecipe: ", recipe["name"])
    print("Cooking time (minutes): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])

# Displays all ingredients from all recipes in alphabetical order
def all_ingredients():
    print("\nIngredients Available Across All Recipes")
    print("________________________________________")
    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()
