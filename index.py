from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import config
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.User import User

# Variables
app = Flask(__name__)
db = MySQL(app)
login_manager_app=LoginManager(app)

#<-----------LOGIN MANAGER----------->

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

#<-----------INDEX PAGE----------->

@app.route("/")
def index():
    return redirect(url_for("login"))

#<-----------LOGIN PAGE----------->

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        
        user =User(0,request.form['username'],request.form['password'])
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                print("Invalid password...")
                flash("Invalid password...")
                return render_template('login.html')
        else:
            print("User not found...")
            flash("User not found...")
            return render_template('login.html')
    else:
        return render_template('login.html')

#<-----------REGISTER PAGE----------->    

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username = request.form['reg_username']
        passwd = request.form['reg_password']
        ModelUser.register(db, username, passwd)
        return redirect(url_for('login'))

    return render_template('register.html')

#<-----------HOME PAGE----------->
@app.route("/home")
@login_required
def home():
    posts = ModelUser.get_post(db)

    admin_posts = ModelUser.get_admin_post(db)

    return render_template('home_page.html', data = posts, data_admin = admin_posts)

#<-----------POST PAGE----------->
@app.route("/post", methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # Obtener el texto del post desde el formulario
        texto_post = request.form['texto_post']

        user = current_user.username

        hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if current_user.id == 2:
            user = "TheGentleman"
            ModelUser.create_admin_post(db, texto_post, user, hora_actual)
        else:
            ModelUser.create_post(db, texto_post, user, hora_actual)
            return redirect(url_for('home'))
    return render_template('post.html')


@app.route('/delete_post', methods=['POST'])
def delete_post():
    id = request.form.get('id_post')

    if id:
        ModelUser.delete_post(db, id)
        return redirect(url_for('home'))
    

#<-----------PROFILE PAGE----------->
@app.route("/profile")
def profile():
    return render_template('profile.html')

#<-----------LOGOUT----------->

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

#<-----------RUN----------->

def status_401(error):
    return redirect(url_for('login')), 401

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(401,status_401)
    app.run()