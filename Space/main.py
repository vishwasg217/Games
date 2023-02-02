
import pygame
import os

pygame.init()

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE BATTLE")

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/blast1.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/gun1.wav')

pygame.mixer.music.load("Assets/background_music.mp3")
pygame.mixer.music.play(-1)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SKY_BLUE = (132, 156, 252)

FPS = 60
MOVE = 3
BULLETS_VEL = 8
MAX_BULLETS = 5

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

SP_WIDTH = 40
SP_HEIGHT = 40

TITLE = pygame.image.load(os.path.join('Assets', 'title.png'))
WELCOME = pygame.image.load(os.path.join("Assets", 'welcome.png'))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space4.png')), (WIDTH, HEIGHT))
YSP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SP_WIDTH, SP_HEIGHT)), 270)
RSP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SP_WIDTH, SP_HEIGHT)), 90)

HEALTH_FONT = pygame.font.Font("Assets/pix_font.ttf", 35)
WIN_FONT = pygame.font.Font("Assets/pix_font.ttf", 80)


def draw_win_text(text, color):
    draw = WIN_FONT.render(text, True, color)
    WIN.blit(draw, (WIDTH/2 - draw.get_width()/2, HEIGHT/2 - draw.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def title():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    run = 200
    clock = pygame.time.Clock()
    while run > 0:
        clock.tick(FPS)
        WIN.blit(SPACE, (0, 0))
        WIN.blit(WELCOME, (WIDTH/2-WELCOME.get_width()/2, HEIGHT/2-WELCOME.get_height()/2))
        pygame.display.update()
        run -= 1

    run = 350

    while run > 0:
        clock.tick(FPS)
        WIN.blit(SPACE, (0, 0))
        WIN.blit(TITLE, (WIDTH / 2 - TITLE.get_width() / 2, HEIGHT / 2 - TITLE.get_height() / 2))
        pygame.display.update()
        run -= 1


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):

    WIN.blit(SPACE, (0, 0))
    red_health_text = HEALTH_FONT.render("Health: "+str(red_health), True, RED)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), True, YELLOW)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (WIDTH-yellow_health_text.get_width()-10, 10))
    WIN.blit(YSP, (yellow.x, yellow.y))
    WIN.blit(RSP, (red.x, red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_move(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - MOVE > BORDER.x + BORDER.width:
        yellow.x -= MOVE
    elif keys_pressed[pygame.K_RIGHT] and yellow.x + yellow.width + MOVE < WIDTH:
        yellow.x += MOVE
    elif keys_pressed[pygame.K_DOWN] and yellow.y + yellow.height + MOVE < HEIGHT:
        yellow.y += MOVE
    elif keys_pressed[pygame.K_UP] and yellow.y - MOVE > 0:
        yellow.y -= MOVE


def red_move(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - MOVE > 0:  # left
        red.x -= MOVE
    elif keys_pressed[pygame.K_d] and red.x + red.width + MOVE < BORDER.x:
        red.x += MOVE
    elif keys_pressed[pygame.K_s] and red.y + red.height + MOVE < HEIGHT:
        red.y += MOVE
    elif keys_pressed[pygame.K_w] and red.y - MOVE > 0:
        red.y -= MOVE


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x -= BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)


title()


def main():
    red = pygame.Rect(100, 300, SP_WIDTH, SP_HEIGHT)
    yellow = pygame.Rect(700, 300, SP_WIDTH, SP_HEIGHT)

    red_health = 10
    yellow_health = 10

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(red_bullets) < MAX_BULLETS:

                    bullet = pygame.Rect(red.x+red.width, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(yellow_bullets) < MAX_BULLETS:

                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                BULLET_HIT_SOUND.play()
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
            draw_win_text(winner_text, YELLOW)
            break

        if yellow_health <= 0:
            winner_text = "Red Wins"
            draw_win_text(winner_text, RED)
            break

        keys_pressed = pygame.key.get_pressed()
        red_move(keys_pressed, red)
        yellow_move(keys_pressed, yellow)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()


if __name__ == "__main__":
    main()
