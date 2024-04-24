import pytest
import pygame
from Characters import Player, Ghost, Pink_directions, Blue_directions, Red_directions, Yellow_directions

# Fixture to initialize pygame
@pytest.fixture(scope="module")
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

# Fixture to create a Player object
@pytest.fixture
def player(init_pygame):
    # Initialize display for loading images
    pygame.display.set_mode((606, 606))
    return Player("Characters/PacmanRight.png", 30, 30)

# Fixture to create a Pink Ghost object
@pytest.fixture
def pink_ghost(init_pygame):
    # Initialize display for loading images
    pygame.display.set_mode((606, 606))
    return Ghost("Characters/Pink.png", 30, 30, Pink_directions)

# Fixture to create a Blue Ghost object
@pytest.fixture
def blue_ghost(init_pygame):
    # Initialize display for loading images
    pygame.display.set_mode((606, 606))
    return Ghost("Characters/Blue.png", 30, 30, Blue_directions)

# Fixture to create a Red Ghost object
@pytest.fixture
def red_ghost(init_pygame):
    # Initialize display for loading images
    pygame.display.set_mode((606, 606))
    return Ghost("Characters/Red.png", 30, 30, Red_directions)

# Fixture to create a Yellow Ghost object
@pytest.fixture
def yellow_ghost(init_pygame):
    # Initialize display for loading images
    pygame.display.set_mode((606, 606))
    return Ghost("Characters/Yellow.png", 30, 30, Yellow_directions)

# Test Player class
def test_player_movement(player):
    # Move player in different directions
    player.changespeed(5, 0)
    player.update([])
    assert player.rect.x == 5
    assert player.rect.y == 0

# Test Player class
def test_player_speed(player):
    # Test speed change for player
    player.changespeed(5, 0)
    assert player.change_x == 5
    assert player.change_y == 0

# Test Pink Ghost class
def test_pink_ghost_movement(pink_ghost):
    # Move pink ghost according to predefined directions
    initial_x, initial_y = pink_ghost.rect.x, pink_ghost.rect.y
    pink_ghost.update_direction()
    pink_ghost.update([], None)
    assert pink_ghost.rect.x != initial_x or pink_ghost.rect.y != initial_y

# Test Pink Ghost class
def test_pink_ghost_speed(pink_ghost):
    # Test speed change for pink ghost
    initial_speed_x, initial_speed_y = pink_ghost.change_x, pink_ghost.change_y
    pink_ghost.update_direction()
    assert pink_ghost.change_x != initial_speed_x or pink_ghost.change_y != initial_speed_y
# Test Blue Ghost class
def test_blue_ghost_movement(blue_ghost):
    # Move blue ghost according to predefined directions
    initial_x, initial_y = blue_ghost.rect.x, blue_ghost.rect.y
    blue_ghost.update_direction()
    blue_ghost.update([], None)
    assert blue_ghost.rect.x != initial_x or blue_ghost.rect.y != initial_y

# Test Blue Ghost class
def test_blue_ghost_speed(blue_ghost):
    # Test speed change for blue ghost
    initial_speed_x, initial_speed_y = blue_ghost.change_x, blue_ghost.change_y
    blue_ghost.update_direction()
    assert blue_ghost.change_x != initial_speed_x or blue_ghost.change_y != initial_speed_y

# Test Red Ghost class
def test_red_ghost_movement(red_ghost):
    # Move red ghost according to predefined directions
    initial_x, initial_y = red_ghost.rect.x, red_ghost.rect.y
    red_ghost.update_direction()
    red_ghost.update([], None)
    assert red_ghost.rect.x != initial_x or red_ghost.rect.y != initial_y

# Test Red Ghost class
def test_red_ghost_speed(red_ghost):
    # Test speed change for red ghost
    initial_speed_x, initial_speed_y = red_ghost.change_x, red_ghost.change_y
    red_ghost.update_direction()
    assert red_ghost.change_x != initial_speed_x or red_ghost.change_y != initial_speed_y

# Test Yellow Ghost class
def test_yellow_ghost_movement(yellow_ghost):
    # Move yellow ghost according to predefined directions
    initial_x, initial_y = yellow_ghost.rect.x, yellow_ghost.rect.y
    yellow_ghost.update_direction()
    yellow_ghost.update([], None)
    assert yellow_ghost.rect.x != initial_x or yellow_ghost.rect.y != initial_y

# Test Yellow Ghost class
def test_yellow_ghost_speed(yellow_ghost):
    # Test speed change for yellow ghost
    initial_speed_x, initial_speed_y = yellow_ghost.change_x, yellow_ghost.change_y
    yellow_ghost.update_direction()
    assert yellow_ghost.change_x != initial_speed_x or yellow_ghost.change_y != initial_speed_y

