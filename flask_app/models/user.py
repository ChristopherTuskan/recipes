from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import recipe
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []
        
    @staticmethod
    def validate_reg(reg_user,users):
        is_valid = True # we assume this is true
        if len(reg_user['first_name']) < 2:
            flash("First Name must be at least 2 characters.", 'category1')
            is_valid = False
        if len(reg_user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", 'category1')
            is_valid = False
        if len(reg_user['password']) < 2:
            flash("Password must be at least 2 characters.", 'category1')
            is_valid = False
        if not reg_user['password'] == reg_user['confirm_password']:
            flash("Passwords do not match", 'category1')
            is_valid=False
        if not EMAIL_REGEX.match(reg_user['email']):
            flash("Invalid email address!", 'category1')
            is_valid = False
        for other_user in users:
            if (reg_user['email'] == other_user.email):
                flash("Email address needs to be unique", 'category1')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login(login_user,users):
        is_valid = False
        for other_user in users:
            print(other_user.email)
            print(login_user['email'])
            if login_user['email'] == other_user.email:
                print('good email')
                print(bcrypt.check_password_hash(other_user.password, login_user['password']))
                if bcrypt.check_password_hash(other_user.password, login_user['password']):
                    print('good password and email')
                    is_valid = True
                    return is_valid
        print('bad email or password')
        flash('Invalid Email/Password', 'category2')
        return is_valid


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        user_id = connectToMySQL("recipes").query_db(query, data)
        return user_id

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_recipes_from_user(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        user = cls(results[0])
        for row_from_db in results:
            recipe_data = {
                "id" : row_from_db["recipes.id"],
                "name" : row_from_db["name"],
                "recipe_desc" : row_from_db["recipe_desc"],
                "instructions" : row_from_db["instructions"],
                "date_made_recipe" : row_from_db["date_made_recipe"],
                "under_30_min" : row_from_db["under_30_min"]
            }
            user.recipes.append( recipe.Recipe(recipe_data))
        print(user.recipes)
        return user