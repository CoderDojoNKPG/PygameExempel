import pygame
import os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plattformskollision")
clock = pygame.time.Clock()

# Sökvägen till det här scriptet.
script_dir = os.path.dirname(os.path.abspath(__file__))
# Ladda spelarens sprite
player_image = pygame.image.load(os.path.join(script_dir, "img", "coderowl.png"))
player_image = pygame.transform.scale(player_image, (50, 50))  # Skala till 50x50 pixlar

# Färger
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
DARK_BLUE = (30, 100, 200) # Outline för spelaren
GREEN = (50, 200, 50)
DARK_GREEN = (30, 120, 30) # Outline för plattformar

# Spelarinställningar
player_rect = pygame.Rect(100, 300, 50, 50)
player_speed = 5
jump_height = -15
gravity = 0.8
vel_y = 0

# Plattformar (trappa)
platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(300, 450, 200, 50),
    pygame.Rect(500, 350, 200, 150)
]

moving_left = False
moving_right = False
is_grounded = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Vi kollar om en knapp tryckts ner
        if event.type == pygame.KEYDOWN:
            # Beroende på riktningen sätter en rörelse till sant
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_UP and is_grounded:
                vel_y = jump_height

        # Vi kollar om någon knapp som var nedtryckt nu har släppts
        if event.type == pygame.KEYUP:
            # Och stänger då av rörelsen i dess riktning
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    # --- RÖRELSE OCH KOLLISION I X-LED ---
    if moving_left:
        player_rect.x -= player_speed
    if moving_right:
        player_rect.x += player_speed

    # Stoppa spelaren vid fönstrets vänster/höger-kant
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > WIDTH:
        player_rect.right = WIDTH

    # Kolla plattformskollision i sidled (X) (Om spelaren kolliderar med någon av rektanglarna i listan)
    for platform in platforms:
        if player_rect.colliderect(platform):
            if moving_right:
                player_rect.right = platform.left
            if moving_left:
                player_rect.left = platform.right

    # --- RÖRELSE OCH KOLLISION I Y-LED ---s
    vel_y += gravity
    player_rect.y += vel_y
    is_grounded = False

    # Kolla plattformskollision i höjdled (Y)
    for platform in platforms:
        if player_rect.colliderect(platform):
            if vel_y > 0:
                player_rect.bottom = platform.top
                vel_y = 0
                is_grounded = True
            elif vel_y < 0:
                player_rect.top = platform.bottom
                vel_y = 0

    # --- RITA ---
    screen.fill(WHITE)
    
    # Rita plattformar med outline
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)           # Fyllning
        pygame.draw.rect(screen, DARK_GREEN, platform, 3)   # Kanter (3 pixlar tjock)
    
    # Rita spelaren sprite
    screen.blit(player_image, player_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()