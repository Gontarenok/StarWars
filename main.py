import pygame
from player import Player
from enemy_left import EnemyLeft
from enemy_right import EnemyRight
from enemy_top import EnemyTop
from enemy_bottom import EnemyBottom
from bullet import Bullet
from explosion import Explosion
from bg import Bg

pygame.init()  # Инициализируем модуль pygame

width = 1366  # ширина игрового окна
height = 768  # высота игрового окна
fps = 30  # частота кадров в секунду
game_name = "Shooter"  # название нашей игры

# Цвета
BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
GREEN = "#008000"
BLUE = "#0000FF"
CYAN = "#00FFFF"

snd_dir = "media/snd/"            # Путь до папки со звуками
img_dir = "media/img/"            # Путь до папки с картинками

icon = pygame.image.load(img_dir + 'icon.png')           # Загружаем файл с иконкой
pygame.display.set_icon(icon)                            # Устанавливаем иконку в окно

pygame.mixer.music.load(snd_dir + "music.mp3")           # Добавляем фоновую музыку
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

all_sprites = pygame.sprite.Group()                      # Создаем группу для спрайтов
mobs_sprites = pygame.sprite.Group()                     # Создаем группу для мобов
bullets_sprites = pygame.sprite.Group()                  # Создаем группу для пуль
players_sprites = pygame.sprite.Group()                  # Создаем группу для игрока

bg = Bg()                                                # Создаем объект класса заднего фона
all_sprites.add(bg)                                      # Добавляем фон во все спрайты самым первым

player = Player()                                        # Создаем объект класса Player
enemy_left = EnemyLeft()
enemy_right = EnemyRight()
enemy_top = EnemyTop()
enemy_bottom = EnemyBottom()

all_sprites.add(player)                                  # Добавляем игрока в группу спрайтов
all_sprites.add(enemy_left)
all_sprites.add(enemy_right)
all_sprites.add(enemy_top)
all_sprites.add(enemy_bottom)                            # Добавляем игрока в группу игрока

players_sprites.add(player)

mobs_sprites.add([enemy_top, enemy_bottom, enemy_right, enemy_left])       # Добавляем мобов в группу мобов


# Создаем игровой экран
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(game_name)  # Заголовок окна

def get_hit_sprite(hits_dict):
   for hit in hits_dict.values():
       return hit[0]

def draw_text(screen, text, size, x, y, color):
    font_name = pygame.font.match_font('arial')  # Выбираем тип шрифта для текста
    font = pygame.font.Font(font_name, size)     # Шрифт выбранного типа и размера
    text_image = font.render(text, True, color)  # Превращаем текст в картинку
    text_rect = text_image.get_rect()            # Задаем рамку картинки с текстом
    text_rect.center = (x, y)                    # Переносим текст в координаты
    screen.blit(text_image, text_rect)           # Рисуем текст на экране

def draw_hp(screen, x, y, hp, hp_width, hp_height):       # Функция для рисования hp
    color = "#32CD32"                                     # Зеленый цвет
    white = "#FFFFFF"                                     # Белый цвет
    rect = pygame.Rect(x, y, hp_width, hp_height)         # Создаем рамку
    fill = (hp / 500) * hp_width                          # Считаем ширину полосы для hp
    fill_rect = pygame.Rect(x, y, fill, hp_height)        # Cоздаем полосу для hp

    pygame.draw.rect(screen, color, fill_rect)            # Рисуем полосу для hp
    pygame.draw.rect(screen, white, rect, 1)              # Рисуем рамку

def new_mobs(count):                                      # Функция для респайна мобов
   for i in range(count):
       el = EnemyLeft()
       er = EnemyRight()
       et = EnemyTop()
       eb = EnemyBottom()
       all_sprites.add([el, er, et, eb])
       mobs_sprites.add([el, er, et, eb])

timer = pygame.time.Clock()  # Создаем таймер pygame

def menu():
    screen.blit(bg.image, bg.rect)                        # Выводим задний фон
    draw_text(screen, game_name, 128, width / 2, height / 4, WHITE)
    draw_text(screen, "Стрелки для движения, пробел - выстрел", 44,
              width / 2, height / 2, WHITE)
    draw_text(screen, "Нажмите любую кнопку для начала игры", 36, width / 2, height * 3 / 4, WHITE)
    pygame.display.flip()                                 # Отображаем содержимое на экране

    run = True

    while run:  # Начинаем бесконечный цикл
        timer.tick(fps)  # Контроль времени (обновление игры)
        for event in pygame.event.get():  # Обработка ввода (события)
            if event.type == pygame.QUIT:  # Проверить закрытие окна
                pygame.quit()
            if event.type == pygame.KEYUP:
                run = False  # Завершаем игровой цикл


level = 1
game_over = True
run = True

while run:  # Начинаем бесконечный цикл
    if game_over:
        level = 1
        player.__init__()                   # Воскрешаем игрока
        for sprite in mobs_sprites:         # Очищаем группу спрайтов
            sprite.kill()
        new_mobs(level)                         # Создаем новых мобов по уровню
        game_over = False
        menu()
    timer.tick(fps)  # Контроль времени (обновление игры)
    all_sprites.update()               # Выполняем действия всех спрайтов в группе
    for event in pygame.event.get():   # Обработка ввода (события)
        if event.type == pygame.QUIT:  # Проверить закрытие окна
            run = False  # Завершаем игровой цикл
        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_SPACE:
                bullet = Bullet(player)
                all_sprites.add(bullet)
                bullets_sprites.add(bullet)
                player.snd_shoot.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet = Bullet(player)
                all_sprites.add(bullet)
                player.snd_shoot.play()

    shots = pygame.sprite.groupcollide(bullets_sprites, mobs_sprites, True, False)
    if shots:
        sprite = get_hit_sprite(shots)
        sprite.hp -= 10
        if sprite.hp <= 0:
            sprite.snd_expl.play()  # Воспроизводим звук взрыва
            expl = Explosion(sprite.rect.center)
            all_sprites.add(expl)
            sprite.kill()           # Уничтожаем моба, когда  у него закончится здоровье


    if len(mobs_sprites) == 0:      # Если мобов в группе не осталось
        level += 1                  # Увеличиваем уровень
        new_mobs(level)             # Создаем новых мобов

    scratch = pygame.sprite.groupcollide(mobs_sprites, players_sprites, False, False)
    if scratch:
        sprite = get_hit_sprite(scratch)         # Получаем спрайт из второй группы
        sprite.snd_scratch.play()                # Воспроизводим звук скрежета
        player.hp -= 1                           # Уменьшаем здоровье игроку при столкновении
        if player.hp <= 0:
            game_over = True                          # Завершаем игру, когда жизни игрока достигнут 0


    # Рендеринг (прорисовка)
    screen.fill(CYAN)          # Заливка заднего фона
    all_sprites.draw(screen)   # Отрисовываем все спрайты
    draw_hp(screen, 50, 50, player.hp, 200, 20)
    #draw_text(screen, "HP: " + str(player.hp), 50, 100, 50, WHITE)
    pygame.display.update()    # Переворачиваем экран

pygame.quit()                  # Корректно завершаем игру