from flask import Flask, render_template, url_for, flash, redirect, request, session
""""
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from pymysql import escape_string as thwart
import gc
"""


app = Flask(__name__)
"""
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please Login")
            return redirect(url_for('login page'))
    return wrap
"""    

# CMS Structure: Title, Path, Message
APP_CONTENT = {
    "Home":[["Welcome","/welcome/","Welcome to my app you can do many things here!"],
            ["Background","/background/","We had a lot of fun building this app.  Learn more about our story."],
            ["Messages","/messages/","Get your messages from the community!"]],
    
    "Profile":[["User Profile","/profile/","Edit your profile here."],
               ["Photo Upload","/upload/","Upload your profile picture here"],
               ["Terms of Service","/tos/","The legal stuff"]],
    
    "Contact":[["Contact Us","/contact/","Get in touch!  We'd love to hear from you"]],
}


@app.route("/", methods=["GET","POST"])
def hello():
    try:
        return render_template("main.html", APP_CONTENT = APP_CONTENT)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        c, conn = connection()
        return("Connected")
    except Exception as e:
        return(str(e))

    
@app.route("/login/", methods=["GET","POST"])
def login():
    error = ""
    try:
        c, conn = connection()
        if request.method == "POST"
        
            data = c.execute("SELECT * FROM users WHERE username = ('{0}')".format(thwart(request.form['username'])))
        
            data = c.fetchone()[2]
            
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                
                flash("You are now logged in")
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid Credentials. Please Try Again"
                return render_template("login.html", error = error)
            
    except Exception as e:
        flash(e)
        error = "Invalid Credentials, Try Again!"
        return render_template("login.html", error = error)

@app.route("/dashboard/")
def dashboard():
    try:
        flash("This is a flash notification")
        return render_template("dashboard.html", APP_CONTENT = APP_CONTENT)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!!")
    gc.collect()
    return redirect(url_for('main'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("405.html")

@app.errorhandler(500)
def internal_server(e):
    return render_template("500.html", error = e)


if __name__ == "__main__":
    app.run()

