import pygame
from bullet import Bullet

for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            bullet = Bullet(player)
            all_sprites.add(bullet)
