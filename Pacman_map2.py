import pygame
from Characters import Player, Ghost, Pink_directions, Blue_directions, Red_directions, Yellow_directions
from Pacman_menu import load_saved_settings, Menu

player_width = 30
player_height = 30
ghost_width = 30
ghost_height = 30
player_initial_x = 140
player_initial_y = 100
level, enemiesNum = load_saved_settings("PacmanSave.json")

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (150,0,255)
yellow   = ( 255, 255,0)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


def setupMaze(all_sprites_list):
    wall_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
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
     
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], purple)
        wall_list.add(wall)
        all_sprites_list.add(wall)
        
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


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect() 


pygame.init()
screen = pygame.display.set_mode([606, 700])
pygame.display.set_caption('Pacman')
background = pygame.Surface(screen.get_size())
background.fill(black)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("Anta-Regular.ttf", 24)

def startGame(enemiesNum):
    pygame.init()
    screen = pygame.display.set_mode([606, 606])
    clock = pygame.time.Clock()
    pygame.font.init()

    done = False
    all_sprites_list = pygame.sprite.RenderPlain()
    wall_list, block_list = setupMaze(all_sprites_list)
    gate = setupGate(all_sprites_list)
    player = Player("Characters/PacmanRight.png", player_width, player_height)
    player.rect.x = player_initial_x
    player.rect.y = player_initial_y
    player_group = pygame.sprite.RenderPlain(player)
   
    ghosts = []
    for i in range(enemiesNum):
        if i % 4 == 0:
            ghost = Ghost("Characters/Pink.png", ghost_width, ghost_height, Pink_directions)
        elif i % 4 == 1:
            ghost = Ghost("Characters/Blue.png", ghost_width, ghost_height, Blue_directions)
        elif i % 4 == 2:
            ghost = Ghost("Characters/Red.png", ghost_width, ghost_height, Red_directions)
        else:
            ghost = Ghost("Characters/Yellow.png", ghost_width, ghost_height, Yellow_directions)
        ghost.num_of_ghosts = enemiesNum
        ghosts.append(ghost)

    # Set positions for ghosts
    ghost_positions = [(282, 242), (282, 242), (282, 242), (282, 242)]  # Example positions, you can modify as needed
    for i, ghost in enumerate(ghosts):
        ghost.rect.x, ghost.rect.y = ghost_positions[i]

    ghost_group = pygame.sprite.RenderPlain(ghosts)
    yellow_points = len(block_list)
    score = 0
    gate_rect = pygame.Rect(282, 242, 42, 2)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Menu()  # Return to the menu when user quits
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Menu()  # Return to the menu when Escape key is pressed
                if event.key == pygame.K_LEFT:
                    player.image = pygame.image.load("Characters/PacmanLeft.png").convert_alpha()
                    player.changespeed(-15, 0)
                elif event.key == pygame.K_RIGHT:
                    player.image = pygame.image.load("Characters/PacmanRight.png").convert_alpha()
                    player.changespeed(15, 0)
                elif event.key == pygame.K_UP:
                    player.image = pygame.image.load("Characters/PacmanUp.png").convert_alpha()
                    player.changespeed(0, -15)
                elif event.key == pygame.K_DOWN:
                    player.image = pygame.image.load("Characters/PacmanDown.png").convert_alpha()
                    player.changespeed(0, 15)
                elif event.key == pygame.K_r:  # Restart when 'R' key is pressed
                    return startGame(enemiesNum)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(15, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-15, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 15)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -15)

        yellow_collisions = pygame.sprite.spritecollide(player, block_list, True)
        if yellow_collisions:
            score += 1

        if pygame.sprite.spritecollide(player, ghost_group, False):
            done = True

        if score == yellow_points:
            done = True
            break

        screen.fill(black)
        wall_list.draw(screen)
        gate.draw(screen)
        block_list.draw(screen)
        player_group.update(wall_list)
        player_group.draw(screen)
        ghost_group.update(wall_list, gate_rect)
        ghost_group.draw(screen)
        text_score = font.render("Score: " + str(score), True, white)
        screen.blit(text_score, [20, 20])
        pygame.display.flip()
        clock.tick(10)
    if score == yellow_points:
        doWon("You Won!", 240, enemiesNum)
    else:
        doLost("You Lost!", 240, enemiesNum)

def doWon(message, left, enemiesNum):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Menu()
                if event.key == pygame.K_RETURN:
                    return startGame(enemiesNum)

        w = pygame.Surface((400,200))
        w.set_alpha(10)
        w.fill((128,128,128))
        screen.blit(w, (100,200))

        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()
        clock.tick(10)

def doLost(message, left, enemiesNum):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Menu()
                if event.key == pygame.K_RETURN:
                    return startGame(enemiesNum)

        w = pygame.Surface((400,200))
        w.set_alpha(10)
        w.fill((128,128,128))
        screen.blit(w, (100,200))

        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()
        clock.tick(10)

startGame(enemiesNum)
pygame.quit()