from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database credentials
USERNAME = 'cf-python'
PASSWORD = 'password'
HOSTNAME = 'localhost'
DATABASE = 'task_database'

# Create the engine
engine = create_engine(f'mysql+pymysql://cf-python:password@localhost/task_database')

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
        ingredient_count = len(self.ingredients.split(', '))
        if ingredient_count <= 5 and self.cooking_time <= 30:
            self.difficulty = 'Easy'
        elif ingredient_count <= 10 and self.cooking_time <= 60:
            self.difficulty = 'Medium'
        elif ingredient_count <= 15 and self.cooking_time <= 90:
            self.difficulty = 'Intermediate'
        else:
            self.difficulty = 'Hard'

    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        return self.ingredients.split(', ')

Base.metadata.create_all(engine)

def create_recipe():
    name = input("Enter recipe name (max 50 characters): ")
    while len(name) > 50:
        name = input("Name too long. Enter again (max 50 characters): ")

    ingredients = []
    num_ingredients = int(input("How many ingredients? "))
    for _ in range(num_ingredients):
        ingredient = input("Enter ingredient: ")
        ingredients.append(ingredient)
    ingredients_str = ', '.join(ingredients)

    cooking_time = input("Enter cooking time in minutes: ")
    while not cooking_time.isnumeric():
        cooking_time = input("Invalid input. Enter cooking time in minutes: ")
    cooking_time = int(cooking_time)

    recipe_entry = Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time)
    recipe_entry.calculate_difficulty()

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
    chosen_indices = []
    for choice in choices.split():
        try:
            chosen_indices.append(int(choice) - 1)
        except ValueError:
            print(f"Invalid input '{choice}'. It should be a number.")

    # Ensure indices are within range
    chosen_indices = [i for i in chosen_indices if 0 <= i < len(all_ingredients)]

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
        new_name = input("Enter new name (max 50 characters): ")
        while len(new_name) > 50:
            new_name = input("Name too long. Enter again (max 50 characters): ")
        recipe_to_edit.name = new_name
    elif attribute == '2':
        new_ingredients = input("Enter new ingredients, separated by commas: ")
        recipe_to_edit.ingredients = new_ingredients
    elif attribute == '3':
        new_cooking_time = input("Enter new cooking time in minutes: ")
        while not new_cooking_time.isnumeric():
            new_cooking_time = input("Invalid input. Enter cooking time in minutes: ")
        recipe_to_edit.cooking_time = int(new_cooking_time)
    else:
        print("Invalid choice.")
        return

    recipe_to_edit.calculate_difficulty()
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
