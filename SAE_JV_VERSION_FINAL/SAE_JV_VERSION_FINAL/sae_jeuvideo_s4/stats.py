from tkinter import ttk  # Importation du module ttk
import tkinter as tk
import psycopg2


def execute_query(query):
    try:
        connection = psycopg2.connect(
            user="lucas",
            password="1362",
            host="localhost",
            port="5432",
            database="saejeuvideo"
        )

        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        return records
    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de l'exécution de la requête SQL:", error)
        return None


# Création de la fenêtre principale
root = tk.Tk()
root.title("Affichage des statistiques")
root.attributes('-fullscreen', True)  # Met la fenêtre en plein écran
root.configure(padx=50, pady=50)  # Ajout de la marge intérieure

# Liste des requêtes avec leurs titres
queries = [
    ("Nombre de fois qu'un joueur est mort",
     "SELECT pseudo_joueur_tue, COUNT(pseudo_joueur_tue) AS nb_kills FROM Kill GROUP BY pseudo_joueur_tue ORDER BY nb_kills DESC;",
     ["Joueur ou ennemi", "Nombre de morts"]),
    ("Nombre de fois qu'un joueur a tué",
     "SELECT pseudo_joueur_tueur, COUNT(pseudo_joueur_tueur) AS nb_kills FROM Kill GROUP BY pseudo_joueur_tueur ORDER BY nb_kills DESC;",
     ["Joueur ou ennemi", "Nombre de kills"]),
    ("Nombre total de kills", "SELECT COUNT(*) AS nb_kills FROM Kill;",
     ["Nombre de kills"]),
    ("Nombre total de parties jouées", "SELECT COUNT(*) AS nb_parties FROM Parties;",
     ["Nombre de parties"]),
    ("Nombre total de joueurs",
     "SELECT COUNT(*) AS nb_joueurs FROM Joueurs;",
     ["Nombre de joueurs"]),

    ("Liste des joueurs",
     "SELECT pseudo FROM Joueurs;",
     ["Pseudo"]),

    ("Moyenne de kills par partie",
     "SELECT COUNT(*) / (SELECT COUNT(*) FROM Parties) AS moyenne_kills_par_partie FROM Kill;",
     ["Moyenne de kills"]),
    ("Moyenne d'événements ramassés par partie",
     "SELECT SUM(nb_events_ramasses) / (SELECT COUNT(*) FROM Parties) AS moyenne_events_ramasses_par_partie FROM Parties;",
     ["Moyenne d'événements ramassés"]),
    ("Moyenne de kills par joueur",
     "SELECT ROUND(AVG(kills), 1) AS moyenne_kills_par_joueur FROM (SELECT COUNT(*) as kills FROM Kill GROUP BY pseudo_joueur_tueur) AS subquery;",
     ["Moyenne de kills"]),
    ("Pire ennemi de chaque joueur",
     """
     SELECT pseudo_joueur_tue, pseudo_joueur_tueur, COUNT(*) AS total_kills
     FROM Kill
     WHERE pseudo_joueur_tue NOT IN ('Gorille Mutant', 'Rat infecté', 'Loup infecté', 'Infecté', 'Expérience ratée')
     GROUP BY pseudo_joueur_tue, pseudo_joueur_tueur
     ORDER BY total_kills DESC;
     """,
     ["Joueur", "Ennemi", "Nombre de kills"]),
    ("Meilleure cible de chaque joueur",
     """
     SELECT pseudo_joueur_tueur, pseudo_joueur_tue, COUNT(*) AS total_kills
     FROM Kill
     WHERE pseudo_joueur_tueur NOT IN ('Gorille Mutant', 'Rat infecté', 'Loup infecté', 'Infecté', 'Expérience ratée')
     GROUP BY pseudo_joueur_tueur, pseudo_joueur_tue
     ORDER BY total_kills DESC;
     """,
     ["Joueur", "Ennemi", "Nombre de kills"]),
]

# Création d'un canvas et d'une barre de défilement
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Ajout du canvas et de la barre de défilement à la fenêtre
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Création d'un frame dans le canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Affichage des résultats des requêtes
for title, query, column_titles in queries:
    records = execute_query(query)
    if records is not None:
        label_title = tk.Label(frame, text=title, anchor="w",
                               justify="left", font=("Helvetica", 16))
        label_title.pack(fill=tk.X, pady=50)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", '10', 'bold'))

        # Création du tableau
        tree = ttk.Treeview(frame, height=min(
            len(records), 10), show="headings", style="Treeview")
        # Configuration des colonnes en fonction du nombre de titres
        tree["columns"] = tuple(range(len(column_titles)))

        # Configuration des colonnes
        for i in range(len(column_titles)):
            tree.column(i, width=100, anchor="w")

        # Configuration des en-têtes
        for i, column_title in enumerate(column_titles):
            tree.heading(i, text=column_title, anchor="w")

        # Ajout des lignes
        for record in records:
            tree.insert("", "end", values=record)

        tree.pack(fill=tk.X)
    else:
        label = tk.Label(
            frame, text=f"Erreur lors de l'exécution de la requête {title}.", anchor="w", justify="left")
        label.pack(fill=tk.X)

# Mise à jour du scrollregion du canvas après avoir ajouté les widgets
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Lancement de la boucle principale
root.mainloop()
