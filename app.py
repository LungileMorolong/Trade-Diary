import io

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response
from functools import wraps
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

import requests


# Configure application
app = Flask(__name__)

# Configure mail service
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///diary.db")

# To ensure no-cache so server will work as intended
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    """
    routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# The first landing page of website
@app.route("/", methods=["GET", "POST"])
def index():

    # Forget any user_id
    session.clear()

    # When button is selected, redirect to login
    if request.method == "POST":

        return render_template("login.html")

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Get all the user input
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirmation")
        email = request.form.get("email")
        question = request.form.get("answer")
        answer = question.capitalize()
        acc_balance = int(request.form.get("account"))

        # Get existin user data
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # flash error if username is empty
        if not username:
            flash("Please input username")
            return redirect("/register")

        # flash error if username is empty
        if not acc_balance:
            flash("Please input Account Balance")
            return redirect("/register")

        # flash error if username already exists
        if existing_user:
            flash("Username already exist")
            return redirect("/register")

        # flash error if password empty
        if not password:
            flash("Please input password")
            return redirect("/register")

        # flash error if confirmation password is empty
        if not confirm_pass:
            flash("Please input confirmation password")
            return redirect("/register")

        # flash error if password and confirmation password don't match
        if confirm_pass != password:
            flash("Passwords do not match.")
            return redirect("/register")

        # flash error if no email address entered
        if not email:
            flash("Please input email address")
            return redirect("/register")

        # flash error if Answer input is empty
        if not answer:
            flash("Please answer the question")
            return redirect("/register")

        # Generate hash password
        password_hash = generate_password_hash(password)

        # Check if hash password is generated and unique
        if check_password_hash(password_hash, password):

            # Store username and hash password in the database
            try:

                db.execute("INSERT INTO users (username, hash, answers, balance, email) VALUES (?, ?, ?, ?, ?)", username, password_hash, answer, acc_balance, email)

            # Flash if there is an error
            except:
                flash("There is an error, please try again!")
                return redirect("/register")

        # Send email if registration is complete
        try:

            msg = Message('Welcome', sender = 'tradediaryinfo@gmail.com', recipients = [email])
            msg.body = f"Hi There {username},\n\nWelcome to the Trade Diary. Best place to keep track of all your trading progress.\n\nYou can also use this site to keep up with daily business news.\n\nHope you have a good time.\n\n\nRegards\nTrade Diary"
            mail.send(msg)

        except:
            flash("Error sending email")
            return redirect("/register")


        # Redirect user to login to access other pages
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        password = request.form.get("password")
        username = request.form.get("username")

        # Ensure username was submitted
        if not username:
            return redirect("/login")

        # Ensure password was submitted
        if not password:
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return redirect("/login")

        # Ensure provided password matches stored password
        if not check_password_hash(rows[0]["hash"], password):
            return redirect("/login")


        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/news")


    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/news")
@login_required
def news():

    # Contact API
    api_key = ''
    url = f'https://newsapi.org/v2/sources?category=business&language=en&apiKey={api_key}'
    response = requests.get(url)

    data = response.json()

    articles = data['sources']

    return render_template('news.html', articles=articles)


@app.route("/diary", methods=["GET","POST"])
@login_required
def diary():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        user_id = session["user_id"]

        # Getting all user input
        stock_name = request.form.get("name")
        name = stock_name.upper()
        pl = request.form.get("pl")
        comment = request.form.get("comments")
        acc_balance = db.execute("SELECT balance FROM users WHERE id = ?", user_id)[0]["balance"]
        image = request.files['file']

        # Flash error if no name is typed
        if not stock_name:
            flash("Please input trade name")
            return redirect("/diary")

        # Flash error if no opening price in typed
        try:
            firstprice = int(request.form.get("firstprice"))

        except:
            flash("Please input the starting price of the trade")
            return redirect("/diary")

        # Flash error if no closing price in typed
        try:
            endprice = int(request.form.get("endprice"))

        except:
            flash("Please input the ending price of the trade")
            return redirect("/diary")

        # Flash error if no win/loss amount in typed
        try:
            win_loss = int(request.form.get("won-loss"))

        except:
            flash("Please input the win or loss amount of the trade")
            return redirect("/diary")

        # Flash error if no comment was typed
        if not comment:
            flash("Please type your comments/thoughts of the trade")
            return redirect("/diary")

        # flash error if no image was selected
        if not image:
            flash("Please select an image of the trade")
            return redirect("/diary")

        # Calculate profit or loss amount
        transaction_price = endprice - firstprice

        # Ensure the profit or loss amount user typed is correct
        if transaction_price != win_loss:
            flash("Incorrect Win or Loss Amount. Calculate the loss/win price again")
            return redirect("/diary")

        # Calculate balance after trade
        current_bal = acc_balance + transaction_price

        # Keep track of date of diary entry
        current_date = datetime.now()

        # To save image data as a standard jpg format
        image.save("trading.jpg")

        with open('trading.jpg', 'rb') as file:
            image_data = file.read()

        # Update transaction table with sold shares
        db.execute("INSERT INTO transactions (user_id, date, name, firstprice, endprice, win_loss, profit_loss, comments, pic, balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        user_id, current_date, name, firstprice, endprice, win_loss, pl, comment, image_data, current_bal)

        # Update user's balance
        db.execute("UPDATE users SET balance = ? WHERE id = ?", current_bal, user_id)

        flash("Diary Updated!")

        return redirect("/history")

    return render_template("diary.html")


@app.route("/view_image/<int:image_id>")
@login_required
def view_image(image_id):


    user_id = session["user_id"]

    # Get image from database
    image_data = db.execute("SELECT pic FROM transactions WHERE id = ? AND user_id = ?", image_id, user_id)[0]

    # if image available in database, allow image to be viewed
    if image_data:
        image = io.BytesIO(image_data['pic'])
        image.seek(0)
        return Response(image, content_type='image/jpeg')

    else:
        flash("Image not found")
        return redirect("/history")


@app.route("/history")
@login_required
def history():

    user_id = session["user_id"]

    # This is to call the user data
    user_data = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", user_data=user_data)


@app.route("/graph")
@login_required
def graph():

    user_id = session["user_id"]

    # Retrieving data for line graph
    account_bal = db.execute("SELECT date, balance FROM transactions WHERE user_id = ?", user_id)

    # storing y axis and x axis data
    dates = [row['date'] for row in account_bal]
    values = [row['balance'] for row in account_bal]

    return render_template("graph.html", labels=dates, values=values)


@app.route("/username",methods=["GET","POST"])
@login_required
def username():

    if request.method == "POST":

        user_id = session["user_id"]

        # Get all user input
        existname = request.form.get("existusername")
        new_name = request.form.get("newuser")
        answer = request.form.get("answer").capitalize()

        # Retrieve user data from users table
        user_data = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        current_user = user_data[0]['username']

        email = user_data[0]['email']

        # Flash error when no existing name has been typed
        if not existname:
            flash("Please input username")
            return redirect("/username")

        # Flash error when no new name has been typed
        if not new_name:
            flash("Please input new username")
            return redirect("/username")

        # Flash error when no answer has been typed
        if not answer:
            flash("Please input answer to the security question")
            return redirect("/username")

        # Flash error when typed existing name is not the same as stored username
        if existname != current_user:
            flash("Please input correct username!")
            return redirect("/username")

        # flash error when typed answer does not match stored security answer
        if answer not in user_data[0]["answers"]:
            flash("Please input correct answer to security question!")
            return redirect("/username")

        # Check if new username already exist
        if current_user == 1:
            flash("Username already exist")
            return redirect("/username")

        db.execute("UPDATE users SET username = ? WHERE id = ?", new_name, user_id)

        # Send email once update is complete
        try:

            msg = Message('Username Update', sender = 'tradediaryinfo@gmail.com', recipients = [email])
            msg.body = f"Hi There {new_name},\n\nYou have updated your username successfuly from {existname}\n\nIf this was not done by you, and you suspect fraud, Please send email to tradediaryinfo@gmail.com.\n\nTake care.\n\n\nRegards\nTrade Diary"
            mail.send(msg)

        except:
            flash("Error sending email")
            return redirect("/username")

        flash("Username updated successfully!")
        return redirect("/news")


    return render_template("username.html")


@app.route("/password",methods=["GET","POST"])
@login_required
def password():

    if request.method == "POST":

        user_id = session["user_id"]

        # Get user input
        existpass = request.form.get("existpassword")
        new_pass = request.form.get("newpass")
        confirm_pass = request.form.get("confirmpass")
        answer = request.form.get("answer").capitalize()

        # Get user data from users table
        user_data = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        email = user_data[0]['email']
        username = user_data[0]['username']

        # flash error if existing password not typed
        if not existpass:
            flash("Please enter current password")
            return redirect("/password")

        # flash error if new password not typed
        if not new_pass:
            flash("Please enter new password")
            return redirect("/password")

        # flash error if confirmation password not typed
        if not confirm_pass:
            flash("Please enter confirmation password")
            return redirect("/password")


        if confirm_pass != new_pass:
            flash("Confirm password does not match.")
            return redirect("/password")

        if answer not in user_data[0]["answers"]:
            flash("Please input correct answer to security question!")
            return redirect("/password")

        if not check_password_hash(user_data[0]["hash"], existpass):
            flash("Invalid existing password")
            return redirect("/password")

        pass_hash = generate_password_hash(new_pass)

        if check_password_hash(pass_hash, new_pass):

            db.execute("UPDATE users SET hash = ? WHERE id = ?", pass_hash, user_id)

        try:

            msg = Message('Password Update', sender = 'tradediaryinfo@gmail.com', recipients = [email])
            msg.body = f"Hi There {username},\n\nYou have updated your password successfuly\n\nIf this was not done by you, and you suspect fraud, send email to tradediaryinfo@gmail.com\n\nTake care.\n\n\nRegards\nTrade Diary"
            mail.send(msg)

        except:
            flash("Error sending email")
            return redirect("/password")

        flash("Password updated successfully!")
        return redirect("/news")

    return render_template("password.html")

