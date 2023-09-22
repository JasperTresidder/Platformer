from settings import *

class Character(pg.sprite.Sprite):
    def __init__(self, space: pm.space.Space, screen: pg.Surface, wall_jump):
        self.space = space
        self.screen = screen
        self.current_animation = 'idle'
        self.previous_animation = 'idle'
        self.wall_jump = wall_jump
        super().__init__()
        self.body = pm.Body()  # Create a Body
        self.body.position = SCREEN_SIZE[0] / 50, 4*SCREEN_SIZE[1]/10  # Set the position of the body

        self.poly = pm.Poly.create_box(self.body, ((SCREEN_SIZE[0]/screen_tiles[0]) - 16, SCREEN_SIZE[1]/screen_tiles[1] - 5), 5)
        self.poly.color = pg.Color("pink")
        self.poly.mass = 10  # Set the mass on the shape
        self.poly.elasticity = 1
        self.poly.density = 1000
        self.poly.friction = 1
        self.body.moment = 100000000000000
        self.space.add(self.body, self.poly)  # Add both body and shape to the simulation
        self.left, self.right, self.up, self.down = False, False, False, False
        self.can_jump = False

        self.size = (100*SCREEN_SIZE[0]/1920, 100*SCREEN_SIZE[1]/1080)
        # self.img = pg.image.load('../data/assets/square_normal.PNG').convert_alpha()
        self.animations = dict()
        for key, value in Frog_Animations.items():
            self.animations[key] = [pg.transform.scale(img, self.size) for img in value]
        self.frame = 0

    def handle_keydown(self, event: pg.event.Event):
        if event.key == pg.K_d:
            # Right
            self.right = True
            self.previous_animation = self.current_animation
            self.current_animation = 'run'
        if event.key == pg.K_a:
            # Left
            self.left = True
            self.previous_animation = self.current_animation
            self.current_animation = 'run_left'
        if (event.key == pg.K_w or event.key == pg.K_SPACE) and self.can_jump:
            # UP
            self.up = True
            self.previous_animation = self.current_animation
            if 'left' in self.previous_animation:
                self.current_animation = 'jump_left'
            else:
                self.current_animation = 'jump'

    def handle_keyup(self, event: pg.event.Event):
        if event.key == pg.K_d:
            # Right
            self.right = False
        if event.key == pg.K_a:
            # Left
            self.left = False

    def update_animation_wall(self, collisions):
        wall_slide_speed = 5
        velocity_x = self.body.velocity.x
        velocity_y = self.body.velocity.y


        if (0, 1) in collisions:  # Touching ground
            self.can_jump = True
            if not pg.key.get_pressed()[pg.K_d] and not pg.key.get_pressed()[pg.K_a]:
                self.previous_animation = self.current_animation
                if 'left' in self.previous_animation:
                    self.current_animation = 'idle_left'
                else:
                    self.current_animation = 'idle'

        if (-1, 0) in collisions:  # Touching Right wall moving Left
            self.left = False
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
            if not pg.key.get_pressed()[pg.K_a]:
                self.body.position = [self.body.position.x + 0.1, self.body.position.y]
                self.current_animation = 'fall'
        elif pg.key.get_pressed()[pg.K_a]:
            self.left = True
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
            self.right = False
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
            if not pg.key.get_pressed()[pg.K_d]:
                self.body.position = [self.body.position.x - 0.1, self.body.position.y]
                self.current_animation = 'fall'
        elif pg.key.get_pressed()[pg.K_d]:
            self.right = True
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
    
    def update_animation_push_object(self, collisions, collisions_wall, push_objects):
        speed = 1.5 * 130/FRAMERATE
        velocity_x = self.body.velocity.x
        velocity_y = self.body.velocity.y
        if (0, 1) in collisions:  # Touching ground
            self.can_jump = True
            if not pg.key.get_pressed()[pg.K_d] and not pg.key.get_pressed()[pg.K_a]:
                self.previous_animation = self.current_animation
                if 'left' in self.previous_animation:
                    self.current_animation = 'idle_left'
                else:
                    self.current_animation = 'idle'
            elif pg.key.get_pressed()[pg.K_d]:
                self.previous_animation = self.current_animation
                self.current_animation = 'run'
            elif pg.key.get_pressed()[pg.K_a]:
                self.previous_animation = self.current_animation
                self.current_animation = 'run_left'

        if (-1, 0) in collisions:  # Touching left wall
            self.previous_animation = self.current_animation
            self.current_animation = 'run_left'
            if (-1, 0) not in collisions_wall:
                self.body.position = (self.body.position.x, self.body.position.y)  # !!!!!
                push_objects[0].body.position = (push_objects[0].body.position.x - speed, push_objects[0].body.position.y)
            else:
                self.body.position = (self.body.position.x + PLAYER_SPEED, self.body.position.y)

        if (1, 0) in collisions:  # Touching right wall
            self.previous_animation = self.current_animation
            self.current_animation = 'run'
            if (1, 0) not in collisions_wall:
                self.body.position = (self.body.position.x, self.body.position.y) # !!!!!
                push_objects[0].body.position = (push_objects[0].body.position.x + speed, push_objects[0].body.position.y)
            else:
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
        if self.right:
            self.body.position += (PLAYER_SPEED, 0)
        if self.left:
            self.body.position += (-PLAYER_SPEED, 0)
        if not self.left and not self.right:
            self.body.velocity = (0, self.body.velocity.y)
        if self.up:
            self.body.velocity += (0, -870)
            self.up = False
            self.can_jump = False

    def draw(self, clock):
        if clock % int(3*FRAMERATE/60) == 0:
            self.frame += 1
        if self.frame >= len(self.animations[self.current_animation]):
            self.frame = 0
        self.screen.blit(self.animations[self.current_animation][self.frame], (self.body.position.x - self.size[0]/2, self.body.position.y - self.size[1]/2 - self.size[1]/8), self.animations[self.current_animation][self.frame].get_rect())







