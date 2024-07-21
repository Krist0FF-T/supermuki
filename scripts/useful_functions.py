from scripts.fonts_and_colors import *
from scripts.button import *
import pygame
import datetime
import os
from math import atan2, sin, cos

pygame.mixer.init()
pygame.display.init()

GRAVITY = 0.6
TRAMPOLINE_VEL = -20
TS = 60
COL = 44
ROW = 12
W, H = (1280, 720)
CX, CY = (W//2, H//2)
FPS = 61
clock = pygame.time.Clock()


def scale_img(img, size):
    return pygame.transform.scale(img, (size, size))


def load_img(file):
    return pygame.image.load(file)


def palette_swap(surf, old_c, new_c):
    img_copy = surf.copy()
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))
    return img_copy


def fade(surface, color=BLACK):
    fade = pygame.Surface((W, H))
    fade.fill(color)
    for alpha in range(63):
        fade.set_alpha(alpha*4)
        surface.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.wait(4)


def long_fade(surface):
    fade = pygame.Surface((W, H))
    fade.fill((0, 0, 0))
    for alpha in range(63):
        fade.set_alpha(alpha*4)
        surface.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.wait(40)


def mts(surface, rect, size, smthing, color, x, y):
    text = font(size).render(smthing, 1, color)
    if rect:
        text_rect = text.get_rect(center=(x, y))
        surface.blit((text), text_rect)
    elif not rect:
        surface.blit(text, (x, y))
    return text


def its(surface, img, scalex, scaley, px, rect, x, y):
    img = pygame.image.load(img)
    if px:
        image = pygame.transform.scale(img, (scalex, scaley))
    elif not px:
        image = pygame.transform.scale(
            img, (img.get_width() * scalex, img.get_height() * scaley))
    if rect:
        image_rect = image.get_rect(center=(x, y))
        surface.blit((image), image_rect)
    elif not rect:
        surface.blit(image, (x, y))
    return img


def blurfade(surf):
    res = [[1280, 720], [640, 360], [320, 180],
           [160, 90], [80, 45], [40, 22], [20, 11]]
    copy = surf.copy()
    for i in range(len(res)):
        e = pygame.transform.scale(copy, (res[i][0], res[i][1]))
        e = pygame.transform.scale(e, (W, H))
        surf.blit(e, (0, 0))
        pygame.display.update()
        pygame.time.wait(300)


def move_towards_rect(r1, r2, speed):
    radians = atan2(r2.centery - r1.centery, r2.centerx -
                    r1.centerx)  # Y van elol!

    dx = cos(radians)*speed
    dy = sin(radians)*speed

    r1.centerx += dx
    r1.centery += dy


def flip(image, boolean):
    flipped_image = pygame.transform.flip(image, boolean, False)
    return flipped_image


def flip_ver(image, boolean):
    f_img = pygame.transform.flip(image, False, boolean)
    return f_img


KSS = 30  # keystroke size
KSG = 8  # keystroke gap

KSP_C = (120, 120, 120)  # keydown color
KSU_C = (0,   0,   255)  # keyup color


def draw_keystroke(surf, key, x, y, text):
    rect = pygame.Rect(x, y, KSS, KSS)
    if key:
        pygame.draw.rect(surf, KSP_C, rect)
    else:
        pygame.draw.rect(surf, KSU_C, rect)
    mts(surf, True, int(KSS/2), text, WHITE, rect.centerx,
        rect.centery + 7 if text == '^' else rect.centery)


def keystrokes(surf, tipus):
    keys = pygame.key.get_pressed()
    if tipus == 'wasd':
        draw_keystroke(surf, keys[pygame.K_a], KSG, H-KSG-KSS,        'a')
        draw_keystroke(surf, keys[pygame.K_w], KSG*2+KSS, H-KSG-KSS,  'w')
        draw_keystroke(surf, keys[pygame.K_d], KSG*3+KSS*2, H-KSG-KSS, 'd')

    elif tipus == 'arrows':
        e = W-((KSS*3)+(KSG*4))
        draw_keystroke(surf, keys[pygame.K_LEFT],
                       KSG+e, H-KSG-KSS,           '<')
        draw_keystroke(surf, keys[pygame.K_UP], KSG*2+KSS+e, H-KSG-KSS, '^')
        draw_keystroke(surf, keys[pygame.K_RIGHT],
                       KSG*3+KSS*2+e, H-KSG-KSS,   '>')


# sounds
trampoline_fx = pygame.mixer.Sound('sound/trampoline.wav')
trampoline_fx.set_volume(0.2)
completed_fx = pygame.mixer.Sound('sound/level_completed.wav')
completed_fx.set_volume(0.4)

enemy_hit_fx = pygame.mixer.Sound('sound/enemy_hit.wav')

checkpoint_fx = pygame.mixer.Sound('sound/checkpoint.wav')
shoot_fx = pygame.mixer.Sound('sound/shoot.wav')
laser_fx = pygame.mixer.Sound('sound/laser.wav')

# images
enemy_folder = 'img/blocks/enemy'
e1 = scale_img(load_img(f'{enemy_folder}/1.png'), TS)
e2 = scale_img(load_img(f'{enemy_folder}/2.png'), TS)
enemy_images = [e1, e2]

checkpoint_f = 'img/blocks/checkpoint'
chp1 = scale_img(load_img(f'{checkpoint_f}/active.png'),   TS)
chp2 = scale_img(load_img(f'{checkpoint_f}/inactive.png'), TS)
checkpoint_images = {'active':   chp1,
                     'inactive': chp2}


def b_img(name):
    return load_img(f'img/blocks/{name}.png')


blocks_names = ['enemy', 'grass', 'dirt', 'trampoline',
                'moving', 'box', 'flag', 'shooter',
                'falling', 'spike', 'checkpoint', 'aimbot']

b_imgs = {}

for bn in blocks_names:
    b_imgs.update({bn: b_img(bn)})


def screenshot():
    screen = pygame.display.get_surface()
    ss_s = screen.copy()
    ss_id = 1
    date = datetime.date.today()
    file = f'screenshots/{date}_{ss_id}.png'
    while os.path.exists(file):
        ss_id += 1
        file = f'screenshots/{date}_{ss_id}.png'

    pygame.image.save(ss_s, file)
