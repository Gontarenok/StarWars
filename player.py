import pygame
from pygame.math import Vector2

snd_dir = "media/snd/"            # Путь до папки со звуками
img_dir = "media/img/"            # Путь до папки с картинками
width = 1366                      # ширина игрового окна
height = 768                      # высота игрового окна

class Player(pygame.sprite.Sprite):
    def __init__(self):                            #Конструктор, где указываем, что будет у объекта
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + 'player/player.png')
        self.rect = self.image.get_rect()
        # self.rect.x = width/2
        # self.rect.y = height/2
        self.rect.center = [width/2, height/2]

        self.speed = 10
        self.copy = self.image                        # Создаем копию, которую будем вращать
        self.position = Vector2(self.rect.center)     # тартовая позиция вектора
        self.direction = Vector2(0, - 1)              # Задаем направление вверх
        self.angle = 0                                # Начальный угол поворота

        self.snd_expl = pygame.mixer.Sound(snd_dir + "expl.mp3")
        self.snd_expl.set_volume(0.3)
        self.snd_shoot = pygame.mixer.Sound(snd_dir + "shoot.mp3")
        self.snd_shoot.set_volume(0.3)
        self.snd_scratch = pygame.mixer.Sound(snd_dir + "scratch.mp3")
        self.snd_scratch.set_volume(0.3)

        self.hp = 500


    def rotate(self, rotate_speed):
        self.direction.rotate_ip(-rotate_speed)        # Изменяем направление взгляда
        self.angle += rotate_speed                     # Изменяем угол поворота
        self.image = pygame.transform.rotate(self.copy, self.angle)    # Поворот картинки
        self.rect = self.image.get_rect(center=self.rect.center)       # Изменение рамки


    def update(self):
        key = pygame.key.get_pressed()                #Сохраняем нажития на кнопки
        if key[pygame.K_RIGHT]:
            self.rotate(-5)
        if key[pygame.K_LEFT]:
            self.rotate(5)
        if key[pygame.K_UP]:
            self.position += self.speed * self.direction
            self.rect.center = self.position
        if key[pygame.K_DOWN]:
            self.position -= self.speed * self.direction
            self.rect.center = self.position







