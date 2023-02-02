import os

import pygame

pygame.init()

# music and sounds
pygame.mixer.music.load("Assets/background_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/blast1.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/gun1.wav')


WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE BATTLE")
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# background and intros
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space4.png')), (WIDTH, HEIGHT))
TITLE = pygame.transform.rotozoom(pygame.image.load("Assets/title1.png"), 0, 1.25)
title_rect = TITLE.get_rect(center=(500, 250))
start_time = pygame.time.get_ticks()
intro_font = pygame.font.Font("Assets/pix_font.ttf", 40)
intro_text = intro_font.render("Press space to play", False, "#03989e")
credit_font = pygame.font.Font("Assets/pix_font.ttf", 30)
credit1 = credit_font.render("Created by:", False, "#89beed")
credit2 = credit_font.render("vishwas gowda", False, "#89beed")
credit1_rect = credit1.get_rect(center=(870, 545))
credit2_rect = credit1.get_rect(center=(870, credit1_rect.midbottom[1]+20))
intro_text_rect = intro_text.get_rect(center=(500, 450))


# game state 1:
max_health = 20
red_health = max_health
yellow_health = max_health
winner_text = ""
win_colour = "Black"
win_font = pygame.font.Font("Assets/pix_font.ttf", 150)
max_bullets = 3


message = intro_font.render("Press space to play again", True, "#03989e")

message_rect = message.get_rect(center=(500, 450))

GAME_STATE = 0


# for GAME_STATE: 0 -> intro, 1 -> game, 2 -> winner text

class Red(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("Assets/spaceship_red.png"), 90, 0.1)
        self.rect = self.image.get_rect(center=(250, 300))
        self.move = 3

    def red_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:  # left
            self.rect.x -= self.move
        elif keys[pygame.K_d] and self.rect.right < BORDER.left:
            self.rect.x += self.move
        elif keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.move
        elif keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.move

    def animation(self):
        pass

    def update(self):
        self.red_move()
        self.animation()


class Yellow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("Assets/spaceship_yellow.png"), 270, 0.1)
        self.rect = self.image.get_rect(center=(750, 300))
        self.move = 3

    def yellow_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > BORDER.right:
            self.rect.x -= self.move
        elif keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.move
        elif keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.move
        elif keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.move

    def animation(self):
        pass

    def update(self):
        self.yellow_move()
        self.animation()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, colour):
        super().__init__()
        if colour == "red_bullet":
            self.image = pygame.transform.rotozoom(pygame.image.load("Assets/red_bullet.png"), 180, 0.1)
            self.rect = self.image.get_rect(center=spaceship1.sprite.rect.midright)
            self.speed = 8
            self.max = WIDTH
            self.colour = colour

        if colour == "yellow_bullet":
            self.image = pygame.transform.rotozoom(pygame.image.load("Assets/yellow_bullet.png"), 0, 0.1)
            self.rect = self.image.get_rect(center=spaceship2.sprite.rect.midleft)
            self.speed = -8
            self.max = 0
            self.colour = colour

    def move(self):
        self.rect.x += self.speed
        if self.colour == "red_bullet" and self.rect.x > WIDTH:
            self.kill()
        if self.colour == "yellow_bullet" and self.rect.x < -50:
            self.kill()

    def update(self):
        self.move()


def collision_sprite():
    if pygame.sprite.spritecollide(spaceship1.sprite, bullet_group, True):
        pygame.event.post(pygame.event.Event(RED_HIT))
    if pygame.sprite.spritecollide(spaceship2.sprite, bullet_group, True):
        pygame.event.post(pygame.event.Event(YELLOW_HIT))


def health(red_health, yellow_health):
    red_health_text = intro_font.render("HEALTH: " + str(red_health), False, (255, 0, 0))
    yellow_health_text = intro_font.render("HEALTH: " + str(yellow_health), False, (255, 255, 0))
    screen.blit(red_health_text, (10, 10))
    screen.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))


# events
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

spaceship1 = pygame.sprite.GroupSingle()
spaceship2 = pygame.sprite.GroupSingle()
spaceship1.add(Red())
spaceship2.add(Yellow())

bullet_group = pygame.sprite.Group()
# bullet_group.add(Bullet("red_bullet"))
# bullet_group.add(Bullet("yellow_bullet"))

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if GAME_STATE == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GAME_STATE = 1

        if GAME_STATE == 1:
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_LSHIFT]:
                    bullet_group.add(Bullet("red_bullet"))
                    BULLET_FIRE_SOUND.play()
                    bullet_group.update()

                if keys[pygame.K_RSHIFT]:
                    bullet_group.add(Bullet("yellow_bullet"))
                    BULLET_FIRE_SOUND.play()
                    bullet_group.update()

            if event.type == RED_HIT:
                BULLET_HIT_SOUND.play()
                red_health -= 1

            if event.type == YELLOW_HIT:
                BULLET_HIT_SOUND.play()
                yellow_health -= 1

        if GAME_STATE == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GAME_STATE = 1

    if GAME_STATE == 0:
        screen.blit(SPACE, (0, 0))
        screen.blit(TITLE, title_rect)
        screen.blit(credit1, credit1_rect)
        screen.blit(credit2, credit2_rect)
        screen.blit(intro_text, intro_text_rect)

    elif GAME_STATE == 1:
        screen.blit(SPACE, (0, 0))

        spaceship1.draw(screen)
        spaceship1.update()
        spaceship2.draw(screen)
        spaceship2.update()
        bullet_group.draw(screen)
        bullet_group.update()
        pygame.draw.rect(screen, (0, 0, 0), BORDER)
        health(red_health, yellow_health)
        collision_sprite()

        if red_health <= 0:
            winner_text = "Yellow wins"
            win_colour = "Yellow"
            red_health = max_health
            yellow_health = max_health
            bullet_group.empty()
            GAME_STATE = 2

        if yellow_health <= 0:
            winner_text = "Red wins"
            win_colour = "Red"
            red_health = max_health
            yellow_health = max_health
            bullet_group.empty()
            GAME_STATE = 2

    elif GAME_STATE == 2:
        draw = win_font.render(winner_text, True, win_colour)
        draw_rect = draw.get_rect(center=(500, 250))
        screen.blit(draw, draw_rect)
        screen.blit(message, message_rect)
        pygame.time.delay(500)

    pygame.display.update()
