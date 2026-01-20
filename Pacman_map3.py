import sys
import asyncio
import pygame
from utils import asset, is_web
from Characters import Player, Ghost, Pink_directions, Blue_directions, Red_directions, Yellow_directions

# ----------------------------
# Level 3 tuning
# ----------------------------
PLAYER_SPEED = 4
WIN_SCORE = 120
GATE_OPENS_AT = 120
WALL_COLOR = (0, 200, 200)

# Colors (Level 3 theme)
black = (0, 0, 0)
white = (255, 255, 255)
cyan  = (0, 180, 255)
yellow = (255, 255, 0)


player_width = 30
player_height = 30
ghost_width = 30
ghost_height = 30
player_initial_x = 140
player_initial_y = 100


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()


def setupMaze(all_sprites_list):
    # New Level 3 wall pattern (harder but still fair)
    walls = [
        # Borders
        [0, 0, 6, 606], [0, 0, 606, 6], [0, 600, 606, 6], [600, 0, 6, 606],

        # Top structure
        [60, 60, 186, 6], [360, 60, 186, 6],
        [300, 0, 6, 120],

        # Upper middle box
        [180, 120, 246, 6],
        [180, 120, 6, 66], [420, 120, 6, 66],

        # Side corridors
        [60, 120, 6, 186], [540, 120, 6, 186],
        [60, 300, 186, 6], [360, 300, 186, 6],

        # Center “arena” (around ghost house)
        # gate-top split wall (LEFT)
        [240, 240, 42, 6],

        # gate-top split wall (RIGHT)
        [324, 240, 42, 6],

        [240, 240, 6, 66], [360, 240, 6, 66],
        [240, 300, 126, 6],

        # Lower mid
        [180, 360, 246, 6],
        [180, 360, 6, 66], [420, 360, 6, 66],

        # Bottom corridors
        [60, 420, 186, 6], [360, 420, 186, 6],
        [300, 420, 6, 120],

        # Bottom blocks
        [120, 480, 366, 6],
        [120, 480, 6, 66], [480, 480, 6, 66],
    ]

    wall_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    gate_rect = pygame.Rect(282, 242, 42, 2)

    for x, y, w, h in walls:
        wall_rect = pygame.Rect(x, y, w, h)
        if wall_rect.colliderect(gate_rect):
            continue  # never place a wall where the gate is
        wall = Wall(x, y, w, h, WALL_COLOR)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # pellets
    for row in range(19):
        for column in range(19):
            # keep ghost house area empty-ish
            if (row in (7, 8)) and (column in (8, 9, 10)):
                continue
            block = Block(yellow, 4, 4)
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26
            if not pygame.sprite.spritecollide(block, wall_list, False):
                block_list.add(block)
                all_sprites_list.add(block)

    return wall_list, block_list


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


# ENTER -> back to menu, ESC -> quit
async def doEndScreen(screen, font, clock, message, left):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        w = pygame.Surface((400, 200))
        w.set_alpha(10)
        w.fill((128, 128, 128))
        screen.blit(w, (100, 200))

        screen.blit(font.render(message, True, white), [left, 233])
        screen.blit(font.render("Press ENTER to restart.", True, white), [120, 303])
        screen.blit(font.render("Press ESC to return to menu.", True, white), [120, 333])

        pygame.display.flip()
        clock.tick(60)
        if is_web():
            await asyncio.sleep(0)



async def startGame(enemiesNum: int):
    pygame.init()
    screen = pygame.display.set_mode([606, 606])
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font(asset("Anta-Regular.ttf"), 24)
    pygame.display.set_caption("Pacman - Level 3")

    all_sprites_list = pygame.sprite.RenderPlain()
    wall_list, block_list = setupMaze(all_sprites_list)
    gate = setupGate(all_sprites_list)

    player = Player(asset("Characters", "PacmanRight.png"), player_width, player_height)
    player.rect.x = player_initial_x
    player.rect.y = player_initial_y

    # preload direction images ONCE
    def load_scaled(path, size):
        return pygame.transform.smoothscale(
            pygame.image.load(path).convert_alpha(),
            size
        )

    size = (player_width, player_height)

    img_left = load_scaled(asset("Characters", "PacmanLeft.png"), size)
    img_right = load_scaled(asset("Characters", "PacmanRight.png"), size)
    img_up = load_scaled(asset("Characters", "PacmanUp.png"), size)
    img_down = load_scaled(asset("Characters", "PacmanDown.png"), size)

    player.image = img_right

    player_group = pygame.sprite.RenderPlain(player)

    # --- fixed ghost count for Level 3 ---
    enemiesNum = 5

    ghosts = []

    for i in range(enemiesNum):
        if i % 5 == 0:
            ghost = Ghost(asset("Characters", "Pink.png"),
                          ghost_width, ghost_height, Pink_directions)
        elif i % 5 == 1:
            ghost = Ghost(asset("Characters", "Blue.png"),
                          ghost_width, ghost_height, Blue_directions)
        elif i % 5 == 2:
            ghost = Ghost(asset("Characters", "Red.png"),
                          ghost_width, ghost_height, Red_directions)
        elif i % 5 == 3:
            ghost = Ghost(asset("Characters", "Yellow.png"),
                          ghost_width, ghost_height, Yellow_directions)
        else:  # i % 5 == 4
            ghost = Ghost(asset("Characters", "Purple.png"),
                          ghost_width, ghost_height, Yellow_directions)

        ghosts.append(ghost)

    # Spawn them just OUTSIDE the doorway (spread them so they don't overlap)
    ghost_positions = [
        (310, 210),
        (285, 310),
        (230, 210),
        (260, 210),
        (315, 310),
    ]

    for i, ghost in enumerate(ghosts):
        ghost.rect.x, ghost.rect.y = ghost_positions[i % len(ghost_positions)]

    ghost_group = pygame.sprite.Group(ghosts)

    score = 0
    gate_open = False
    gate_rect = pygame.Rect(282, 242, 42, 2)

    done = False
    won = False

    # IMPORTANT: don’t demand more pellets than exist
    required = min(GATE_OPENS_AT, len(block_list))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_LEFT:
                    player.image = img_left
                    player.changespeed(-PLAYER_SPEED, 0)
                elif event.key == pygame.K_RIGHT:
                    player.image = img_right
                    player.changespeed(PLAYER_SPEED, 0)
                elif event.key == pygame.K_UP:
                    player.image = img_up
                    player.changespeed(0, -PLAYER_SPEED)
                elif event.key == pygame.K_DOWN:
                    player.image = img_down
                    player.changespeed(0, PLAYER_SPEED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(PLAYER_SPEED, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-PLAYER_SPEED, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, PLAYER_SPEED)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -PLAYER_SPEED)

        score += len(pygame.sprite.spritecollide(player, block_list, True))

        if (not gate_open) and score >= required:
            gate_open = True

        if pygame.sprite.spritecollide(player, ghost_group, False):
            done = True

        if gate_open and player.rect.colliderect(gate_rect):
            won = True
            done = True

        screen.fill(black)
        wall_list.draw(screen)
        if not gate_open:
            gate.draw(screen)
        block_list.draw(screen)

        player_group.update(wall_list)
        player_group.draw(screen)

        active_gate_rect = gate_rect if not gate_open else pygame.Rect(0, 0, 0, 0)
        ghost_group.update(wall_list, active_gate_rect)
        ghost_group.draw(screen)

        screen.blit(
            font.render(f"Score: {score}/{required}", True, white),
            (20, 20)
        )

        pygame.display.flip()
        clock.tick(60)
        if is_web():
            await asyncio.sleep(0)

    if won:
        return await doEndScreen(screen, font, clock, "You Won!", 240)
    return await doEndScreen(screen, font, clock, "You Lost!", 240)


async def run(enemiesNum: int):
    enemiesNum = 5
    return await startGame(enemiesNum)




if __name__ == "__main__":
    print(asyncio.run(run(2)))
    pygame.quit()
