import pygame


class Tower:
    def __init__(self, x, y, image, rate, price, attack_count):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image = image
        self.radius = 150
        self.rate = rate
        self.price = price
        self.attack_count = attack_count
        self.last_attack_time = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()

    def draw(self, surface):
        surface.blit(self.image, (self.x - 25, self.y - 25))

        for bullet in self.bullets:
            surface.blit(bullet.image, bullet.rect)
            if bullet.destroy:
                self.bullets.remove(bullet)

    def attack(self, enemies, score):
        current_time = pygame.time.get_ticks()
        enemies_in_range = []

        for enemy in enemies:
            distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
            if distance <= self.radius:
                enemies_in_range.append(enemy)

        if current_time - self.last_attack_time >= self.rate:
            for i in range(min(self.attack_count, len(enemies_in_range))):
                enemy = enemies_in_range[i]
                distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
                if distance <= self.radius:
                    bullet = Bullet(self.x, self.y, enemy.x, enemy.y)
                    self.bullets.add(bullet)
            self.last_attack_time = current_time

        for bullet in self.bullets.sprites():
            bullet.update()
            for enemy in enemies:
                if bullet.check_collision(enemy):
                    enemy.health -= 1
                    score += 1
                    bullet.destroy = True

        self.bullets.update()

        return score

    def remove(self, towers):
        towers.remove(self)

    def is_in_range(self, x, y):
        distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return distance <= 52


class Tower1(Tower):
    def __init__(self, x, y):
        tower_image = pygame.image.load('images/tower.png')
        super().__init__(x, y, tower_image, 900, 30, 1)


class Tower2(Tower):
    def __init__(self, x, y):
        tower_image = pygame.image.load('images/tower_c.png')
        super().__init__(x, y, tower_image, 900, 50, 2)


class Tower3(Tower):
    def __init__(self, x, y):
        tower_image = pygame.image.load('images/tower_s.png')
        super().__init__(x, y, tower_image, 400, 70, 1)


class Tower4(Tower):
    def __init__(self, x, y):
        tower_image = pygame.image.load('images/tower_g.png')
        super().__init__(x, y, tower_image, 500, 105, 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.original_image = pygame.image.load('images/bullet.png')
        self.image = self.original_image
        self.rect = self.original_image.get_rect(center=(x, y))
        self.original_rect = self.rect
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 4
        self.damage = 1
        self.destroy = False

    def update(self):
        direction_x = self.target_x - self.rect.centerx
        direction_y = self.target_y - self.rect.centery
        distance = ((direction_x ** 2) + (direction_y ** 2)) ** 0.5
        if distance != 0:
            self.rect.centerx += (direction_x / distance) * self.speed
            self.rect.centery += (direction_y / distance) * self.speed

        if self.target_x - self.original_rect.centerx > 0 >= direction_x:
            self.destroy = True
        if self.target_x - self.original_rect.centerx < 0 <= direction_x:
            self.destroy = True

        angle = -pygame.math.Vector2(direction_x, direction_y).angle_to((1, 0))
        self.image = pygame.transform.rotozoom(self.original_image, angle, 0.4)  # 傳遞計算的角度
        self.rect = self.image.get_rect(center=self.rect.center)

    def check_collision(self, enemy):
        return pygame.sprite.collide_rect(self, enemy)


class Hammer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image = pygame.image.load('images/hammer.png')

    def draw(self, surface):
        surface.blit(self.image, (self.x - 25, self.y - 25))
