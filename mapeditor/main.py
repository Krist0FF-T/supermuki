import pygame as pg
from second import *
# from os.path import exists
# from random import choice, randint

f_name = input('filename: ')
f_name = f'../levels/{f_name}.txt'

try:
    blocks = []
    with open(f_name, 'r') as f:
        loaded = f.readlines()
        for y, row in enumerate(loaded):
            therow = []
            for x, col in enumerate(row):
                therow.append(col)
            blocks.append(therow)

except:
    blocks = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            row.append('.')
        row.append('\n')
        blocks.append(row)

screen = pg.display.set_mode((W, H))
pg.display.set_caption('MapMaker for Dungeon')

scroll = 0
sel_letter = 'g'
sel_num = 0

def savetxt():
    with open(f_name, 'w') as f:
        for row in blocks:
            f.writelines(row)

def b_selection() -> int:
    e = True
    sel = sel_num
    while e:
        pos = pg.mouse.get_pos()
        clock.tick(30)
        screen.fill((0,0,50))
        
        for i, letter in enumerate(letter_list):
            img = b_imgs[b_letters[letter]]
            img = pg.transform.scale(img, (TS, TS))
            r = pg.Rect(i*80+100, 400, TS, TS)

            screen.blit(img, (r.x, r.y))
            if sel == i:
                pg.draw.rect(screen, (255,0,0), r, 8)
            if r.collidepoint(pos):
                if pg.mouse.get_pressed()[0]:
                    sel = i

        mts(screen, True, 40, 'block selection', (255,255,255), CX, 100)

        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT: e = False
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE: e = False
                if ev.key == pg.K_SPACE:
                    return sel

    return sel_num

grid = False

run = True
while run:
    pos = pg.mouse.get_pos()
    clock.tick(FPS)
    screen.fill((100,180,240))

    if scroll > 0: scroll = 0
    if scroll < -4720: scroll = -4720

    sel_pos = [int((pos[0]-scroll)/TS), int((pos[1])/TS)]

    for y, row in enumerate(blocks):
        for x, col in enumerate(row):
            if col in letter_list and -scroll-TS < x*TS < -scroll+W:
                img = b_imgs[b_letters[col]]
                screen.blit(img, (x*TS+scroll, y*TS))

    if grid:
        for x in range(1, 21):
            for y in range(1, ROWS):
                x += int(-scroll/TS)
                tx = x*TS+scroll
                pg.draw.line(screen, (0,0,0), (tx, 0), (tx, H))
                pg.draw.line(screen, (0,0,0), (0, y*TS), (W, y*TS))
    
    e = b_imgs[b_letters[sel_letter]].copy()
    e.set_alpha(80)
    screen.blit(e, (sel_pos[0]*TS+scroll, sel_pos[1]*TS))

    mts(screen, False, 30, f'{sel_pos[0]};{sel_pos[1]}', (255,255,255), 20, 20)

    pg.display.update()

    keys = pg.key.get_pressed()
    if keys[pg.K_RIGHT] or keys[pg.K_d]: scroll -= 20
    if keys[pg.K_LEFT]  or keys[pg.K_a]: scroll += 20

    mb = pg.mouse.get_pressed()

    # left click: destroy
    if mb[0]:
        blocks[sel_pos[1]][sel_pos[0]] = '.'

    # right click: place
    if mb[2]:
        blocks[sel_pos[1]][sel_pos[0]] = sel_letter

    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False

        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                run = False

            if ev.key == pg.K_SPACE:
                sel_num = b_selection()
                try:
                    sel_letter = letter_list[sel_num]
                except Exception:
                    pass

            if ev.key == pg.K_g:
                grid = not grid

            if ev.key == pg.K_x:
                e = blocks[sel_pos[1]][sel_pos[0]]
                if e in letter_list:
                    sel_letter = e

            if ev.key == pg.K_s:
                savetxt()

            if ev.key == pg.K_F11:
                pg.display.toggle_fullscreen()

        if ev.type == pg.MOUSEBUTTONDOWN:
            if ev.button == 4 and sel_num > 0:
                sel_num -= 1
                sel_letter = letter_list[sel_num]

            if ev.button == 5 and sel_num < len(letter_list)-1:
                sel_num += 1
                sel_letter = letter_list[sel_num]

savetxt()

pg.quit()
