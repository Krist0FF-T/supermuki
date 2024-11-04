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

