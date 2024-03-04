import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self, walls):
        # Store the old position before updating
        old_x = self.rect.x
        old_y = self.rect.y

        # Update the position based on the speed
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Check for collisions with walls
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in wall_hit_list:
            # If the player collided with a wall, move them back to their old position
            self.rect.x = old_x
            self.rect.y = old_y

class Ghost(Player):
    def __init__(self, color, width, height, directions):
        super().__init__(color, width, height)
        self.directions = directions
        self.direction_index = 0
        self.steps = 0
        self.reverse = False

    def changespeed(self):
        try:
            x, y, steps = self.directions[self.direction_index]
            if self.steps < steps:
                self.change_x = x
                self.change_y = y
                self.steps += 1
            else:
                if self.reverse:
                    self.direction_index = (self.direction_index - 1) % len(self.directions)
                else:
                    self.direction_index = (self.direction_index + 1) % len(self.directions)
                    if self.direction_index == 0:
                        self.reverse = True

                x, y, _ = self.directions[self.direction_index]
                self.change_x = x
                self.change_y = y
                self.steps = 0
        except IndexError:
            pass

    def update(self, walls):
        old_x = self.rect.x
        old_y = self.rect.y

        self.changespeed()

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Check for collisions with walls
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in wall_hit_list:
            # If the ghost collided with a wall, move them back to their old position
            self.rect.x = old_x
            self.rect.y = old_y

Pink_directions = [
    [0, -1, 40],
    [1, 0, 120],
    [0, 1, 150],
    [-1, 0, 240],
    [0, 1, 70],
    [1, 0, 30],
    [0, -1, 30],
    [1, 0, 190],
    [0, 1, 30],
    [1, 0, 30],
    [0, 1, 30],
    [1, 0, 30],
    [0, -1, 150],
    [-1, 0, 70],
    [0, 1, 30],
    [-1, 0, 190],
    [0, -1, 120],
    [1, 0, 90]
]

Blue_directions = [
    [0, -1, 40],
    [1, 0, 120],
    [0, 1, 150],
    [1, 0, 30],
    [0, 1, 70],
    [-1, 0, 110],
    [0, 1, 30],
    [1, 0, 150],
    [0, -1, 150],
    [1, 0, 30],
    [0, -1, 120],
    [-1, 0, 30],
    [0, -1, 120],
    [-1, 0, 30],
    [0, -1, 30],
    [-1, 0, 70],
    [0, -1, 30],
    [1, 0, 150],
    [0, 1, 150],
    [-1, 0, 30],
    [0, 1, 30],
    [-1, 0, 30],
    [0, -1, 70],
    [-1, 0, 30],
    [0, 1, 70],
    [-1, 0, 120],
    [0, -1, 70],
    [1, 0, 50]
]

Red_directions = [
    [1, 0, 20],
    [0, -1, 40],
    [1, 0, 100],
    [0, 1, 70],
    [1, 0, 30],
    [0, -1, 30],
    [1, 0, 30],
    [0, -1, 150],
    [-1, 0, 150],
    [0, 1, 30],
    [1, 0, 150],
    [0, 1, 110],
    [-1, 0, 30],
    [0, -1, 70],
    [-1, 0, 110],
    [0, 1, 30],
    [-1, 0, 110],
    [0, 1, 70],
    [-1, 0, 30],
    [0, -1, 30],
    [-1, 0, 30],
    [0, -1, 150],
    [1, 0, 150],
    [0, 1, 30],
    [-1, 0, 150],
    [0, 1, 110],
    [1, 0, 30],
    [0, -1, 110],
    [1, 0, 110],
    [0, 1, 30],
    [1, 0, 10],
]

Yellow_directions = [
    [-1, 0, 20],
    [0, -1, 40],
    [1, 0, 50],
    [0, 1, 70],
    [-1, 0, 110],
    [0, -1, 70],
    [-1, 0, 30],
    [0, 1, 70],
    [-1, 0, 70],
    [0, 1, 150],
    [1, 0, 150],
    [0, -1, 30],
    [-1, 0, 110],
    [0, -1, 70],
    [1, 0, 30],
    [0, -1, 110],
    [1, 0, 90],
]

