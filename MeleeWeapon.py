import pygame


def load_melee_images():
    return {
        "down": [],
        "up": [],
        "left": [],
        "right": []
    }


class MeleeWeapon:
    def __init__(self, x, y, direction, melee_images):
        self.x = x
        self.y = y
        self.direction = direction

        self.life = 15
        self.hit_enemies = set()

        if direction == "right":
            self.attack_rect = pygame.Rect(x + 10, y - 30, 50, 60)

        elif direction == "left":
            self.attack_rect = pygame.Rect(x - 60, y - 30, 50, 60)

        elif direction == "up":
            self.attack_rect = pygame.Rect(x - 40, y - 40, 80, 50)

        else:
            self.attack_rect = pygame.Rect(x - 40, y + 10, 80, 50)

    def update(self):
        self.life -= 1

        if self.life <= 0:
            return False

        return True

    def hit_enemy(self, enemy):
        if enemy in self.hit_enemies:
            return False

        if self.attack_rect.colliderect(enemy.get_rect()):
            self.hit_enemies.add(enemy)
            return True

        return False

    def hit_boss(self, enemy):
        if enemy in self.hit_enemies:
            return False

        if self.attack_rect.colliderect(enemy.get_hurt_rect()):
            self.hit_enemies.add(enemy)
            return True

        return False

    def draw(self, screen):
        pass