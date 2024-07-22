import os
import pickle
import sys
from pymunk.pygame_util import DrawOptions
from src.character import Character
from src.settings import *
from src.wall import Wall
from src.push_obstacle import Obstacle
from src.spike import Spike
from src.flag import Flag
from src.item import Item
from src.timer import Timer
from src.end_level_text import Menu
from src.ai import Ai

BACKGROUNDS = [
    pg.image.load('data/raw/Background/' + filename).convert_alpha()
    for filename in os.listdir('data/raw/Background/') if
    'png' in filename
]
BACKGROUNDS = [pg.transform.scale(image, SCREEN_SIZE) for image in BACKGROUNDS]
BACKGROUND = pg.Surface(SCREEN_SIZE)
for image in BACKGROUNDS:
    BACKGROUND.blit(image, (0, 0), image.get_rect())


def load_level(level_number: int):
    filename1, filename2 = 'data/tiled/level' + str(level_number) + '_Tile Layer 1.csv', 'data/tiled/level' + str(
        level_number) + '_Tile Layer 2.csv'
    filename1, filename2 = resource_path(filename1), resource_path(filename2)
    level = []
    level_box = []
    item = None
    FLAG_LOCATION_1 = None
    FLAG_LOCATION_2 = None
    level_spikes = []
    level_flag = None
    level.append(Wall(SPACE, (2000, 100), (-100, -100), True))
    level.append(Wall(SPACE, (100, 2000), (-100, -100), True))
    level.append(Wall(SPACE, (100, 2000), (SCREEN_SIZE[0], -100), True))
    level.append(Wall(SPACE, (2000, 100), (-100, SCREEN_SIZE[1]), True))
    data = open(filename1)
    array = np.loadtxt(data, delimiter=",")
    data = open(filename2)
    array2 = np.loadtxt(data, delimiter=",")
    LEVEL_IMAGE = pg.image.load(resource_path('data/tiled/level' + str(level_number) + '.png')).convert_alpha()
    LEVEL_IMAGE = pg.transform.scale(LEVEL_IMAGE, SCREEN_SIZE)
    for j, row in enumerate(array):
        for i, point in enumerate(row):
            if point not in [-1, 0]:
                level.append(Wall(SPACE, (SCREEN_SIZE[0] / screen_tiles[0], SCREEN_SIZE[1] / screen_tiles[1]),
                                  (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                   j * SCREEN_SIZE[1] / screen_tiles[1] + 0.06)))
            if array2[j][i] == 215:
                level_box.append(Obstacle(SCREEN, SPACE, (17 * SCREEN_SIZE[0] / (10 * screen_tiles[0]) - 0.01,
                                                          17 * SCREEN_SIZE[1] / (10 * screen_tiles[1]) - 0.1), (
                                              i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                              (j - 1) * SCREEN_SIZE[1] / screen_tiles[1] + 0.06)))
            if array2[j][i] == 210:
                FLAG_LOCATION_1 = (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                                             j * SCREEN_SIZE[1] / screen_tiles[1] - SCREEN_SIZE[1] / screen_tiles[1])
                level_flag = Flag(SCREEN, SPACE, (SCREEN_SIZE[0] / screen_tiles[0], 2*SCREEN_SIZE[1] / screen_tiles[1]), (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                                             j * SCREEN_SIZE[1] / screen_tiles[1] - SCREEN_SIZE[1] / screen_tiles[1]))
            if array2[j][i] == 122:
                FLAG_LOCATION_2 = (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                                                             j * SCREEN_SIZE[1] / screen_tiles[1] - SCREEN_SIZE[1] / screen_tiles[1])
            if array2[j][i] == 105:
                item = Item(SCREEN, SPACE,
                            (SCREEN_SIZE[0] / (2 * screen_tiles[0]), SCREEN_SIZE[1] / (2 * screen_tiles[1])),
                            (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06,
                             j * SCREEN_SIZE[1] / screen_tiles[1] + 0.06))
            if point == 0:
                level_spikes.append(
                    Spike(SPACE, (SCREEN_SIZE[0] / screen_tiles[0], SCREEN_SIZE[1] / (3 * screen_tiles[1])),
                          (i * SCREEN_SIZE[0] / screen_tiles[0] + 0.06, (j * SCREEN_SIZE[1] / screen_tiles[1]) + (
                                  2 * SCREEN_SIZE[1] / (3 * screen_tiles[1])) + 0.06)))
    return level, level_box, level_spikes, level_flag, FLAG_LOCATION_1, FLAG_LOCATION_2, item, LEVEL_IMAGE


class App:
    def __init__(self, screen: pg.Surface, space: pm.Space):
        pg.display.set_caption("Flag Rush")
        icon = pg.image.load("data\icon\icon.png").convert_alpha()
        pg.display.set_icon(icon)
        self.screen = screen
        self.space = space
        self.started = False
        self.can_start = False
        self.curr_fps = FRAMERATE
        self.space.gravity = 0, 1800  # * 1080/SCREEN_SIZE[1]
        self.game_clock = pg.time.Clock()
        self.running = True
        self.player = Character(self.space, self.screen, WALL_JUMP)
        self.level = LEVEL
        self.menu = Menu(self.screen)
        self.replay_on = False

        # screen_dim = (150, 85)
        self.game_tick = 1
        if self.replay_on:
            self.ai = Ai(self.player, self.level)
            if self.ai.valid:
                self.game_tick = -120
                self.can_start = True
                self.started = True
            else:
                self.replay_on = False
            
        self.level_end = False
        self.time_hit_flag = 0
        self.events = [[] for i in range(20000)]
        self.walls, self.push_objects, self.spikes, self.flag, self.flag_location_1, self.flag_location_2, self.item, self.level_image = load_level(
            self.level)
        if self.item is not None:
            self.item.add_to_space()
        self.flag.add_to_space()

        for wall in self.walls:
            wall.add_to_space()
        for thing in self.push_objects:
            thing.add_to_space()
        for thing in self.spikes:
            thing.add_to_space()

    def run(self) -> None:
        """
        Main game loop
        :return: None
        """
        # print_options = pm.SpaceDebugDrawOptions()  # For easy printing
        options = DrawOptions(self.screen)
        self.timer = Timer(self.screen)
        while self.running:
            self.draw_background()
            # Print the state of the simulation
            self.player.draw(self.game_tick, self.started)
            for thing in self.push_objects:
                thing.draw()
            if self.item is not None:
                if not self.item.got:
                    self.item.draw(self.game_tick, self.started)
                    self.player_collide_item()
            self.flag.draw(self.game_tick, self.started)
            self.timer.draw(self.game_tick, self.replay_on)
            if DEBUG:
                self.space.debug_draw(options)
            self.player_collide_wall()
            self.player_collide_push_object()
            self.player_collide_flag()
            self.player_collide_spike()
            self.handle_game_events()
            self.update()
            self.space.step(0.02 * 60 / FRAMERATE)  # Step the simulation one step forward

    def handle_game_events(self) -> None:
        """
        Handle events such as inputs and exit screen
        :return:
        """
        if self.replay_on:
            self.ai.handle_events(self.game_tick)
        for event in pg.event.get():
            if not self.replay_on and not self.level_end:
                self.events[self.game_tick].append([event.type, event.dict])
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            if event.type == pg.KEYDOWN and self.can_start:
                self.started = True
                if not self.replay_on:
                    self.player.handle_keydown(event)
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit(0)
                if event.key == pg.K_r:
                    self.next_level(1)
                if event.key == pg.K_t:
                    self.replay_on = not self.replay_on
                    self.next_level(1)
                if event.key == 61:
                    self.next_level(2)
                if event.key == 45:
                    self.level -= 1
                    self.next_level(3)
            elif event.type == pg.KEYUP and not self.replay_on:
                self.player.handle_keyup(event)


    def update(self) -> None:
        """
        Flip the screen and tick the clock
        :return:
        """
        self.player.update()
        self.curr_fps = self.game_clock.get_fps()
        self.game_clock.tick(FRAMERATE)
        if self.started:
            self.game_tick += 1
        self.curr_fps = self.game_clock.get_fps()
        pg.display.flip()

    def draw_background(self) -> None:
        self.screen.blit(BACKGROUND, (0, 0), BACKGROUND.get_rect())
        self.screen.blit(self.level_image, (0, 0), self.level_image.get_rect())

    def player_collide_wall(self) -> None:
        player_wall_collisions = []
        self.can_start = True
        for wall in self.walls:
            if not wall.is_boundary:
                normal = self.player.poly.shapes_collide(wall.poly).normal
                player_wall_collisions.append((round(normal.x), round(normal.y)))

        self.player.update_animation_wall(player_wall_collisions)

    def player_collide_push_object(self) -> None:
        player_box_collisions = []
        for thing in self.push_objects:
            normal = self.player.poly.shapes_collide(thing.poly).normal
            player_box_collisions.append((round(normal.x), round(normal.y)))

        self.player.update_animation_push_object(player_box_collisions, self.push_objects, self.walls)

    def player_collide_flag(self) -> None:
        if self.player.poly.shapes_collide(self.flag.poly).points:
            if not self.flag.got:
                self.flag.body.position = (
                    self.flag_location_2[0] + self.flag.flag_size[0] / 2,
                    self.flag_location_2[1] + self.flag.flag_size[1] / 2)
                self.flag.got = True
                self.time_hit_flag = self.game_tick
            else:
                self.next_level(0)

    def player_collide_item(self) -> None:
        if self.player.poly.shapes_collide(self.item.poly).points:
            self.item.body.position = (SCREEN_SIZE[0] + 200, 0)
            self.item.got = True
            self.player.wall_jump = True

    def player_collide_spike(self) -> None:
        for spike in self.spikes:
            if self.player.poly.shapes_collide(spike.poly).points:
                self.next_level(1)
                break


    def reset_level(self):
        self.player.body.position = SCREEN_SIZE[0] / 50, 4 * SCREEN_SIZE[1] / 10
        self.player.body.velocity = (0, 0)
        self.game_tick = 1
        if self.replay_on:
            self.game_tick = -120
        self.events = [[] for i in range(20000)]
        for thing in self.push_objects:
            thing.body.position = thing.initial_position
            thing.body.velocity = (0, 0)
            thing.body.angle = 0
        if self.flag.got:
            self.flag.body.position = (
                self.flag_location_1[0] + self.flag.flag_size[0] / 2,
                self.flag_location_1[1] + self.flag.flag_size[1] / 2)
            self.flag.got = False
        if self.level == 3:
            if self.item.got:
                self.item.body.position = self.item.initial_position
                self.item.got = False
                self.player.wall_jump = False
        self.started = False
        self.can_start = False
        if self.replay_on:
            self.can_start = True
            self.started = True
        else:
            self.player.right = False
            self.player.left = False
        # if pg.key.get_pressed()[pg.K_a] or pg.key.get_pressed()[pg.K_LEFT]:
        #     self.events[0] = [[pg.KEYDOWN, {'key': pg.K_a}]]
        # elif pg.key.get_pressed()[pg.K_d] or pg.key.get_pressed()[pg.K_RIGHT]:
        #     self.events[0] = [[pg.KEYDOWN, {'key': pg.K_d}]]

    def next_level(self, i):
        if i != 1 and i != 2 and i != 3:
            self.next_level_screen()
        self.level_end = False
        if self.level == MAX_LEVEL:
            self.level = 0
        for thing in self.walls:
            self.space.remove(thing.body, thing.poly)
        for thing in self.push_objects:
            self.space.remove(thing.body, thing.poly)
        for thing in self.spikes:
            self.space.remove(thing.body, thing.poly)
        self.space.remove(self.flag.body, self.flag.poly)
        self.space.remove(self.player.body, self.player.poly)
        if self.item is not None:
            self.space.remove(self.item.body, self.item.poly)
        if i != 1:
            self.level += 1
        if i == 3:
            self.level -= 1
        if self.level == 0:
            self.level = MAX_LEVEL
        self.walls, self.push_objects, self.spikes, self.flag, self.flag_location_1, self.flag_location_2, self.item, self.level_image = load_level(
            self.level)
        self.player = Character(self.space, self.screen, self.player.wall_jump)
        if self.item is not None:
            self.item.add_to_space()
            self.item.got = False
        self.flag.add_to_space()

        for wall in self.walls:
            wall.add_to_space()
        for thing in self.push_objects:
            thing.add_to_space()
        for thing in self.spikes:
            thing.add_to_space()
        self.reset_level()
        if self.level > 3:
            self.player.wall_jump = True
        else:
            self.player.wall_jump = False
        if self.replay_on:
            self.ai = Ai(self.player, self.level)
            if not self.ai.valid:
                self.replay_on = False
        if DEBUG:
            print(self.level)

    def next_level_screen(self):
        if not self.replay_on:
            file = open(resource_path('data/saves/' + str(self.level) + '/run_' + str(self.game_tick)), 'wb')
            pickle.dump(self.events[0:self.game_tick + 20], file)
            file.close()
            files = os.listdir(resource_path('data/saves/' + str(self.level)))
            delete = 1;
            while len(files) > 10:
                os.remove('data/saves/' + str(self.level) + '/' + files[-delete])
                files.pop()
                delete += 1
        self.level_end = True
        while not pg.key.get_pressed()[pg.K_RETURN]:
            self.handle_game_events()
            self.menu.draw(self.game_tick)
            self.update()
            self.game_tick -= 1
            if pg.key.get_pressed()[pg.K_r] or pg.key.get_pressed()[pg.K_t]:
                self.level -= 1
                break


def Main():
    app = App(SCREEN, SPACE)
    app.run()
