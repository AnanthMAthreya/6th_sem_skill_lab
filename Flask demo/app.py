from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymongo

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["library_db"]
users_collection = db["users"]

@app.route('/')
def home():
    # If the user is logged in, display a personalized greeting
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verify user credentials from MongoDB
        user = users_collection.find_one({'username': username, 'password': password})
        
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user from the session
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        # Save the new user to the database
        users_collection.insert_one({'name': name, 'email': email, 'username': username, 'password': password})
        flash('Registration successful, please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reg_form.html')

if __name__ == '__main__':
    app.run(debug=True)
