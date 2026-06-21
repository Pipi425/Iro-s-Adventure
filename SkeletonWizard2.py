import pygame
import math


DIRECTIONS = ["down", "up", "left", "right"]


def load_skeleton_row(sheet, row, frame_count, size):
    images = []

    frame_width = sheet.get_width() // 6
    frame_height = sheet.get_height() // 8

    for i in range(frame_count):
        image = sheet.subsurface(
            pygame.Rect(
                i * frame_width,
                row * frame_height,
                frame_width,
                frame_height
            )
        ).copy()

        image = pygame.transform.scale(image, size)
        images.append(image)

    return images


def load_skeleton_images(path, size):
    sheet = pygame.image.load(path).convert_alpha()

    return {
        "idle": {
            "down": load_skeleton_row(sheet, 0, 4, size),
            "up": load_skeleton_row(sheet, 2, 4, size),
            "left": load_skeleton_row(sheet, 4, 4, size),
            "right": load_skeleton_row(sheet, 6, 4, size)
        },

        "walk": {
            "down": load_skeleton_row(sheet, 1, 6, size),
            "up": load_skeleton_row(sheet, 3, 6, size),
            "left": load_skeleton_row(sheet, 5, 6, size),
            "right": load_skeleton_row(sheet, 7, 6, size)
        }
    }


def load_book_images(path, size):
    sheet = pygame.image.load(path).convert_alpha()
    images = {}

    frame_width = sheet.get_width() // 32
    frame_height = sheet.get_height()

    starts = {
        "down": 0,
        "up": 8,
        "right": 16,
        "left": 24
    }

    for direction in DIRECTIONS:
        images[direction] = []

        start = starts[direction]

        for i in range(8):
            image = sheet.subsurface(
                pygame.Rect(
                    (start + i) * frame_width,
                    0,
                    frame_width,
                    frame_height
                )
            ).copy()

            image = pygame.transform.scale(image, size)
            images[direction].append(image)

    return images


def load_explosion_images(path, size):
    sheet = pygame.image.load(path).convert_alpha()
    images = []

    frame_count = 13
    frame_width = sheet.get_width() // frame_count
    frame_height = sheet.get_height()

    for i in range(frame_count):
        image = sheet.subsurface(
            pygame.Rect(
                i * frame_width,
                0,
                frame_width,
                frame_height
            )
        ).copy()

        image = pygame.transform.scale(image, size)
        images.append(image)

    return images


def damage_player(player, damage):
    if player.dead or player.hit:
        return

    player.health -= damage
    player.hp = player.health

    player.hit = True
    player.hit_timer = 60
    player.hit_flash_counter = 0

    if player.health <= 0:
        player.health = 0
        player.hp = 0
        player.dead = True

    if len(player.hurt_sound) > 0:
        player.hurt_sound[0].play()


class WizardExplosion:
    def __init__(self, x, y, images):
        self.x = x
        self.y = y

        self.images = images

        self.frame = 0
        self.frame_count = 0

        self.radius = 60
        self.damage = 3

        self.damage_done = False
        self.active = True

    def player_inside(self, player):
        player_rect = player.get_hurt_rect()

        dx = player_rect.centerx - self.x
        dy = player_rect.centery - self.y

        distance = math.sqrt(dx * dx + dy * dy)

        return distance <= self.radius

    def move(self, player):
        if not self.active:
            return

        self.frame_count += 1

        if self.frame_count < 4:
            return

        self.frame_count = 0
        self.frame += 1

        if self.frame == 5 and not self.damage_done:
            if self.player_inside(player):
                damage_player(player, self.damage)

            self.damage_done = True

        if self.frame >= len(self.images):
            self.frame = len(self.images) - 1
            self.active = False

    def draw(self, screen):
        if not self.active:
            return

        image = self.images[self.frame]

        draw_x = int(self.x) - image.get_width() // 2
        draw_y = int(self.y) - image.get_height() // 2

        screen.blit(image, (draw_x, draw_y))


class SkeletonWizard2:
    def __init__(self, x, y):
        self.images = load_skeleton_images(
            "SkeletonWizard/Skeleton_8-Sheet-NoOutline.png",
            (70, 70)
        )

        self.book_images = load_book_images(
            "SkeletonWizard/Book-Sheet-NoOutline.png",
            (90, 90)
        )

        self.explosion_images = load_explosion_images(
            "SkeletonWizard/explosion-b.png",
            (160, 96)
        )

        self.x = x
        self.y = y

        self.state = "idle"
        self.direction = "down"

        self.frame = 0
        self.frame_count = 0

        self.book_frame = 0
        self.book_frame_count = 0

        self.hp = 10
        self.max_hp = 10

        self.alive = True
        self.dead_done = False

        self.speed = 1

        self.detect_range = 550
        self.attack_range = 420
        self.safe_range = 170

        self.attack_cooldown = 0
        self.attack_timer = 0
        self.cast_done = False

        self.target_x = 0
        self.target_y = 0

        self.warning_circle = False
        self.warning_radius = 60

        self.hurt_time = 0

        self.explosions = []

        self.die_sound = pygame.mixer.Sound("SkeletonWizard/Sounds/Die.mp3")
        self.hurt_sound = pygame.mixer.Sound("SkeletonWizard/Sounds/Hurt.mp3")
        self.walk_sound = pygame.mixer.Sound("SkeletonWizard/Sounds/Walk.mp3")
        self.explosion_sound = pygame.mixer.Sound("SkeletonWizard/Sounds/Explosion.mp3")

        self.walk_sound.set_volume(0.3)

        self.walk_sound_timer = 0

        self.hurt_sound.set_volume(0.4)
        self.die_sound.set_volume(0.4)
        self.explosion_sound.set_volume(0.2)

    def set_state(self, state):
        if self.state == state:
            return

        self.state = state

        self.frame = 0
        self.frame_count = 0

        if state == "attack":
            self.book_frame = 0
            self.book_frame_count = 0
            self.cast_done = False

        else:
            self.warning_circle = False

    def get_images(self):
        if self.state == "walk":
            images = self.images["walk"][self.direction]
        else:
            images = self.images["idle"][self.direction]

        if self.frame >= len(images):
            self.frame = 0

        return images

    def play_animation(self, speed):
        images = self.get_images()

        self.frame_count += 1

        if self.frame_count < speed:
            return

        self.frame_count = 0
        self.frame += 1

        if self.frame >= len(images):
            self.frame = 0

    def play_book_animation(self, speed):
        images = self.book_images[self.direction]

        self.book_frame_count += 1

        if self.book_frame_count < speed:
            return

        self.book_frame_count = 0
        self.book_frame += 1

        if self.book_frame >= len(images):
            self.book_frame = len(images) - 1

    def get_rect(self):
        return pygame.Rect(
            int(self.x) + 24,
            int(self.y) + 40,
            22,
            22
        )

    def get_hurt_rect(self):
        return pygame.Rect(
            int(self.x) + 18,
            int(self.y) + 12,
            34,
            54
        )

    def get_player_distance(self, player):
        player_rect = player.get_rect()
        wizard_rect = self.get_rect()

        dx = player_rect.centerx - wizard_rect.centerx
        dy = player_rect.centery - wizard_rect.centery

        distance = math.sqrt(dx * dx + dy * dy)

        if distance == 0:
            distance = 1

        return dx, dy, distance

    def face_player(self, dx, dy):
        if abs(dx) > abs(dy):
            if dx < 0:
                self.direction = "left"
            else:
                self.direction = "right"

        else:
            if dy < 0:
                self.direction = "up"
            else:
                self.direction = "down"

    def move_and_check_wall(self, move_x, move_y, walls):
        old_x = self.x
        old_y = self.y

        self.x += move_x

        for wall in walls:
            if self.get_rect().colliderect(wall):
                self.x = old_x
                break

        self.y += move_y

        for wall in walls:
            if self.get_rect().colliderect(wall):
                self.y = old_y
                break

    def walk_to_player(self, dx, dy, distance, walls):
        self.set_state("walk")

        move_x = dx / distance * self.speed
        move_y = dy / distance * self.speed

        self.move_and_check_wall(
            move_x,
            move_y,
            walls
        )

        self.play_animation(8)

        if self.walk_sound_timer > 0:
            self.walk_sound_timer -= 1

        if self.walk_sound_timer <= 0:
            self.walk_sound.play()
            self.walk_sound_timer = 20

    def walk_away_from_player(self, dx, dy, distance, walls):
        self.set_state("walk")

        move_x = -dx / distance * self.speed
        move_y = -dy / distance * self.speed

        self.move_and_check_wall(
            move_x,
            move_y,
            walls
        )

        self.play_animation(8)

        if self.walk_sound_timer > 0:
            self.walk_sound_timer -= 1

        if self.walk_sound_timer <= 0:
            self.walk_sound.play()
            self.walk_sound_timer = 20

    def start_attack(self, player):
        self.set_state("attack")

        self.attack_cooldown = 140
        self.attack_timer = 48

        player_rect = player.get_hurt_rect()

        self.target_x = player_rect.centerx
        self.target_y = player_rect.centery

        self.warning_circle = True

    def cast_explosion(self):
        if self.cast_done:
            return

        self.explosion_sound.play()  # ⭐这里

        explosion = WizardExplosion(
            self.target_x,
            self.target_y,
            self.explosion_images
        )

        self.explosions.append(explosion)

        self.cast_done = True
        self.warning_circle = False

    def update_explosions(self, player):
        for explosion in self.explosions[:]:
            explosion.move(player)

            if not explosion.active:
                self.explosions.remove(explosion)

    def count_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def hit(self, damage):
        if not self.alive:
            return

        self.hurt_sound.play()

        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.die_sound.play()
            self.dead_done = True
            self.warning_circle = False
            return

        self.set_state("hurt")
        self.hurt_time = 18

    def move(self, player, walls):
        self.update_explosions(player)

        if not self.alive:
            return

        self.count_cooldown()

        if self.state == "hurt":
            self.hurt_time -= 1
            self.play_animation(6)

            if self.hurt_time <= 0:
                self.set_state("idle")

            return

        dx, dy, distance = self.get_player_distance(player)

        self.face_player(dx, dy)

        if self.state == "attack":
            self.play_animation(10)
            self.play_book_animation(5)

            self.attack_timer -= 1

            if self.attack_timer <= 24:
                self.cast_explosion()

            if self.attack_timer <= 0:
                self.set_state("idle")

            return

        if distance < self.safe_range:
            self.walk_away_from_player(
                dx,
                dy,
                distance,
                walls
            )
            return

        if distance <= self.attack_range:
            if self.attack_cooldown <= 0:
                self.start_attack(player)
                return

            self.set_state("idle")
            self.play_animation(10)
            return

        if distance <= self.detect_range:
            self.walk_to_player(
                dx,
                dy,
                distance,
                walls
            )
            return

        self.set_state("idle")
        self.play_animation(10)

    def draw_warning_circle(self, screen):
        if not self.warning_circle or not self.alive:
            return

        position = (
            int(self.target_x),
            int(self.target_y)
        )

        pygame.draw.circle(
            screen,
            (100, 0, 0),
            position,
            self.warning_radius,
            6
        )

        pygame.draw.circle(
            screen,
            (255, 0, 0),
            position,
            self.warning_radius,
            3
        )

        pygame.draw.circle(
            screen,
            (255, 80, 80),
            position,
            5
        )

    def draw_health_bar(self, screen):
        if not self.alive:
            return

        bar_x = int(self.x) + 8
        bar_y = int(self.y) - 8

        width = 55
        height = 6

        current_width = int(
            width * self.hp / self.max_hp
        )

        pygame.draw.rect(
            screen,
            (40, 40, 40),
            (bar_x, bar_y, width, height)
        )

        pygame.draw.rect(
            screen,
            (180, 30, 30),
            (bar_x, bar_y, current_width, height)
        )

    def draw(self, screen):
        self.draw_warning_circle(screen)

        for explosion in self.explosions:
            explosion.draw(screen)

        if not self.alive:
            return

        images = self.get_images()
        image = images[self.frame]

        screen.blit(
            image,
            (
                int(self.x),
                int(self.y)
            )
        )

        if self.state == "attack":
            book = self.book_images[
                self.direction
            ][self.book_frame]

            book_x = (
                self.get_rect().centerx
                - book.get_width() // 2
            )

            book_y = (
                self.get_rect().centery
                - book.get_height() // 2
            )

            screen.blit(
                book,
                (
                    book_x,
                    book_y
                )
            )

        self.draw_health_bar(screen)