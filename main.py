from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

no_spec_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

@app.route('/', methods=['GET', 'POST'])
def signup_form():
    #Initial Rendering Return (Method = GET)
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':

        #Set Variables
        username = request.form['username_name']
        password = request.form['password_name']
        v_password = request.form['v-password_name']
        email = request.form['email_name']

        username_error = ''
        password_error = ''
        v_password_error = ''
        email_error = ''

        email_at_counter = 0
        email_dot_counter = 0

        #Error Messages and Conditions
        if username:
            for char in username:
                if char not in no_spec_char:
                    username_error = "Not Valid: Use Only Alphabet and Numbers."
            if len(username) < 3 or len(username) > 20:
                username_error = "Username must be between 3-20 characters."
        else:
            username_error = "Username field is Blank."

        if not password:
            password_error = "Password field is Blank."
            password = ""
            v_password = ""
        
        if len(password) > 16:
            password_error = "Not Valid: Password between the length of 1-16."
            password = ""
            v_password = ""

        if " " in password:
            password_error = "Not Valid: Do not use space in Password."
            password = ""
            v_password = ""
        
        if v_password != password:
            v_password_error = "The Passwords do not match."
            password = ""
            v_password = ""

        if " " in v_password:
            v_password_error = "Not Valid: Do not use space in Password."
            password = ""
            v_password = ""

        if email:
            for char in email:
                if char == "@":
                    email_at_counter += 1
                if char == ".":
                    email_dot_counter += 1
                if email_dot_counter == 1 and email_at_counter == 0:
                    email_error = "Enter a Valid E-mail."
            if len(email) < 3 or len(email) > 20:
                email_error = "Not Valid: E-mail length must be shorter than 20 characters long."
            if email_at_counter > 1 or email_dot_counter > 1 or " " in email:
                email_error = "Enter a Valid E-mail."

        #Successful Entry with No Error    
        if not username_error and not password_error and not v_password_error and not email_error:
            return redirect('/welcome?username={0}'.format(username))

        
        #Error Entry Return (Method = Post) : Conditional @ Line 14
        return render_template('signup.html',
            username_value=username,
            password_value=password,
            v_password_value=v_password,
            email_value=email,
            username_error=username_error,
            password_error=password_error,
            v_password_error=v_password_error,
            email_error=email_error
            )

#Welcome Page
@app.route('/welcome', methods=['POST', 'GET'])
def  welcome():
    username = request.args.get("username")
    return render_template('welcome.html', username=username)


app.run()