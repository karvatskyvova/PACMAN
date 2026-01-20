import pygame


GHOST_SPEED_SCALE = 0.15  # 0.2 turns 15 -> 3, 30 -> 6 (adjust later)

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

GHOST_SPEED_SCALE = 0.2  # 0.2 means 15px -> 3px per frame

class Ghost(Player):
    def __init__(self, color, width, height, directions):
        super().__init__(color, width, height)
        self.directions = directions
        self.direction_index = 0
        self.steps_done = 0          # how many "frames" moved in current segment
        self.steps_target = 0        # how many frames this segment should last (scaled)
        self.reverse = False

    def _scale_speed(self, v: int) -> int:
        """Scale speed but never return 0 if v != 0."""
        if v == 0:
            return 0
        scaled = int(round(v * GHOST_SPEED_SCALE))
        if scaled == 0:
            return 1 if v > 0 else -1
        return scaled

    def _scale_steps(self, steps: int) -> int:
        """Increase steps so total distance stays the same after speed scaling."""
        # if speed is 0.2, steps must be /0.2 = *5
        scaled = int(round(steps / GHOST_SPEED_SCALE))
        return max(1, scaled)

    def update_direction(self):
        x, y, steps = self.directions[self.direction_index]

        # compute scaled target once per segment
        if self.steps_done == 0:
            self.steps_target = self._scale_steps(steps)

        if self.steps_done < self.steps_target:
            self.change_x = self._scale_speed(x)
            self.change_y = self._scale_speed(y)
            self.steps_done += 1
            return

        # segment finished → switch direction
        self.steps_done = 0

        if self.reverse:
            self.direction_index = (self.direction_index - 1) % len(self.directions)
        else:
            self.direction_index = (self.direction_index + 1) % len(self.directions)
            if self.direction_index == 0:
                self.reverse = True


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