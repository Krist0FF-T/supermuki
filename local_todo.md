
- [x] shooter not solid
- [x] button behavior: act on press consistently
- move _ into Game:
    - [x] blocks, bullets, lasers, etc.
    - [x] game loop
    - [x] init logic
- trampoline: always jump
- bg lines: real-time gen, no unnecessary cache
- [ ] remove bullets when out of screen vertically

- new classes instead of lists
    - [ ] Bullet: pos, vel
    - [ ] Block: rect, image, name, props
- Supermupla-like menu/`View` system
    - mapeditor: accessible through the game
        - (e.g. in pause menu or by hotkey)
- `BlockManager` used by both the game and the editor

- [ ] window res independent
    - use tile size as base unit instead of px
- [ ] fps independent

bugs:
- box kills when pushing off the edge
    - (seems to be fixed somehow, haven't been an issue lately)
- player-enemy collision when they're going in the same direction
    - the player stays alive and moves roughly

