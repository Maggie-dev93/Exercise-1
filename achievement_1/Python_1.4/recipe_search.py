import pickle

def display_recipe(recipe):
    print("Recipe Name: {}".format(recipe['recipe_name']))
    print("Cooking Time: {}".format(recipe['cooking_time']))
    print("Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(" - {}".format(ingredient))
    print("Difficulty: {}".format(recipe['difficulty']))
    print("")


# Function to search ingredients
def search_ingredients(data):
    # Adds number to each element in the list
    available_ingredients = enumerate(data["all_ingredients"])
    # Put enumerated data into a list
    numbered_list = list(available_ingredients)
    print("Ingredients List: ")

    for ele in numbered_list:
        print(ele[0], ele[1])
    try:
        num = int(input("Enter the number for the ingredient you would like to search: "))
        ingredient_searched = numbered_list[num][1]
        print("Searching for recipes with", ingredient_searched, "...")
    except ValueError:
        print("Only numbers are allowed")
    except IndexError:
        print("Oops! Your input doesn't match any ingredients. Make sure you enter a number that matches the ingredients list.")
    else:
        for ele in data["recipes_list"]:
            if ingredient_searched in ele["ingredients"]:
                display_recipe(ele)


filename = input("Enter the name of the file you want to load from: ")

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
        print("File loaded successfully!")
except FileNotFoundError:
    print("No files match that name - please try again")
except Exception as e:
    print(f"Oops, there was an unexpected error: {e}")
else:
    print("Displaying all recipes:")
    for recipe in data["recipes_list"]:
        display_recipe(recipe)
    search_ingredients(data)
