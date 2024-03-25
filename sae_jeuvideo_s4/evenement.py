import random,os,sys,pygame
from Objet import Objet, liste_objets
import time

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                    Systèmes de gestion d'événements
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)


# Définir le chemin
chemin = [(10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15),
(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15),
(19, 14), (19, 13), (19, 12), (19, 11),
(18, 11), (17, 11), (16, 11),
(16, 10), (16, 9), (16, 8), (16, 7), (16, 6), (16, 5), (16, 4), (16, 3),
(17, 3), (18, 3), (19, 3), (20, 3), (21, 3), (22, 3), (23, 3), (24, 3),
(24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18)]

pygame.init()

# Obtenir les dimensions de l'écran
infoEcran = pygame.display.Info()
LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

# Calculer la taille de la case en fonction de la taille de l'écran
taille_case = min(LARGEUR_ECRAN // 20, HAUTEUR_ECRAN // 20)

# Calculer le nombre de cases en largeur et en hauteur
largeur_plateau = LARGEUR_ECRAN // taille_case
hauteur_plateau = HAUTEUR_ECRAN // taille_case

# Créer une fenêtre en plein écran
fenetre = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                              Les événements
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def rencontre_amicale(joueur,ennemis):
    """
    Ajoute un objet aléatoire à la liste d'objets du joueur et affiche un événement de rencontre amicale.

    Args:
        joueur (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.
    """
    try:
        objet = random.choice(liste_objets)
        joueur.objets.append(objet)
        
        evenement = "Rencontre amicale"
        image_path = os.path.join(repertoire_script, 'img', 'evenement', 'rencontre_amicale2.jpeg')
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier image {image_path} n'existe pas.")
        
        
        texte = f"Un ami vous a donné un {objet.nom} !"
        
        afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
        return f"Vous avez rencontré un ami qui vous a donné un {objet.nom} !"
    
    except Exception as e:
        print(f"Une erreur est survenue lors de la rencontre amicale : {e}")
        raise
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def maladie(joueur,ennemis):
    """
    Enlève tous les objets du joueur, il perd et def maladie affiche un événement de maladie.

    Args:
        joueur (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.

    """
    try:
        joueur.enlever_tous_objets()
        joueur.est_vaincu()
        
        derniers_ennemis_battus = joueur.derniers_ennemis_battus
        if derniers_ennemis_battus:
            dernier_ennemi_battu = derniers_ennemis_battus[-1]
            joueur.x, joueur.y = dernier_ennemi_battu
        else:
            joueur.x, joueur.y = (10, 0) 
            
        evenement = "Maladie"
        image_path = os.path.join(repertoire_script, 'img', 'evenement', 'maladie2.jpeg')
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier image {image_path} n'existe pas.")
        
        
        texte = f"Vous avez attrapé une maladie, vous etes mort !"
        afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
        return "Vous avez attrapé une maladie vous etes mort !"
    except Exception as e:
        print(f"Une erreur est survenue lors de la maladie : {e}")
        raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def tresor_enfoui(joueur,ennemis):
    """
    Ajoute un objet "pistolet" à la liste d'objets du joueur et affiche un événement de trésor enfoui.

    Args:
        joueur (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.

    """
    try:
        objet = Objet("pistolet", "arme", 6, joueur.x, joueur.y, os.path.join(repertoire_script, 'img', 'objet', 'pistolet.jpeg'), 39)
        joueur.objets.append(objet)
        
        evenement = "Tresor enfoui"
        image_path = image_path = os.path.join(repertoire_script, 'img', 'evenement', 'tresor_enfoui2.jpeg')
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier image {image_path} n'existe pas.")
        
        texte = f"Vous avez trouvé un pistolet enfoui dans le sol !"
        
        afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
        return "Vous avez trouvé un pistolet enfoui dans le sol !"
    except Exception as e:
        print(f"Une erreur est survenue lors de la découverte du trésor enfoui : {e}")
        raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def vautour(joueur,ennemis):
    """
    Enlève tous les objets du joueur et ses stats pour les remettres à leur valeur depart, def vautour affiche un événement de vautour.

    Args:
        joueur (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.

    """
    try:
        joueur.enlever_tous_objets()
        joueur.est_vaincu()
        
        evenement = "Vautour"
        image_path = image_path = os.path.join(repertoire_script, 'img', 'evenement', 'vautour2.jpeg')
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier image {image_path} n'existe pas.")
        
        texte = f"Un vautour vous a attaqué et vous a volé tous vos objets !"
        
        afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
        return "Un vautour vous a attaqué et vous a volé tous vos objets !"
    
    except Exception as e:
        print(f"Une erreur est survenue lors de la rencontre avec le vautour : {e}")
        raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def raccourci(joueur_actif,ennemis):
    """
    Déplace le joueur sur une case aléatoire du chemin et affiche un événement de raccourci.

    Args:
        joueur_actif (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.
    """
    try:
        positions_interdites = [(16, 18)] + [(ennemi.x, ennemi.y) for ennemi in ennemis]
        nouvelle_position = random.choice([pos for pos in chemin if pos not in positions_interdites])
        joueur_actif.x, joueur_actif.y = nouvelle_position
        
        evenement = "Raccourci"
        image_path = image_path = os.path.join(repertoire_script, 'img', 'evenement', 'raccourci2.jpeg')
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier image {image_path} n'existe pas.")
        
        texte = f"Vous avez pris un autre chemin !"
        
        afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
        return "Vous avez pris un autre chemin !"
    
    except Exception as e:
        print(f"Une erreur est survenue lors de la prise du raccourci : {e}")
        raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def blessure(joueur_actif,ennemis):
    """
    Enlève 4 points de vie au joueur et affiche un événement de blessure.

    Args:
        joueur_actif (Personnage): Le personnage du joueur.
        ennemis (list): Une liste d'ennemis.
    """
    try:
        joueur_actif.vie -= 4
        
        if joueur_actif.vie <= 0:
                joueur_actif.enlever_tous_objets()
                joueur_actif.est_vaincu()
                derniers_ennemis_battus = joueur_actif.derniers_ennemis_battus
                
                if derniers_ennemis_battus:
                    dernier_ennemi_battu = derniers_ennemis_battus[-1]
                    joueur_actif.x, joueur_actif.y = dernier_ennemi_battu
                else:
                    joueur_actif.x, joueur_actif.y = (10,0)
                    
        evenement = "Blessure"
        image_path = image_path = os.path.join(repertoire_script, 'img', 'evenement', 'blessure2.jpeg')
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier image {image_path} n'existe pas.")
        
        texte = f"Vous avez perdu de la vie  !"
        
        afficher_evenement(evenement, image_path, texte , (largeur_plateau * taille_case, hauteur_plateau * taille_case))
        return f"Vous avez perdu 4 points de vie ! Il vous reste {joueur_actif.vie} points de vie."
    except Exception as e:
        print(f"Une erreur est survenue lors de la blessure : {e}")
        raise

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                    La classe CarteAleatoire 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class CarteAleatoire:
    def __init__(self, largeur, hauteur,image_path,taille_case,liste_objets):
        """
        Classe représentant une carte aléatoire pour un jeu.

        args:
            largeur (int): La largeur de la carte en nombre de cases.
            hauteur (int): La hauteur de la carte en nombre de cases.
            image_path (str): Le chemin d'accès à l'image de la carte.
            taille_case (int): La taille en pixels d'une case de la carte.
            liste_objets (list): Une liste d'objets à placer sur la carte.
        """
        
        self.largeur = largeur
        self.hauteur = hauteur
        if os.path.isfile(image_path):
            self.image = pygame.image.load(image_path)  # Charger l'image de l'événement
        else:
            self.image = None
              
        self.taille_case = taille_case
        self.objets = liste_objets  
        self.evenements = {
            "Rencontre amicale": rencontre_amicale,
            "Maladie": maladie, 
            "Trésor enfoui": tresor_enfoui,
            "Vautour": vautour, 
            "Raccourci": raccourci, 
            "Blessure": blessure
        }
        self.joueurs = []   # Ajouter un attribut joueurs pour stocker une liste de joueurs
        self.ennemis = []   # Ajouter une liste pour stocker les ennemis
        self.chemin = chemin
        self.occupe = {}    # Ajouter un dictionnaire pour stocker les événements placés
        self.carte = self.generer_carte()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def generer_carte(self):
        """
        Génère une carte aléatoire en plaçant des événements et des objets sur la carte.

        Returns:
            list: Une liste de tuples représentant les événements et les objets placés sur la carte.
        """
        try: 
            carte = []
            evenements = list(self.evenements.keys())
            random.shuffle(evenements)      # Mélanger la liste des événements
            cases_occupees = [(10, 0), (24, 18)]  # Les coordonnées spécifiques à éviter
                                        
            for evenement in evenements:
                if evenement in self.occupe:    # Utiliser les coordonnées stockées si l'événement a déjà été placé
                    x, y = self.occupe[evenement]
                    image_path = self.get_image_path(evenement)
                    carte.append((x, y, image_path, evenement))
                    
                else:
                    cases_libres = [(x, y) for x, y in self.chemin if (x, y) not in cases_occupees and not any(ennemi.x == x and ennemi.y == y for ennemi in self.ennemis)]
                    if cases_libres:
                        
                        x, y = random.choice(cases_libres)
                        image_path = self.get_image_path(evenement)
                        cases_occupees.append((x, y))   # Ajouter la case occupée à la liste
                        carte.append((x, y, image_path, evenement))
                        self.occupe[evenement] = (x, y)     # Stocker les coordonnées de l'événement
                        
                    else:
                        carte.append((None, None, None, evenement))
            
            # Ajouter les coordonnées des ennemis et des objets à la liste des cases occupées après avoir placé tous les événements
            cases_occupees += [(ennemi.x, ennemi.y) for ennemi in self.ennemis] + \
                            [(objet.x, objet.y) for objet in self.objets]           

            return carte
        except Exception as e:
            print(f"Une erreur est survenue lors de la génération de la carte : {e}")
            raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Rend l'objet CarteAleatoire iterable
    def __iter__(self):
        """
        Renvoie un itérateur sur la carte.

        Returns:
            iter: Un itérateur sur la carte.
        """
        return iter(self.carte)
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #l'image de l'événement correspondant sur le plateau
    def get_image_path(self, evenement):
        """
        Renvoie le chemin d'accès à l'image correspondant à l'événement .

        Args:
            evenement (str): Le nom de l'événement.

        """
        try:
            if evenement == "Rencontre amicale":
                return os.path.join(repertoire_script, 'img', 'evenement', 'rencontre_amicale.jpeg')
            elif evenement == "Maladie":
                return os.path.join(repertoire_script, 'img', 'evenement', 'maladie.jpeg')
            elif evenement == "Trésor enfoui":
                return os.path.join(repertoire_script, 'img', 'evenement', 'tresor_enfoui.jpeg')
            elif evenement == "Vautour":
                return os.path.join(repertoire_script, 'img', 'evenement', 'vautour.jpeg')
            elif evenement == "Raccourci":
                return os.path.join(repertoire_script, 'img', 'evenement', 'raccourci.jpeg')
            elif evenement == "Blessure":
                return os.path.join(repertoire_script, 'img', 'evenement', 'blessure.jpeg')
        except Exception as e:
            print(f"Une erreur est survenue lors de la récupération du chemin de l'image de l'événement : {e}")
            raise

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                   Affichage les événements sur le plateau
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def afficher_evenement(nom, image_path, texte, taille_fenetre):
    """
    Affiche un événement dans une fenêtre.

    Args:
        nom (str): Le nom de l'événement.
        image_path (str): Le chemin d'accès à l'image de l'événement.
        texte (str): Le texte à afficher avec l'événement.
        taille_fenetre (tuple): Un tuple contenant la largeur et la hauteur de la fenêtre.
    """
    try:
        repertoire_script = os.path.dirname(__file__)
        dossier_evenement = os.path.join(repertoire_script, 'img', 'evenement')

        # Obtenir la liste des fichiers dans le dossier
        fichiers = os.listdir(dossier_evenement)

        # Initialiser Pygame
        pygame.init()

        # Obtenir les dimensions de l'écran
        infoEcran = pygame.display.Info()
        LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

        # Créer une fenêtre en plein écran
        fenetre_evenement = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)

        # Charger l'image de fond
        image_fondflou = os.path.join(repertoire_script, 'img','fondjeu',  'fondjeu_complet.jpg')
        background_image = pygame.image.load(image_fondflou)
        background_image = pygame.transform.scale(background_image, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

        # Boucle principale
        start_time = time.time()
        while time.time() - start_time < 1:  # Boucle pendant 1 secondes
            for fichier in fichiers:
                # Construire le chemin complet vers le fichier
                chemin_fichier = os.path.join(dossier_evenement, fichier)

                # Charger l'image avec transparence
                image = pygame.image.load(chemin_fichier).convert_alpha()

                # Obtenir un rectangle de la même taille que l'image et le centrer
                rect = image.get_rect()
                rect.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2)

                # Dessiner l'image de fond
                fenetre_evenement.blit(background_image, (0, 0))

                # Afficher l'image
                fenetre_evenement.blit(image, rect)
                pygame.display.flip()

                # Attendre 0,2 seconde
                pygame.time.wait(200)

        chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
        font = pygame.font.Font(chemin_police, 20)

        # Obtenir les dimensions de l'écran
        infoEcran = pygame.display.Info()
        LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

        # Créer une fenêtre en plein écran
        fenetre_evenement = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)
        pygame.display.set_caption(nom)

        # Charger l'image de fond
        image_fondflou = os.path.join(repertoire_script, 'img','fondjeu',  'fondjeu_complet.jpg')
        background_image = pygame.image.load(image_fondflou)
        background_image = pygame.transform.scale(background_image, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        taille_fenetre = (LARGEUR_ECRAN, HAUTEUR_ECRAN)

        # Position de départ de l'image de fond
        x_background = 0

        # Vitesse de défilement
        background_speed = 3

        temps_affichage = 0     # Initialiser le temps d'affichage à 0

        while temps_affichage < 1500:   # Boucler pendant 1,5 seconde
            # Déplacer l'image de fond
            x_background -= background_speed

            # Si l'image est complètement défilée hors de l'écran, réinitialiser sa position
            if x_background <= -taille_fenetre[0]:
                x_background = 0

            # Dessiner l'image de fond avec répétition
            fenetre_evenement.blit(background_image, (x_background, 0))
            fenetre_evenement.blit(background_image, (x_background + taille_fenetre[0], 0))

            # Dessiner le texte et l'image de l'événement
            image = pygame.image.load(image_path)
            image_rect = image.get_rect()
            image_rect.center = (taille_fenetre[0] // 2, taille_fenetre[1] // 2.7)      # Descendre l'image
            
            texte_surface = font.render(texte, True, (255, 255, 255))
            texte_rect = texte_surface.get_rect()
            texte_rect.center = (taille_fenetre[0] // 2, taille_fenetre[1] // 1.2)      # Descendre le texte
            
            nom_surface = font.render(nom, True, (255, 255, 255))   # Créer une surface de texte pour le nom de l'événement
            nom_rect = nom_surface.get_rect()
            nom_rect.center = (taille_fenetre[0] // 2, taille_fenetre[1] // 1.3)    # Positionner le nom de l'événement
            
            fenetre_evenement.blit(image, image_rect)
            fenetre_evenement.blit(texte_surface, texte_rect)
            fenetre_evenement.blit(nom_surface, nom_rect)   # Mettre le nom de l'événement sur la fenêtre d'affichage

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.time.wait(10)
            temps_affichage += 10  # Ajouter 10 millisecondes au temps d'affichage à chaque boucle
    except Exception as e:
        print(f"Une erreur est survenue lors de l'affichage de l'événement : {e}")
        raise