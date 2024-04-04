import psycopg2


def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="lucas",
            password="1362",
            host="localhost",
            port="5432",
            database="saejeuvideo"
        )

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("Vous êtes connecté à - ", record, "\n")

        return connection, cursor

    except (Exception, psycopg2.Error) as error:
        print("Erreur en vous connectant à PostgreSQL", error)


# fais une fonction inserer_nb_joueurs qui insère le nombre de joueurs dans la base de données
def inserer_nb_joueurs(nb_joueurs):
    connection, cursor = connect_to_database()
    try:
        cursor.execute(
            "INSERT INTO parties (nb_joueurs) VALUES (%s) RETURNING id_partie;", (nb_joueurs,))
        id_partie = cursor.fetchone()[0]
        connection.commit()
        print("Nombre de joueurs inséré avec succès avec l'ID de partie:", id_partie)
    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'insertion du nombre de joueurs:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("La connexion est fermée.")

# fais une fonction inserer_nb_events_ramasses qui insère à la fin de la partie le nombre d'êvènements qu'il y a eu dans la partie dans la base de données


def inserer_nb_events_ramasses(nb_events_ramasses):
    connection, cursor = connect_to_database()
    try:
        cursor.execute(
            "INSERT INTO parties (nb_events_ramasses) VALUES (%s) RETURNING id_partie;", (nb_events_ramasses,))
        id_partie = cursor.fetchone()[0]
        connection.commit()
        print("Nombre d'events inséré avec succès avec l'ID de partie:", id_partie)
    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'insertion du nombre d'events:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("La connexion est fermée.")


# les fonctions inserer_nb_joueurs et inserer_nb_events_ramasses insèrent toutes les deux dans la table parties, il faudrait donc les fusionner en une seule fonction qui prend en paramètre le nombre de joueurs et le nombre d'évènements ramassés

def inserer_donnees_partie(nb_joueurs, nb_events_ramasses, id_partie=None):
    connection, cursor = connect_to_database()
    try:
        if id_partie is None:
            # Insertion d'une nouvelle partie
            cursor.execute(
                "INSERT INTO parties (nb_joueurs, nb_events_ramasses) VALUES (%s, %s) RETURNING id_partie;", (nb_joueurs, nb_events_ramasses))
            id_partie = cursor.fetchone()[0]
            print(
                "Données de la partie insérées avec succès avec l'ID de partie:", id_partie)
        else:
            # Mise à jour de la partie existante
            cursor.execute(
                "UPDATE parties SET nb_events_ramasses = %s WHERE id_partie = %s;", (nb_events_ramasses, id_partie))
            print(
                "Données de la partie mises à jour avec succès pour l'ID de partie:", id_partie)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'insertion/mise à jour des données de la partie:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("La connexion est fermée.")
    return id_partie


def inserer_donnees_joueur(pseudo):
    connection, cursor = connect_to_database()
    try:
        cursor.execute("INSERT INTO Joueurs (pseudo) VALUES (%s) RETURNING id_joueur;",
                       (pseudo,))  # Notez la virgule après pseudo
        id_joueur = cursor.fetchone()[0]
        connection.commit()
        print("Données du joueur insérées avec succès avec l'ID de joueur:", id_joueur)
    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'insertion des données du joueur:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("La connexion est fermée.")


# fais la fonction pour inserer les données de kill dans la base de données (pseudo_joueur_tueur et pseudo_joueur_tue)
def inserer_donnees_kill(pseudo_joueur_tueur, pseudo_joueur_tue):
    connection, cursor = connect_to_database()
    try:
        cursor.execute("INSERT INTO Kill (pseudo_joueur_tueur, pseudo_joueur_tue) VALUES (%s, %s) RETURNING id_kill;",
                       (pseudo_joueur_tueur, pseudo_joueur_tue))
        id_kill = cursor.fetchone()[0]
        connection.commit()
        print("Données du kill insérées avec succès avec l'ID de kill:", id_kill)
    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'insertion des données du kill:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("La connexion est fermée.")
