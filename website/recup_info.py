"""Handles loading data from a JSON file.

This script contains a function 'donnees' to read data from a specified JSON file path
and return it as a Python dictionary. It manages file-related exceptions such as file not
found or JSON decoding errors, displaying error messages when necessary.

Functions:
    donnees: Loads data from a JSON file and returns its content as a dictionary.

Dependencies:
    json: Module for JSON data encoding and decoding.
"""

import json

def donnees(nom_fichier = "data/data.json"):
    """Loads data from a JSON file.

    Attempts to open and read the specified JSON file and returns its contents as a Python dictionary.

    Args:
        nom_fichier (str, optional): The path to the JSON file. Defaults to "data/data.json".

    Returns:
        dict or None: A dictionary containing the data from the JSON file, or None if an error occurs.
    
    Raises:
        FileNotFoundError: If the specified file is not found.
        json.JSONDecodeError: If there's an error decoding the JSON data.
    """
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
