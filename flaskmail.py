from flask import Flask
from flask_mail import Mail
from flask_mail import Message
import website.recup_info as rc 

code_secret = rc.donnees()
app = Flask(__name__)
print(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'skycord.code@gmail.com'
app.config['MAIL_PASSWORD'] = "ovzw edjh klmk bhkg"
mail = Mail(app)

@app.route("/")
def index():

    # confirmation_token = user.token
    msg = Message('Confirmation de compte', sender='skycord.code@gmail.com', recipients=['lucas.dreano@gmail.com'])
    msg.body = "Pour confirmer votre compte, veuillez cliquer sur le lien suivant: http://127.0.0.1:5000/confirm_account/TipFFN9FPA_FQitaCIAyAmSvhiWj950kkroECA6S"
    print(msg.body)
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)