import sys

import pygame

# from pygame import font

size = width, height = 800, 600
screen = pygame.display.set_mode(size)

# horizontal_borders = pygame.sprite.Group()
# vertical_borders = pygame.sprite.Group()
# all_enemies = pygame.sprite.Group()

menu_item_color = (255, 215, 205)
menu_selected_item_color = (255, 215, 0)
game_info_color = (135, 206, 250)
game_over_color = (255, 165, 0)

pygame.init()
fps = 60
clock = pygame.time.Clock()

# кол-во снарядов на игру
max_hit = 5

score = 0
hit_count = max_hit
enemy_speed = 2
game_over = False

# Меню


class Menu:
    def __init__(self, items):
        self.items = items
        self.bitmap = pygame.image.load('images/menu.png')

    def render(self, surface, item_id):
        surface.blit(self.bitmap, (0, 0))

        for i in self.items:
            if item_id == i[3]:
                font = pygame.font.Font(None, 130)
                surface.blit(font.render(i[2], 1, menu_selected_item_color), (i[0], i[1]))
            else:
                font = pygame.font.Font(None, 115)
                surface.blit(font.render(i[2], 1, menu_item_color), (i[0], i[1]))

    def menu(self):
        current = 0
        menu_active = True
        while menu_active:
            # screen.fill((25, 25, 112))
            mp = pygame.mouse.get_pos()
            for i in self.items:
                if i[0] < mp[0] < i[0] + 155 and i[1] < mp[1] < i[1] + 50:
                    current = i[3]
            self.render(screen, current)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if current > 0:
                            current -= 1
                    if event.key == pygame.K_DOWN:
                        if current < len(self.items) - 1:
                            current += 1

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if current == 0:
                        global score, hit_count, enemy_speed, game_over
                        score = 0
                        hit_count = max_hit
                        enemy_speed = 2
                        enemy.x = enemy_start_pos
                        # print('start game!')
                        menu_active = False
                        game_over = False
                        break
                    else:
                        sys.exit()

            # window.blit(screen, (0, 0)
            clock.tick(fps)
            pygame.display.flip()


class Sprite():
    def __init__(self, x, y, file_name):
        self.x = x
        self.y = y
        self.bitmap = pygame.image.load(file_name)
        self.bitmap.set_colorkey((255, 255, 255))

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

    def x2(self):
        return self.x + self.bitmap.get_width()

    def y2(self):
        return self.y + self.bitmap.get_height()


enemy_start_pos = -150
enemy = Sprite(50, 150, 'images/enemy.png')
enemy.go_right = True

core_start = 440
core = Sprite(382, core_start, 'images/burning_core.png')
core.boom = False

menu_items = [(215, 230, 'GAME', 0),
              (225, 330, 'exit', 1)]
game_menu = Menu(menu_items)
game_menu.menu()

background = pygame.image.load('images/background.jpeg')
game_info_font = pygame.font.Font(None, 30)
game_over_font = pygame.font.Font(None, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_menu.menu()
            if event.key == pygame.K_SPACE and hit_count == 0:
                event.key = None
                game_menu.menu()
            if event.key == pygame.K_SPACE and hit_count > 0 and not core.boom:
                hit_count -= 1
                core.y = core_start
                core.boom = True
                event.key = None

    # screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # корабль пришельцев
    if hit_count >= 0 and not score == max_hit:
        if enemy.go_right:
            enemy.x += enemy_speed
            if enemy.x > width:
                enemy.go_right = False
        else:
            enemy.x -= enemy_speed
            if enemy.x < enemy_start_pos:
                enemy.go_right = True
        enemy.render()

    # снаряд
    if core.boom:
        core.y -= 4
        if core.y < 0:
            core.boom = False
            if hit_count == 0:
                game_over = True
        core.render()

    # счет
    hit_text = game_info_font.render(f"Осталось снарядов: {hit_count}", True, game_info_color)
    screen.blit(hit_text, (5, 5))
    score_text = game_info_font.render(f"Подбито: {score}", True, game_info_color)
    screen.blit(score_text, (5, 30))

    # GAME OVER
    if score == max_hit:
        text = 'YOU WIN!!!'
    else:
        text = 'GAME OVER'
    if game_over:
        game_over_text = game_over_font.render(text, True, game_over_color)
        screen.blit(game_over_text, (200, 250))

    # проверка попадания
    if (core.boom
            and ((enemy.x + 10 < core.x < enemy.x2() - 10) or (enemy.x + 10 < core.x2() < enemy.x2() - 10))
            and enemy.y2() >= core.y - 15 and core.y2() > enemy.y):
        score += 1
        core.boom = False
        enemy.x = enemy_start_pos
        enemy_speed += .4
        if hit_count == 0:
            game_over = True

    # all_sprites.draw(screen)
    # all_sprites.update()

    clock.tick(fps)
    pygame.display.flip()
