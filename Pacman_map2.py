import pygame
from Characters import Player, Ghost, Pink_directions, Blue_directions, Red_directions, Yellow_directions
import sys
from pathlib import Path
from utils import asset, is_web
import asyncio


# Define constants for player and ghost dimensions and initial positions
player_width = 30
player_height = 30
ghost_width = 30
ghost_height = 30
player_initial_x = 140
player_initial_y = 100
WIN_SCORE = 80
GATE_OPENS_AT = 80  # when the gate opens (must be <= WIN_SCORE)
PLAYER_SPEED = 4

# Load saved settings for level and number of enemies

# Define color constants
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (150,0,255)
yellow   = ( 255, 255,0)
orange = (255, 165, 0)

# Define Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# Define setupMaze function to create maze walls and blocks
def setupMaze(all_sprites_list):
    # Define coordinates and dimensions for walls in the maze
    walls = [ [0,0,6,600], [0,0,600,6], [0,600,600,6], [600,0,6,600],
                [60,60,66,36],[180,60,66,36],[300,0,6,66],
             [360,60,66,36],[480,60,66,36],[300,120,6,66],
             [240,150,126,6],[60,150,36,6],[150,150,6,36],
             [150,180,36,6],[420,180,36,6],[450,150,6,36],
             [510,150,36,6],[0,210,36,6],[570,210,36,6],
             [90,210,6,96],[510,210,6,96],[60,300,36,6],
             [510,300,36,6],[180,240,6,126],[420,240,6,126],
             [240,360,126,6],[60,360,36,6],[90,360,6,66],
             [510,360,36,6],[510,360,6,66],[0,420,36,6],
             [180,420,66,6],[360,420,66,6],[570,420,36,6],
             [300,420,6,126],[60,480,36,6],[180,480,6,66],
             [240,480,126,6],[420,480,6,66],[510,480,36,6],
             [90,480,6,66],[510,480,6,66],[0,540,36,6],
             [180,540,66,6],[360,540,66,6],[570,540,36,6],
             [240,240,42,6], [324,240,42,6], [240,240,6,66],
             [240,300,126,6], [360,240,6,66]
               ]

    # Create walls and blocks based on the defined coordinates
    wall_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()

    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], orange)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # Create blocks for empty spaces in the maze
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(yellow, 4, 4)
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26
                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                if not b_collide:
                    block_list.add(block)
                    all_sprites_list.add(block)
         
    return wall_list, block_list

# Define setupGate function to create the gate in the maze
def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate

# Define Block class for representing yellow blocks in the maze
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect() 



# Define function to start the game
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
        all_sprites_list = pygame.sprite.RenderPlain()

        wall_list, block_list = setupMaze(all_sprites_list)
        required = min(WIN_SCORE, len(block_list))

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

            if not gate_open and score >= required:
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

            screen.blit(
                font.render(f"Score: {score}/{required}", True, white),
                (20, 20)
            )

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



# Function to display winning message
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

        y = 303

        t1 = font.render("Press ENTER to restart.", True, white)
        t2 = font.render("Press ESC to return to menu.", True, white)

        r1 = t1.get_rect(center=(303, y))
        r2 = t2.get_rect(center=(303, y + 30))

        screen.blit(t1, r1)
        screen.blit(t2, r2)

        pygame.display.flip()
        clock.tick(60)
        if is_web():
            await asyncio.sleep(0)





        # Display winning message and options
        w = pygame.Surface((400,200))
        w.set_alpha(10)
        w.fill((128,128,128))
        screen.blit(w, (100,200))

        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])



        pygame.display.flip()
        clock.tick(10)

# Function to display losing message
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

        y = 303

        t1 = font.render("Press ENTER to restart.", True, white)
        t2 = font.render("Press ESC to return to menu.", True, white)

        r1 = t1.get_rect(center=(303, y))
        r2 = t2.get_rect(center=(303, y + 30))

        screen.blit(t1, r1)
        screen.blit(t2, r2)

        pygame.display.flip()
        clock.tick(60)
        if is_web():
            await asyncio.sleep(0)





        # Display losing message and options
        w = pygame.Surface((400,200))
        w.set_alpha(10)
        w.fill((128,128,128))
        screen.blit(w, (100,200))

        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])





# Start the game
async def run(enemiesNum: int) -> str:
    return await startGame(enemiesNum)



if __name__ == "__main__":
    import asyncio
    asyncio.run(run(2))
    pygame.quit()

