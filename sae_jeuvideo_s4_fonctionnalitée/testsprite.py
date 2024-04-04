import pygame
import os

# Initialiser Pygame
pygame.init()

# Définir la taille de la fenêtre
LARGEUR_ECRAN, HAUTEUR_ECRAN = 800, 600
fenetre = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))

# Charger le sprite
chemin_sprite = os.path.join(os.path.dirname(__file__), '2.png')
sprite_sheet = pygame.image.load(chemin_sprite)

# Diviser le sprite en plusieurs frames
largeur_frame, hauteur_frame = 32, 32  # Chaque frame fait 32x32 pixels
nouvelle_largeur, nouvelle_hauteur = 64, 64  # Nouvelles dimensions pour chaque frame
frames = []
for y in range(sprite_sheet.get_height() // hauteur_frame):
    for x in range(sprite_sheet.get_width() // largeur_frame):
        frame = pygame.Surface((largeur_frame, hauteur_frame))
        frame.blit(sprite_sheet, (0, 0), (x * largeur_frame, y * hauteur_frame, largeur_frame, hauteur_frame))
        frame = pygame.transform.scale(frame, (nouvelle_largeur, nouvelle_hauteur))  # Agrandir la frame
        frames.append(frame)

# Obtenir un rectangle de la même taille que le sprite et le centrer
rect = frames[0].get_rect()
rect.center = (LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2)

# Boucle principale
running = True
index_frame = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessiner le sprite
    fenetre.fill((0, 0, 0))  # Remplir l'écran avec du noir
    fenetre.blit(frames[index_frame], rect)
    pygame.display.flip()

    # Passer à la frame suivante
    index_frame = (index_frame + 1) % len(frames)

    # Attendre un peu avant de passer à la frame suivante pour ralentir l'animation
    pygame.time.wait(100)

pygame.quit()