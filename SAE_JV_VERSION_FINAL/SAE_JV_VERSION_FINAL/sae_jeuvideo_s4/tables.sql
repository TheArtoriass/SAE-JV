------------------------------------------------------------------------------------------------------
-- BDD pour enregistrer les stats de notre jeux SAE
-- Auteur : Erwan
------------------------------------------------------------------------------------------------------
CREATE DATABASE saejeuvideo;


\c saejeuvideo


CREATE TABLE Joueurs (
  id_joueur SERIAL PRIMARY KEY,
  pseudo VARCHAR(255) NOT NULL,
  CONSTRAINT pseudo_unique UNIQUE (pseudo)
);


CREATE TABLE Parties (
  id_partie SERIAL PRIMARY KEY,
  nb_joueurs INT NOT NULL,
  nb_events_ramasses INT DEFAULT 0
);


CREATE TABLE Jouer (
  id_joueur INT,
  id_partie INT,
  FOREIGN KEY (id_joueur) REFERENCES Joueurs(id_joueur),
  FOREIGN KEY (id_partie) REFERENCES Parties(id_partie)
);


CREATE TABLE Avoir_lieu (
  id_partie INT,
  date_heure TIMESTAMP NOT NULL,
  FOREIGN KEY (id_partie) REFERENCES Parties(id_partie)
);


CREATE TABLE Kill (
  id_kill SERIAL PRIMARY KEY,
  pseudo_joueur_tueur VARCHAR(255),
  pseudo_joueur_tue VARCHAR(255)
);