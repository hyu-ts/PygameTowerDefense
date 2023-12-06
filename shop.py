import pygame

shop = {
    "tower1": (pygame.image.load("images/tower.png"), 30),
    "tower2": (pygame.image.load("images/tower_c.png"), 50),
    "tower3": (pygame.image.load("images/tower_s.png"), 70),
    "tower4": (pygame.image.load("images/tower_g.png"), 105),
    "destroy": (pygame.image.load("images/hammer.png"), 0),
}


def render_shop(window, money):
    shop_font = pygame.font.Font('adventures.ttf', 18)
    shop_surface = pygame.Surface((100, 400))
    shop_surface.fill((80, 77, 74))

    coin_image = pygame.image.load("images/coin.png")
    coin_rect = coin_image.get_rect(center=(25, 375))
    shop_surface.blit(coin_image, coin_rect)

    money_text = shop_font.render(str(money), True, (255, 255, 255))
    money_text_rect = money_text.get_rect(center=(shop_surface.get_width() // 2 + 10, 375))
    shop_surface.blit(money_text, money_text_rect)

    y_offset = 15

    button_images = []
    for i in range(1, 6):
        filename = f"images/shopBtn{i}.png"
        image = pygame.image.load(filename)
        button_images.append(image)

    for idx, button_image in enumerate(button_images):
        button_rect = button_image.get_rect(topleft=(10, y_offset))
        shop_surface.blit(button_image, button_rect)
        y_offset += 70

    window.blit(shop_surface, (700, 80))


def shop_click(event, money, selected_item, selected_price):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 700 <= mouse_x <= 800 and 95 <= mouse_y <= 430:
            item_offset = (mouse_y - 95) // 70

            if 0 <= (mouse_y - 95) % 70 < 60:
                if item_offset < len(shop):
                    item_type = list(shop.keys())[item_offset]
                    item_price = shop[item_type][1]

                    if money >= item_price and selected_item != item_type:
                        selected_item = item_type
                        selected_price = item_price

                    elif selected_item == item_type:
                        selected_item = None
                        selected_price = 0

    return money, selected_item, selected_price
