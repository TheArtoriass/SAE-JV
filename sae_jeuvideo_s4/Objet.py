import pygame,os,random

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       CLASSE OBJET  
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Obtenir le répertoire du script actuel
pygame.init()

# Obtenir les dimensions de l'écran
infoEcran = pygame.display.Info()
LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h


repertoire_script = os.path.dirname(__file__)
taille_case = min(LARGEUR_ECRAN // 20, HAUTEUR_ECRAN // 20)

# Définir le chemin
chemin = [(10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15),
(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15),
(19, 14), (19, 13), (19, 12), (19, 11),
(18, 11), (17, 11), (16, 11),
(16, 10), (16, 9), (16, 8), (16, 7), (16, 6), (16, 5), (16, 4), (16, 3),
(17, 3), (18, 3), (19, 3), (20, 3), (21, 3), (22, 3), (23, 3), (24, 3),
(24, 4), (24, 5), (24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18)]


# chemin1 = [(10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10, 10)]
           
# chemin2=[(10, 11), (10, 12), (10, 13), (10, 14), (10, 15),(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), 
# (18, 15), (19, 15),(19, 14), (19, 13), (19, 12), (19, 11),(18, 11), (17, 11), (16, 11),(16, 10), (16, 9), (16, 8), (16, 7)]

# chemin3=[(16, 6), (16, 5), (16, 4), (16, 3),(17, 3), (18, 3), (19, 3), (20, 3), (21, 3), (22, 3), (23, 3), (24, 3),(24, 4), (24, 5)]

# chemin4=[(24, 6), (24, 7), (24, 8), (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18)]

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Objet:
    """
    Classe représentant un objet sur le plateau.
    """
    def __init__(self, nom, type_objet, bonus, x, y, image_path,taille_case):
        """
        Initialise un nouvel objet.

        Args:
            nom (str): Le nom de l'objet.
            type_objet (str): Le type de l'objet ('soins', 'arme' ou 'armure').
            bonus (int): Le bonus que l'objet confère au joueur.
            x (int): La position x de l'objet sur le plateau.
            y (int): La position y de l'objet sur le plateau.
            image_path (str): Le chemin d'accès à l'image de l'objet.
            taille_case (int): La taille d'une case sur le plateau.
        """
        self.nom = nom
        self.type_objet = type_objet
        self.bonus = bonus
        self.x = x
        self.y = y
        self.image_path = image_path
        self.image = pygame.image.load(image_path)  # Charger l'image du joueur
        self.image = pygame.transform.scale(self.image, (taille_case, taille_case))  
        self.taille_case = taille_case
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def dessiner(self, surface, taille_case):
        """
        Dessine l'objet sur la surface donnée.

        Args:
            surface (pygame.Surface): La surface sur laquelle dessiner l'objet.
            taille_case (int): La taille d'une case sur le plateau.
        """
        try:
            image = pygame.image.load(self.image_path)
            image = pygame.transform.scale(image, (taille_case, taille_case))
            surface.blit(image, (self.x * taille_case, self.y * taille_case))
        except Exception as e:
            print(f"Une erreur est survenue lors du dessin de l'objet : {e}")
            
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                               Création d'une liste d'objets 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Création d'une liste d'objets avec des chemins d'accès aux images relatives

liste_objets = [
    Objet("bandage", "soins", 2, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'bandage.jpeg'), taille_case),
    Objet("trousse de soin", "soins", 4, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'kit.jpeg'), taille_case),
    Objet("pistolet", "arme", 6, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'pistolet.jpeg'), taille_case),
    Objet("gants de boxe", "arme", 2, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'gantsboxe.jpeg'), taille_case),
    Objet("médicaments", "soins", 3, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'medoc.jpeg'), taille_case),
    Objet("pelle", "arme", 3, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'pelle.jpeg'), taille_case),
    Objet("masque à gaz", "armure", 2, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'smoke.jpeg'), taille_case),
    Objet("casque", "armure", 5, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'casque.jpeg'), taille_case),
    Objet("grolles renforcées", "armure", 3, *random.choice(chemin), os.path.join(repertoire_script, 'img', 'objet', 'grolle.jpeg'), taille_case),
]
