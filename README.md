# Trade Diary
#### Video Demo:  <https://youtu.be/RDw-QPCg7xU>
#### Description:

  **Web Application Overview**

    This web application is built for a data driven approach, allowing the trader to quantify their trading ideas over time. This is especially important as the trader will have a better idea of which strategies/ markets/risk management protocols work and which don't.
    This web application has a graph that will show you your profit/loss journey, and a comment section that will allow you to enter your thoughts as to why you entered and/or existed a given trade. You'll also be able to upload a screenshot of your trade, which will give you a better reference point as to whether that trade was a sound business decision or an impulsive entry/exit.
    The web application also provides multiple business news options, allowing trader to keep up to date with daily business news which improves the trader's market awareness.

  **Each Webpage Details**

    When you open the web app url, it lands on the website starting page (index.html). I provides a brief explanation of what the web app is about. To move on to the next page, you will need to select the "LET'S GET STARTED" button. I chose a background picture that shows a laptop, phone, and smart watch that shows a trading price chart, to connect it to my web app's theme. I chose the stock price bar for the logo to further connect with the web app's theme. When you hover over the "LET'S GET STARTED" button, it turns green. I chose that feature as a trading color for positive trade. The background image, logo, and hover over button is consistent throughout the web app.

    Then the web app takes you to the login page (login.html). Here you input your details and select "LOGIN"if you already have a profile. If not, you can select "Register" in green under the input fields, or the "REGISTTER" in the navbar. Throughout the web app, I use the horizontal centering element class="mb-3". Meaning setting the margin bottom to $spacer 1. When you hover over the nav-items (LOGIN, REGISTER), they turn green and a line crosses under the text. This is an interactive design I chose to make my web app more dynamic. The spacing and nav-item design is consistent throughout the web app.

    After selecting "Register", the web app will take you to the register page (register.html). You will be prompted to input the registration details on the input field. Once registration is done, you will be redirected to the login page to log in. You will also receive a welcome email. A white bar error will flash just below the nav-bar with whatever error you made. This feature is consistent throughout the web app.

    After logging in, you will be redirected to the daily business news page (news.html). Here the user will find different news outlets decriptions and a hyperlink to the outlet's website to get daily business news throughout the world. The hyperlink is in green to keep up with the green theme throughout the web app. After each news outlet description, I placed a thematic break to section the descriptions. New nav-items are NEWS, DIARY, HISTORY(which is a dropdown list containing: HISTORY GRAPH, HISTORY TABLE), ACCOUNTS (which is also a dropdown list containing: UPDATE USERNAME, UPDATE PASSWORD), and LOGOUT.

    When you select DIARY, it will take you to the diary page (diary.html). This is where you input your trade details as a trader such as Name of trade, opening trade price, closing trade price, how much your won/loss, whether it was a profit or loss, trade image, and trade comments. After inputting the details and selecting submit, you will be redirected to the history table page (history.html).

    When you arrive to the history table, you will see all your previous trade details displayed in a bordered-table form with a white background. I chose the white background so that the table details can be clear and stand out from the background. Which includes all the details you inputted in DIARY. If you want to see your trade image, select the trade image hyperlink in the table row. The image will download for you to view and save on your computer.

    When you select the HISTORY nav-item you will be given two options: HISTORY TABLE, and HISTORY GRAPH. When hovering over the two options, they will turn green and a line crosses below them.

    After selecting HISTORY GRAPH, you will be redirected to the history graph page (graph.html). Here you will see a line graph showing your account balance over time from your first trade. I made the background white so it stands out from the background. I used javascript <script> tag to display the line graph. I made the line in the line graph green to maintain the theme throughout the web app.

    After selecting ACCOUNTS in the nav-bar, it will dropdown to a list showing UPDATE USERNAME, and UPDATE PASSWORD. When hovering over the two options, they will also turn green with a line crossing below them.

    After selecting UPDATE USERNAME, you will be redirected to the username page (username.html). You will find input fields prompting you to fill in your current username, new username, and answer the security question. If all input is correct, you will be send an email confirming the update, and if it is not you who updated, to email back. You when then be redirected to the news page.

    After selecting UPDATE PASSWORD, you will be redirected to the password page (password.html). You will find input fields prompting you to fill in your current password, new password, enter the new password again as confirmation, answer the security question. If all input is correct, you will be send an email confirming the update, and if it is not you who updated, to email back. You when then be redirected to the news page.

    To logout, you can either select log out, or the Trade Diary logo. It will redirect you to the website starting page.


  **Installation/ Imports**

    I was using the cs50 codespace so most of the programs I needed such as sql, flask, etc, where already in the codespace. I installed flask-mail so I will be able to send emails using python for the flask application.

    Below are the imports needed for the flask application:

    import io
    from cs50 import SQL
    from flask import Flask, flash, redirect, render_template, request, session, Response
    from functools import wraps
    from flask_session import Session
    from flask_mail import Mail, Message
    from werkzeug.security import check_password_hash, generate_password_hash
    from datetime import datetime
    import requests


  **Configuration**

    Below are the configurations for the flask application:
    - To configure the flask application:
        app = Flask(__name__)
    - To configure the flask-mail feature for the application
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USE_SSL'] = True
        app.config['MAIL_USERNAME'] = 'tradediaryinfo@gmail.com'
        app.config['MAIL_PASSWORD'] = 'mjiimzhsmpuxknuz'
        mail = Mail(app)
    - To configure session so we can use filesystem, instead of using signed cookies
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_TYPE"] = "filesystem"
        Session(app)
    - To configure cs50 library to use sqlite database
        db = SQL("sqlite:///diary.db")


  **diary.db**

    This is a database file for this web application.
    In the file consists of tables:
        - transactions table:
            This table is used to store the diary page inputs. This table is also used to displayed the store data in a history table and history graph.
        - users table:
            This table is used to store all registered users' information. We dp this to keep track of which user is inputting the above transactions details and to be able to send the user an email.


  **app.py**

    After the abovementioned imports and configurations, I have the below functions:
    - after_request function:
        This function is to ensure each response is not cached to ensure the web application works as intended. Such as avoiding data lacks, too much storage usage, and ensuring web page shows the most updated content.
    - login_required function:
        This function is to ensure certain aspects of the web page is not available unless the user is logged in.
    - @app.route:
        This feature is to map the specific url to the function to perform a specified task.
    - index function:
        This takes us to the first page of the website. This also ensures that when the button is selected it takes us to the login page. This page also clears any session that existed prior, so the user will need to log in again to access some parts of the web application.
    - register function:
        This function takes in user input. It verifies if the user input is correct or in the correct format. If not, a flash error will appear. Once verified, the input is stored in the sql database. This function also ensures an email is sent once all input is verified and stored. Then it will redirect to login page.
    - login function:
        This function takes in username and password input. It verifies if the input matches that which is stored in the database. If so, the user will be logged in and redirected to the news page.
    - logout function:
        This function allows user to end their session on the web app, and redirects them to the index/first page.
    - news functions:
        This function requires user to be logged in first. This function calls on the news api to be able to display the data onto the html news document.
    - diary function:
        This function requires user to be logged in first. This function gets user input. Verifies if the input is correct or in correct format. This function also allows user to store images into the database as a jpg. Once verified, input is stored in the database and the page redirects to the history page (history table).
    - view_image function:
        This function requires user to be logged in first and requires image_id as an agrument. This function is to allows user to be able to view the image that is stored in the database.
    - history function:
        This function requires user to be logged in first. This function calls information from the database and stores it in a variable which can be used in html to display a table.
    - graph function:
        This function requires user to be logged in first. This funcation calls information from the database and stores it in account_bal variable. This variable is then used to be able to store the x-axis and y-axis variable to be used to display a line graph in the html document.
    - username function:
        This function requires user to be logged in first. This function gets user input,  verifies if it is correct, correct format or matches the imformation stored in the database. Once verified, the database will be updated with the information retrieved from the user. Once the update is done, an email will be sent to confirm update. Then the user will be redirected to the news page.
    - password function:
        This function requires user to be logged in first. This function gets user input,  verifies if it is correct, correct format or matches the imformation stored in the database. Once verified, the database will be updated with the information retrieved from the user. Once the update is done, an email will be sent to confirm update. Then the user will be redirected to the news page.


  **layout.html**

    This html documents is used to maintain the same layout through the website to reduce redundancy throughout all the other html documents.
    The <meta> tag allows the web application to be compactable for mobile view.
    Bootstrap was linked as I will use bootstrap elements throughout the web application.
    I linked Chart.js as I will be using the chart element in my web application.
    I linked the icon image for the web application, with reference link of where I found the image. The image is stored in the static folder.
    The css style sheet is linked for the style design of the web application.
    The remix icon library is linked, it is used for the Trade Diary logo.
    I linked the googlefonts api to give the bold Poppin font throughout my web application.
    I used jinja syntax so that the title of the web page can be updated thoughout the other html documents.
    The <style> tag was place specifically to ensure all the web pages in the web application will have this background image and settings.
    Used the jinja syntax to set up the nav-bar in a way where some nav-items were visable if not logged in (such as the logo, LOGIN, and REGISTER) and some nav-items were visable if logged in (such as NEWS, DIARY, HISTORY, ACCOUNTS, and LOG OUT).
    The flash alerts were set up to be updated and appear throughout the website if an error is made.
    Used jinja to have a blockmain section which allows (outside of the abovementioned page set up) the other html documents to have specific page details/set up.







