import pygame
  
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
    walls = [ [60,60,66,36],[180,60,66,36],[300,0,6,66],
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
         
    return wall_list


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
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()

    wall_list = setupMaze(all_sprites_list)
    gate = setupGate(all_sprites_list)

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
  

    bll = len(block_list)
    score = 0
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(black)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)

        text = font.render("Score: " + str(score) + "/" + str(bll), True, white)
        screen.blit(text, [10, 5])
        text_pacman = font_pacman.render("PACMAN", True, yellow)
        screen.blit(text_pacman, [175, 610])
        '''
        if score == bll:
            doWon("Great, you won!", 145, all_sprites_list, block_list, monsta_list, pacman_collide,
                   wall_list, gate)
        monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

        if monsta_hit_list:
            doLost("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate) #
        '''
        pygame.display.flip()
        clock.tick(10)
      
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



startGame()
pygame.quit()
