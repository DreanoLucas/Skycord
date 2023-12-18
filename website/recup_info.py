import json

def donnees(nom_fichier = "data/data.json"):
    try:
        with open(nom_fichier, 'r') as fichier :
            donnees = json.load(fichier)
            return donnees
    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
        return None
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")
        return None

if __name__ =="__main__" :
    print(donnees())
