from flask import Flask, render_template, url_for, flash, redirect, request, session, make_response
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta 
from wtforms import Form, BooleanField, TextField, PasswordField, validators
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__))) 
from passlib.hash import sha256_crypt
from functools import wraps
from pymysql import escape_string as thwart
import gc

from hellosports import get_baseball, get_basketball, get_hockey, get_football


app = Flask(__name__, instance_path='/var/www/FlaskApp/FlaskApp/protected')
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please Login")
            return redirect(url_for('login page'))
    return wrap   

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

UPLOAD_FOLDER = '/var/www/FlaskApp/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

@app.route("/", methods=["GET","POST"])
def hello():
    try:
        flash("This website prototype is intended to display live sports scores from your favorite teams")
        return render_template("main.html", APP_CONTENT = APP_CONTENT, matches = matches)
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/basketball/', methods=["GET", "POST"])
def basketball():
    try:
        matches = get_basketball()
        return render_template("basketball.html", matches = matches)
        
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/baseball/', methods=["GET", "POST"])
def baseball():
    try:
        matches = get_baseball()
        return render_template("baseball.html", matches = matches)
        
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/football/', methods=["GET", "POST"])
def football():
    try:
        matches = get_football()
        return render_template("football.html", matches = matches)
        
    except Exception as e:
        return render_template("500.html", error = e)

@app.route('/hockey/', methods=["GET", "POST"])
def hockey():
    try:
        matches = get_hockey()
        return render_template("hockey.html", matches = matches)
        
    except Exception as e:
        return render_template("500.html", error = e)
    
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        c, conn = connection()
        return("Connected")
    except Exception as e:
        return(str(e))
    
@app.route('/welcome/')
@login_required
def templating():
    try:
        output = ["DIGIT 400 is coolio", "Python, Java, PHP, SQL, C++", "<p><string>HELLO WORLD</string></p>", 42, "42"]
        return render_template("templating.html", output = output)
        
    except Exception as e:
        return(str(e)) # remove for prductions
    
@app.route("/login/", methods=["GET","POST"])
def login():
    error = ""
    try:
        c, conn = connection()
        if request.method == "POST":
        
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

@app.route('/uploads/', methods=['GET', 'POST'])
@login_required
def upload_file():
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File upload successful')
                return render_template('uploads.html', filename = filename)
            return render_template('uploads.html')
    except:
            flash('Please upload a valid file')
            return render_template('uploads.html')
        
@app.route("/download/")
@login_required
def download():
    try:
        return send_file('/var/www/FlaskApp/FlaskApp/uploads/golden.jpg', attachment_filename="Alternative_Facts.jpg")
    except Exception as e:
        return(str(e)) # remove for production     
        
    
@app.route('/sitemap.xml/', methods =["GET"])
def sitemap():
    try:
        page = []
        week = (datetime.now() - timedelta(days = 7).date()).isoformat()
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and len(rule.arguments)==0:
                page.append(["http://165.227.212.179/"+str(rule.rule),week])
                
        sitemap_xml = render_template('sitemap_template.xml', page = page)
        response = make_response(sitemap.xml)
        response.headers["Content-Type"] = "application/xml"
            
    except Exception as e:
            returns(str(e))
    
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

