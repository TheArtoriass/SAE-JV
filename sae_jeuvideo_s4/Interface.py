from Joueur import Joueur, Joueur1, Joueur2, Joueur3, Joueur4, Joueur5
import tkinter.simpledialog,sys,os,pygame
from PIL import Image, ImageTk
import numpy as np

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                               Systèmes de gestion des interfaces qui n'ont pas de lien trés rapproché avec les autres fichiers
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
fenetre = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))

# Obtenir le répertoire du script actuel
repertoire_script = os.path.dirname(__file__)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def choisir_skin():
    """
    Affiche une interface pour choisir un skin de personnage.

    Returns:
        Le chemin vers le fichier image du skin choisi.
    """
    try:
        # Créer une nouvelle fenêtre tkinter
        fenetre_skin = tkinter.Tk()
        fenetre_skin.title("Choix du skin")

        # Charger les images des skins
        skins = []
        # Obtenir le chemin du répertoire contenant les skins
        repertoire_skins = os.path.join(repertoire_script, 'img', 'personne')
        # Obtenir la liste des fichiers dans le répertoire des skins
        fichiers = [f for f in os.listdir(repertoire_skins) if os.path.isfile(os.path.join(repertoire_skins, f)) and f.startswith('Joueur') and f.endswith('.jpeg')]

        # Pour chaque fichier dans le répertoire des skins
        for fichier in fichiers:
            # Obtenir le chemin complet du fichier
            chemin_image = os.path.join(repertoire_skins, fichier)
            image = Image.open(chemin_image)
            image = image.resize((100, 100), Image.ANTIALIAS)  # Redimensionner l'image
            # Convertir l'image en format PhotoImage de tkinter
            photo = ImageTk.PhotoImage(image)
            # Ajouter l'image et le nom du fichier à la liste des skins
            skins.append((photo, fichier))

        # Variable pour stocker le choix de l'utilisateur
        choix_skin = tkinter.StringVar()

        # Créer un bouton pour chaque skin
        for skin, fichier in skins:
            # Créer un bouton radio avec l'image du skin
            bouton = tkinter.Radiobutton(fenetre_skin, image=skin, variable=choix_skin, value=fichier.replace('.jpeg', ''), indicatoron=0)
            # Ajouter le bouton à la fenêtre
            bouton.pack(side=tkinter.LEFT)

        # Créer un bouton pour valider le choix
        bouton_valider = tkinter.Button(fenetre_skin, text="Valider", command=fenetre_skin.quit)
        bouton_valider.pack(side=tkinter.BOTTOM)

        # Lancer la boucle principale de la fenêtre tkinter
        fenetre_skin.mainloop()
        
        # Fermer la fenêtre tkinter
        try:
            fenetre_skin.destroy() or fenetre_skin.quit()
        except tkinter.TclError:
            pass 

        # Récupérer le choix de l'utilisateur
        skin_choisi = choix_skin.get()
        
        # Si l'utilisateur n'a pas choisi de skin, renvoyer None
        if not skin_choisi:
            return None
        
        # Renvoyer le chemin complet du skin choisi
        return os.path.join(repertoire_script, 'img', 'personne', f'{skin_choisi}.jpeg')
    
    except Exception as e:
        print(f"Une erreur est survenue lors du choix du skin : {e}")
        raise
    
def afficher_resultat_de(resultat_de):
    """
    Affiche le résultat d'un lancer de dé dans la fenêtre Pygame.

    Args:
        resultat_de (int): Le résultat du lancer de dé.
    """
    try:
        # Obtenir les dimensions de l'écran
        infoEcran = pygame.display.Info()
        LARGEUR_ECRAN, HAUTEUR_ECRAN = infoEcran.current_w, infoEcran.current_h
        taille_fenetre = (LARGEUR_ECRAN, HAUTEUR_ECRAN)
        # Créer une fenêtre en plein écran
        fenetre_evenement = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)

        # Définition de la police de caractères pour le texte
        chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
        font = pygame.font.Font(chemin_police, 120)
        NOIR = (0, 0, 0)
        texte = font.render(f"{resultat_de}", True, NOIR)

        # Charger l'image de fond
        image_fondflou = os.path.join(repertoire_script, 'img','fondjeu',  'fondjeu_complet.jpg')
        background_image = pygame.image.load(image_fondflou)
        background_image = pygame.transform.scale(background_image, (LARGEUR_ECRAN, HAUTEUR_ECRAN))


        # Charger l'image du dé
        image_fond_de = os.path.join(repertoire_script, 'img','interface', 'interface_de.jpeg')
        dice_image = pygame.image.load(image_fond_de).convert_alpha()
        dice_image = pygame.transform.scale(dice_image, (dice_image.get_width() * 1.5, dice_image.get_height() * 1.5))

        # Position de départ de l'image de fond
        x_background = 0

        # Vitesse de défilement
        background_speed = 1

        temps_affichage = 0     # Initialiser le temps d'affichage à 0

        while temps_affichage < 3000:   # Boucler pendant 3 seconde
            # Déplacer l'image de fond
            x_background -= background_speed

            # Si l'image est complètement défilée hors de l'écran, réinitialiser sa position
            if x_background <= -taille_fenetre[0]:
                x_background = 0

            # Dessiner l'image de fond avec répétition
            fenetre_evenement.blit(background_image, (x_background, 0))
            fenetre_evenement.blit(background_image, (x_background + taille_fenetre[0], 0))

            # Dessiner l'image du dé
            fenetre_evenement.blit(dice_image, (fenetre_evenement.get_width() // 2 - dice_image.get_width() // 2, fenetre_evenement.get_height() // 2 - dice_image.get_height() // 2))
            
            # Centrer le texte sur l'écran
            texte_rect = texte.get_rect(center=(fenetre_evenement.get_width() // 2, fenetre_evenement.get_height() // 2 + 150))
            fenetre_evenement.blit(texte, texte_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            temps_affichage += 10   # Ajouter 10 millisecondes au temps d'affichage à chaque boucle
    except Exception as e:
        print(f"Une erreur est survenue lors de l'affichage du résultat du dé : {e}")
        raise

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                
def choisir_classe():
    """
    Affiche les statistiques des classes de personnages ( stats_perso ) et demande à l'utilisateur de choisir une classe.

    Returns:
        La classe de personnage choisie par l'utilisateur.
    """
    try:
        Force = '           force: 4, vie: 12, agilite: 3'
        Vie = '              force: 3, vie: 15, agilite: 2'
        Polyvalent = '  force: 6 , vie: 8 , agilite: 6'
        Agilité = '         force: 3, vie: 12, agilite: 4'
        
        classe = tkinter.simpledialog.askinteger("Choix de classe", "Choisissez la classe de votre personnage \n \n 1 - Force:" + Force + "\n 2 - Vie:  " + Vie + "\n 3 - Polyvalent: " + Polyvalent + "\n 4 - Agilité: " + Agilité + "\n 5 - Personnalisable: comme vous voulez ! \n ", minvalue=1, maxvalue=5)    
        
        if classe == 1:
            return Joueur1
        elif classe == 2:
            return Joueur2
        elif classe == 3:
            return Joueur3
        elif classe == 4:
            return Joueur4
        elif classe == 5:
            
            total_points = 19
            points_restants = total_points
            
            force = tkinter.simpledialog.askinteger("Force", f"Entrez le nombre de points de force (1 à {points_restants - 2}):", minvalue=1, maxvalue=points_restants - 2)
            points_restants -= force

            vie = tkinter.simpledialog.askinteger("Vie", f"Entrez le nombre de points de vie (1 à {points_restants - 1}):", minvalue=1, maxvalue=points_restants - 1)
            points_restants -= vie

            agilite = points_restants  
                
            return lambda x, y, taille_case,pseudo,skin_path: Joueur5(force, vie, agilite, x, y, taille_case,pseudo,skin_path)
            
        else:
            return pygame.quit() ,sys.exit()   
    except Exception as e:
        print(f"Une erreur est survenue lors du choix de la classe : {e}")
        raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
def choisir_personnages():
    """
    Demande à l'utilisateur de choisir le nombre de joueur , pour aprés choisir sa classe.

    Returns:
        Une liste de la classe Joueur correspondant aux personnages choisis.
    """
    try:
        # Charger l'image de fond
        image_fond = pygame.image.load(os.path.join(repertoire_script, 'img','fondjeu',  'fondjeu_complet.jpg'))

        # Redimensionner l'image de fond pour qu'elle corresponde à la taille de la fenêtre
        image_fond = pygame.transform.scale(image_fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

        # Afficher l'image de fond
        fenetre.blit(image_fond, (0, 0))
        pygame.display.flip()
        
        nombre_joueurs = tkinter.simpledialog.askinteger("Nombre de joueurs", "Entrez le nombre de joueurs (entre 1 et 4):", minvalue=1, maxvalue=4)
       
        
        if nombre_joueurs is None:              # Si l'utilisateur a appuyé sur "Cancel"
            return  pygame.quit() ,sys.exit()   # Quitter le jeu
        joueurs = []
        
        for i in range(nombre_joueurs):
            pseudo = tkinter.simpledialog.askstring("Pseudo", f"Entrez le pseudo du joueur {i+1} (15 caractères max,facultatif):")
            while pseudo is not None and len(pseudo) > 15:
                pseudo = tkinter.simpledialog.askstring("Pseudo", f"Le pseudo est trop long. Entrez le pseudo du joueur {i+1} (15 caractères max):")
            print(pseudo)
            classe = choisir_classe()
            skin = choisir_skin()
            
            if classe is not None and skin is not None:
                x_depart = 10
                y_depart = 0
                joueur = classe(x_depart, y_depart, taille_case,pseudo, skin)
                joueurs.append(joueur)
            else:
                return pygame.quit() ,sys.exit()

        return joueurs
    except Exception as e:
        print(f"Une erreur est survenue lors du choix des personnages : {e}")
        raise
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def message_interface(joueur_index,de_restant,joueur_actif,joueurs):
    """
    Affiche l'interface de jeu avec les informations du joueur actuel et le nombre de déplacements restants.

    Args:
        joueur_index (int): L'index du joueur actuel.
        de_restant (int): Le nombre de déplacements restants pour le joueur actuel.
    """
    try:
        blanc_cassé = (223, 242, 255)
        Noir = (0, 0, 0)
        # Définir la couleur
        couleur_bleu_clair = (162, 200, 252)
        # Obtenir l'état des touches
        touches = pygame.key.get_pressed()
        
        # Charger l'image du parchemin
        image_parchemin = pygame.image.load(os.path.join(repertoire_script, 'img','fondjeu', 'nom.png'))
        image_parchemin = pygame.transform.scale(image_parchemin, (image_parchemin.get_width() * 1.1, image_parchemin.get_height() * 1.1))
        image_parchemin_rect = image_parchemin.get_rect(center=(largeur_plateau * taille_case // 2 - 580, 70))

        # Afficher l'image du parchemin
        fenetre.blit(image_parchemin, image_parchemin_rect)

        # Afficher le joueur actuel en haut de la fenêtre
        chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
        font = pygame.font.Font(chemin_police, 25)
        message_joueur = font.render(f"Joueur {joueur_index+1} joue", True, Noir)
        message_joueur_rect = message_joueur.get_rect(center=(largeur_plateau * taille_case // 2- 550, 80))
        
        fenetre.blit(message_joueur, message_joueur_rect)
        
        font_emplacement = pygame.font.Font(chemin_police, 20)
        # Afficher le nombre de de_restant au-dessus des flèches
        de_restant_surface = font.render(str(de_restant), True, blanc_cassé)
        de_restant_rect = de_restant_surface.get_rect(center=(largeur_plateau * taille_case // 2 - 580, 150))
        fenetre.blit(de_restant_surface, de_restant_rect)
        
        # Afficher le texte "Emplacements restants" au-dessus du nombre de de_restant
        emplacement_restant_surface = font_emplacement.render("Emplacements restants", True, blanc_cassé)
        emplacement_restant_rect = emplacement_restant_surface.get_rect(center=(largeur_plateau * taille_case // 2 - 580, 120))
        fenetre.blit(emplacement_restant_surface, emplacement_restant_rect)
        
        # Charger l'image de la touche ECHAP
        image_esc = pygame.image.load(os.path.join(repertoire_script, 'img', 'fondjeu', 'esc.png'))
        if touches[pygame.K_ESCAPE]:
            arr = pygame.surfarray.pixels3d(image_esc)
            arr[..., :] = arr.mean(axis=-1, keepdims=1)
        image_esc = pygame.transform.scale(image_esc, (80, 80))  
        image_esc_rect = image_esc.get_rect(center=(largeur_plateau * taille_case - 10, 40))  # Positionner l'image en haut à droite
        fenetre.blit(image_esc, image_esc_rect)

        # Afficher un message "Appuyez sur ESPACE pour lancer le dé" juste au-dessus du texte "Joueur n joue"
        chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
        font = pygame.font.Font(chemin_police, 13)
        message = font.render("Appuyez sur ESPACE pour lancer le dé", True, blanc_cassé)
        message_rect = message.get_rect(center=(largeur_plateau * taille_case - 140, 155))
        fenetre.blit(message, message_rect)
        

        # Charger l'image de la touche ESPACE
        image_espace = pygame.image.load(os.path.join(repertoire_script, 'img', 'fondjeu', 'espace.png'))
        if touches[pygame.K_SPACE]:
            arr = pygame.surfarray.pixels3d(image_espace)
            arr[..., :] = arr.mean(axis=-1, keepdims=1)
        image_espace = pygame.transform.scale(image_espace, (150, 80))  
        image_espace_rect = image_espace.get_rect(center=(largeur_plateau * taille_case - 140, 200))  # Positionner l'image en dessous du texte
        fenetre.blit(image_espace, image_espace_rect)
        
        # Charger l'image du skin du joueur actuel
        skin_path = joueur_actif.get_skin_path()
        if skin_path:  
            joueur_skin = pygame.image.load(skin_path)
            joueur_skin = pygame.transform.scale(joueur_skin, (45, 45))  
            joueur_skin_rect = joueur_skin.get_rect(center=(largeur_plateau * taille_case // 2 - 712, 65))
            fenetre.blit(joueur_skin, joueur_skin_rect)

        image_cadre_stats = pygame.image.load(os.path.join(repertoire_script, 'img','fondjeu', 'cadre_stats.png'))
        image_cadre_stats = pygame.transform.scale(image_cadre_stats, (image_cadre_stats.get_width() * 1, image_cadre_stats.get_height() * 1))
        image_cadre_stats_rect = image_cadre_stats.get_rect(center=(largeur_plateau * taille_case // 2 - 580, 400))
        fenetre.blit(image_cadre_stats, image_cadre_stats_rect)
            
        # Parcourir la liste des joueurs et afficher le pseudo et les statistiques de chaque joueur
        fontstats = pygame.font.Font(chemin_police, 15)
        couleurs = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]  # Rouge, Bleu, Vert, Jaune
        couleur_noir = (0, 0, 0)
        
        for i, joueur in enumerate(joueurs):
            couleur = couleurs[i % len(couleurs)]  # Utiliser l'indice du joueur pour sélectionner la couleur
            message_pseudo = fontstats.render(f"Joueur {i+1} : {joueur.pseudo}", True, couleur)                    
            message_pseudo_rect = message_pseudo.get_rect(center=(largeur_plateau * taille_case // 2 - 580, 260 + i*85))  # Positionner chaque message en dessous du précédent
            fenetre.blit(message_pseudo, message_pseudo_rect)

            message_stats = fontstats.render(f"Force: {joueur.force} | Vie: {joueur.vie} | Agilité: {joueur.agilite}", True, couleur_noir)
            message_stats_rect = message_stats.get_rect(center=(largeur_plateau * taille_case // 2 - 580, 290 + i*85))  # Positionner chaque message en dessous du précédent
            fenetre.blit(message_stats, message_stats_rect)
            
            # Afficher les objets du joueur s'il est vivant
            if joueur.vie > 0:
                for j, objet in enumerate(joueur.objets):
                    image_objet = pygame.image.load(os.path.join(repertoire_script, 'img', 'objet', f'{objet.nom}.jpeg'))
                    image_objet = pygame.transform.scale(image_objet, (30, 30))  # Redimensionner l'image à 30x30 pixels
                    image_objet_rect = image_objet.get_rect(center=(largeur_plateau * taille_case // 2 - 580 + j*35, 320 + i*85))  # Positionner chaque image à côté de la précédente
                    fenetre.blit(image_objet, image_objet_rect)  
                    
        couleur_blanc = (255, 255, 255)
        
        fonttime = pygame.font.Font(chemin_police, 30)
        
        # Afficher le temps de jeu depuis le lancement du jeu
        temps_de_jeu = pygame.time.get_ticks() // 1000  # Convertir le temps en secondes
        heures = temps_de_jeu // 3600
        minutes = (temps_de_jeu % 3600) // 60
        secondes = temps_de_jeu % 60
        message_temps = fonttime.render(f"{heures}h {minutes}m {secondes}s", True, couleur_blanc)
        message_temps_rect = message_temps.get_rect(center=(largeur_plateau * taille_case // 2 - 580, 830))  # Positionner le message à côté de l'image de l'horloge
        fenetre.blit(message_temps, message_temps_rect)
        
        # Obtenir l'état des touches
        touches = pygame.key.get_pressed()
                     
        # Afficher l'image de la flèche gauche
        image_gauche = pygame.image.load(os.path.join(repertoire_script, 'img', 'fondjeu', 'gauche.png'))
        if touches[pygame.K_LEFT]:
            arr = pygame.surfarray.pixels3d(image_gauche)
            arr[..., :] = arr.mean(axis=-1, keepdims=1) 
        image_gauche = pygame.transform.scale(image_gauche, (60, 60))  
        image_gauche_rect = image_gauche.get_rect(center=(largeur_plateau * taille_case - 200, hauteur_plateau * taille_case - 80))  # Positionner l'image en bas à droite
        fenetre.blit(image_gauche, image_gauche_rect)

        # Afficher l'image de la flèche droite
        image_droite = pygame.image.load(os.path.join(repertoire_script, 'img', 'fondjeu', 'droite.png'))
        if touches[pygame.K_RIGHT]:
            arr = pygame.surfarray.pixels3d(image_droite)
            arr[..., :] = arr.mean(axis=-1, keepdims=1)
        image_droite = pygame.transform.scale(image_droite, (60, 60))  
        image_droite_rect = image_droite.get_rect(center=(largeur_plateau * taille_case - 80, hauteur_plateau * taille_case - 80))
        fenetre.blit(image_droite, image_droite_rect)

        # Afficher l'image de la flèche haut
        image_haut = pygame.image.load(os.path.join(repertoire_script, 'img', 'fondjeu', 'haut.png'))
        if touches[pygame.K_UP]:
            arr = pygame.surfarray.pixels3d(image_haut)
            arr[..., :] = arr.mean(axis=-1, keepdims=1)
        image_haut = pygame.transform.scale(image_haut, (60, 60))  
        image_haut_rect = image_haut.get_rect(center=(largeur_plateau * taille_case - 140, hauteur_plateau * taille_case - 130))
        fenetre.blit(image_haut, image_haut_rect)

        # Afficher l'image de la flèche bas
        image_bas = pygame.image.load(os.path.join(repertoire_script, 'img', 'fondjeu', 'bas.png'))
        if touches[pygame.K_DOWN]:
            arr = pygame.surfarray.pixels3d(image_bas)
            arr[..., :] = arr.mean(axis=-1, keepdims=1)
        image_bas = pygame.transform.scale(image_bas, (60, 60))  
        image_bas_rect = image_bas.get_rect(center=(largeur_plateau * taille_case - 140, hauteur_plateau * taille_case - 77))
        fenetre.blit(image_bas, image_bas_rect)

        # Afficher un message "Déplacez-vous avec les flèches directionnelles" juste au-dessus du texte "Joueur n joue"
        chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
        font = pygame.font.Font(chemin_police, 10)
        message = font.render("Déplacez-vous avec les flèches directionnelles", True, couleur_bleu_clair)
        message_rect = message.get_rect(center=(largeur_plateau * taille_case - 140, hauteur_plateau * taille_case - 30))
        fenetre.blit(message, message_rect)

        pygame.display.flip()
    except Exception as e:
        print(f"Une erreur est survenue lors de l'affichage de l'interface : {e}")
        raise

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def end_game(joueur_index):
    """
    Affiche un message de fin de jeu indiquant le joueur gagnant avec une image de trophé.

    Args:
        joueur_index (int): L'index du joueur gagnant.
    """
    try: 
        chemin_police = os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf')
        font = pygame.font.Font(chemin_police, 36)
        Jaune = (255, 255, 0)
        message = font.render(f"Le joueur {joueur_index+1} a gagné !", True, Jaune)
        message_rect = message.get_rect(center=(largeur_plateau * taille_case // 2, hauteur_plateau * taille_case // 2))
        
        # Chargement de l'image
        chemin_image = os.path.join(repertoire_script, 'img','interface',  'trophe.png')
        image = pygame.image.load(chemin_image)
        image_rect = image.get_rect()
        
        # Positionnement de l'image
        image_rect.move_ip((largeur_plateau * taille_case // 2 - image_rect.width // 2, message_rect.top - image_rect.height + 60 ))
        
        fenetre.fill((255, 255, 255))
        fenetre.blit(image, image_rect)
        fenetre.blit(message, message_rect)
        
        pygame.display.flip()
        pygame.time.wait(5000) # Pause de 5 secondes pour voir le message
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Une erreur est survenue lors de l'affichage du message de fin de jeu : {e}")
        raise
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def pause(fenetre, paused=False):
    """
    Met le jeu en pause et affiche un écran avec deux boutons "Reprendre" et "Quitter".
    Args:
        fenetre: la fenêtre Pygame sur laquelle afficher l'écran de pause
        paused: un booléen indiquant si le jeu est déjà en pause ou non
    """
    try:
        # On crée un écran sombre pour mettre le jeu en pause
        ecran_pause = pygame.Surface(fenetre.get_size())
        ecran_pause.set_alpha(128)  # 128 est la transparence de l'écran de pause
        ecran_pause.fill((0, 0, 0)) # On remplit l'écran de pause avec du noir
        fenetre.blit(ecran_pause, (0, 0))

        # On crée les boutons "Reprendre" et "Quitter"
        font = pygame.font.Font(os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf'), 36)
       
        
        blanc = (255, 255, 255)
        texte_reprendre = font.render("Reprendre", True, blanc)
        texte_quitter = font.render("Quitter", True, blanc)
        rect_reprendre = texte_reprendre.get_rect(center=fenetre.get_rect().center)
        rect_quitter = texte_quitter.get_rect(center=(fenetre.get_rect().centerx, fenetre.get_rect().centery + 50))

        # On affiche les boutons sur l'écran de pause
        fenetre.blit(texte_reprendre, rect_reprendre)
        fenetre.blit(texte_quitter, rect_quitter)

        # On affiche le nom du jeu en haut de la fenêtre
        rouge =  (255, 0, 0)
        font = pygame.font.Font(os.path.join(repertoire_script, 'minecraftia', 'Minecraftia-Regular.ttf'), 50)
        
        nom_jeu = font.render("The Last Path", True, rouge)
        rect_nom_jeu = nom_jeu.get_rect(center=(fenetre.get_rect().centerx, fenetre.get_rect().centery - 100))
        fenetre.blit(nom_jeu, rect_nom_jeu)

        pygame.display.flip()

        # On attend que l'utilisateur clique sur un bouton ou appuie sur la touche "Escape"
        while True:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE and not paused:
                    paused = True
                elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE and paused:
                    pass
                elif evenement.type == pygame.MOUSEBUTTONDOWN:
                    if rect_reprendre.collidepoint(evenement.pos):
                        return True
                    elif rect_quitter.collidepoint(evenement.pos):
                        pygame.quit()
                        sys.exit()                                                                          
    except Exception as e:
        print(f"Une erreur est survenue lors de la mise en pause du jeu : {e}")
        raise
