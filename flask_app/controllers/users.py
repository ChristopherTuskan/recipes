from flask import redirect, request, session, url_for, render_template, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login_and_registration.html')

@app.route('/user/register/', methods=['POST'])
def register_user():
    if not User.validate_reg(request.form, User.get_all()):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # confirm_pw_hash = bcrypt.generate_password_hash(request.form['confirm_password'])
    
    
        
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['id'] = user_id
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    session['email'] = data['email']
    return redirect('/dashboard/')

@app.route('/dashboard/')
def success():
    if session == {}:
        return redirect('/')
    return render_template('dashboard.html', recipes=Recipe.get_all_recipes_with_creator(), user=User.get_recipes_from_user(session))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route('/user/login/', methods=['POST'])
def login():
    if not User.validate_login(request.form, User.get_all()):
        return redirect('/')

    data = {
        'email' : request.form['email']
    }
    user = User.get_by_email(data)
    print(user.id)

    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email
    session['id'] = user.id
    print(session['id'])

    return redirect('/dashboard/')
