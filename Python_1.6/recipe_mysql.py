import mysql.connector

def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients.split(', '))
    if cooking_time < 10:
        if num_ingredients < 4:
            return 'Easy'
        else:
            return 'Medium'
    else:
        if num_ingredients < 4:
            return 'Intermediate'
        else:
            return 'Hard'

def sanitize_ingredients(ingredients):
    # Split by comma, trim spaces, and rejoin with ', '
    return ', '.join([ingredient.strip() for ingredient in ingredients.split(',')])

def create_recipe(conn, cursor):
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter the ingredients (comma-separated): ")
    
    # Sanitize the ingredients input
    sanitized_ingredients = sanitize_ingredients(ingredients)
    
    difficulty = calculate_difficulty(cooking_time, sanitized_ingredients)

    insert_query = """
    INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, sanitized_ingredients, cooking_time, difficulty))
    conn.commit()
    print("Recipe added successfully!")

def search_recipe(conn, cursor):
    cursor.execute("SELECT DISTINCT ingredients FROM Recipes")
    results = cursor.fetchall()

    all_ingredients = set()
    for row in results:
        ingredients = row[0]
        all_ingredients.update(ingredients.split(', '))

    print("\nAvailable ingredients:")
    for idx, ingredient in enumerate(sorted(all_ingredients), start=1):
        print(f"{idx}. {ingredient}")

    choice = int(input("Choose an ingredient by number to search: ")) - 1
    search_ingredient = sorted(all_ingredients)[choice]

    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(search_query, ('%' + search_ingredient + '%',))
    
    results = cursor.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("No recipes found with that ingredient.")

def update_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    
    print("\nExisting recipes:")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe to update: "))
    column_to_update = input("Enter the column to update (name, ingredients, cooking_time): ")

    new_value = None
    if column_to_update == 'name':
        new_value = input("Enter the new name: ")
        update_query = "UPDATE Recipes SET name = %s WHERE id = %s"
        cursor.execute(update_query, (new_value, recipe_id))
    elif column_to_update == 'ingredients':
        new_value = input("Enter the new ingredients (comma-separated): ")
        
        # Sanitize the new ingredients input
        sanitized_ingredients = sanitize_ingredients(new_value)
        
        update_query = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
        cursor.execute(update_query, (sanitized_ingredients, recipe_id))
    elif column_to_update == 'cooking_time':
        new_value = int(input("Enter the new cooking time (in minutes): "))
        update_query = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
        cursor.execute(update_query, (new_value, recipe_id))
    else:
        print("Invalid column.")
        return

    if column_to_update in ['ingredients', 'cooking_time']:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        row = cursor.fetchone()
        difficulty = calculate_difficulty(row[0], row[1])
        update_query = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
        cursor.execute(update_query, (difficulty, recipe_id))

    conn.commit()
    print("Recipe updated successfully!")

def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    
    print("\nExisting recipes:")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe to delete: "))

    delete_query = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(delete_query, (recipe_id,))
    conn.commit()
    print("Recipe deleted successfully!")

def create_database_and_table(conn, cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
    cursor.execute("USE task_database")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS Recipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

def main_menu(conn, cursor):
    while True:
        print("\nMain Menu:")
        print("1. Create a new recipe")
        print("2. Search for recipes by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print("Exiting...")
            conn.commit()
            cursor.close()
            conn.close()
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    conn = mysql.connector.connect(
        host='localhost',
        user='cf-python',
        passwd='password',
        database='task_database'
    )
    cursor = conn.cursor()

    create_database_and_table(conn, cursor)
    
    main_menu(conn, cursor)

