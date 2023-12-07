import pygame 
import os

WIDTH, HEIGHT = (900, 600)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("First one!")

BLUE = (25, 35, 255)

FPS = 60
SPC_WIDTH, SPC_HEIGHT = 55, 40

YELLOW_SPACESHIP = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png')) 
YELLOW_SPC = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP, (SPC_WIDTH, SPC_HEIGHT)), 90).

RED_SPACESHIP = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))   
RED_SPC = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP, (SPC_WIDTH, SPC_HEIGHT)), 270)


def draw_window():
    WIN.fill(BLUE)
    WIN.blit(YELLOW_SPC, (200,100))
    WIN.blit(RED_SPC, (700,100))

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()