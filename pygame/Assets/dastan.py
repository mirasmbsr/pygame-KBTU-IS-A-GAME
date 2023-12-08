import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Window settings
width, height = 1300, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Life Adventure Game")
sprite_folder = os.path.join('pygame', 'Assets', 'aset', 'sprites')

# Load player images for movement
player_frames = [pygame.image.load(os.path.join(sprite_folder, f'{i}.png')) for i in range(2, 4)]
player_index = 0

# Load images for details
detail_images = {
    "HEALTH": pygame.transform.scale(pygame.image.load(os.path.join(sprite_folder, 'money.png')), (70, 70)),
    "MOOD": pygame.transform.scale(pygame.image.load(os.path.join(sprite_folder, 'coffee.png')), (70, 70)),
    "NEGATIVE": pygame.transform.scale(pygame.image.load(os.path.join(sprite_folder, 'vape.png')), (70, 70)),
    "LIGHT_BLUE": pygame.transform.scale(pygame.image.load(os.path.join(sprite_folder, 'books.png')), (70, 70)),
    "PINK": pygame.transform.scale(pygame.image.load(os.path.join(sprite_folder, 'dumbell.png')), (70, 70)),
}

# Player settings
player_size = 100
player_x = 100
player_y = height - player_size - 90
jump_count = 10
is_jumping = False

# Details for collection
details = []
detail_speed = 8

# Health and score
health = 100
score = 0
font = pygame.font.Font(None, 36)
mood = 100

# Spawn zone for details
spawn_zone = pygame.Rect(0, 0, width, height - player_size)

# Background settings
bg_img = pygame.image.load("pygame/Assets/aset/bg/1.png").convert()
bg = pygame.transform.scale(bg_img, (width, height))
bg_x = 0
bg_speed = 6

# Green door settings
door_width = 100
door_height = 250

door_x = width - door_width - 20
door_y = height - door_height - 10
door_color=GREEN
# Main game loop
clock = pygame.time.Clock()
running = True

def draw_player(x, y):
    global player_index
    screen.blit(player_frames[player_index], (x, y))
    player_index = (player_index + 1) % len(player_frames)

def draw_details(details_list):
    for detail in details_list:
        screen.blit(detail["image"], detail["rect"])


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
    if keys[pygame.K_LEFT] and player_x - detail_speed > 0:
        player_x -= detail_speed
    if keys[pygame.K_RIGHT] and player_x + player_size + detail_speed < width:
        player_x += detail_speed
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

    # Background scrolling
    bg_x -= bg_speed
    if bg_x < -width:
        bg_x = 0

    # Draw background
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + width, 0))

    # Check collision with the door
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    door_rect = pygame.Rect(door_x, door_y, door_width, door_height)

    if player_rect.colliderect(door_rect):
        # Change background image when the player collides with the door
        player_x=0
        bg_img = pygame.image.load("/Users/akbotasmail/Desktop/pygame/bg.png")
        bg = pygame.transform.scale(bg_img, (width, height))

    # Add details in the spawn zone
    if random.randint(0, 100) < 20:
        horizontal_gap = 200
        detail_x = width + horizontal_gap
        if details:
            last_detail = details[-1]
            detail_x = last_detail["rect"].x + last_detail["rect"].w + horizontal_gap
        max_jump_height = player_y - (jump_count ** 2) * 2.0
        detail_y = random.randint(int(max_jump_height), height - player_size)
        health_effect = random.uniform(-10, 10)
        mood_effect = random.uniform(-10, 10)
        color = "HEALTH" if health_effect > 0 else "MOOD" if mood_effect > 0 else "NEGATIVE"
        details.append({"rect": pygame.Rect(detail_x, detail_y, 50, 50),
                        "health_effect": health_effect,
                        "mood_effect": mood_effect,
                        "image": detail_images[color]})

    for _ in range(5):
        if random.randint(0, 100) < 10:
            horizontal_gap = 200
            detail_x = width + horizontal_gap
            if details:
                last_detail = details[-1]
                detail_x = last_detail["rect"].x + last_detail["rect"].w + horizontal_gap
            max_jump_height = player_y - (jump_count ** 2) * 2.0
            detail_y = random.randint(int(max_jump_height), height - player_size)
            health_effect = random.uniform(5, 10) if random.choice([True, False]) else random.uniform(-10, -5)
            mood_effect = random.uniform(5, 10) if random.choice([True, False]) else random.uniform(-10, -5)
            color = "LIGHT_BLUE" if health_effect > 0 else "PINK" if mood_effect > 0 else "NEGATIVE"
            details.append({"rect": pygame.Rect(detail_x, detail_y, 50, 50),
                            "health_effect": health_effect,
                            "mood_effect": mood_effect,
                            "image": detail_images[color]})

    for detail in details:
        detail["rect"].x -= detail_speed

    for detail in details:
        if detail["rect"].colliderect(pygame.Rect(player_x, player_y, player_size, player_size)):
            details.remove(detail)
            score += 1
            health = min(100, health + detail["health_effect"])
            mood = min(100, mood + detail["mood_effect"])
        elif detail["rect"].x < 0:
            details.remove(detail)
            mood = max(0, mood - 0.5)

    health = max(0, health - 0.1)
    mood = max(0, mood - 0.1)

    if health <= 0:
        print("Game Over!")
        running = False

    # Draw player
    draw_player(player_x, player_y)

    # Draw details
    draw_details(details)

    # Draw health bar
    draw_health_bar()

    # Draw mood bar
    draw_mood_bar(mood)

    # Show score
    show_score()

    pygame.draw.rect(screen,GREEN, (door_x, door_y, door_width, door_height))

    # Display updates
    pygame.display.flip()

    # Control frame rate
    clock.tick(10)

pygame.quit()
sys.exit()