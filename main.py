import pygame
import sys
import random

from shop import render_shop, shop_click
from enemy import Enemy
from item import Tower1, Tower2, Tower3, Tower4, Hammer

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('塔防遊戲')
clock = pygame.time.Clock()


def menu():
    while True:
        window.fill((0, 0, 0))  # 背景顏色
        font = pygame.font.Font(None, 50)
        text = font.render("Game Title", True, (255, 255, 255))  # 顯示「Main Menu」文字
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 180))
        window.blit(text, text_rect)

        # 定義按鈕的屬性
        button_width, button_height = 200, 50
        button_x = (WINDOW_WIDTH - button_width) // 2
        button_y = 280

        # 建立按鈕 Rect
        start_button = pygame.Rect(button_x, button_y, button_width, button_height)
        rule_button = pygame.Rect(button_x, button_y + 70, button_width, button_height)
        quit_button = pygame.Rect(button_x, button_y + 140, button_width, button_height)

        # 渲染按鈕
        pygame.draw.rect(window, (100, 100, 100), start_button)
        pygame.draw.rect(window, (100, 100, 100), rule_button)
        pygame.draw.rect(window, (100, 100, 100), quit_button)

        # 顯示按鈕上的文字
        font = pygame.font.Font('adventures.ttf', 30)
        start_text = font.render("Start Game", True, (255, 255, 255))
        rule_text = font.render("    Rule", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        # 放置文字在按鈕中間
        start_text_rect = start_text.get_rect(center=start_button.center)
        rule_text_rect = start_text.get_rect(center=rule_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)

        # 在視窗上顯示文字
        window.blit(start_text, start_text_rect)
        window.blit(rule_text, rule_text_rect)
        window.blit(quit_text, quit_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_x, mouse_y):
                    main(True)
                    break
                elif rule_button.collidepoint(mouse_x, mouse_y):
                    pass
                elif quit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


# 主遊戲與相關設置
def draw_castle_health(castle_health):
    bar_width = 100
    bar_x = 524
    bar_y = 540

    health_bar_length = (castle_health / 200) * bar_width

    pygame.draw.rect(window, (20, 20, 20), pygame.Rect(bar_x - 1, bar_y - 1, bar_width + 2, 10),
                     border_radius=5)
    pygame.draw.rect(window, (0, 255, 0), pygame.Rect(bar_x, bar_y, health_bar_length, 8), border_radius=5)

    font = pygame.font.Font('adventures.ttf', 18)
    outline_text = font.render(str(castle_health), True, (20, 20, 20))
    text = font.render(str(castle_health), True, (0, 255, 0))

    text_rect = text.get_rect(center=(bar_x - 23 + bar_width + 40, bar_y + 5))

    window.blit(outline_text, text_rect.move(1, 1))
    window.blit(outline_text, text_rect.move(-1, -1))
    window.blit(outline_text, text_rect.move(1, -1))
    window.blit(outline_text, text_rect.move(-1, 1))
    window.blit(text, text_rect)


def valid_position(x, y, towers, enemy_path):
    if not (22 < x < 678 and 22 < y < 578):
        return False

    if 513 < x < 660 and 420 < y < 660:
        return False

    for path_index in range(len(enemy_path) - 1):
        start_x, start_y = enemy_path[path_index]
        end_x, end_y = enemy_path[path_index + 1]

        if start_x == end_x:
            if start_y < end_y:
                path_rect = pygame.Rect(start_x - 25, start_y - 25, 50, abs(end_y - start_y))
            else:
                path_rect = pygame.Rect(start_x - 25, end_y + 25, 50, abs(end_y - start_y))
        else:
            if start_x < end_x:
                path_rect = pygame.Rect(start_x - 25, start_y - 25, abs(end_x - start_x), 50)
            else:
                path_rect = pygame.Rect(end_x + 25, start_y - 25, abs(end_x - start_x), 50)

        if path_rect.collidepoint(x, y):
            return False

    for tower in towers:
        if tower.is_in_range(x, y):
            return False

    return True


def main(game):
    background = pygame.image.load('map.jpg')

    start_time = pygame.time.get_ticks()
    castle_health = 200
    castle_image = pygame.image.load('images/fort.png')
    castle_image = pygame.transform.scale(castle_image, (140, 120))
    castle_width, castle_height = 120, 100
    castle_x = 525
    castle_y = 420
    castle = pygame.Rect(castle_x, castle_y, castle_width, castle_height)

    # 商店相關
    money = 50
    last_money_increase = pygame.time.get_ticks()
    placeholder = None

    # 敵人相關

    enemy_path = [
        (0, 100),
        (220, 100),
        (220, 300),
        (80, 300),
        (80, 500),
        (390, 500),
        (390, 150),
        (590, 150),
        (590, 450)
    ]

    enemies = []

    enemy_spawn_timer = 0
    enemy_spawn_interval = 8000

    score = 0

    # 防禦塔相關
    selected_item = None
    selected_price = 0

    towers = []

    # 主程式

    while game:
        window.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        max_health = 10 + (elapsed_time // 25000) * 3 + random.randint(-1, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            money, selected_item, selected_price = shop_click(event, money, selected_item, selected_price)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if selected_item == "tower1":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_tower = Tower1(mouse_x, mouse_y)
                    placeholder = Tower1(mouse_x, mouse_y)
                    placeholder.image.set_alpha(200)
                    if valid_position(mouse_x, mouse_y, towers, enemy_path):
                        towers.append(new_tower)
                        money -= selected_price
                        selected_item = None
                        selected_price = 0
                        placeholder = None
                if selected_item == "tower2":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_tower = Tower2(mouse_x, mouse_y)
                    placeholder = Tower2(mouse_x, mouse_y)
                    placeholder.image.set_alpha(200)
                    if valid_position(mouse_x, mouse_y, towers, enemy_path):
                        towers.append(new_tower)
                        money -= selected_price
                        selected_item = None
                        selected_price = 0
                        placeholder = None
                if selected_item == "tower3":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_tower = Tower3(mouse_x, mouse_y)
                    placeholder = Tower3(mouse_x, mouse_y)
                    placeholder.image.set_alpha(200)
                    if valid_position(mouse_x, mouse_y, towers, enemy_path):
                        towers.append(new_tower)
                        money -= selected_price
                        selected_item = None
                        selected_price = 0
                        placeholder = None
                if selected_item == "tower4":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_tower = Tower4(mouse_x, mouse_y)
                    placeholder = Tower4(mouse_x, mouse_y)
                    placeholder.image.set_alpha(200)
                    if valid_position(mouse_x, mouse_y, towers, enemy_path):
                        towers.append(new_tower)
                        money -= selected_price
                        selected_item = None
                        selected_price = 0
                        placeholder = None
                if selected_item == "destroy":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    placeholder = Hammer(mouse_x, mouse_y)
                    for tower in towers:
                        if tower.rect.collidepoint(mouse_x + 25, mouse_y + 25):
                            money += tower.price
                            tower.remove(towers)
                            selected_item = None
                            selected_price = 0
                            placeholder = None
                if selected_item is None:
                    placeholder = None

        if current_time - last_money_increase > 1200:
            money += 1
            last_money_increase = current_time

        if elapsed_time - enemy_spawn_timer > enemy_spawn_interval:
            new_enemy = Enemy(enemy_path, max_health)
            enemies.append(new_enemy)
            enemy_spawn_timer = elapsed_time
            enemy_spawn_interval = random.randint(2500, 8500)

        for enemy in enemies:
            enemy.move()

            if enemy.collision(castle):
                castle_health -= enemy.health
                enemy.health = 0

            if enemy.health <= 0:
                enemies.remove(enemy)

            if castle_health <= 0:
                game = False
                game_over(score)

        for tower in towers:
            tower.draw(window)
            score = tower.attack(enemies, score)

        window.blit(castle_image, (castle_x - 10, castle_y - 5))

        draw_castle_health(castle_health)

        for enemy in enemies:
            enemy.draw(window)

        func_surface = pygame.Surface((100, 700))
        func_surface.fill((200, 200, 200))
        window.blit(func_surface, (700, 0))

        font = pygame.font.Font('adventures.ttf', 28)
        text = font.render("Score", True, (0, 0, 0))
        num = font.render(str(score), True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH - 50, 27))
        num_rect = num.get_rect(center=(WINDOW_WIDTH - 50, 57))
        window.blit(text, text_rect)
        window.blit(num, num_rect)

        render_shop(window, money)

        if placeholder:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            placeholder.x, placeholder.y = mouse_x, mouse_y
            placeholder.draw(window)

        pygame.display.update()
        clock.tick(60)


# 遊戲結束相關
def game_over(score):
    while True:
        window.fill((0, 0, 0))  # 清空視窗，可以使用其他顏色
        font = pygame.font.Font(None, 50)
        text = font.render("Game Over", True, (255, 0, 0))  # 顯示「Game Over」文字
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 180))
        window.blit(text, text_rect)

        # 顯示分數
        font_score = pygame.font.Font(None, 36)
        score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 230))
        window.blit(score_text, score_rect)

        # 定義按鈕的屬性
        button_width, button_height = 200, 50
        button_x = (WINDOW_WIDTH - button_width) // 2
        button_y = 280
        button_spacing = 20  # 按鈕之間的間距

        # 建立按鈕 Rect
        restart_button = pygame.Rect(button_x, button_y, button_width, button_height)
        menu_button = pygame.Rect(button_x, button_y + button_height + button_spacing, button_width, button_height)
        quit_button = pygame.Rect(button_x, button_y + (button_height + button_spacing) * 2, button_width,
                                  button_height)

        # 渲染按鈕
        pygame.draw.rect(window, (100, 100, 100), restart_button)
        pygame.draw.rect(window, (100, 100, 100), menu_button)
        pygame.draw.rect(window, (100, 100, 100), quit_button)

        # 顯示按鈕上的文字
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Restart", True, (255, 255, 255))
        menu_text = font.render("Back To Menu", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        # 放置文字在按鈕中間
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)

        # 在視窗上顯示文字
        window.blit(restart_text, restart_text_rect)
        window.blit(menu_text, menu_text_rect)
        window.blit(quit_text, quit_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_x, mouse_y):
                    main(True)
                    break

                elif menu_button.collidepoint(mouse_x, mouse_y):
                    menu()
                    break

                elif quit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


menu()
