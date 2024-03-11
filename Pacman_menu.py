import subprocess
import pygame, json
from sys import argv, exit
from os import path, system

pygame.init()
SCREEN_SIZE: int = 606
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE)) #Розмір вікна
pygame.display.set_caption("PACMAN")
pygame.display.set_icon(pygame.image.load("Resourses/icon.png")) #Значок вікна

def DrawArrow(x: int, y: int, direction: str, size: int, color: tuple):
    """Малює кнопки у вигляді стрілок для вибору рівня\n
    x, y: координати точки, в яку вказує стрілка
    direction: напрямок (right/left)
    size: розмір у пікселях (стрілка вписана у квадрат)
    color: колір стрілки"""
    if direction == "right":
        points = [(x, y), (x - size, y - size / 2), (x - size, y + size / 2)]
    elif direction == "left":
        points = [(x, y), (x + size, y + size / 2), (x + size, y - size / 2)]
    pygame.draw.polygon(screen, color, points)

def PlaceText(topLeftX: int, topLeftY: int, text: str, textColor: tuple, backgroundColor: tuple, fontSize: float, centered: bool):
    """Додає текст на екран, шрифт - freesansbold\n
    topLeftX, topLeftY - координати верхньої лівої точки прямокутника з текстом\n
    text - зміст тексту\n
    textColor - колір тексту, формат: (х, х, х)\n
    backgroundColor - колір фону (не обов'язково), формат: (х, х, х)\n
    fontSize - розмір тексту\n
    centered - відцентрований текст чи ні. Якщо так, topLeftX та topLeftY будуть вказувати в центр тексту"""
    font = pygame.font.Font("freesansbold.ttf", fontSize)
    renderedText = font.render(text, True, textColor, backgroundColor)
    textRectangle = renderedText.get_rect()
    if centered:
        textRectangle.center = (topLeftX, topLeftY)
    else:
        textRectangle.left = topLeftX
        textRectangle.top = topLeftY
    screen.blit(renderedText, textRectangle)

#Винесена логіка з event для скорочення коду (використовується при виборі значення стрілочками)
def Decrease(value: int, valueRange: tuple)->int:
    """Використовується для зменшення лівою стрілкою значення на 1
    value: поточне значення
    valueRange: діапазон допустимих значень value
    returns: оновлене значення"""
    if value == valueRange[0]:
        return valueRange[1]
    else:
        return value - 1
        
def Increase(value: int, valueRange: tuple)->int:
    """Використовується для збільшення правою стрілкою значення на 1
    value: поточне значення
    valueRange: діапазон допустимих значень value
    returns: оновлене значення"""
    if value == valueRange[1]:
        return valueRange[0]
    else:
        return value + 1
    
def MenuInterface(chosenLevel: int):
    """Малює інтерфейс меню (зображення та кнопки)"""
    #Логотип та фонове зображення
    logo = pygame.image.load("Resourses/logo.png")
    background1 = pygame.image.load("Resourses/level1.png")
    background2 = pygame.image.load("Resourses/level2.png")
    settings = pygame.image.load("Resourses/settings.png")
    settings = pygame.transform.smoothscale(settings, (30, 30))
    if chosenLevel == 1:
        screen.blit(background1, (0, 0))
    elif chosenLevel == 2:
        screen.blit(background2, (0, 0))
    screen.blit(logo, (68, 40))
    screen.blit(settings, (15, 15))
    #Кнопки вибору рівня
    DrawArrow(20, SCREEN_SIZE / 2, "left", 50, (255, 234, 0))
    DrawArrow(SCREEN_SIZE - 20, SCREEN_SIZE / 2, "right", 50, (255, 234, 0))
    PlaceText(SCREEN_SIZE / 2, SCREEN_SIZE / 4 * 3 + 60, f"Press ENTER to Start Level {chosenLevel}", (255, 234, 0), (0, 0, 0), 18, True)

def SettingsMenuInterface(enemiesNum: int):
    """Інтерфейс меню налаштувань"""
    screen.fill((255, 234, 0))
    close = pygame.image.load("Resourses/close.png")
    oneGhost = pygame.image.load("Resourses/ghost.png")
    manyGhosts = pygame.image.load("Resourses/ghosts.png")

    close = pygame.transform.smoothscale(close, (30, 30))
    oneGhost = pygame.transform.smoothscale(oneGhost, (40, 40))
    manyGhosts = pygame.transform.smoothscale(manyGhosts, (80, 40))
    
    screen.blit(close, (15, 15))
    screen.blit(oneGhost, (SCREEN_SIZE / 6 - 20, SCREEN_SIZE / 3 - 20))
    screen.blit(manyGhosts, ((SCREEN_SIZE - SCREEN_SIZE / 6) - 40, SCREEN_SIZE / 3 - 20))

    DrawArrow(SCREEN_SIZE / 3, SCREEN_SIZE / 3, "left", 20, (0, 0, 0))
    PlaceText(SCREEN_SIZE / 2, SCREEN_SIZE / 3, str(enemiesNum), (0, 0, 0), None, 30, True)
    DrawArrow(SCREEN_SIZE / 3 * 2, SCREEN_SIZE / 3, "right", 20, (0, 0, 0))

def SettingsMenu(level: int, enemiesNum: int, enemiesNumRange: tuple)->tuple:
    """Головна функція меню налаштувань"""
    SettingsMenuInterface(enemiesNum)
    closeButton = pygame.Rect(15, 15, 30, 30)
    enemNumLeftButton = pygame.Rect(SCREEN_SIZE / 3, SCREEN_SIZE / 3 - 10, 20, 20)
    enemNumRightButton = pygame.Rect(SCREEN_SIZE / 3 * 2 - 20, SCREEN_SIZE / 3 - 10, 20, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MouseOn(closeButton):
                    MenuInterface(level)
                    return enemiesNum
                elif MouseOn(enemNumLeftButton):
                    enemiesNum = Decrease(enemiesNum, enemiesNumRange)
                elif MouseOn(enemNumRightButton):
                    enemiesNum = Increase(enemiesNum, enemiesNumRange)
                SettingsMenuInterface(enemiesNum)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    MenuInterface(level)
                    return enemiesNum
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if MouseOn(closeButton) or MouseOn(enemNumLeftButton) or MouseOn(enemNumRightButton):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()

def load_saved_settings(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        level = data.get("Level", 1)
        enemiesNum = data.get("Number of Enemies", 4)
    return level, enemiesNum

def MouseOn(button: pygame.Rect)->bool:
    """Перевіряє чи знаходиться курсор миші над даною кнопкою класу pygame.Rect"""
    return button.collidepoint(pygame.mouse.get_pos())

def SaveData(filename: str, level: int, enemiesNum: int):
    """Записує останній вибір користувача (номер рівня, кількість ворогів) у json файл
    filename: ім'я сейв файлу (наприклад, PacmanSave.json)"""
    data = {"Level": level, "Number of Enemies": enemiesNum}
    with open(filename, 'w') as f:
        json.dump(data, f)

def ReadData(filename: str, levelMax: int, enemiesNumRange: tuple)->tuple:
    """Зчитує номер рівня, к-сть ворогів з вказаного сейв файлу\n
    filename: ім'я сейв файлу (наприклад, PacmanSave.json)\n
    levelMax - максимальне значення змінної level (використовується для перевірки даних у сейві)\n
    enemiesNumRange - діапазон значень enemiesNum"""
    if path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            level = data["Level"]
            enemiesNum = data["Number of Enemies"]
        try:
            if level < 1 or level > levelMax:
                raise Exception
            elif enemiesNum < enemiesNumRange[0] or enemiesNum > enemiesNumRange[1]:
                raise Exception
            else:
                return level, enemiesNum
        except:
            print("Error: Save File contains incorrect data")
    else:
        return None

def Menu() -> tuple:
    """Стартове вікно гри. Вікривається одразу після запуску\n
    returns: номер обраного користувачем рівня, кількість ворогів\n
    Якщо ці значення були передані через argv, одразу їх повертає"""
    # Значення номеру рівня, к-сті ворогів за замовчуванням
    level: int = 1
    enemiesNum: int = 2
    saveFile: str = "PacmanSave.json"
    # Крайні значення номеру рівня, к-сті ворогів (вик. для перевірок крайніх значень)
    levelMax: int = 2
    enemiesNumRange: tuple = (1, 4)
    
    if len(argv) == 4:  # Передача номеру рівня та к-сті ворогів через argv
        try:
            if 1 <= int(argv[1]) <= levelMax and enemiesNumRange[0] <= int(argv[2]) <= enemiesNumRange[1]:
                return int(argv[1]), int(argv[2])
            else:
                print("Wrong argv numbers")
        except ValueError:
            print("Wrong argv type, expected int")
    
    save = ReadData(saveFile, levelMax, enemiesNumRange)
    if save is not None:
        level, enemiesNum = save
    
    MenuInterface(level)
    # Створення колізій для кнопок
    leftArrow = pygame.Rect(20, SCREEN_SIZE / 2 - 25, 50, 50)
    rightArrow = pygame.Rect(SCREEN_SIZE - 70, SCREEN_SIZE / 2 - 25, 50, 50)
    settingsButton = pygame.Rect(15, 15, 30, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MouseOn(leftArrow):
                    level = Decrease(level, (1, levelMax))
                    MenuInterface(level)
                elif MouseOn(rightArrow):
                    level = Increase(level, (1, levelMax))
                    MenuInterface(level)
                elif MouseOn(settingsButton):
                    enemiesNum = SettingsMenu(level, enemiesNum, enemiesNumRange)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    level = Decrease(level, (1, levelMax))
                    MenuInterface(level)
                elif event.key == pygame.K_RIGHT:
                    level = Increase(level, (1, levelMax))
                    MenuInterface(level)
                elif event.key == pygame.K_RETURN:
                    if level == 1:
                        SaveData(saveFile, level, enemiesNum)
                        # Start the Pacman_map.py script using subprocess
                        subprocess.Popen(["python", "Pacman_map.py", str(level), str(enemiesNum)])
                        return level, enemiesNum
                elif event.key == pygame.K_ESCAPE:
                    enemiesNum = SettingsMenu(level, enemiesNum, enemiesNumRange)
            elif event.type == pygame.QUIT:
                return
        if MouseOn(leftArrow) or MouseOn(rightArrow) or MouseOn(settingsButton):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()

if __name__ == "__main__":
    userChoice = Menu()
    if userChoice != None:
        print(f"\nUSER CHOICE\nLevel: {userChoice[0]}\nNumber of Enemies: {userChoice[1]}\n")
    pygame.quit()
