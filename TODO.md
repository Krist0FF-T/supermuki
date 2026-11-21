
Todo:
- trampoline: always jump
- bg lines: don't cache, generate real-time
- remove bullets when out of screen vertically
- new classes instead of lists
    - Bullet: pos, vel
    - Block: rect, image, name, props
- Supermupla-like menu/`View` system
    - mapeditor: accessible through the game
        - (e.g. in pause menu or by hotkey)
- impl `BlockManager` used by both the game and the editor
- window res independence - use tile size as base unit instead of px
- fps independence

Fix:
- box sometimes kills the player when pushed off the edge
- player-enemy collision when they're going in the same direction
    - (the player stays alive and moves slowly)

Repo stuff:
- create branches
    - "simple": simplified version (1 player, 1 level, 0 menus, etc.): make it clean and good for education purposes (even a tutorial crosses my mind)
    - "original": without newer modifications since Feb. 2022.
    - "improved" (or main): with newer improvements (this)
- installation steps in readme
- create tags and releases

