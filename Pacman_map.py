import sys
import asyncio
from pathlib import Path
from utils import asset, is_web
import pygame
from Characters import Player, Ghost, Pink_directions, Blue_directions, Red_directions, Yellow_directions

# --- Path helper (pygbag-safe) ---


# --- Constants ---
player_width = 30
player_height = 30
ghost_width = 30
ghost_height = 30
player_initial_x = 140
player_initial_y = 100
PLAYER_SPEED = 4

WIN_SCORE = 50
GATE_OPENS_AT = 50  # when the gate opens (must be <= WIN_SCORE)

# --- Colors ---
black = (0, 0, 0)
white = (255, 255, 255)
blue  = (0, 0, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
purple = (150, 0, 255)
yellow = (255, 255, 0)

# --- Wall / Block ---
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
    walls = [
        [0,0,6,600], [0,0,600,6], [0,600,600,6], [600,0,6,600],
        [300,0,6,66], [60,60,186,6], [360,60,186,6],
        [60,120,66,6], [60,120,6,126], [180,120,246,6], [300,120,6,66],
        [480,120,66,6], [540,120,6,126],
        [120,180,126,6], [120,180,6,126], [360,180,126,6], [480,180,6,126],
        [180,240,6,126], [180,360,246,6],
        [420,240,6,126], [240,240,42,6], [324,240,42,6], [240,240,6,66],
        [240,300,126,6], [360,240,6,66],
        [0,300,66,6], [540,300,66,6],
        [60,360,66,6], [60,360,6,186], [480,360,66,6], [540,360,6,186],
        [120,420,366,6], [120,420,6,66], [480,420,6,66],
        [180,480,246,6], [300,480,6,66],
        [120,540,126,6], [360,540,126,6]
    ]

    wall_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()

    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], purple)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    for row in range(19):
        for column in range(19):
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

# --- Win/Lose screens (async, yield once per frame) ---
async def doWon(screen, font, clock, message, left) -> str:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return "restart"

        # overlay
        w = pygame.Surface((400, 200))
        w.set_alpha(10)
        w.fill((128, 128, 128))
        screen.blit(w, (100, 200))

        screen.blit(font.render(message, True, (255, 255, 255)), [left, 233])
        screen.blit(font.render("Press ENTER to restart.", True, (255, 255, 255)), [120, 303])
        screen.blit(font.render("Press ESC return to menu.", True, (255, 255, 255)), [170, 333])

        pygame.display.flip()
        clock.tick(60)
        if is_web():
            await asyncio.sleep(0)


async def doLost(screen, font, clock, message, left) -> str:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return "restart"

        # overlay
        w = pygame.Surface((400, 200))
        w.set_alpha(10)
        w.fill((128, 128, 128))
        screen.blit(w, (100, 200))

        screen.blit(font.render(message, True, (255, 255, 255)), [left, 233])
        y = 303

        text1 = font.render("Press ENTER to restart.", True, white)
        text2 = font.render("Press ESC return to menu.", True, white)

        rect1 = text1.get_rect(center=(303, y))
        rect2 = text2.get_rect(center=(303, y + 30))  # if you want stacked
        # OR same y if you truly want same line:
        # rect2 = text2.get_rect(center=(303, y))

        screen.blit(text1, rect1)
        screen.blit(text2, rect2)

        pygame.display.flip()
        clock.tick(60)
        if is_web():
            await asyncio.sleep(0)


# --- Main game (async) ---
async def startGame(enemiesNum: int):
    pygame.init()
    screen = pygame.display.set_mode([606, 606])
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font(asset("Anta-Regular.ttf"), 24)
    pygame.display.set_caption("Pacman")

    # preload direction images ONCE (good)
    def load_scaled(path, size):
        return pygame.transform.smoothscale(pygame.image.load(path).convert_alpha(), size)

    size = (player_width, player_height)
    img_left  = load_scaled(asset("Characters", "PacmanLeft.png"), size)
    img_right = load_scaled(asset("Characters", "PacmanRight.png"), size)
    img_up    = load_scaled(asset("Characters", "PacmanUp.png"), size)
    img_down  = load_scaled(asset("Characters", "PacmanDown.png"), size)

    while True:  # <-- THIS is "restart"

        # --- RESET ALL GAME STATE HERE ---
        all_sprites_list = pygame.sprite.RenderPlain()
        wall_list, block_list = setupMaze(all_sprites_list)

        required = min(GATE_OPENS_AT, len(block_list))  # <-- add this line

        gate = setupGate(all_sprites_list)

        player = Player(asset("Characters", "PacmanRight.png"), player_width, player_height)
        player.rect.x = player_initial_x
        player.rect.y = player_initial_y
        player.image = img_right
        player_group = pygame.sprite.RenderPlain(player)

        ghosts = []
        for i in range(enemiesNum):
            if i % 4 == 0:
                ghost = Ghost(asset("Characters", "Pink.png"), ghost_width, ghost_height, Pink_directions)
            elif i % 4 == 1:
                ghost = Ghost(asset("Characters", "Blue.png"), ghost_width, ghost_height, Blue_directions)
            elif i % 4 == 2:
                ghost = Ghost(asset("Characters", "Red.png"), ghost_width, ghost_height, Red_directions)
            else:
                ghost = Ghost(asset("Characters", "Yellow.png"), ghost_width, ghost_height, Yellow_directions)
            ghost.num_of_ghosts = enemiesNum
            ghost.rect.x, ghost.rect.y = (282, 242)
            ghosts.append(ghost)

        ghost_group = pygame.sprite.Group(ghosts)

        score = 0
        gate_open = False
        gate_rect = pygame.Rect(282, 242, 42, 2)
        done = False
        won = False

        # --- MAIN GAME LOOP ---
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"   # esc during gameplay = menu (your choice)
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
                    elif event.key == pygame.K_RIGHT:
                        player.changespeed(-PLAYER_SPEED, 0)
                    elif event.key == pygame.K_UP:
                        player.changespeed(0, PLAYER_SPEED)
                    elif event.key == pygame.K_DOWN:
                        player.changespeed(0, -PLAYER_SPEED)

            yellow_collisions = pygame.sprite.spritecollide(player, block_list, True)
            score += len(yellow_collisions)

            if (not gate_open) and score >= required:
                gate_open = True

            if pygame.sprite.spritecollide(player, ghost_group, False):
                done = True
                won = False
                break

            if gate_open and player.rect.colliderect(gate_rect):
                done = True
                won = True
                break

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

            screen.blit(font.render(f"Score: {score}/{required}", True, white), [20, 20])

            pygame.display.flip()
            clock.tick(60)

            if is_web():
                await asyncio.sleep(0)

        # --- WIN/LOSE SCREEN ---
        if won:
            action = await doWon(screen, font, clock, "You Won!", 240)
        else:
            action = await doLost(screen, font, clock, "You Lost!", 240)

        if action == "quit":
            return "quit"
        if action == "menu":
            return "menu"
        if action == "restart":
            continue  # <-- THIS is the whole point


    if action == "quit":
        return "quit"
    return "menu"


# --- Public entry for menu/main.py ---
async def run(enemiesNum: int) -> str:
    return await startGame(enemiesNum)


if __name__ == "__main__":
    asyncio.run(run(2))
    pygame.quit()
