import pygame

pygame.font.init()

W, H = 1280, 720
CX, CY = W/2, H/2

clock = pygame.time.Clock()
FPS = 61

TS = 60

ROWS = 12
COLS = 100

def mts(surface, rect, size, smthing, color, x, y):
    font = pygame.font.Font('../fonts/fffforwa.ttf', size)
    text = font.render(smthing, 1, color)
    if rect:
        text_rect = text.get_rect(center = (x, y))
        surface.blit((text), text_rect)
    elif not rect:
        surface.blit(text, (x, y))
    return text

b_names = ['aimbot', 'box', 'checkpoint', 'dirt', 'enemy',
           'falling', 'flag', 'grass', 'laser', 'moving',
           'playerpos', 'shooter', 'spike', 'trampoline']

b_letters = {'a': 'aimbot',
             'B': 'box',
             'c': 'checkpoint',
             'd': 'dirt',
             'e': 'enemy',
             'f': 'falling',
             'G': 'flag',
             'g': 'grass',
             '-': 'laser',
             'm': 'moving',
             'P': 'playerpos',
             's': 'shooter',
             'S': 'spike',
             'T': 'trampoline'}

letter_list = ['a', 'B', 'c', 'd', 'e', 'f', 'G', 'g', '-', 'm', 'P', 's', 'S', 'T']

b_imgs = {}
def nbi(name, w=1, h=1): # new block img
    img = pygame.image.load(f'../img/blocks/{name}.png')
    img = pygame.transform.scale(img, (w*TS, h*TS))
    b_imgs.update({name: img})

for bn in b_names:
    if bn == 'moving':
        nbi(bn, 2)
    else:
        nbi(bn)


          
