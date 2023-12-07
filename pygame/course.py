import pygame
import sys
import random
import os

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)  # RGB color for orange

# Настройки окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Life Adventure Game")
sprite_folder = os.path.join('pygame', 'Assets', 'aset', 'sprites')
# Загрузка изображений
player_frames = [pygame.image.load(os.path.join(sprite_folder, f'{i}.png')) for i in range(1, 4)]  # Replace "path_to_frame_" with the actual path and prefix of your sprite frames
player_index = 0  # Index to keep track of the current frame
player_image = player_frames[player_index]

# Игрок
player_size = 80
player_x = 50  # Moved the player more to the left
player_y = height - player_size - 100
jump_count = 10
is_jumping = False

# Детали для сбора
details = []
detail_size = 30
detail_speed = 5


details1 = []
detail_size1 = 30
detail_speed1 = 5
# Здоровье и очки
health = 100
score = 0
font = pygame.font.Font(None, 36)
mood = 100  # Initial mood value

# Зона для появления деталей
spawn_zone = pygame.Rect(0, 0, width, height - player_size - 10)

# Основной цикл игры
clock = pygame.time.Clock()
running = True

def draw_player(x, y):
    screen.blit(player_image, (x, y))

def draw_details(details_list):
    for detail in details_list:
        pygame.draw.rect(screen, BLACK, detail)


def draw_details1(details1_list):
    for detail1 in details1_list:
        pygame.draw.rect(screen, GREEN, detail1)

def draw_health_bar():
    health_bar_width = int(200 * (health / 100))
    pygame.draw.rect(screen, GREEN, (width - 220, 20, health_bar_width, 20))

def show_score():
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_mood_bar(mood):
    mood_bar_width = int(200 * (mood / 100))
    pygame.draw.rect(screen, ORANGE, (width - 220, 60, mood_bar_width, 20))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True

    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Добавление деталей в зоне для появления
    if random.randint(0, 100) < 20:
        horizontal_gap = 200
        detail_x = width + horizontal_gap
        if details:
            last_detail = details[-1]
            detail_x = last_detail.x + last_detail.width + horizontal_gap
        max_jump_height = player_y - (jump_count ** 2) * 2.0
        detail_y = random.randint(int(max_jump_height), height - player_size)
        details.append(pygame.Rect(detail_x, detail_y, detail_size, detail_size))

    # Обновление позиции деталей
    for detail in details:
        detail.x -= detail_speed
        if detail.colliderect(pygame.Rect(player_x, player_y, player_size, player_size)):
            details.remove(detail)
            score += 1
            health = min(100, health + 5)
            mood = max(0, mood - 0.5)
        elif detail.x < 0:
            details.remove(detail)

    if random.randint(0, 100) < 20:
        horizontal_gap = 200
        detail_x = width + horizontal_gap
        if details1:
            last_detail1 = details1[-1]
            detail1_x = last_detail1.x + last_detail1.width + horizontal_gap
        max_jump_height = player_y - (jump_count ** 2) * 2.0
        detail1_y = random.randint(int(max_jump_height), height - player_size)
        details1.append(pygame.Rect(detail1_x, detail1_y, detail_size1, detail_size1))

        # Обновление позиции деталей
        for detail1 in details1:
            detail1.x -= detail_speed1
            if detail1.colliderect(pygame.Rect(player_x, player_y, player_size, player_size)):
                details1.remove(detail1)
                score += 1
                health = min(100, health + 5)
                mood = max(0, mood - 0.5)
            elif detail1.x < 0:
                details1.remove(detail1)

    health = max(0, health - 0.1)
    mood = max(0, mood - 0.1)

    if health <= 0:
        print("Game Over!")
        running = False

    # Update player image for animation
    player_index = (player_index + 1) % len(player_frames)
    player_image = player_frames[player_index]


    screen.fill(WHITE)
    draw_player(player_x, player_y)
    draw_details(details)
    draw_details1(details1)
    draw_health_bar()
    draw_mood_bar(mood)
    show_score()

    pygame.display.flip()
    clock.tick(10)  # Adjust the frame rate here

pygame.quit()
sys.exit()

