from flask import redirect, request, session, url_for, render_template, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipe/new/')
def new_recipe():
    if session == {}:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipe/submit/', methods=['POST'])
def submit_recipe():

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new/')

    data = {
        'name': request.form['name'],
        'recipe_desc': request.form['recipe_desc'],
        'under_30_min': request.form['under_30_min'],
        'instructions': request.form['instructions'],
        'date_made_recipe': request.form['date_made_recipe'],
        'user_id' : session['id']
    }

    Recipe.save(data)

    return redirect('/dashboard/')

@app.route('/recipe/view/<int:id>/')
def view_recipe(id):
    data = {
        'id' : id
    }
    return render_template('view_recipe.html', recipe = Recipe.get_by_id(data),)

@app.route('/recipe/edit/<int:id>/')
def edit_recipe(id):
    data = {
        'id' : id
    }
    session['recipe_id'] = id
    return render_template('edit_recipe.html', recipe = Recipe.get_by_id(data))

@app.route('/recipe/update/', methods=['POST'])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect(url_for('edit_recipe', id=session['recipe_id']))

    data = {
        'id' : session['recipe_id'],
        'name' : request.form['name'],
        'recipe_desc' : request.form['recipe_desc'],
        'instructions' : request.form['instructions'],
        'date_made_recipe' : request.form['date_made_recipe'],
        'under_30_min' : request.form['under_30_min']
    }
    session.pop('recipe_id')

    Recipe.update(data)
    return redirect('/dashboard/')

@app.route('/recipe/destroy/<int:id>')
def destroy_recipe(id):
    data = {
        'id' : id
    }

    Recipe.destroy(data)
    return redirect('/dashboard/')