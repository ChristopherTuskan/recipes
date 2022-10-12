from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user
import datetime

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.recipe_desc = data['recipe_desc']
        self.under_30_min = data['under_30_min']
        self.instructions = data['instructions']
        self.date_made_recipe = data['date_made_recipe']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, recipe_desc, under_30_min, instructions, date_made_recipe, user_id) VALUES (%(name)s, %(recipe_desc)s, %(under_30_min)s, %(instructions)s, %(date_made_recipe)s, %(user_id)s);"
        recipe_id = connectToMySQL("recipes").query_db(query, data)
        return recipe_id

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id=%(id)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        main_result = result[0]
        one_recipe = cls(result[0])
        one_recipe_author_info = {
            'id' : main_result['users.id'],
            'first_name' : main_result['first_name'],
            'last_name' : main_result['last_name'],
            'email' : main_result['email'],
            'password' : main_result['password'],
            'created_at' : main_result['users.created_at'],
            'updated_at' : main_result['users.updated_at']
        }
        author = user.User(one_recipe_author_info)
        one_recipe.creator = author
        return one_recipe

    @classmethod
    def get_all_recipes_with_creator(cls):
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;'
        results = connectToMySQL('recipes').query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipe_author_info = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            author = user.User(one_recipe_author_info)
            one_recipe.creator = author
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name = %(name)s, recipe_desc = %(recipe_desc)s, instructions = %(instructions)s, date_made_recipe = %(date_made_recipe)s, under_30_min = %(under_30_min)s WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True # we assume this is true
        print(recipe['under_30_min'])
        if len(recipe['name']) < 3:
            flash("Recipe Name must be at least 3 characters.")
            is_valid = False
        if len(recipe['recipe_desc']) < 3:
            flash("Recipe Description must be at least 3 characters.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        if len(recipe['date_made_recipe']) < 1:
            flash("Date Cooked/Made cannot be blank")
            is_valid = False
        if recipe['under_30_min'] != 'Yes' and recipe['under_30_min'] != 'No':
            flash("Under 30 Minutes cannnot be blank")
            is_valid = False
        print(is_valid)
        return is_valid
