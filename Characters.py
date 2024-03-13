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

    def check_valid_direction(self, direction, walls, gate_rect):
        # Check if the next direction goes out of the screen boundaries
        if (self.rect.left + direction[0] < 0 or self.rect.right + direction[0] > 600 or
                self.rect.top + direction[1] < 0 or self.rect.bottom + direction[1] > 600):
            return False

        # Check for collision with obstacles
        if pygame.sprite.spritecollide(self, walls, False):
            return False

        # Check for collision with gates
        if gate_rect.colliderect(self.rect.move(direction)):
            return False

        return True

    def update_direction(self):
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

    def update(self, walls, gate_rect):
        old_x = self.rect.x
        old_y = self.rect.y

        self.update_direction()

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Check for collisions with walls
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in wall_hit_list:
            # If the ghost collided with a wall, move them back to their old position
            self.rect.x = old_x
            self.rect.y = old_y

Pink_directions = [
    [0,-15,10],
    [15,0,9],
    [0,15,11],
    [-15,0,23],
    [0,15,7],
    [15,0,3],
    [0,-15,3],
    [15,0,19],
    [0,15,3],
    [15,0,3],
    [0,15,3],
    [15,0,3],
    [0,-15,15],
    [-15,0,7],
    [0,15,3],
    [-15,0,19],
    [0,-15,11],
    [15,0,9]
]

Blue_directions = [
    [0,-15,4],
    [15,0,9],
    [0,15,11],
    [15,0,3],
    [0,15,7],
    [-15,0,11],
    [0,15,3],
    [15,0,15],
    [0,-15,15],
    [15,0,3],
    [0,-15,11],
    [-15,0,3],
    [0,-15,11],
    [-15,0,3],
    [0,-15,3],
    [-15,0,7],
    [0,-15,3],
    [15,0,15],
    [0,15,15],
    [-15,0,3],
    [0,15,3],
    [-15,0,3],
    [0,-15,7],
    [-15,0,3],
    [0,15,7],
    [-15,0,11],
    [0,-15,7],
    [15,0,5]
]

Red_directions = [
    [30,0,2],
    [0,-15,4],
    [15,0,10],
    [0,15,7],
    [15,0,3],
    [0,-15,3],
    [15,0,3],
    [0,-15,15],
    [-15,0,15],
    [0,15,3],
    [15,0,15],
    [0,15,11],
    [-15,0,3],
    [0,-15,7],
    [-15,0,11],
    [0,15,3],
    [-15,0,11],
    [0,15,7],
    [-15,0,3],
    [0,-15,3],
    [-15,0,3],
    [0,-15,15],
    [15,0,15],
    [0,15,3],
    [-15,0,15],
    [0,15,11],
    [15,0,3],
    [0,-15,11],
    [15,0,11],
    [0,15,3],
    [15,0,1],
]


Yellow_directions = [
    [-30,0,2],
    [0,-15,4],
    [15,0,5],
    [0,15,7],
    [-15,0,11],
    [0,-15,7],
    [-15,0,3],
    [0,15,7],
    [-15,0,7],
    [0,15,15],
    [15,0,15],
    [0,-15,3],
    [-15,0,11],
    [0,-15,7],
    [15,0,3],
    [0,-15,11],
    [15,0,9],
]