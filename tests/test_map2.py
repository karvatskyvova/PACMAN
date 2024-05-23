import unittest
import pygame
from unittest.mock import patch, MagicMock
from Pacman_map2 import setupMaze, setupGate, Wall, Block, startGame

class TestPacmanGame(unittest.TestCase):
    
    def setUp(self):
        # Initialize Pygame and create a screen
        pygame.init()
        self.screen = pygame.display.set_mode((606, 700))
        self.all_sprites_list = pygame.sprite.RenderPlain()
    
    def tearDown(self):
        # Quit Pygame after tests
        pygame.quit()

    def test_wall_creation(self):
        wall = Wall(10, 10, 30, 30, (255, 0, 0))
        self.assertEqual(wall.rect.top, 10)
        self.assertEqual(wall.rect.left, 10)
        self.assertEqual(wall.image.get_size(), (30, 30))
    
    def test_block_creation(self):
        block = Block((255, 255, 0), 4, 4)
        self.assertEqual(block.image.get_size(), (4, 4))
        self.assertEqual(block.rect.width, 4)
        self.assertEqual(block.rect.height, 4)
    
    @patch('pygame.sprite.spritecollide', return_value=False)
    def test_setupMaze(self, mock_spritecollide):
        wall_list, block_list = setupMaze(self.all_sprites_list)
        
        # Check the number of walls created
        self.assertEqual(len(wall_list), len(self.all_sprites_list) - len(block_list))
        
        # Check if blocks are created correctly
        self.assertGreater(len(block_list), 0)
        
        # Ensure blocks do not collide with walls
        for block in block_list:
            self.assertFalse(pygame.sprite.spritecollide(block, wall_list, False))

    def test_setupGate(self):
        gate = setupGate(self.all_sprites_list)
        self.assertEqual(len(gate), 1)
        
        gate_sprite = next(iter(gate))
        self.assertEqual(gate_sprite.rect.top, 242)
        self.assertEqual(gate_sprite.rect.left, 282)
        self.assertEqual(gate_sprite.rect.width, 42)
        self.assertEqual(gate_sprite.rect.height, 2)

    @patch('your_module.load_saved_settings', return_value=(1, 4))
    @patch('pygame.display.set_mode')
    @patch('pygame.font.Font')
    def test_startGame(self, mock_font, mock_display, mock_load_saved_settings):
        mock_display.return_value = MagicMock()
        mock_font.return_value = MagicMock()
        
        startGame(4)  

if __name__ == '__main__':
    unittest.main()
