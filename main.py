import asyncio
import Pacman_menu
import Pacman_map
import Pacman_map2
import Pacman_map3

async def play_level(level: int, enemies: int):
    while True:
        if level == 1:
            result = await Pacman_map.run(enemies)
        elif level == 2:
            result = await Pacman_map2.run(enemies)
        elif level == 3:
            result = await Pacman_map3.run(enemies)
        else:
            return "menu"

        if result == "restart":
            continue          # replay same level
        return result         # "menu" or "quit"

async def main():
    while True:
        level, enemies = await Pacman_menu.run()
        if level is None:
            return

        result = await play_level(level, enemies)

        if result == "quit":
            return
        # if "menu" -> loop back and show menu again

if __name__ == "__main__":
    asyncio.run(main())
