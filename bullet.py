import pygame
from pygame.math import Vector2

snd_dir = "media/snd/"            # Путь до папки со звуками
img_dir = "media/img/"            # Путь до папки с картинками
width = 1366                      # ширина игрового окна
height = 768                      # высота игрового окна

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):                            #Конструктор, где указываем, что будет у объекта
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + 'bullet.png')
        self.image = pygame.transform.rotate(self.image, player.angle)   # Поворот пули
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(player.rect.center)                   # Пуля там же где игрок
        self.speed = 30                                                  # Скорость полета пуди
        self.move = self.speed * player.direction                        # Направление движения пули от игрока

    def update(self):
        self.rect.center += self.move
        if self.rect.x > width or self.rect.y > height or self.rect.x < 0 or self.rect.y < 0:
            self.kill()                                                  # При достижении краев экрана уничтожаем пулю


