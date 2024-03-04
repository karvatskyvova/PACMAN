import pygame
from Characters import Player, Ghost, Pink_directions, Blue_directions, Red_directions, Yellow_directions

player_width = 30
player_height = 30
ghost_width = 30
ghost_height = 30

player_initial_x = 140
player_initial_y = 100
  
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
    walls = [ [0,0,6,600], [0,0,600,6], [0,600,600,6], [600,0,6,600], [300,0,6,66], [60,60,186,6], [360,60,186,6],
              [60,120,66,6], [60,120,6,126], [180,120,246,6], [300,120,6,66], [480,120,66,6], [540,120,6,126],
              [120,180,126,6], [120,180,6,126], [360,180,126,6], [480,180,6,126], [180,240,6,126], [180,360,246,6],
              [420,240,6,126], [240,240,42,6], [324,240,42,6], [240,240,6,66], [240,300,126,6], [360,240,6,66],
              [0,300,66,6], [540,300,66,6], [60,360,66,6], [60,360,6,186], [480,360,66,6], [540,360,6,186],
              [120,420,366,6], [120,420,6,66], [480,420,6,66], [180,480,246,6], [300,480,6,66], [120,540,126,6],
              [360,540,126,6] ]
     
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
font_pacman = pygame.font.Font("PAC-FONT.TTF", 48)  

def startGame():
    pygame.init()

    screen = pygame.display.set_mode([606, 700])
    pygame.display.set_caption('Pacman')

    clock = pygame.time.Clock()
    
    pygame.font.init()
    font = pygame.font.Font("Anta-Regular.ttf", 24)
    font_pacman = pygame.font.Font("PAC-FONT.TTF", 48)

    done = False

    all_sprites_list = pygame.sprite.RenderPlain()
    wall_list, block_list = setupMaze(all_sprites_list)
    gate = setupGate(all_sprites_list)

    player = Player("Characters/PacmanRight.png", player_width, player_height)
    player.rect.x = player_initial_x
    player.rect.y = player_initial_y

    pink_ghost = Ghost("Characters/Pink.png", ghost_width, ghost_height, Pink_directions)
    blue_ghost = Ghost("Characters/Blue.png", ghost_width, ghost_height, Blue_directions)
    red_ghost = Ghost("Characters/Red.png", ghost_width, ghost_height, Red_directions)
    yellow_ghost = Ghost("Characters/Yellow.png", ghost_width, ghost_height, Yellow_directions)

    pink_ghost.rect.x, pink_ghost.rect.y = 282, 242
    blue_ghost.rect.x, blue_ghost.rect.y = 282, 242
    red_ghost.rect.x, red_ghost.rect.y = 282, 242
    yellow_ghost.rect.x, yellow_ghost.rect.y = 282, 242

    player_group = pygame.sprite.RenderPlain(player)
    ghost_group = pygame.sprite.RenderPlain(pink_ghost, blue_ghost, red_ghost, yellow_ghost)

    yellow_points = len(block_list)

    score = 0
    gate_rect = pygame.Rect(282, 242, 42, 2)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.image = pygame.image.load("Characters/PacmanLeft.png").convert_alpha()
                    player.changespeed(-30, 0)
                elif event.key == pygame.K_RIGHT:
                    player.image = pygame.image.load("Characters/PacmanRight.png").convert_alpha()
                    player.changespeed(30, 0)
                elif event.key == pygame.K_UP:
                    player.image = pygame.image.load("Characters/PacmanUp.png").convert_alpha()
                    player.changespeed(0, -30)
                elif event.key == pygame.K_DOWN:
                    player.image = pygame.image.load("Characters/PacmanDown.png").convert_alpha()
                    player.changespeed(0, 30)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -30)

        yellow_collisions = pygame.sprite.spritecollide(player, block_list, True)
        if yellow_collisions:
            score += 1

        if pygame.sprite.spritecollide(player, ghost_group, False):
            done = True

        if score == yellow_points:
            done = True

        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        block_list.draw(screen)

        player_group.update(wall_list)
        player_group.draw(screen)

        ghost_group.update(wall_list, gate_rect)
        ghost_group.draw(screen)
        text_pacman = font_pacman.render("PACMAN", True, yellow)
        screen.blit(text_pacman, [175, 610])

        text_score = font.render("Score: " + str(score), True, white)
        screen.blit(text_score, [20, 20])

        pygame.display.flip()

        clock.tick(10)

    if score == yellow_points:
        doWon("You Won!", 240)
    else:
        doLost("You Lost!", 240)

    pygame.quit()

      
def doWon(message, left):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    startGame()

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

def doLost(message, left):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    startGame()

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
        
startGame()
pygame.quit()

