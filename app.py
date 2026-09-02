from flask import Flask, request, render_template
import validate_login

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/Login', methods=['GET'])
def hello_world():

    Username = request.args.get('Username')
    Password = request.args.get('Password')

    result = validate_login.check_user_existence(Username, Password)

    return result, 200


# Forgot Username
@app.route('/forgot-username', methods=['GET'])
def forgot_username():

    Email = request.args.get('Email')

    if Email:
        result = validate_login.get_username_by_email(Email)

        if result:
            return "Your username is: " + result[0]
        else:
            return "Email not found"

    return render_template('forgotlogin.html')


if __name__ == '__main__':
    app.run(debug=True)