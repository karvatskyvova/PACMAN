import pygame
from sys import argv, exit

pygame.init()
SCREEN_SIZE: int = 500
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE)) #Розмір вікна
pygame.display.set_caption("PACMAN")
pygame.display.set_icon(pygame.image.load("Resourses\icon.png")) #Значок вікна

def DrawArrow(x, y, direction):
    """Малює кнопки у вигляді стрілок для вибору рівня\n
    x, y: координати точки, в яку вказує стрілка
    direction: напрямок (right/left)"""
    if direction == "right":
        points = [(x, y), (x - 50, y - 25), (x - 50, y + 25)]
    elif direction == "left":
        points = [(x, y), (x + 50, y + 25), (x + 50, y - 25)]
    pygame.draw.polygon(screen, (255, 234, 0), points)

def PlaceText(topLeftX: int, topLeftY: int, text: str, textColor: tuple, backgroundColor: tuple, fontSize: float, centered: bool):
    """Додає текст на екран, шрифт - freesansbold\n
    topLeftX, topLeftY - координати верхньої лівої точки прямокутника з текстом\n
    text - зміст тексту\n
    textColor - колір тексту, формат: (х, х, х)\n
    backgroundColor - колір фону (не обов'язково), формат: (х, х, х)\n
    fontSize - розмір тексту\n
    centered - відцентрований текст чи ні. Якщо так, topLeftX та topLeftY будуть вказувати в центр тексту, якщо ні, то у лівий верхній кут"""
    font = pygame.font.Font("freesansbold.ttf", fontSize)
    renderedText = font.render(text, True, textColor, backgroundColor)
    textRectangle = renderedText.get_rect()
    if centered:
        textRectangle.center = (topLeftX, topLeftY)
    else:
        textRectangle.left = topLeftX
        textRectangle.top = topLeftY
    screen.blit(renderedText, textRectangle)

def MenuInterface(chosenLevel: int):
    """Малює інтерфейс меню (зображення та кнопки)"""
    #Логотип та фонове зображення
    logo = pygame.image.load("Resourses\logo.png")
    background1 = pygame.image.load("Resourses\level1.png")
    background2 = pygame.image.load("Resourses\level2.png")
    settings = pygame.image.load("Resourses\settings.png")
    settings = pygame.transform.smoothscale(settings, (30, 30))
    if chosenLevel == 1:
        screen.blit(background1, (0, 0))
    elif chosenLevel == 2:
        screen.blit(background2, (0, 0))
    screen.blit(logo, (35, 30))
    screen.blit(settings, (10, 10))
    #Кнопки вибору рівня
    DrawArrow(20, SCREEN_SIZE / 2, "left")
    DrawArrow(SCREEN_SIZE - 20, SCREEN_SIZE / 2, "right")
    PlaceText(SCREEN_SIZE / 2, SCREEN_SIZE / 4 * 3 + 65, f"Press ENTER to Start Level {chosenLevel}", (255, 234, 0), (0, 0, 0), 17, True)

def SettingsMenu(level: int, enemiesNum: int, enemiesSpeed: int)->tuple:
    screen.fill((255, 234, 0))
    close = pygame.image.load("Resourses\close.png")
    close = pygame.transform.smoothscale(close, (30, 30))
    screen.blit(close, (10, 10))
    closeButton = pygame.Rect(10, 10, 30, 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MouseOn(closeButton):
                    MenuInterface(level)
                    return enemiesNum, enemiesSpeed
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if MouseOn(closeButton):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()

def MouseOn(button: pygame.Rect)->bool:
    """Перевіряє чи знаходиться курсор миші над даною кнопкою класу pygame.Rect"""
    return button.collidepoint(pygame.mouse.get_pos())

def Menu()->tuple:
    """Стартове вікно гри. Вікривається одразу після запуску\n
    returns: номер обраного користувачем рівня, кількість та швидкість ворогів\n
    Якщо ці значення були передані через argv, одразу їх повертає"""
    MenuInterface(1)
    #Створення колізій для кнопок
    leftArrow = pygame.Rect(20, SCREEN_SIZE / 2 - 25, 50, 50)
    rightArrow = pygame.Rect(SCREEN_SIZE - 70, SCREEN_SIZE / 2 - 25, 50, 50)
    settingsButton = pygame.Rect(10, 10, 30, 30)
    #Значення номеру рівня, к-сті та швидкості ворогів за замовчуванням (ПОТРЕБУЄ УТОЧНЕННЯ)
    level: int = 1
    enemiesNum: int = 5
    enemiesSpeed: int = 5
    #Крайні значення номеру рівня, к-сті та швидкості ворогів (вик. для перевірок крайніх значень)
    levelMax: int = 2
    enemiesNumRange: tuple = (1, 10)
    enemiesSpeedRange: tuple = (1, 10)
    if len(argv) == 4: #Передача номеру рівня, к-сті ворогів та їх швидкості через argv
        try:
            if int(argv[1]) >= 1 and int(argv [1]) <= levelMax and int(argv[2]) >= enemiesNumRange[0] and int(argv[2]) <= enemiesNumRange[1] and int(argv[3]) >= enemiesSpeedRange[0] and int(argv[3]) <= enemiesSpeedRange[1]:
                return int(argv[1]), int(argv[2]), int(argv[3])
            else:
                print("Wrong argv numbers")
        except Exception:
            print("Wrong argv type, expected int")

    #Винесена логіка з event для скорочення коду (використовується при виборі рівнів)
    def LevelToLeft(level, levelMax):
        if level == 1:
            return levelMax
        else:
            return level - 1
            
    def LevelToRight(level, levelMax):
        if level == levelMax:
            return 1
        else:
            return level + 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MouseOn(leftArrow):
                    level = LevelToLeft(level, levelMax)
                    MenuInterface(level)
                elif MouseOn(rightArrow):
                    level = LevelToRight(level, levelMax)
                    MenuInterface(level)
                elif MouseOn(settingsButton):
                    enemiesNum, enemiesSpeed = SettingsMenu(level, enemiesNum, enemiesSpeed)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    level = LevelToLeft(level, levelMax)
                    MenuInterface(level)
                elif event.key == pygame.K_RIGHT:
                    level = LevelToRight(level, levelMax)
                    MenuInterface(level)
                elif event.key == pygame.K_RETURN:
                    return level, enemiesNum, enemiesSpeed
            elif event.type == pygame.QUIT:
                return
        if MouseOn(leftArrow) or MouseOn(rightArrow) or MouseOn(settingsButton):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()

if __name__ == "__main__":
    chosenLevel = Menu()
    print(chosenLevel)
    pygame.quit()
