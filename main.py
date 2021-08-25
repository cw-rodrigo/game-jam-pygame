import sys
import pygame

MAIN_PATH = "data"

window_size = (0, 0)

player_speed = 0.17

player_movement = [0, 0]
camera_position = [0, 0]

window_title = "Default Title"

framerate = pygame.time.Clock()
sprites_group = pygame.sprite.Group()
hud_sprites_group = pygame.sprite.Group()

pygame.init()

icon = pygame.image.load(f"{MAIN_PATH}/Icon.png")

user_resolution = pygame.display.Info()

window_size = (user_resolution.current_w, user_resolution.current_h)

screen = pygame.display.set_mode((window_size))
display = pygame.Surface((640, 360))

pygame.display.set_caption(window_title)
pygame.display.set_icon(icon)

text_font = pygame.font.SysFont("arial", 15)

class HUDManager(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(f"{MAIN_PATH}/Text-HUD.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = (320, 180 + 130)

    def update(self):
        display.blit(self.image, (self.rect[0], self.rect[1]))

class PlayerManager(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.animation_speed = 0

        self.up_walk_anim_sprites = [ pygame.image.load(f"{MAIN_PATH}/Player-Sprite_1.png").convert_alpha(), 
                                      pygame.image.load(f"{MAIN_PATH}/Player-Sprite_2.png").convert_alpha(),
                                      pygame.image.load(f"{MAIN_PATH}/Player-Sprite_3.png").convert_alpha(),
                                      pygame.image.load(f"{MAIN_PATH}/Player-Sprite_4.png").convert_alpha(),
                                      pygame.image.load(f"{MAIN_PATH}/Player-Sprite_5.png").convert_alpha() ]

        self.down_walk_anim_sprites = [ pygame.image.load(f"{MAIN_PATH}/Player-Sprite_6.png").convert_alpha(),
                                        pygame.image.load(f"{MAIN_PATH}/Player-Sprite_7.png").convert_alpha(),
                                        pygame.image.load(f"{MAIN_PATH}/Player-Sprite_8.png").convert_alpha(),
                                        pygame.image.load(f"{MAIN_PATH}/Player-Sprite_9.png").convert_alpha(),
                                        pygame.image.load(f"{MAIN_PATH}/Player-Sprite_10.png").convert_alpha() ]

        self.side_walk_anim_sprites = [ pygame.image.load(f"{MAIN_PATH}/Player-Sprite_11.png").convert_alpha(),
                                        pygame.image.load(f"{MAIN_PATH}/Player-Sprite_12.png").convert_alpha(),
                                        pygame.image.load(f"{MAIN_PATH}/Player-Sprite_13.png").convert_alpha(),
                                        pygame.image.load(f"{MAIN_PATH}/Player-Sprite_14.png").convert_alpha(),
                                        pygame.image.load(f"{MAIN_PATH}/Player-Sprite_15.png").convert_alpha() ]
        
        self.current_walk_anim_sprite = 0
        self.current_idle_anim_sprite = 0

        self.image = pygame.image.load(f"{MAIN_PATH}/Player-Sprite_1.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = (320, 180)

    def update(self):
        display.blit(self.image, (int(self.rect.x) - int(camera_position[0]), int(self.rect.y) - int(camera_position[1])))

    def walk(self, axis, direction, delta_time_value):
        if self.animation_speed >= 1:
            self.animation_speed = 0

            self.current_walk_anim_sprite = (self.current_walk_anim_sprite + 1) % 5

        if direction == 1:
            player_movement[axis] += player_speed * delta_time_value
        else:
            player_movement[axis] -= player_speed * delta_time_value

        if axis == 1 and direction == 1:
            self.image = self.up_walk_anim_sprites[ self.current_walk_anim_sprite ]
        elif axis == 1  and direction == 0:
            self.image = self.down_walk_anim_sprites[ self.current_walk_anim_sprite ]

        elif axis == 0:
            self.image = self.side_walk_anim_sprites[ self.current_walk_anim_sprite ]

class InteractiveObjectManager(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.object_position = None

        self.text = ""

        self.sentence = -1

        self.is_interacting = False

        self.image = None

        self.object_current_rect = None

    def update(self):
        display.blit(self.image, (self.object_position[0] - int(camera_position[0]), self.object_position[1] - int(camera_position[1])))

    def initial_set(self, object_sprite ,text, object_position):
        self.image = pygame.image.load(f"{MAIN_PATH}/{object_sprite}").convert_alpha()

        self.rect = self.image.get_rect()

        self.text = text

        self.object_position = object_position

        self.object_current_rect = pygame.Rect(self.object_position[0], self.object_position[1], self.image.get_width(), self.image.get_height())

class TriggerManager(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(f"{MAIN_PATH}/Game-Map_8.png").convert()

        self.rect = None

class EnvironmentManager(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.game_map = None

        self.collision_tiles_home_rect = []
        self.collision_tiles_outside_rect = []

        self.home_game_map = [ ["-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",],
                               ["-1", "4", "2", "2", "2", "2", "2", "3", "-1"],
                               ["-1", "6", "10", "1", "1", "1", "1", "5", "-1"],
                               ["-1", "6", "1", "1", "1", "1", "9", "5", "-1"],
                               ["-1", "2", "2", "2", "1", "2", "2", "2", "-1"],
                               ["-1", "-1", "-1", "6", "1", "5", "-1", "-1", "-1"],
                               ["-1", "-1", "-1", "6", "1", "5", "-1", "-1", "-1"],
                               ["-1", "-1", "-1", "2", "8", "2", "-1", "-1", "-1"] ]

        self.outside_game_map = [ ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                  ["0", "7", "7", "7", "7", "7", "7", "7", "13", "12", "12", "12", "13", "11", "12", "13", "12", "13", "12", "0"],
                                  ["0", "7", "7", "7", "7", "7", "7", "7", "12", "13", "12", "13", "12", "11", "13", "12", "12", "12", "13", "0"],
                                  ["0", "7", "7", "7", "7", "7", "7", "7", "12", "12", "12", "12", "12", "11", "12", "12", "13", "12", "12", "0"],
                                  ["0", "7", "7", "7", "7", "7", "7", "7", "12", "12", "13", "12", "13", "11", "12", "13", "12", "13", "12", "0"],
                                  ["0", "12", "13", "7", "7", "7", "12", "12", "13", "12", "12", "13", "12", "11", "13", "12", "13", "12", "13", "0"],
                                  ["0", "13", "12", "12", "12", "12", "13", "12", "12", "13", "12", "13", "12", "11", "12", "12", "12", "12", "12", "0"],
                                  ["0", "12", "13", "12", "12", "12", "12", "13", "12", "13", "12", "12", "13", "11", "12", "13", "12", "13", "12", "0"],
                                  ["0", "12", "13", "12", "13", "12", "12", "13", "12", "13", "12", "12", "13", "11", "13", "13", "12", "13", "12", "0"],
                                  ["0", "11", "11", "11", "11", "11", "11", "11", "11", "11", "11", "11", "11", "11", "12", "13", "12", "13", "12", "0"],
                                  ["0", "13", "12", "13", "12", "13", "12", "12", "13", "12", "13", "12", "13", "11", "13", "12", "13", "12", "13", "0"],
                                  ["0", "12", "13", "12", "13", "12", "12", "13", "12", "13", "12", "13", "12", "11", "13", "12", "12", "13", "12", "0"],
                                  ["0", "13", "12", "13", "12", "12", "13", "12", "13", "12", "13", "12", "13", "11", "12", "13", "12", "12", "13", "0"],
                                  ["0", "12", "13", "12", "13", "12", "12", "13", "12", "13", "12", "13", "12", "11", "13", "12", "13", "13", "12", "0"],
                                  ["0", "13", "12", "13", "12", "12", "13", "12", "13", "12", "13", "12", "13", "11", "12", "13", "12", "13", "12", "0"],
                                  ["0", "12", "13", "13", "12", "13", "12", "13", "12", "13", "12", "13", "12", "11", "13", "12", "13", "12", "13", "0"],
                                  ["0", "13", "12", "13", "12", "12", "13", "12", "13", "12", "13", "12", "13", "11", "12", "13", "12", "13", "12", "0"],
                                  ["0", "12", "12", "12", "12", "12", "12", "12", "12", "12", "12", "12", "12", "11", "11", "11", "11", "11", "11", "0"],
                                  ["0", "13", "12", "13", "12", "13", "12", "13", "12", "13", "12", "13", "12", "13", "12", "13", "13", "12", "13", "0"],
                                  ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"] ]

        self.map_sprite = pygame.image.load(f"{MAIN_PATH}/Game-Map_1.png").convert()
        self.map_sprite2 = pygame.image.load(f"{MAIN_PATH}/Game-Map_2.png").convert()
        self.map_sprite3 = pygame.image.load(f"{MAIN_PATH}/Game-Map_3.png").convert()
        self.map_sprite4 = pygame.image.load(f"{MAIN_PATH}/Game-Map_4.png").convert()
        self.map_sprite5 = pygame.image.load(f"{MAIN_PATH}/Game-Map_5.png").convert()
        self.map_sprite6 = pygame.image.load(f"{MAIN_PATH}/Game-Map_6.png").convert()
        self.map_sprite7 = pygame.image.load(f"{MAIN_PATH}/Game-Map_7.png").convert()
        self.map_sprite9 = pygame.image.load(f"{MAIN_PATH}/Game-Map_9.png").convert()
        self.map_sprite10 = pygame.image.load(f"{MAIN_PATH}/Game-Map_10.png").convert()
        self.map_sprite11 = pygame.image.load(f"{MAIN_PATH}/Game-Map_11.png").convert()
        self.map_sprite12 = pygame.image.load(f"{MAIN_PATH}/Game-Map_12.png").convert()
        self.map_sprite13 = pygame.image.load(f"{MAIN_PATH}/Game-Map_13.png").convert()

        self.render_home = True
        self.render_outside = False

    def update(self):
        if self.render_home:
            self.game_map = self.home_game_map

        if self.render_outside:
            self.game_map = self.outside_game_map

        y = 0
        for row in self.game_map:
            x = 0

            for tile in row:
                x += 1

                if tile == "-1":
                    self.collision_tiles_home_rect.append(pygame.Rect(x * 64, y * 64, 64, 64))

                if tile == "0":
                    self.collision_tiles_outside_rect.append(pygame.Rect(x * 64, y * 64, 64, 64))

                if tile == "1":
                    display.blit(self.map_sprite, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "2":
                    display.blit(self.map_sprite2, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "3":
                    display.blit(self.map_sprite3, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "4":
                    display.blit(self.map_sprite4, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "5":
                    display.blit(self.map_sprite5, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "6":
                    display.blit(self.map_sprite6, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "7":
                    display.blit(self.map_sprite7, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                    self.collision_tiles_outside_rect.append(pygame.Rect(x * 64, y * 64, 64, 64))

                if tile == "8":
                    display.blit(scene_transition_trigger.image, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                    scene_transition_trigger.rect = pygame.Rect(x * 64, y * 64, scene_transition_trigger.image.get_width(), scene_transition_trigger.image.get_height())

                if tile == "9":
                    display.blit(self.map_sprite9, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "10":
                    display.blit(self.map_sprite10, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "11":
                    display.blit(self.map_sprite11, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "12":
                    display.blit(self.map_sprite12, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))

                if tile == "13":
                    display.blit(self.map_sprite13, (x * 64 - int(camera_position[0]), y * 64 - int(camera_position[1])))
            y += 1

def change_window_title(window_title, window_title_value):
    window_title = window_title_value

    pygame.display.set_caption(window_title)

def draw_text(font, text, color, text_position):
    text_object = font.render(text, 1, color)

    text_rect = text_object.get_rect()

    text_rect.center = (text_position[0], text_position[1])

    display.blit(text_object, text_rect)

def load_music(audio_name, repetitions):
        pygame.mixer.music.load(f"{MAIN_PATH}/{audio_name}.ogg")
        pygame.mixer.music.play(repetitions)

def collisions_on_scene_transition():
    if map.render_home:
        return map.collision_tiles_home_rect

    if map.render_outside:
        return map.collision_tiles_outside_rect

def check_collisions(first_rect, second_rect):
    collision = first_rect.colliderect(second_rect)

    if collision == True:
        return True

def collision_test(rect, tiles):
    hit_list = []

    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)

    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
        elif movement[0] < 0:
            rect.left = tile.right
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)

    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
        elif movement[1] < 0:
            rect.top = tile.bottom
    return rect

def start_screen():
    change_window_title(window_title, "Game Jaaj 6")

    sentence = 0

    start_screen_text = """Há muito tempo atrás alguém lançou um feitiço contra a terra,
    um feitiço de medo e insegurança, fazendo todos desistirem dos seus sonhos.
    Esse feitiço já foi quebrado uma vez, porém ele sempre volta por motivos desconhecidos.
    Diz a lenda que apenas a pessoa mais motivada conseguirá restaurar a esperança no mundo,
    e apenas ela conseguirá livrá-lo desse feitiço para sempre..."""

    draw_text(text_font, "Pressione Enter pra Continuar!", (255, 255, 255), (320, 180))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    display.fill([0, 0, 0])

                    draw_text(text_font, "Pressione Enter pra Continuar!", (255, 255, 255), (320, 180 + 100))

                    if sentence <= int(len(start_screen_text.split('\n')) - 1):
                        draw_text(text_font, str(start_screen_text.split('\n')[sentence]), (255, 255, 255), (320, 180))

                        sentence += 1

                    else:
                        main_menu_screen()

        surf = pygame.transform.scale(display, window_size)
        screen.blit(surf, (0, 0))

        pygame.display.update()

def main_menu_screen():
    change_window_title(window_title, "Menu Principal")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_screen()

        display.fill([0, 0, 0])

        draw_text(text_font, "The Legend About Me", (255, 255, 255), (320, 180))
        draw_text(text_font, "Pressione Espaço para Começar o Jogo!", (255, 255, 255), (320, 180 + 100))

        surf = pygame.transform.scale(display, window_size)
        screen.blit(surf, (0, 0))

        pygame.display.update()

def game_screen():
    change_window_title(window_title, "Gameplay")
    load_music("Main Theme", -1)

    interacting_id = None

    is_interacting = False
    is_enter_pressed = False

    global screen_color
    global player_movement

    while True:

        delta_time = framerate.tick(60)
        player_controller.player_current_rect = pygame.Rect(player_controller.rect.x, player_controller.rect.y, player_controller.image.get_width(), player_controller.image.get_height())

        player_controller.animation_speed += 0.02 * delta_time

        camera_position[0] += (player_controller.rect.x - camera_position[0] - 320) / 18
        camera_position[1] += (player_controller.rect.y - camera_position[1] - 180) / 18

        move(player_controller.rect, player_movement, collisions_on_scene_transition())

        surf = pygame.transform.scale(display, window_size)
        screen.blit(surf, (0, 0))

        display.fill([25, 25, 25])

        sprites_group.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen()            

                if event.key == pygame.K_RETURN:
                    if check_collisions(player_controller.player_current_rect, npc_test.object_current_rect):
                        is_enter_pressed = True

                        npc_test.sentence += 1
                        interacting_id = 0

                    if check_collisions(player_controller.player_current_rect, npc_test2.object_current_rect):
                        is_enter_pressed = True

                        npc_test2.sentence += 1
                        interacting_id = 1

                    if check_collisions(player_controller.player_current_rect, npc_test3.object_current_rect):
                        is_enter_pressed = True

                        npc_test3.sentence += 1
                        interacting_id = 2

                    if check_collisions(player_controller.player_current_rect, npc_test2_2.object_current_rect):
                        is_enter_pressed = True

                        npc_test2_2.sentence += 1
                        interacting_id = 3

                    if check_collisions(player_controller.player_current_rect, npc_test3_2.object_current_rect):
                        is_enter_pressed = True

                        npc_test3_2.sentence += 1
                        interacting_id = 4

        player_movement = [0, 0]
            
        is_holding = pygame.key.get_pressed()

        if not is_interacting:
            if is_holding[ pygame.K_w ]:
                player_controller.walk(1, 0, delta_time)

            elif is_holding[ pygame.K_s ]:
                player_controller.walk(1, 1, delta_time)

            if is_holding[ pygame.K_a ]:
                player_controller.walk(0, 0, delta_time)

                player_controller.image = pygame.transform.flip(player_controller.image, True, False)

            elif is_holding[ pygame.K_d ]:
                player_controller.walk(0, 1, delta_time)

        if is_interacting:
            hud_sprites_group.update()

        if npc_test2.sentence == int(len(npc_test2.text.split('\n')) - 1):
            sprites_group.add(npc_test3)

        if npc_test3.sentence == int(len(npc_test3.text.split('\n')) - 1):
            sprites_group.remove(npc_test2)
            sprites_group.add(npc_test2_2)

            npc_test2.kill()

        if npc_test2_2.sentence == int(len(npc_test2_2.text.split('\n')) - 1):
            sprites_group.remove(npc_test3)
            sprites_group.add(npc_test3_2)

            npc_test3.kill()

        if npc_test3_2.sentence == int(len(npc_test3_2.text.split('\n')) - 1):
            display.fill([25, 25, 25])

            pygame.mixer.stop()
            
            credits_screen()

        if is_enter_pressed and interacting_id == 0:
            if npc_test.sentence <= int(len(npc_test.text.split('\n')) - 1):
                draw_text(text_font, str(npc_test.text.split('\n')[npc_test.sentence]), (255, 255, 255), (320, 180 + 130))

                is_interacting = True
            else:
                is_interacting = False

        if is_enter_pressed and interacting_id == 1:
            if npc_test2.sentence <= int(len(npc_test2.text.split('\n')) - 1):
                draw_text(text_font, str(npc_test2.text.split('\n')[npc_test2.sentence]), (255, 255, 255), (320, 180 + 130))

                is_interacting = True
            else:
                is_interacting = False

        if is_enter_pressed and interacting_id == 2:
            if npc_test3.sentence <= int(len(npc_test3.text.split('\n')) - 1):
                draw_text(text_font, str(npc_test3.text.split('\n')[npc_test3.sentence]), (255, 255, 255), (320, 180 + 130))

                is_interacting = True
            else:
                is_interacting = False

        if is_enter_pressed and interacting_id == 3:
            if npc_test2_2.sentence <= int(len(npc_test2_2.text.split('\n')) - 1):
                draw_text(text_font, str(npc_test2_2.text.split('\n')[npc_test2_2.sentence]), (255, 255, 255), (320, 180 + 130))

                is_interacting = True
            else:
                is_interacting = False

        if is_enter_pressed and interacting_id == 4:
            if npc_test3_2.sentence <= int(len(npc_test3_2.text.split('\n')) - 1):
                draw_text(text_font, str(npc_test3_2.text.split('\n')[npc_test3_2.sentence]), (255, 255, 255), (320, 180 + 130))

                is_interacting = True
            else:
                is_interacting = False

        if check_collisions(player_controller.player_current_rect, scene_transition_trigger.rect):
            map.render_home = False
            map.render_outside = True

        if map.render_outside:
            sprites_group.add(npc_test)

        pygame.display.update()

def pause_screen():
    change_window_title(window_title, "Menu de Pausa")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_screen()

                if event.key == pygame.K_q:
                    main_menu_screen()

        display.fill([25, 25, 25])

        draw_text(text_font, "Jogo Pausado!", (255, 255, 255), (320, 180))
        draw_text(text_font, "Pressione ESC para Continuar o Jogo!", (255, 255, 255), (320, 180 + 100))
        draw_text(text_font, "Pressione Q para ir ao Menu Principal!", (255, 255, 255), (320, 180 + 50))

        surf = pygame.transform.scale(display, window_size)
        screen.blit(surf, (0, 0))

        pygame.display.update()

def credits_screen():
    change_window_title(window_title, "Créditos!")

    sentence = 0

    final_screen_text = """Há muito tempo atrás alguém lançou um feitiço contra a terra,
    um feitiço de medo e insegurança, fazendo todos desistirem dos seus sonhos.
    Esse feitiço já foi quebrado uma vez, porém ele sempre volta por motivos desconhecidos.
    Diz a lenda que apenas a pessoa mais motivada conseguirá restaurar a esperança no mundo,
    e apenas ela conseguirá livrá-lo desse feitiço para sempre...
    ...
    E esta pessoa é você!"""

    draw_text(text_font, "Pressione Enter pra Continuar!", (255, 255, 255), (320, 180))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RETURN:
                    display.fill([0, 0, 0])

                    if sentence <= int(len(final_screen_text.split('\n')) - 1):
                        draw_text(text_font, str(final_screen_text.split('\n')[sentence]), (255, 255, 255), (320, 180))

                        sentence += 1

                        draw_text(text_font, "Pressione Enter pra Continuar!", (255, 255, 255), (320, 180 + 100))

                    else:
                        draw_text(text_font, "Fim!", (255, 255, 255), (320, 180))
                        draw_text(text_font, "Muito obrigado por jogar!", (255, 255, 255), (320, 180 + 50))
                        draw_text(text_font, "Criado por Rodrigo.", (255, 255, 255), (320, 180 + 100))
                        draw_text(text_font, "Pressione ESC para sair...", (255, 255, 255), (320, 180 + 150))

        surf = pygame.transform.scale(display, window_size)
        screen.blit(surf, (0, 0))

        pygame.display.update()

map = EnvironmentManager()
scene_transition_trigger = TriggerManager()
player_controller = PlayerManager()
npc_test = InteractiveObjectManager()
npc_test2 = InteractiveObjectManager()
npc_test2_2 = InteractiveObjectManager()
npc_test3 = InteractiveObjectManager()
npc_test3_2 = InteractiveObjectManager()
text_background = HUDManager()

npc_test.initial_set("NPC-Sprite_3.png",
"""Oi bom dia, em que posso ajudar?
Hope: Queria uma informação.
Hope: Sonhei com algo estranho
Hope: Conhece a lenda dos sonhos?
Não, o que é isso?
Hope: Uma lenda sobre um escolhido,
Hope: Alguém que é capaz de restaurar...
Hope: a esperança no mundo...
Eu já ouvi falar disso, mas não acredito não...
Inclusive o pesquisador vive falando sobre isto
Não seria uma má ideia visitá-lo,
Tenho certeza que ele sabe mais sobre isto!""", (16 * 32, 12 * 32))

npc_test2.initial_set("NPC-Sprite_2.png",
"""Hope: Bom dia você que é o pesquisador?,
Sim, sou eu mesmo.
Hope: Queria saber mais sobre uma lenda,
Hope: Tive um sonho estranho hoje,
Hope: Sonhei com uma lenda dos sonhos,
Hope: Uma lenda sobre um escolhido que...
Você sonhou com esta lenda?
Hope: Sim, e queria saber mais sobre ela.
...
Bom,
Há muito tempo atrás...
Alguém lançou um feitiço.
Um feitiço que provoca medo e insegurança,
E ele é o motivo...
Das pessoas desistirem dos seus sonhos,
A lenda diz sobre um escolhido,
Alguém motivado o suficiente...
Para salvar o mundo...
E apenas ele...
Irá quebrar o feitiço para sempre...
Hope: Isso significa que...
Isso mesmo, você é o escolhido!
Hope: Mas como vou conseguir?
Hope: Como vou quebrar este feitiço?
Hope: Como vou restaurar...
Hope: a esperança do mundo?
Hope: Se até mesmo eu não a tenho...
A lenda não falha, então...
Se ela escolheu você...
Então tem um motivo!
Hope: ...
Hope: O que preciso fazer?
Isso apenas o escolhido pode saber...
Tente várias coisas até descobrir,
Essa não é a primeira vez,
Esse feitiço volta sempre,
E sempre uma nova pessoa é escolhida.
Não dá para saber o que quebrará...
O que quebrará o feitiço dessa vez...
Mas em todas as vezes,
Tem algo relacionado com a esperança
Hope: ...
Hope: Muito obrigado por isso tudo,
Hope: Vou ver o que consigo descobrir...""", (17 * 32, 25 * 32))

npc_test3.initial_set("NPC-Sprite_1.png",
"""Hope, você por aqui?
A quando tempo não te vejo,
Hope: Também digo o mesmo,
Hope: O que faz aqui?
Me mudei pra cá recentemente,
Estava falando com o pesquisador?
Hope: Sim, sobre uma lenda estranha
Hope: Acredita que eu posso ser...
Hope: O escolhido!
Escolhido para que?
Hope: ...Restaurar a esperança...
Hope: Do mundo...
Ahh, acho que já ouvi essa lenda.
Mas o que vai fazer?
Como vai completar a lenda?
Hope: Esse é o problema,
Hope: Eu não sei...
Hope: O pesquisador disse que...
Hope: O que tenho que fazer está relacionado...
Hope: ...Com esperança...
...
Você já pensou em...
Realizar o sonho de alguma pessoa!
Alguém que não tenha mais motivação,
Isso seria relacionado com esperança!
Hope: Verdade! mas quem?,
O que acha do pesquisador?
Fiquei sabendo que ele tem um sonho...
Um sonho secreto,
Quem sabe você descobre o sonho...
Falando com ele...
Hope: Verdade, vou tentar fazer isto,
Hope: Muito obrigado pela ajuda!
Por nada, se quiser ajuda com mais algo me fale,
Vou estar aqui mesmo no parque,
Estou planejando com calma os nossos passos!
Enquanto isso...
Tente realizar o sonho do pesquisador,
Acho que é disso que precisamos!""", (29 * 32, 22 * 32))

npc_test2_2.initial_set("NPC-Sprite_2.png",
"""Olá novamente! O que você quer?
Hope: Queria saber mais uma coisa...
Hope: Quando o feitiço for quebrado...
Hope: O que acontecerá?
...
Infelizmente ele sempre volta...
Você terá que continuar o ciclo...
Continuar o ciclo dos escolhidos...
Escolhendo outra pessoa.
Hope: Tem como fazer algo para...
Hope: Para acabar com o feitiço?
Hope: Acabar com ele para sempre!
Infelizmente é impossível,
O melhor jeito então é planejar...
Planejar em algo que escolha o escolhido,
E que esse processo de escolha seja...
Automático...
Hope: ...
Hope: Muito obrigado novamente!
Hope: Uma coisa que ainda não me disse...
Hope: Foi o seu nome.
Desculpe, mas você não posso...
Me chame de pesquisador mesmo...
Hope: Conte mais algo sobre você,
Hope: Mesmo que seja apenas,
Hope: O seu sonho...
Hope: Uma informação a mais talvez...
Hope: ...Ajude na lenda!
...
Não gosto muito de falar sobre mim...
...
Mas se é pela lenda, então...
Meu sonho é...
Simplesmente ter um amigo...
Não sou muito socializável,
Acho que você já percebeu isso...
Hope: Interessante...
Hope: Também sou assim, 
Hope: Nunca tive muitos amigos,
Hope: Por isso ainda não entendo...
Hope: Qual o motivo da lenda me escolher...
Talvez foi por isso mesmo...
Hope: Como assim?
Talvez a lenda te escolheu...
Para lhe dar uma lição...
Ou até mesmo...
Para você dar uma lição a alguém...
Você me disse que não tem esperanças,
Talvez a chave para quebrar o feitiço...
Seria você mesmo...
Hope: ...
E você, qual é o seu sonho?
Hope: ...
Hope: Sonho em ser um...
Hope: Desenvolvedor de jogos...
Hope: Jogos é uma forma de arte espetacular!
Hope: Neles conseguímos...
Hope: Transmitir qualquer emoção!
Hope: Mas infelizmente tenho medo,
Hope: Tenho medo do que vão dizer,
Hope: Do que vão dizer do meu jogo...
...
O que acha de apenas tentar?
Se não der certo...
Então tente de novo!
Tenho certeza que os próximos...
Os próximos serão melhores!
Hope: ...
Hope: Muito obrigado!
Hope: Eu acho que seríamos ótimos amigos!
Hope: Agora preciso voltar,
Hope: Ainda não terminei com a lenda...""", (17 * 32, 22 * 32))

npc_test3_2.initial_set("NPC-Sprite_1.png", 
"""Bom dia novamente!
Hope: Bom dia!
Hope: De certa forma...
Hope: Consegui realizar...
Hope: O sonho do pesquisador!
Hope: Mas parece que não mudou nada,
Hope: O feitiço continuou igual...
Hope: Consegui algumas informações,
Hope: Mas nada de mudança no feitiço...
Hope: Alguma ideia do que fazer?
Fiquei pensando...
E se na verdade...
Quem precisar realizar o sonho...
For você...
Hope: Isso é verdade...
Hope: Mas não acredito que...
Hope: Eu consiga realizá-lo.
Isso é o efeito do feitiço,
Não deixe isso te fazer desistir!
Hope: ...
Hope: Falando nisso,
Hope: Sabe algo que eu possa fazer que,
Hope: Escolha novos escolhidos e...
Hope: Seja automático?
O que acha de...
Algo que motive alguém...
Algo que faça alguém se sentir,
Se sentir o escolhido...
Com isso poderemos ficar seguros,
Pois sempre haverá um escolhido!
Hope: Você acabou de me dar uma idéia!
Hope: Não vou poder contar ela agora,
Hope: Mas ao mesmo tempo...
Hope: Vou completar meu sonho e...
Hope: Escolher outro escolhido!
Ótimo! mas pode me dizer como?
Hope: Ainda não, acho melhor...
Hope: Fazer isso logo!
Não vai me contar nada não?
Hope: Melhor do que isso,
Hope: Vou te mostrar o resultado!
.""", (29 * 32, 27 * 32))

sprites_group.add(map)
sprites_group.add(npc_test2)
sprites_group.add(player_controller)
hud_sprites_group.add(text_background)

start_screen()
