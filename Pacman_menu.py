import pygame
import json
import sys
import asyncio
from sys import argv
from os import path as ospath
from pathlib import Path
from utils import asset, is_web

# --------------------------
# Helpers (pygbag-safe paths)
# --------------------------


# --------------------------
# Globals (created in run())
# --------------------------
SCREEN_SIZE = 606
screen = None

# --------------------------
# UI helpers
# --------------------------
def DrawArrow(x: int, y: int, direction: str, size: int, color: tuple):
    if direction == "right":
        points = [(x, y), (x - size, y - size / 2), (x - size, y + size / 2)]
    else:  # "left"
        points = [(x, y), (x + size, y + size / 2), (x + size, y - size / 2)]
    pygame.draw.polygon(screen, color, points)

def PlaceText(x: int, y: int, text: str, textColor: tuple, backgroundColor, fontSize: int, centered: bool):
    font = pygame.font.Font(None, fontSize)  # default font is safest for web
    rendered = font.render(text, True, textColor, backgroundColor)
    rect = rendered.get_rect()
    if centered:
        rect.center = (x, y)
    else:
        rect.left = x
        rect.top = y
    screen.blit(rendered, rect)

def MouseOn(button: pygame.Rect) -> bool:
    return button.collidepoint(pygame.mouse.get_pos())

def Decrease(value: int, valueRange: tuple) -> int:
    return valueRange[1] if value == valueRange[0] else value - 1

def Increase(value: int, valueRange: tuple) -> int:
    return valueRange[0] if value == valueRange[1] else value + 1

def SaveData(filename: str, level: int, enemiesNum: int):
    data = {"Level": level, "Number of Enemies": enemiesNum}
    with open(filename, "w") as f:
        json.dump(data, f)

def ReadData(filename: str, levelMax: int, enemiesNumRange: tuple):
    if not ospath.exists(filename):
        return None
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        level = int(data["Level"])
        enemiesNum = int(data["Number of Enemies"])
        if not (1 <= level <= levelMax):
            return None
        if not (enemiesNumRange[0] <= enemiesNum <= enemiesNumRange[1]):
            return None
        return level, enemiesNum
    except Exception:
        return None

# --------------------------
# Cached images (loaded once)
# --------------------------
_assets = {}

def img(name: str, fallback_size=(SCREEN_SIZE, SCREEN_SIZE)):
    key = ("Resources", name)
    if key in _assets:
        return _assets[key]

    try:
        surf = pygame.image.load(asset("Resources", name)).convert_alpha()
    except Exception:
        surf = pygame.Surface(fallback_size)
        surf.fill((0, 0, 0))  # fallback black

    _assets[key] = surf
    return surf


def MenuInterface(chosenLevel: int):
    logo_raw = img("logo.png")

    # Scale logo relative to menu/screen width (adjust 0.85 to taste)
    target_w = int(SCREEN_SIZE * 0.72)
    scale = target_w / logo_raw.get_width()
    target_h = int(logo_raw.get_height() * scale)

    logo = pygame.transform.smoothscale(logo_raw, (target_w, target_h))

    # Position: top-center with padding
    logo_rect = logo.get_rect(midtop=(SCREEN_SIZE // 2, 6))
    screen.blit(logo, logo_rect)

    settings = pygame.transform.smoothscale(img("settings.png"), (30, 30))

    background1 = img("level1.png")
    background2 = img("level2.png")
    background3 = img("level3.png")  # optional; fallback black if missing

    if chosenLevel == 1:
        screen.blit(background1, (0, 0))
    elif chosenLevel == 2:
        screen.blit(background2, (0, 0))
    else:
        screen.blit(background3, (0, 0))

    screen.blit(logo, (68, 40))
    screen.blit(settings, (15, 15))

    DrawArrow(20, SCREEN_SIZE / 2, "left", 50, (255, 234, 0))
    DrawArrow(SCREEN_SIZE - 20, SCREEN_SIZE / 2, "right", 50, (255, 234, 0))

    PlaceText(
        SCREEN_SIZE / 2, SCREEN_SIZE / 4 * 3 + 60,
        f"Press ENTER to Start Level {chosenLevel}",
        (255, 234, 0), None, 18, True
    )


def SettingsMenuInterface(enemiesNum: int):
    screen.fill((255, 234, 0))
    close = pygame.transform.smoothscale(img("close.png"), (30, 30))
    oneGhost = pygame.transform.smoothscale(img("ghost.png"), (40, 40))
    manyGhosts = pygame.transform.smoothscale(img("ghosts.png"), (80, 40))

    screen.blit(close, (15, 15))
    screen.blit(oneGhost, (SCREEN_SIZE / 6 - 20, SCREEN_SIZE / 3 - 20))
    screen.blit(manyGhosts, ((SCREEN_SIZE - SCREEN_SIZE / 6) - 40, SCREEN_SIZE / 3 - 20))

    DrawArrow(SCREEN_SIZE / 3, SCREEN_SIZE / 3, "left", 20, (0, 0, 0))
    PlaceText(SCREEN_SIZE / 2, SCREEN_SIZE / 3, str(enemiesNum), (0, 0, 0), None, 30, True)
    DrawArrow(SCREEN_SIZE / 3 * 2, SCREEN_SIZE / 3, "right", 20, (0, 0, 0))

async def SettingsMenu_async(level: int, enemiesNum: int, enemiesNumRange: tuple) -> int:
    SettingsMenuInterface(enemiesNum)

    closeButton = pygame.Rect(15, 15, 30, 30)
    leftBtn = pygame.Rect(SCREEN_SIZE / 3, SCREEN_SIZE / 3 - 10, 20, 20)
    rightBtn = pygame.Rect(SCREEN_SIZE / 3 * 2 - 20, SCREEN_SIZE / 3 - 10, 20, 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return enemiesNum

            if event.type == pygame.MOUSEBUTTONDOWN:
                if MouseOn(closeButton):
                    MenuInterface(level)
                    return enemiesNum
                if MouseOn(leftBtn):
                    enemiesNum = Decrease(enemiesNum, enemiesNumRange)
                    SettingsMenuInterface(enemiesNum)
                if MouseOn(rightBtn):
                    enemiesNum = Increase(enemiesNum, enemiesNumRange)
                    SettingsMenuInterface(enemiesNum)

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    MenuInterface(level)
                    return enemiesNum

        if MouseOn(closeButton) or MouseOn(leftBtn) or MouseOn(rightBtn):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()

        if is_web():
            await asyncio.sleep(0)

async def Menu_async() -> tuple:
    level = 1
    enemiesNum = 2

    levelMax = 3
    enemiesNumRange = (1, 4)
    saveFile = asset("PacmanSave.json")

    # argv shortcut (desktop only)
    if len(argv) == 4:
        try:
            lv = int(argv[1])
            en = int(argv[2])
            if 1 <= lv <= levelMax and enemiesNumRange[0] <= en <= enemiesNumRange[1]:
                return lv, en
        except Exception:
            pass

    saved = ReadData(saveFile, levelMax, enemiesNumRange)
    if saved is not None:
        level, enemiesNum = saved

    MenuInterface(level)

    leftArrow = pygame.Rect(20, SCREEN_SIZE / 2 - 25, 50, 50)
    rightArrow = pygame.Rect(SCREEN_SIZE - 70, SCREEN_SIZE / 2 - 25, 50, 50)
    settingsButton = pygame.Rect(15, 15, 30, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if MouseOn(leftArrow):
                    level = Decrease(level, (1, levelMax))
                    MenuInterface(level)
                elif MouseOn(rightArrow):
                    level = Increase(level, (1, levelMax))
                    MenuInterface(level)
                elif MouseOn(settingsButton):
                    enemiesNum = await SettingsMenu_async(level, enemiesNum, enemiesNumRange)
                    # redraw after returning
                    MenuInterface(level)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    level = Decrease(level, (1, levelMax))
                    MenuInterface(level)
                elif event.key == pygame.K_RIGHT:
                    level = Increase(level, (1, levelMax))
                    MenuInterface(level)
                elif event.key == pygame.K_RETURN:
                    SaveData(saveFile, level, enemiesNum)
                    return level, enemiesNum
                elif event.key == pygame.K_ESCAPE:
                    enemiesNum = await SettingsMenu_async(level, enemiesNum, enemiesNumRange)
                    MenuInterface(level)

        if MouseOn(leftArrow) or MouseOn(rightArrow) or MouseOn(settingsButton):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()

        if is_web():
            await asyncio.sleep(0)

async def run():
    global screen

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("PACMAN")

    # icon AFTER display init
    pygame.display.set_icon(img("icon.png"))

    return await Menu_async()

if __name__ == "__main__":
    choice = asyncio.run(run())
    print(choice)
    pygame.quit()
