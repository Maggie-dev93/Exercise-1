from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database credentials
USERNAME = 'cf-python'
PASSWORD = 'password'
HOSTNAME = 'localhost'
DATABASE = 'task_database'

engine = create_engine (f'mysql+pymysql://cf-python:password@localhost/t
ask_database' )
# Create a session maker
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'final_recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    ingredients = Column(String(255), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})>"

    def __str__(self):
        return (f"Recipe ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Ingredients: {self.ingredients}\n"
                f"Cooking Time: {self.cooking_time} minutes\n"
                f"Difficulty: {self.difficulty}")

    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients.split(', '))
        if self.cooking_time < 10:
            if num_ingredients < 4:
                return 'Easy'
            else:
                return 'Medium'
        else:
            if num_ingredients < 4:
                return 'Intermediate'
            else:
                return 'Hard'

    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        return self.ingredients.split(', ')

Base.metadata.create_all(engine)

def input_name():
    name = input("Enter recipe name (max 50 characters): ")
    while len(name) > 50:
        name = input("Name too long. Enter again (max 50 characters): ")
    return name

def input_ingredients():
    ingredients = []
    num_ingredients = int(input("How many ingredients? "))
    for _ in range(num_ingredients):
        while True:
            ingredient = input("Enter ingredient: ")
            if any(char.isalpha() for char in ingredient) and not ingredient.isnumeric():
                ingredients.append(ingredient)
                break
            else:
                print("Invalid ingredient. It should not be purely numeric and must contain at least one letter. Please try again.")
    return ', '.join(ingredients)

def input_cooking_time():
    cooking_time = input("Enter cooking time in minutes: ")
    while not cooking_time.isnumeric():
        cooking_time = input("Invalid input. Enter cooking time in minutes: ")
    return int(cooking_time)

def create_recipe():
    name = input_name()
    ingredients = input_ingredients()
    cooking_time = input_cooking_time()

    recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time)
    recipe_entry.difficulty = recipe_entry.calculate_difficulty()

    session.add(recipe_entry)
    session.commit()
    print("Recipe added successfully!")

def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes found.")
        return

    for recipe in recipes:
        print(recipe)
        print("-" * 40)

def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("No recipes found.")
        return

    results = session.query(Recipe.ingredients).all()
    all_ingredients = set()
    for result in results:
        ingredients = result[0].split(', ')
        all_ingredients.update(ingredients)

    all_ingredients = list(all_ingredients)
    for i, ingredient in enumerate(all_ingredients, 1):
        print(f"{i}. {ingredient}")

    choices = input("Enter the numbers of the ingredients you want to search for, separated by spaces: ")

    # Remove any commas and split by spaces
    choices = choices.replace(',', ' ')
    input_choices = choices.split()

    # Check if all input choices are digits and within the allowed range
    if not all(choice.isdigit() and 1 <= int(choice) <= len(all_ingredients) for choice in input_choices):
        print("Invalid input. Please enter valid numbers corresponding to the ingredients list.")
        return

    chosen_indices = [int(choice) - 1 for choice in input_choices]
    search_ingredients = [all_ingredients[i] for i in chosen_indices]

    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    recipes = session.query(Recipe).filter(*conditions).all()
    if not recipes:
        print("No recipes found for the selected ingredients.")
        return

    for recipe in recipes:
        print(recipe)
        print("-" * 40)

def edit_recipe():
    if session.query(Recipe).count() == 0:
        print("No recipes found.")
        return

    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe in recipes:
        print(f"ID: {recipe.id}, Name: {recipe.name}")

    id_to_edit = input("Enter the ID of the recipe you want to edit: ")
    recipe_to_edit = session.query(Recipe).filter_by(id=id_to_edit).first()
    if not recipe_to_edit:
        print("Recipe not found.")
        return

    print(recipe_to_edit)

    attribute = input("Which attribute would you like to edit? (1: Name, 2: Ingredients, 3: Cooking Time): ")
    if attribute == '1':
        recipe_to_edit.name = input_name()
    elif attribute == '2':
        recipe_to_edit.ingredients = input_ingredients()
    elif attribute == '3':
        recipe_to_edit.cooking_time = input_cooking_time()
    else:
        print("Invalid choice.")
        return

    recipe_to_edit.difficulty = recipe_to_edit.calculate_difficulty()
    session.commit()
    print("Recipe updated successfully!")

def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("No recipes found.")
        return

    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe in recipes:
        print(f"ID: {recipe.id}, Name: {recipe.name}")

    id_to_delete = input("Enter the ID of the recipe you want to delete: ")
    recipe_to_delete = session.query(Recipe).filter_by(id=id_to_delete).first()
    if not recipe_to_delete:
        print("Recipe not found.")
        return

    confirm = input(f"Are you sure you want to delete the recipe '{recipe_to_delete.name}'? (yes/no): ")
    if confirm.lower() == 'yes':
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Deletion cancelled.")

def main_menu():
    while True:
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice.lower() == 'quit':
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()
    engine.dispose()

if __name__ == "__main__":
    main_menu()

