import pygame
import random


DIRECTIONS = ["down", "left", "right", "up"]


def load_npc_images(path, size):
    sheet = pygame.image.load(path).convert_alpha()
    images = {}

    frame_width = sheet.get_width() // 3
    frame_height = sheet.get_height() // 4

    for row in range(4):
        direction = DIRECTIONS[row]
        images[direction] = []

        for col in range(3):
            image = sheet.subsurface(
                pygame.Rect(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )
            ).copy()

            image = pygame.transform.scale(
                image,
                size
            )

            images[direction].append(image)

    return images


class RandomNPC:
    def __init__(
            self,
            npc_id,
            x,
            y,
            size=48,
            image_path="RandomNPCs/Male 18-1.png",
            lines=None,
            gift_item=None,
            gift_key="random_npc_gift",
            can_move=True,
            gender = "male"

    ):
        self.size = size
        self.images = load_npc_images(
            image_path,
            (size, size)
        )

        self.can_move_enabled = can_move

        self.npc_id = npc_id

        self.x = x
        self.y = y

        self.direction = "down"
        self.frame = 1
        self.frame_count = 0

        self.speed = 1
        self.moving = False

        self.wait_timer = 60
        self.walk_timer = 0

        self.move_x = 0
        self.move_y = 0

        if lines is None:
            self.lines = [
                "Hello there.",
                "The city is peaceful today.",
                "Take this. It may help you later."
            ]
        else:
            self.lines = lines

        self.gift_item = gift_item
        self.gift_key = gift_key

        self.gender = gender

        if self.gender == "female":

            self.sound = [
                pygame.mixer.Sound(
                    f"NPCs/Sounds/Female{random.randint(1, 3)}.mp3"
                )
            ]

        else:

            self.sound = [
                pygame.mixer.Sound(
                    f"NPCs/Sounds/Male{random.randint(1, 3)}.mp3"
                )
            ]


    def get_rect(self):
        return pygame.Rect(
            int(self.x) + self.size/3,
            int(self.y) + self.size/1.5,
            self.size/3,
            self.size/4
        )

    def get_talk_rect(self):
        return self.get_rect().inflate(
            self.size/0.96,
            self.size/0.96
        )

    def is_near(self, player):
        return self.get_talk_rect().colliderect(
            player.get_rect()
        )

    def choose_new_move(self):
        choice = random.randint(0, 4)

        self.move_x = 0
        self.move_y = 0
        self.moving = False

        if choice == 0:
            self.direction = "down"
            self.move_y = self.speed
            self.moving = True

        if choice == 1:
            self.direction = "up"
            self.move_y = -self.speed
            self.moving = True

        if choice == 2:
            self.direction = "left"
            self.move_x = -self.speed
            self.moving = True

        if choice == 3:
            self.direction = "right"
            self.move_x = self.speed
            self.moving = True

        self.walk_timer = random.randint(
            40,
            120
        )

    def can_move(self, dx, dy, walls):
        test_rect = self.get_rect().move(
            dx,
            dy
        )

        for wall in walls:
            if test_rect.colliderect(wall):
                return False

        return True

    def move(self, walls):
        if not self.can_move_enabled:
            self.animate()
            return

        if self.wait_timer > 0:
            self.wait_timer -= 1

            if self.wait_timer <= 0:
                self.choose_new_move()

            self.animate()
            return

        if self.walk_timer > 0:
            self.walk_timer -= 1

            if self.moving:
                if self.can_move(self.move_x, self.move_y, walls):
                    self.x += self.move_x
                    self.y += self.move_y

                else:
                    self.walk_timer = 0

            self.animate()

            if self.walk_timer <= 0:
                self.wait_timer = random.randint(
                    30,
                    90
                )

                self.moving = False

            return

        self.wait_timer = random.randint(
            30,
            90
        )

    def talk(
            self,
            player,
            dialogue,
            inventory,
            game_data
    ):
        if not self.is_near(player):
            return False

        self.moving = False
        self.move_x = 0
        self.move_y = 0
        self.walk_timer = 0
        self.wait_timer = 90

        if len(self.sound) > 0:
            random.choice(self.sound).play()

        dialogue.start(self.lines)

        if self.gift_item is not None:

            if self.npc_id not in game_data["npc_gifts"]:
                inventory.add_item(self.gift_item)
                game_data["npc_gifts"].add(self.npc_id)

        return True

    def animate(self):
        self.frame_count += 1

        if self.moving:
            if self.frame_count >= 10:
                self.frame_count = 0
                self.frame += 1

                if self.frame >= 3:
                    self.frame = 0

        else:
            self.frame = 1

    def draw(self, screen):
        image = self.images[self.direction][self.frame]

        screen.blit(
            image,
            (
                int(self.x),
                int(self.y)
            )
        )