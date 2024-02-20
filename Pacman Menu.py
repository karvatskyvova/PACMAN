import pygame
from sys import exit

pygame.init()
SCREEN_SIZE: int = 500
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE)) #Розмір вікна
pygame.display.set_caption("PACMAN")
pygame.display.set_icon(pygame.image.load("Resourses\icon.png")) #Значок вікна

class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def IsPressed(self)->bool:
        """Перевіряє чи нажата ця клавіша курсором миші"""
        mousePos = pygame.mouse.get_pos()
        if self.x <= mousePos[0] <= self.x + self.width and self.y <= mousePos[1] <= self.y + self.height:
            return True
        else:
            return False

def DrawTriangle(x, y, direction):
    """Малює кнопки у вигляді стрілок для вибору рівня\n
    x, y: координати точки, в яку вказує стрілка
    direction: напрямок (right/left)"""
    if direction == "right":
        points = [(x, y), (x - 50, y - 25), (x - 50, y + 25)]
    elif direction == "left":
        points = [(x, y), (x + 50, y + 25), (x + 50, y - 25)]
    pygame.draw.polygon(screen, (255, 234, 0), points)

def DrawInterface(chosenLevel: int):
    """Малює інтерфейс меню (зображення та кнопки)"""
    #Логотип та фонове зображення
    logo = pygame.image.load("Resourses\logo.png")
    background1 = pygame.image.load("Resourses\level1.png")
    background2 = pygame.image.load("Resourses\level2.png")
    if chosenLevel == 1:
        screen.blit(background1, (0, 0))
    elif chosenLevel == 2:
        screen.blit(background2, (0, 0))
    screen.blit(logo, (35, 20))
    #Кнопки вибору рівня
    DrawTriangle(20, SCREEN_SIZE / 2, "left")
    DrawTriangle(SCREEN_SIZE - 20, SCREEN_SIZE / 2, "right")

def Menu()->int:
    """Стартове вікно гри. Вікривається одразу після запуску\n
    returns: номер обраного користувачем рівня"""
    DrawInterface(1)
    leftArrow = Button(20, SCREEN_SIZE / 2 - 25, 50, 50)
    rightArrow = Button(SCREEN_SIZE - 70, SCREEN_SIZE / 2 - 25, 50, 50)
    level: int = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if leftArrow.IsPressed() or rightArrow.IsPressed():
                    if level == 1:
                        level = level + 1
                    elif level == 2:
                        level = 1
                    DrawInterface(level)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if level == 1:
                        level = level + 1
                    elif level == 2:
                        level = 1
                    DrawInterface(level)
                elif event.key == pygame.K_RETURN:
                    return level
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.update()

chosenLevel = Menu()
running: bool = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()