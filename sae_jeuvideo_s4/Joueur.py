import pygame,os 


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           CLASSE JOUEUR   
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Définir le chemin
chemin = [(10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15),
(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15),
(19, 14), (19, 13), (19, 12), (19, 11),
(18, 11), (17, 11), (16, 11),
(16, 10), (16, 9), (16, 8), (16, 7), (16, 6), (16, 5), (16, 4), (16, 3),
(17, 3), (18, 3), (19, 3), (20, 3), (21, 3), (22, 3), (23, 3), (24, 3),
(24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18)]


# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Joueur:
    """
    Classe représentant un joueur dans le jeu.
    """
    def __init__(self, nom, force, vie, agilite, x_depart, y_depart, image_path,taille_case,pseudo):
        """
        Initialise un joueur avec ses caractéristiques.

        Args:
            nom (str): Le nom du joueur.
            force (int): La force du joueur.
            vie (int): Les points de vie du joueur.
            agilite (int): L'agilité du joueur.
            x_depart (int): La position horizontale de départ du joueur.
            y_depart (int): La position verticale de départ du joueur.
            image_path (str): Le chemin vers l'image représentant le joueur.
            taille_case (int): La taille en pixels d'une case sur le plateau.
        """
        self.nom = nom
        self.force = force
        self.vie = vie
        self.vie_max = vie
        
        self.agilite = agilite
        self.x = x_depart
        self.y = y_depart
        self.image = pygame.image.load(image_path)  # Charger l'image du joueur
        self.image = pygame.transform.scale(self.image, (taille_case, taille_case))  
        self.taille_case = taille_case
        
        self.remaining_moves = 0            # Nombre de déplacements restants
        
        self.direction_precedente = None
        self.position_precedente = None
        self.peut_combattre = True
        self.dernier_ennemi_battu = None    # Coordonnées du dernier ennemi battu 
        
        self.derniers_ennemis_battus = []   # Liste des coordonnées des derniers ennemis battus
        self.objets = []                    # Liste des objets possédés par le joueur
        
        self.force_base = force             
        self.vie_base = vie
        self.pseudo = pseudo
       
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def deplacer(self, direction):
        """
        Déplace le joueur dans une direction donnée.

        Args:
            direction (str): La direction du déplacement ('gauche', 'droite', 'haut', 'bas').
        """
        try:
            # Vérifier si la direction est valide
            if direction not in ['gauche', 'droite', 'haut', 'bas']:
                raise ValueError("La direction doit être 'gauche', 'droite', 'haut' ou 'bas'.")

            # Vérifier si le déplacement est possible sur le chemin
            if direction == 'gauche':
                # Vérifier si la case à gauche du joueur est dans le chemin
                if (self.x - 1, self.y) in chemin:
                    # Déplacer le joueur vers la gauche
                    self.x -= 1
            elif direction == 'droite':
                # Vérifier si la case à droite du joueur est dans le chemin
                if (self.x + 1, self.y) in chemin:
                    # Déplacer le joueur vers la droite
                    self.x += 1
            elif direction == 'haut':
                # Vérifier si la case en haut du joueur est dans le chemin
                if (self.x, self.y - 1) in chemin:
                    # Déplacer le joueur vers le haut
                    self.y -= 1
            elif direction == 'bas':
                # Vérifier si la case en bas du joueur est dans le chemin
                if (self.x, self.y + 1) in chemin:
                    # Déplacer le joueur vers le bas
                    self.y += 1
                    
            # Décrémenter le nombre de déplacements restants  
            self.remaining_moves -= 1
            self.direction_precedente = direction
            self.position_precedente = (self.x, self.y)
        except Exception as e:
            print(f"Une erreur est survenue lors du déplacement du joueur : {e}")
            raise
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
           
    def dessiner(self, surface, taille_case,num_joueur):
        """
        Dessine le joueur sur la surface donnée à sa position actuelle avec son numéro et son dernier objet (s'il en a un).

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner le joueur.
            taille_case (int): La taille d'une case en pixels.
            num_joueur (int): Le numéro du joueur à afficher.
        """
        try:
            # Afficher l'image du joueur à sa position actuelle
            surface.blit(self.image, (self.x * taille_case, self.y * taille_case))
            
            # Définir la police et la couleur du texte
            chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
            if not os.path.exists(chemin_police):
                raise FileNotFoundError(f"Le fichier de police {chemin_police} est introuvable.")
            
            font = pygame.font.Font(chemin_police, 17)
            white = (255, 255, 255)
            
            # Afficher le numéro du joueur au-dessus de son image
            text_surface = font.render(f"J{num_joueur}", True, white)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (self.x * taille_case + taille_case // 2, self.y * taille_case + 10)
            surface.blit(text_surface, text_rect)
            
            # Afficher le dernier objet ajouté au joueur, s'il en a un
            if self.objets:
                objet = self.objets[-1]
                font = pygame.font.Font(chemin_police, 10)
                
                if objet.type_objet == "soins" or objet.type_objet == "armure" :
                    text_surface = font.render(f"+{objet.bonus} vie ({objet.nom})", True, white)
                elif objet.type_objet == "arme":
                    text_surface = font.render(f"+{objet.bonus} force ({objet.nom})", True, white)
                    
                text_rect = text_surface.get_rect()
                text_rect.midtop = (self.x * taille_case + taille_case // 2, self.y * taille_case + 30)
                surface.blit(text_surface, text_rect)
        except Exception as e:
            print(f"Une erreur est survenue lors du dessin du joueur : {e}")
            raise

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def prendre_objet(self, objet):
        """
        Ajoute un objet à l'inventaire du joueur et applique ses effets.

        Args:
            objet (Objet): L'objet à ajouter à l'inventaire du joueur.
        """
        try:
            # Ajouter l'objet à l'inventaire du joueur
            self.objets.append(objet)
            
            # Si l'objet est de type "soins", augmenter la vie du joueur
            if objet.type_objet == 'soins':
                self.vie += objet.bonus
                if self.vie > self.vie_max:
                    self.vie = self.vie_max
                    
            # Si l'objet est de type "armure", augmenter la vie maximale et la vie du joueur
            elif objet.type_objet == 'armure':
                self.vie_max += objet.bonus
                self.vie += objet.bonus
                
            # Si l'objet est de type "arme", augmenter la force du joueur
            elif objet.type_objet == 'arme':
                self.force += objet.bonus
        except Exception as e:
            print(f"Une erreur est survenue lors de la prise de l'objet : {e}")
            raise
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def est_vaincu(self):
        """
        Réinitialise les statistiques du joueur et le replace à sa position précédente s'il est vaincu.
        """
        try:
            self.reset_stats()
            self.x, self.y = self.position_precedente
            if self.vie <= 0:
                self.peut_combattre = False
        except Exception as e:
            print(f"Une erreur est survenue lors de la vérification de la défaite du joueur : {e}")
            raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def ajouter_objet(self, objet):
        """
        Ajoute un objet au joueur.

        Args:
            objet (Objet): L'objet à ajouter.
        """
        try:
            if self.objets:
                self.objets.pop()
            self.objets.append(objet)
        except Exception as e:
            print(f"Une erreur est survenue lors de l'ajout de l'objet au joueur : {e}")
            raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def enlever_tous_objets(self):
        """
        Enlève tous les objets du joueur.
        """
        self.objets = []

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_stats(self):
        """
        Réinitialise les statistiques du joueur à leurs valeurs par défaut.
        """
        self.force = self.force_base
        self.vie_max = self.vie_base
        self.vie = self.vie_max
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                   Création des classes de joueurs 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
class Joueur1(Joueur):
    """
    Classe représentant un joueur de la classe Force.
    """
    def __init__(self, x_depart, y_depart,taille_case,pseudo,skin_path):
        """
        Args:
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Force', 4, 12, 3, x_depart, y_depart, skin_path,taille_case,pseudo)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Joueur2(Joueur):
    """
    Classe représentant un joueur de la classe Vie.
    """
    def __init__(self, x_depart, y_depart,taille_case,pseudo,skin_path):
        """
        Args:
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Vie', 3, 15, 2, x_depart, y_depart, skin_path,taille_case,pseudo)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Joueur3(Joueur):
    """
    Classe représentant un joueur de la classe Polyvalent.
    """
    def __init__(self, x_depart, y_depart,taille_case,pseudo,skin_path):
        """
        Args:
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Polyvalent', 6, 8, 6, x_depart, y_depart,skin_path,taille_case,pseudo)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Joueur4(Joueur):
    """
    Classe représentant un joueur de la classe Agilité.
    """
    def __init__(self, x_depart, y_depart,taille_case,pseudo,skin_path):
        """
        Args:
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Agilité', 3, 12, 4, x_depart, y_depart, skin_path,taille_case,pseudo)
        
class Joueur5(Joueur):
    """
    Classe représentant un joueur avec des points de compétence personnalisables.
    """
    def __init__(self, force, vie, agilite, x_depart, y_depart, taille_case,pseudo,skin_path):
        """
        Args:
            force (int): Les points de force du joueur.
            vie (int): Les points de vie du joueur.
            agilite (int): Les points d'agilité du joueur.
            x_depart (int): La position horizontale de départ du joueur sur le plateau.
            y_depart (int): La position verticale de départ du joueur sur le plateau.
            taille_case (int): La taille d'une case du plateau.
        """
        super().__init__('Personnalisable',force, vie, agilite, x_depart, y_depart, skin_path,taille_case,pseudo)