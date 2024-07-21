class Recipe:
    # Class attribute to keep track of all unique ingredients used in any recipe
    all_ingredients = set()
    
    def __init__(self, name, ingredients, cooking_time):
        # Initialize the Recipe object with name, ingredients, cooking time, and difficulty
        self._name = name
        self._ingredients = ingredients
        self._cooking_time = cooking_time
        self._difficulty = None
        self.update_all_ingredients()  # Ensure all ingredients are tracked

    def add_ingredients(self, *ingredients):
        # Add additional ingredients to the recipe and update the global ingredient list
        self._ingredients.extend(ingredients)
        self.update_all_ingredients()
    
    def search_ingredient(self, ingredient):
        # Check if a particular ingredient is in the recipe
        return ingredient in self._ingredients
    
    def update_all_ingredients(self):
        # Add all ingredients of the current recipe to the class-wide set of all ingredients
        for ingredient in self._ingredients:
            Recipe.all_ingredients.add(ingredient)
    
    def calculate_difficulty(self):
        # Determine the difficulty level of the recipe based on the cooking time and number of ingredients
        num_ingredients = len(self._ingredients)
        if self._cooking_time < 10:
            if num_ingredients < 4:
                self._difficulty = "Easy"
            else:
                self._difficulty = "Medium"
        else:
            if num_ingredients < 4:
                self._difficulty = "Intermediate"
            else:
                self._difficulty = "Hard"
    
    def get_difficulty(self):
        # Get the difficulty of the recipe, calculating it if not already done
        if not self._difficulty:
            self.calculate_difficulty()
        return self._difficulty
    
    def get_name(self):
        # Return the name of the recipe
        return self._name
    
    def set_name(self, name):
        # Set a new name for the recipe
        self._name = name
    
    def get_cooking_time(self):
        # Return the cooking time of the recipe
        return self._cooking_time
    
    def set_cooking_time(self, cooking_time):
        # Set a new cooking time for the recipe
        self._cooking_time = cooking_time
    
    def get_ingredients(self):
        # Return the list of ingredients for the recipe
        return self._ingredients
    
    def __str__(self):
        # Return a string representation of the recipe, including name, ingredients, cooking time, and difficulty
        return f"Recipe Name: {self._name}\nIngredients: {', '.join(self._ingredients)}\nCooking Time: {self._cooking_time} minutes\nDifficulty: {self.get_difficulty()}\n"
    

def recipe_search(data, search_term):
    # Search and print recipes that contain a specific ingredient
    print(f"Recipes that contain '{search_term}':\n")
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


# Create recipe instances
tea = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 5)
coffee = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"], 5)

# Add recipes to a list
recipes_list = [tea, coffee, cake, smoothie]

# Display string representation of each recipe
for recipe in recipes_list:
    print(recipe)

# Search for recipes that contain certain ingredients
for ingredient in ["Water", "Sugar", "Bananas"]:
    recipe_search(recipes_list, ingredient)
