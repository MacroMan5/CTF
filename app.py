
# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User, create_db_and_populate, session
from sqlalchemy import inspect


app = Flask(__name__)
app.config.from_object('config')

# Import the User model after initializing the database
from models import User

# Call create_db_and_populate() when the app is initialized
@app.before_first_request
def init_db():
    create_db_and_populate()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Ici, vous devriez vérifier les informations d'identification à l'aide de votre base de données
        if username == 'User' and password == 'Qwerty!':
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
    
        else:
            flash('Login failed')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    list_employes = session.query(User).all() # Récupérer tous les utilisateurs
    full_names = [user.full_name for user in list_employes]
    return render_template('dashboard.html', full_names=full_names)

@app.route('/listeEmployes')
def listeEmployes():
    list_employes = session.query(User).all()
    return render_template('listeEmployes.html', list_employes=list_employes)

if __name__ == '__main__':
    app.run(debug=True) # Laissez debug=True pour le développement

