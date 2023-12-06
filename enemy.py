import pygame


class Enemy:
    def __init__(self, path, mh):
        self.path = path
        self.speed = 1
        self.index = 0
        self.x, self.y = self.path[self.index]
        self.width, self.height = 50, 50
        self.rect = pygame.Rect(self.x - 25, self.y - 25, self.width, self.height)
        self.radius = 50
        self.reached = False
        self.max_health = mh
        self.health = mh

    def move(self):
        if not self.reached:
            next_x, next_y = self.path[self.index + 1]
            if self.x != next_x or self.y != next_y:
                if next_x > self.x:
                    self.x += self.speed
                elif next_x < self.x:
                    self.x -= self.speed
                if next_y > self.y:
                    self.y += self.speed
                elif next_y < self.y:
                    self.y -= self.speed
            else:
                self.index += 1
                if self.index == len(self.path) - 1:
                    self.reached = True

        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        enemy_image = pygame.image.load("images/enemy.png")
        enemy_rect = enemy_image.get_rect()
        enemy_rect.center = (self.x, self.y)
        surface.blit(enemy_image, enemy_rect)
        pygame.draw.rect(surface, (20, 20, 20), pygame.Rect(self.x - 25, self.y - 35, 50, 5), border_radius=2)
        health_bar_length = (self.health / self.max_health) * 48
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.x - 24, self.y - 34, health_bar_length, 3),
                         border_radius=2)
        font = pygame.font.Font('adventures.ttf', 14)
        text = font.render(str(self.health), True, (235, 0, 0))
        outline_text_e = font.render(str(self.health), True, (20, 20, 20))
        text_rect = text.get_rect(center=(self.x, self.y - 42))
        surface.blit(outline_text_e, text_rect.move(0, 1))
        surface.blit(text, text_rect)

    def collision(self, target):
        return self.rect.colliderect(target)
