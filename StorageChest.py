import pygame
import math

from Inventory import Inventory


class StorageChest:

    def __init__(self, x, y, chest_id, game_data):

        self.chest_id = chest_id
        self.game_data = game_data

        self.rect = pygame.Rect(
            x,
            y,
            64,
            64
        )

        self.inventory = Inventory(cols=8, rows=6)

        chests = self.game_data.get("storage_chests", {})

        if self.chest_id in chests:
            self.inventory.load(chests[self.chest_id])

        self.ui_open = False

        self.f_image = pygame.image.load(
            "Graphics/F.png"
        ).convert_alpha()

        self.f_image = pygame.transform.scale(self.f_image, (32, 32))

    def save(self):
        if "storage_chests" not in self.game_data:
            self.game_data["storage_chests"] = {}

        self.game_data["storage_chests"][self.chest_id] = self.inventory.save()

    def can_interact(self, player):

        area = self.rect.inflate(
            120,
            120
        )

        return area.colliderect(
            player.get_rect()
        )

    def draw_prompt(self, screen, player):

        if not self.can_interact(player):
            return

        offset = math.sin(
            pygame.time.get_ticks() * 0.01
        ) * 5

        screen.blit(
            self.f_image,
            (
                self.rect.centerx - 45,
                self.rect.top - 45 + offset
            )
        )

    def draw_collision(self, screen):

        pygame.draw.rect(
            screen,
            (255, 0, 255),
            self.rect,
            2
        )