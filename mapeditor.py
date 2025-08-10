import pygame as pg

from scripts import consts, util, menu
from scripts.assets import asset_manager

def block_image(name):
    img = asset_manager.get_image(f"blocks/{name}.png").convert_alpha()
    w = 2 if name == "moving" else 1
    img = pg.transform.scale(img, (consts.TS * w, consts.TS))
    # b_imgs.update({name: img})
    return img

def save_txt():
    with open(f_name, 'w') as f:
        for row in blocks:
            f.writelines(row)

def block_selection() -> int | None:
    e = True
    while e:
        consts.clock.tick(consts.FPS)
        events = pg.event.get()
        mouse_pos = pg.mouse.get_pos()

        for ev in events:
            if ev.type == pg.QUIT:
                util.close()
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    return None

        screen.fill(consts.GUI_BG_COLOR)

        for i, letter in enumerate(block_letters):
            img = b_imgs[letter_to_name[letter]]
            img = pg.transform.scale(img, (consts.TS, consts.TS))
            r = pg.Rect(i * 80 + 100, 400, consts.TS, consts.TS)

            screen.blit(img, (r.x, r.y))
            if r.collidepoint(mouse_pos):
                if pg.mouse.get_pressed()[0]:
                    return i

        util.draw_text(
            screen,
            True,
            40,
            "block selection",
            "white",
            consts.CX,
            100,
        )

        pg.display.update()

    return None

pg.font.init()
screen = pg.display.set_mode((consts.W, consts.H))
pg.display.set_caption('MapMaker for Dungeon')

block_names = [
    'aimbot', 'box', 'checkpoint', 'dirt', 'enemy',
    'falling', 'flag', 'grass', 'laser', 'moving',
    'playerpos', 'shooter', 'spike', 'trampoline'
]

letter_to_name = {
    "a": "aimbot",
    "B": "box",
    "c": "checkpoint",
    "d": "dirt",
    "e": "enemy",
    "f": "falling",
    "G": "flag",
    "g": "grass",
    "-": "laser",
    "m": "moving",
    "P": "playerpos",
    "s": "shooter",
    "S": "spike",
    "T": "trampoline",
}

block_letters = ['a', 'B', 'c', 'd', 'e', 'f', 'G', 'g', '-', 'm', 'P', 's', 'S', 'T']

b_imgs = {}

# for bn in b_names:
#     new_block_image(bn)

n = menu.level_selection(screen)
f_name = f'assets/levels/{n}.txt'

blocks = []
try:
    with open(f_name, 'r') as f:
        lines = f.readlines()
        # blocks = [
        #     [
        #         block
        #         for block in row
        #     ]
        #     for row in lines
        # ]
        # print(lines)
        for y, row in enumerate(lines):
            therow = []
            for x, col in enumerate(row):
                therow.append(col)
            blocks.append(therow)

except Exception:
    for y in range(consts.ROW):
        row = []
        for x in range(consts.COL):
            row.append('.')
        row.append('\n')
        blocks.append(row)


scroll = 0
sel_letter = 'g'
sel_num = 0

grid = False

run = True
while run:
    consts.clock.tick(consts.FPS)
    events = pg.event.get()
    mouse_pos = pg.mouse.get_pos()
    mouse_btn = pg.mouse.get_pressed()
    keys = pg.key.get_pressed()

    # --- update ---

    sel_pos = [
        int((mouse_pos[0] - scroll) / consts.TS),
        int((mouse_pos[1]) / consts.TS),
    ]

    scroll += (
        (keys[pg.K_LEFT] or keys[pg.K_a])
        - (keys[pg.K_RIGHT] or keys[pg.K_d])
    ) * 20

    if scroll > 0:
        scroll = 0
    if scroll < -4720:
        scroll = -4720

    # left click: destroy
    if mouse_btn[0]:
        blocks[sel_pos[1]][sel_pos[0]] = '.'

    # right click: place
    if mouse_btn[2]:
        blocks[sel_pos[1]][sel_pos[0]] = sel_letter

    for ev in events:
        if ev.type == pg.QUIT:
            util.close()

        elif ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                util.close()

            elif ev.key == pg.K_SPACE:
                n = block_selection()
                if n is not None:
                    sel_num = n
                    sel_letter = block_letters[n]

            elif ev.key == pg.K_g:
                grid = not grid

            elif ev.key == pg.K_x:
                e = blocks[sel_pos[1]][sel_pos[0]]
                if e in block_letters:
                    sel_letter = e

            elif ev.key == pg.K_s:
                save_txt()

            elif ev.key == pg.K_F11:
                pg.display.toggle_fullscreen()

        elif ev.type == pg.MOUSEBUTTONDOWN:
            d: int = (ev.button == 5) - (ev.button == 4)
            if d != 0:
                sel_num = (sel_num + d) % len(block_letters)
                sel_letter = block_letters[sel_num]

    # --- render ---

    screen.fill(consts.GAME_BG_COLOR)


    for y, row in enumerate(blocks):
        for x, col in enumerate(row):
            if col in block_letters and -scroll-consts.TS < x*consts.TS < -scroll+consts.W:
                img = block_image(letter_to_name[col])
                # img = b_imgs[letter_to_name[col]]
                screen.blit(img, (x*consts.TS+scroll, y*consts.TS))

    for x in range(1, 21):
        if not grid:
            break
        for y in range(1, consts.ROW):
            # tx = (x - scroll / consts.TS) * consts.TS + scroll
            tx = x * consts.TS + scroll
            ty = y * consts.TS
            pg.draw.line(screen, "black", (tx, 0), (tx, consts.H))
            pg.draw.line(screen, "black", (0, ty), (consts.W, ty))

    # e = b_imgs[letter_to_name[sel_letter]].copy()
    e = block_image(letter_to_name[sel_letter])
    e.set_alpha(80)
    screen.blit(e, (sel_pos[0] * consts.TS + scroll, sel_pos[1] * consts.TS))

    util.draw_text(screen, False, 30, f'{sel_pos[0]};{sel_pos[1]}', "white", 20, 20)

    pg.display.update()


