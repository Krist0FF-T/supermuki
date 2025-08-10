import pygame as pg
from scripts import consts, button, util

def color_selection(surf: pg.Surface, colors: list[list]):
    two_players = len(colors) >= 2

    lines = [
        ("red", 200, 300, 450),
        ("green", 200, 410, 450),
        ("blue", 200, 520, 450),
    ]

    if two_players:
        lines += [
            ("red", consts.W - 450, 300, consts.W - 200),
            ("green", consts.W - 450, 410, consts.W - 200),
            ("blue", consts.W - 450, 520, consts.W - 200),
        ]

    c_b1 = [button.p1_red, button.p1_green, button.p1_blue]
    c_b2 = [button.p2_red, button.p2_green, button.p2_blue]

    confirm_r = button.confirm_c.rect
    confirm_s = pg.Surface((confirm_r.width, confirm_r.height))

    c_s = True
    while c_s:
        consts.clock.tick(consts.FPS)

        pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                util.close()
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_SPACE, pg.K_ESCAPE, pg. K_RETURN):
                    c_s = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if button.confirm_c.rect.collidepoint(pos):
                    c_s = False

        if pg.mouse.get_pressed()[0]:
            for bu in c_b1:
                if pg.Rect(
                    bu.rect.x - 25,
                    bu.rect.y - 25,
                    bu.rect.width + 50,
                    bu.rect.height + 50,
                ).collidepoint(pos):
                    bu.rect.centerx = pos[0]
                if bu.rect.left < 200:
                    bu.rect.left = 200
                if bu.rect.right > 450:
                    bu.rect.right = 450

            if two_players:
                for bu in c_b2:
                    if pg.Rect(
                        bu.rect.x - 20,
                        bu.rect.y - 20,
                        bu.rect.width + 40,
                        bu.rect.height + 40,
                    ).collidepoint(pos):
                        bu.rect.centerx = pos[0]

                    if bu.rect.left < consts.W - 450:
                        bu.rect.left = consts.W - 450

                    if bu.rect.right > consts.W - 200:
                        bu.rect.right = consts.W - 200

        surf.fill(consts.GUI_BG_COLOR)
        # button.colored_b(confirm_s, confirm_r, (80, 80, 80), pos)
        button.green_button(confirm_s, confirm_r, pos)
        surf.blit(confirm_s, confirm_r)
        util.draw_text(
            surf,
            True,
            30,
            "Done",
            "white",
            confirm_r.centerx,
            confirm_r.centery,
        )

        for li in lines:
            pg.draw.line(surf, li[0], [li[1], li[2]], [li[3], li[2]], 7)

        for bu1 in c_b1:
            bu1.draw(surf)

        if two_players:
            for bu2 in c_b2:
                bu2.draw(surf)

        for i in range(3):
            if c_b1[i].rect.left < 200:
                c_b1[i].rect.left = 200
            if c_b1[i].rect.right > 450:
                c_b1[i].rect.right = 450

            if two_players:
                if c_b2[i].rect.left < consts.W - 450:
                    c_b2[i].rect.left = consts.W - 450
                if c_b2[i].rect.right > consts.W - 200:
                    c_b2[i].rect.right = consts.W - 200

            colors[0][i] = c_b1[i].rect.centerx - 200
            if two_players:
                colors[1][i] = c_b2[i].rect.centerx - (consts.W - 450)

        player_images = [
            util.recolor_player(color)[2]
            for color in colors
        ]

        p1_pv_image = pg.transform.scale(player_images[0], (80, 80))
        p1_pv_rect = p1_pv_image.get_rect()
        p1_pv_rect.center = (350, 120)

        if two_players:
            p2_pv_image = pg.transform.scale(player_images[1], (80, 80))
            p2_pv_rect = p2_pv_image.get_rect()
            p2_pv_rect.center = (consts.W - 350, 120)

        surf.blit(p1_pv_image, p1_pv_rect)
        if two_players:
            surf.blit(p2_pv_image, p2_pv_rect)

        util.draw_text(
            surf,
            True,
            30,
            str(colors[0]),
            "white",
            p1_pv_rect.centerx,
            consts.H - 100,
        )

        if two_players:
            util.draw_text(
                surf,
                True,
                30,
                str(colors[1]),
                "white",
                p2_pv_rect.centerx,
                consts.H - 100,
            )

        pg.display.update()
