import pygame
import random


class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("runner_graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("runner_graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load("runner_graphics/Player/jump.png").convert_alpha()
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('runner_audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= 2:
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()


class Obstacle(pygame.sprite.Sprite):
    speed: int

    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.transform.rotozoom(pygame.image.load("runner_graphics/Fly/Fly1.png"), 0, 0.5)
            fly_2 = pygame.transform.rotozoom(pygame.image.load("runner_graphics/Fly/Fly2.png"), 0, 0.5)
            self.frames = [fly_1, fly_2]
            self.y_pos = 200
            self.speed = 7
        else:
            snail_1 = pygame.image.load("runner_graphics/snail/snail1.png")
            snail_2 = pygame.image.load("runner_graphics/snail/snail2.png")
            self.frames = [snail_1, snail_2]
            self.y_pos = 300
            self.speed = 5

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), self.y_pos))

    def obstacle_animation(self):
        self.index += 0.1
        if self.index >= 2:
            self.index = 0
        self.image = self.frames[int(self.index)]



    def update(self):
        self.obstacle_animation()
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    s = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = score_font.render("SCORE: " + str(s), False, "Black").convert()
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return s


def collision_sprite():
    if pygame.sprite.spritecollide(player1.sprite, obstacle_group, True):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
bg_Music = pygame.mixer.Sound('runner_audio/music.wav')
bg_Music.play(loops=-1)
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("RUNNER")
clock = pygame.time.Clock()
score_font = pygame.font.Font("Pixeltype.ttf", 40)
GAME_STATE = False
start_time = 0
score = 0
ground = pygame.image.load("runner_graphics/ground.png").convert()
sky = pygame.image.load("runner_graphics/sky.png").convert()


player1 = pygame.sprite.GroupSingle()
player1.add(Player())
obstacle_group = pygame.sprite.Group()


player_stand = pygame.transform.rotozoom(pygame.image.load("runner_graphics/Player/player_stand.png"), 0, 1.5)
player_stand_rect = player_stand.get_rect(center=(400, 200))
title_font = pygame.font.Font("Pixeltype.ttf", 65)
title = title_font.render("PIXEL RUNNER", False, "Black").convert()
title_rect = title.get_rect(center=(400, 100))
message_font = pygame.font.Font("Pixeltype.ttf", 40)
message = message_font.render("Press space to play", False, "Black").convert()
message_rect = message.get_rect(center=(400, 350))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()

        if GAME_STATE:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("hello")
                    GAME_STATE = True
                    start_time = pygame.time.get_ticks()

    if GAME_STATE:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))

        player1.draw(screen)
        player1.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        GAME_STATE = collision_sprite()

        score = display_score()

    else:
        screen.fill((50, 150, 150))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title, title_rect)
        if score == 0:
            screen.blit(message, message_rect)
        else:
            final_score = score_font.render("Final Score: " + str(score), False, "Black")
            final_score_rect = final_score.get_rect(center=(400, 350))
            screen.blit(final_score, final_score_rect)

    pygame.display.update()
    clock.tick(60)
