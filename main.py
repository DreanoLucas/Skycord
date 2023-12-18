
from website import create_app
from flask_mail import Mail
app = create_app()


if (__name__) == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request
# import psycopg2 

# app = Flask(__name__)

# class Student:
#     def __init__(self, _name, _psd):
#         self.login = _name
#         self.mot_de_passe = _psd

# @app.route("/")
# def hello_world():
#     return render_template("page_de_connexion.html")

# @app.route('/acceuil', methods=["POST"])
# def acceuil():
#     conn = psycopg2.connect(database="v0_1", user="postgres", 
#                             password="admin", host="localhost", port="5432") 

#     cur = conn.cursor() 

#     data = request.form
#     _username = data.get('username')
#     _password = data.get('password')
  
#     cur.execute(f"SELECT * FROM utilisateurs")
#     all_users = cur.fetchall()  # Récupérer tous les utilisateurs de la base de données
    
#     for user in all_users:
#         print(user)  # Afficher chaque utilisateur
    
#     cur.execute(f"SELECT * FROM utilisateurs WHERE login = '{_username}'")
#     utilisateur_existant = cur.fetchone()
    
#     if utilisateur_existant and utilisateur_existant[2] == _password:  # Assuming the password is at index 2
#         print("A")
#         return render_template("acceuil.html", prenom=_username)
#     else:
#         print("B")
#         return render_template("acceuil.html", _username=None, _password=None)

# if __name__ == '__main__':
#     app.run(debug=True)


