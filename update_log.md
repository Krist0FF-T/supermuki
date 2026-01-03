# 1.4 Update Log (old versioning)
- added brown box
- added falling block
- ability to shoot screenshots
- settings:
    - flip when jump
    - keystrokes
    - show deaths
- animated enemy
- new levels
- speedrun mode
- added background blocks:
    - flower
    - grass
- parallax background
- added checkpoints

# 2024-07-21
- upload code to GitHub ([link](https://github.com/Krist0FF-T/supermuki))
- a little cleanup
- impl asset manager

# 2024-07-22
- yet another cleanup:
    - del fade effect (had to wait too much)
    - del game over screen
    - player explosion animation
- add vsync
- style fixes:
    - "from scripts.x import *" -> to "from scripts import x"
    - long lines
- new death animation: (the game doesn't freeze, the other can move freely)
    1. jumps a little (vel_y = -10)
    2. rotates while falling through blocks
    3. respawns when rect.top > consts.H
- when a player dies, the other doesn't need to restart
- when players are far apart, the moving player is the camera's target

# 2024-11-03
- small bugfixes
    - (blocks interacting with dead players)

# 2024-11-04
- avoid too much indentation
- snake case, better names, other small changes
- aliases for better readibility in update_block
- make respawn point global

# 2025-02-25
- remove GUI settings (use config.json instead)
- remove devmode
- re-order main loop to reduce input lag
- avoid expensive trigonometric functions (atan2, sin, cos)

# 2025-06-29
- simplify and optimize player controls logic

# 2025-07-19
- asset manager: actually lazy-load
    - (loads assets on first use)
    - (applies to sounds, fonts, images)
- utils: remove unused (keystrokes, move_towards_rect, draw_image)
- config: json -> py
    - make controls configurable
- map editor: refactor
    - integrate (use consts, util, assets)
- blocks:
    - spike: kill: always (not just when falling)
    - trampoline: bump: only when jumping
    - checkpoint: activation: only by alive player
- menus:
    - separate files (pause, color selection)
    - move menus to `scripts/menu`
- (+ other stuff I forgot to mention)

# 2025-08-10
- git: commit changes since 2025-06-29
- move screenshots out of repo - use GitHub assets instead

# 2025-08-11 - _
- move main loop into `Game`

# 2025-10- _

# 2026-01-03
- move global game functions (updating and rendering logic) into `Game`


