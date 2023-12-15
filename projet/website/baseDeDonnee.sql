CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    utilisateur_id INT REFERENCES utilisateurs(utilisateur_id),
    conversation_id INT REFERENCES conversations(conversation_id)
);
CREATE TABLE utilisateurs (
    utilisateur_id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL
);

CREATE TABLE groupes (
    groupe_id SERIAL PRIMARY KEY,
    nom_du_groupe VARCHAR(100) NOT NULL
);

CREATE TABLE utilisateurs_groupes (
    utilisateur_id INT REFERENCES utilisateurs(utilisateur_id),
    groupe_id INT REFERENCES groupes(groupe_id),
    PRIMARY KEY (utilisateur_id, groupe_id)
);


CREATE TABLE utilisateurs_conversations (
    utilisateur_id INT REFERENCES utilisateurs(utilisateur_id),
    conversation_id INT REFERENCES conversations(conversation_id),
    PRIMARY KEY (utilisateur_id, conversation_id)
);