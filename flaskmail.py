from flask import Flask
from flask_mail import Mail
from flask_mail import Message
import recup_info as rc 

code_secret = rc.donnees()
app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'skycord.code@gmail.com'
app.config['MAIL_PASSWORD'] = code_secret['cle']
mail = Mail(app)

@app.route("/")
def index():

    msg = Message("Hello",
                  sender="skycord.code@gmail.com",
                  recipients=["chadimangle@pompiersparis.fr"])
    
    msg.body = "samouelle"
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)