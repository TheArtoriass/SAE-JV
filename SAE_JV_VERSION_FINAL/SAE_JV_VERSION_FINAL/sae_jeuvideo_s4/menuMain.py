import pygame
import os
import subprocess
import webbrowser

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                       MENU DU JEU 
#   DELRUE ANTOINE
#   TD2 TPC
#   2023-2024
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Initialiser pygame
pygame.init()
pygame.mixer.init()

# Charger la musique
pygame.mixer.music.load("musique_jeu.mp3")
# Mettre la musique en boucle
pygame.mixer.music.play(-1)

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

# Obtenir les dimensions de l'écran
infoEcran = pygame.display.Info()
LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h

# Constantes
COULEUR_FOND = (0, 0, 0)  # Fond noir
COULEUR_BOUTON = (128, 128, 128)  # Couleur de fond des boutons gris
COULEUR_TEXTE = (255, 255, 255)  # Couleur du texte blanc
TAILLE_POLICE = 36

# Chemin de la police Minecraftia
chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')

# Créer la fenêtre en plein écran
ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Menu du jeu")

# Charger la nouvelle image de fond
image_fond = pygame.image.load(os.path.join(repertoire_script, 'img','fondjeu',  'fondjeu_complet.jpg'))
image_fond = pygame.transform.scale(image_fond, (pygame.display.Info().current_w, pygame.display.Info().current_h))

# Fonction pour dessiner du texte centré
def dessiner_texte(texte, x, y, couleur):
    police = pygame.font.Font(chemin_police, TAILLE_POLICE)  # Utiliser la police Minecraftia
    surface_texte = police.render(texte, True, couleur)
    rect_texte = surface_texte.get_rect()
    rect_texte.center = (x, y)
    ecran.blit(surface_texte, rect_texte)

# Position de départ de l'image de fond
x_fond = 0

# Vitesse de défilement
vitesse_fond = 3

# Boutons
boutons = [
    ("Jouer", pygame.Rect(0, 0, 0, 0)), 
    ("WIKI", pygame.Rect(0, 0, 0, 0)),
    ("Stats", pygame.Rect(0, 0, 0, 0)),
    ("Quitter", pygame.Rect(0, 0, 0, 0))
]

# Largeur maximale des boutons
largeur_max = max(pygame.font.Font(chemin_police, TAILLE_POLICE).size(bouton[0])[0] for bouton in boutons)
largeur_max += 100
# Hauteur totale des boutons
hauteur_totale = len(boutons) * 70 - 10  # 70 pixels de hauteur par bouton, espacement de 10 pixels

# Position de départ pour centrer les boutons verticalement
y_depart = (HAUTEUR_ECRAN - hauteur_totale) // 2

# Calculer les positions x et y des boutons pour les centrer
x_centre = LARGEUR_ECRAN // 2
for i, bouton in enumerate(boutons):
    rect_bouton = pygame.Rect(x_centre - largeur_max // 2, y_depart + i * 70, largeur_max, 60)
    bouton = (bouton[0], rect_bouton)
    boutons[i] = bouton

# Boucle principale du menu
en_menu = True
while en_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_menu = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for bouton in boutons:
                if bouton[1].collidepoint(x, y):
                    if bouton[0] == "Jouer":
                        # Action lorsque le bouton "Jouer" est cliqué
                        pygame.mixer.music.stop()
                        subprocess.call(["python", "Main.py"])
                        
                        pygame.mixer.init()
                        pygame.mixer.music.load("musique_jeu.mp3")
                        pygame.mixer.music.play(-1)
                        
                    elif bouton[0] == "WIKI":
                        # Action lorsque le bouton "WIKI" est cliqué
                        webbrowser.open("WIKI_DELRUEANTOINE.html")  
                    elif bouton[0] == "Stats":
                        # Action lorsque le bouton "Stats" est cliqué
                        subprocess.call(["python", "stats.py"])
                        
                    elif bouton[0] == "Quitter":
                        en_menu = False

    # Déplacer l'image de fond
    x_fond -= vitesse_fond

    # Si l'image est complètement défilée hors de l'écran, réinitialiser sa position
    if x_fond <= -LARGEUR_ECRAN:
        x_fond = 0

    # Dessiner l'image de fond avec répétition
    ecran.fill(COULEUR_FOND)
    ecran.blit(image_fond, (x_fond, 0))
    ecran.blit(image_fond, (x_fond + LARGEUR_ECRAN, 0))

    # Dessiner le texte "Nom du jeu" en rouge
    rouge = (255, 0, 0)
    jaune = (255, 255, 0)
    dessiner_texte("The Last Path", LARGEUR_ECRAN // 2, 120, jaune)  # Centré en haut

    
    # Dessiner les boutons
    for bouton in boutons:
        pygame.draw.rect(ecran, COULEUR_BOUTON, bouton[1])
        dessiner_texte(bouton[0], bouton[1].centerx, bouton[1].centery, COULEUR_TEXTE)

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()