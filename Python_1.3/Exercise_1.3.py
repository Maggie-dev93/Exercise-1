recipes_list = []
ingredients_list = []

# Function to take recipe input
def take_recipe():
    # Function to process recipe input
    name = str(input("Enter the name of the recipe: "))
    
    # Function to process cooking time input
    cooking_time = int(input("Enter the cooking time (in minutes): "))

    # Function to process ingredients input
    ingredients = input("Enter the ingredients, separated by commas: ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]  # Remove any extra spaces
    
    # Store the values in a dictionary
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    # Function to create and return the recipe dictionary

    return recipe

n = int(input("How many recipes would you like to enter?: "))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
      recipe['difficulty'] = 'easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
      recipe['difficulty'] = 'medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
      recipe['difficulty'] = 'intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
      recipe['difficulty'] = 'hard'

for recipe in recipes_list:
   print('Recipe:', recipe['name'])
   print('Cooking time (min):', recipe['cooking_time'])
   print('Ingredients:')
   for ingredient in recipe['ingredients']:
      print(ingredient)
   print('Difficulty:', recipe['difficulty'])

def print_ingredients():
   ingredients_list.sort()
   print('All Ingredients')
   print('_______________')
   for ingredient in ingredients_list:
     print(ingredient)

print_ingredients()
