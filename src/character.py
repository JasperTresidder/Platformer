from src.settings import *


class Character(pg.sprite.Sprite):
    def __init__(self, space: pm.space.Space, screen: pg.Surface, wall_jump):
        self.space = space
        self.screen = screen
        self.current_animation = 'idle'
        self.previous_animation = 'idle'
        self.wall_jump = wall_jump
        self.screen_adjust = 0
        if SCREEN_SIZE[1] < 1080:
            self.screen_adjust = 135
        super().__init__()
        self.body = pm.Body()  # Create a Body
        self.body.position = SCREEN_SIZE[0] / 50, 4 * SCREEN_SIZE[1] / 10  # Set the position of the body

        self.poly = pm.Poly.create_box(self.body,
                                       ((SCREEN_SIZE[0] / screen_tiles[0]) - 16, SCREEN_SIZE[1] / screen_tiles[1] - 5),
                                       5)
        self.poly.color = pg.Color("pink")
        self.poly.mass = 10  # Set the mass on the shape
        self.poly.elasticity = 0
        self.poly.density = 1000
        self.poly.friction = 1
        self.body.moment = 100000000000000
        self.space.add(self.body, self.poly)  # Add both body and shape to the simulation
        self.left, self.right, self.up, self.down = False, False, False, False
        self.can_move_left = True
        self.can_move_right = True
        self.can_jump = False

        self.size = (100 * SCREEN_SIZE[0] / 1920, 100 * SCREEN_SIZE[1] / 1080)
        # self.img = pg.image.load('../data/assets/square_normal.PNG').convert_alpha()
        self.animations = dict()
        for key, value in Frog_Animations.items():
            self.animations[key] = [pg.transform.scale(img, self.size) for img in value]
        self.frame = 0

    def handle_keydown(self, event: pg.event.Event):
        if event.key == pg.K_d or event.key == pg.K_RIGHT:
            # Right
            self.right = True
            self.previous_animation = self.current_animation
            self.current_animation = 'run'
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            # Left
            self.left = True
            self.previous_animation = self.current_animation
            self.current_animation = 'run_left'
        if (event.key == pg.K_w or event.key == pg.K_SPACE or event.key == pg.K_UP) and self.can_jump:
            # UP
            self.up = True
            self.previous_animation = self.current_animation
            if 'left' in self.previous_animation:
                self.current_animation = 'jump_left'
            else:
                self.current_animation = 'jump'

    def handle_keydown_ai(self, event: pg.event.Event):
        if event['key'] == pg.K_d or event['key'] == pg.K_RIGHT:
            # Right
            self.right = True
            self.previous_animation = self.current_animation
            self.current_animation = 'run'
        if event['key'] == pg.K_a or event['key'] == pg.K_LEFT:
            # Left
            self.left = True
            self.previous_animation = self.current_animation
            self.current_animation = 'run_left'
        if (event['key'] == pg.K_w or event['key'] == pg.K_SPACE or event['key'] == pg.K_UP) and self.can_jump:
            # UP
            self.up = True
            self.previous_animation = self.current_animation
            if 'left' in self.previous_animation:
                self.current_animation = 'jump_left'
            else:
                self.current_animation = 'jump'

    def handle_keyup(self, event: pg.event.Event):
        if event.key == pg.K_d or event.key == pg.K_RIGHT:
            # Right
            self.right = False
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            # Left
            self.left = False

    def handle_keyup_ai(self, event: pg.event.Event):
        if event['key'] == pg.K_d or event['key'] == pg.K_RIGHT:
            # Right
            self.right = False
        if event['key'] == pg.K_a or event['key'] == pg.K_LEFT:
            # Left
            self.left = False

    def update_animation_wall(self, collisions):
        wall_slide_speed = 5
        velocity_x = self.body.velocity.x
        velocity_y = self.body.velocity.y

        if (0, 1) in collisions:  # Touching ground
            self.can_jump = True
            if not self.left and not self.right:
                self.previous_animation = self.current_animation
                if 'left' in self.previous_animation:
                    self.current_animation = 'idle_left'
                else:
                    self.current_animation = 'idle'

        if (-1, 0) in collisions:  # Touching Right wall moving Left
            self.can_move_left = False
            if (0, 1) not in collisions and velocity_y > wall_slide_speed:
                self.previous_animation = self.current_animation
                self.current_animation = 'wall_jump_left'
                if self.wall_jump:
                    self.can_jump = True
                else:
                    self.can_jump = False
            elif (0, 1) in collisions:
                self.previous_animation = self.current_animation
                self.current_animation = 'idle'
            if velocity_y > 80:
                self.body.velocity = (velocity_x, 80)
            if not self.left:
                self.body.position = [self.body.position.x + 0.1, self.body.position.y]
                self.current_animation = 'fall'
        elif self.left:
            self.can_move_left = True
            if (0, 1) not in collisions:
                self.previous_animation = self.current_animation
                if velocity_y > 40:
                    self.current_animation = 'fall_left'
                else:
                    self.current_animation = 'jump_left'
            else:
                self.previous_animation = self.current_animation
                self.current_animation = 'run_left'

        if (1, 0) in collisions:  # Touching Left wall moving Right
            self.can_move_right = False
            if (0, 1) not in collisions and velocity_y > wall_slide_speed:
                self.previous_animation = self.current_animation
                self.current_animation = 'wall_jump'
                if self.wall_jump:
                    self.can_jump = True
                else:
                    self.can_jump = False
            elif (0, 1) in collisions:
                self.previous_animation = self.current_animation
                self.current_animation = 'idle'
            if velocity_y > 80:
                self.body.velocity = (velocity_x, 80)
            if not self.right:
                self.body.position = [self.body.position.x - 0.1, self.body.position.y]
                self.current_animation = 'fall'
        elif self.right:
            self.can_move_right = True
            if (0, 1) not in collisions:
                self.previous_animation = self.current_animation
                if velocity_y > 40:
                    self.current_animation = 'fall'
                else:
                    self.current_animation = 'jump'
            else:
                self.previous_animation = self.current_animation
                self.current_animation = 'run'

        if (1, 0) not in collisions and (-1, 0) not in collisions and (0, 1) not in collisions and -velocity_y > 1:
            self.previous_animation = self.current_animation
            if 'left' in self.previous_animation:
                if velocity_y > 40:
                    self.current_animation = 'fall_left'
                else:
                    self.current_animation = 'jump_left'
            else:
                if velocity_y > 40:
                    self.current_animation = 'fall'
                else:
                    self.current_animation = 'jump'

    def update_animation_push_object(self, collisions, push_objects, walls):
        speed = 3 * 130 / FRAMERATE
        velocity_x = self.body.velocity.x
        velocity_y = self.body.velocity.y
        touching = [box for box in push_objects if self.poly.shapes_collide(box.poly).points]
        if (0, 1) in collisions:  # Touching ground
            self.can_jump = True
            if not self.left and not self.right:
                self.previous_animation = self.current_animation
                if 'left' in self.previous_animation:
                    self.current_animation = 'idle_left'
                else:
                    self.current_animation = 'idle'
            elif self.right:
                self.previous_animation = self.current_animation
                self.current_animation = 'run'
            elif self.left:
                self.previous_animation = self.current_animation
                self.current_animation = 'run_left'
        if (0, -1) in collisions:  # Touching bottom
            self.can_jump = True
            if not self.left and not self.right:
                self.previous_animation = self.current_animation
                if 'left' in self.previous_animation:
                    self.current_animation = 'idle_left'
                else:
                    self.current_animation = 'idle'
            elif self.right:
                self.previous_animation = self.current_animation
                self.current_animation = 'run'
            elif self.left:
                self.previous_animation = self.current_animation
                self.current_animation = 'run_left'

        if (-1, 0) in collisions:  # Touching left wall
            self.previous_animation = self.current_animation
            self.current_animation = 'run_left'
            for box in touching:
                wall_collide = []
                for wall in walls:
                    normal = box.poly.shapes_collide(wall.poly).normal
                    wall_collide.append((round(normal.x), round(normal.y)))
                if (-1, 0) not in wall_collide:
                    box.body.position = (box.body.position.x - speed, box.body.position.y)
            self.body.position = (self.body.position.x + PLAYER_SPEED, self.body.position.y)

        if (1, 0) in collisions:  # Touching right wall
            self.previous_animation = self.current_animation
            self.current_animation = 'run'
            for box in touching:
                wall_collide = []
                for wall in walls:
                    normal = box.poly.shapes_collide(wall.poly).normal
                    wall_collide.append((round(normal.x), round(normal.y)))
                if (1, 0) not in wall_collide:
                    box.body.position = (box.body.position.x + speed, box.body.position.y)
            self.body.position = (self.body.position.x - PLAYER_SPEED, self.body.position.y)

        if (1, 0) not in collisions and (-1, 0) not in collisions and (0, 1) not in collisions and -velocity_y > 1:
            self.previous_animation = self.current_animation
            if 'left' in self.previous_animation:
                if velocity_y > 40:
                    self.current_animation = 'fall_left'
                else:
                    self.current_animation = 'jump_left'
            else:
                if velocity_y > 40:
                    self.current_animation = 'fall'
                else:
                    self.current_animation = 'jump'

    def update(self):
        self.body.angle = 0
        if self.right and self.can_move_right and 'wall' not in self.current_animation:
            self.body.position += (PLAYER_SPEED*SCREEN_SIZE[0]/1920 + self.screen_adjust/230, 0)
        if self.left and self.can_move_left and 'wall' not in self.current_animation:
            self.body.position += (-PLAYER_SPEED*SCREEN_SIZE[0]/1920 - self.screen_adjust/230, 0)
        if not self.left and not self.right:
            self.body.velocity = (0, self.body.velocity.y)
        if self.up:
            self.body.velocity += (0, -870*SCREEN_SIZE[1]/1080 - self.screen_adjust)
            self.up = False
            self.can_jump = False

    def draw(self, clock, started):
        if clock % int(3 * FRAMERATE / 60) == 0:
            if started:
                self.frame += 1
        if self.frame >= len(self.animations[self.current_animation]):
            self.frame = 0
        self.screen.blit(self.animations[self.current_animation][self.frame], (
        self.body.position.x - self.size[0] / 2, self.body.position.y - self.size[1] / 2 - self.size[1] / 8),
                         self.animations[self.current_animation][self.frame].get_rect())
