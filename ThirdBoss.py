import pygame
import math
import random


DIRECTIONS = ["down", "up", "left", "right"]


def load_images(path, frame_count, size):
    sheet = pygame.image.load(path).convert_alpha()
    images = []

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


def load_action(folder, boss_name, action_name, frame_count, size):
    images = {}

    for direction in DIRECTIONS:
        big_direction = direction.capitalize()

        path = (
            "Bosses/"
            + folder
            + "/"
            + boss_name
            + big_direction
            + action_name
            + ".png"
        )

        images[direction] = load_images(
            path,
            frame_count,
            size
        )

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

def load_sheet_images(path, frame_count, size):
    sheet = pygame.image.load(path).convert_alpha()
    images = []

    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()

    for i in range(frame_count):
        start_x = round(
            i * sheet_width / frame_count
        )

        end_x = round(
            (i + 1) * sheet_width / frame_count
        )

        frame_width = end_x - start_x

        image = sheet.subsurface(
            pygame.Rect(
                start_x,
                0,
                frame_width,
                sheet_height
            )
        ).copy()

        image = pygame.transform.scale(
            image,
            size
        )

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


class BossExplosion:
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
                damage_player(
                    player,
                    self.damage
                )

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

        screen.blit(
            image,
            (
                draw_x,
                draw_y
            )
        )

class WizardMagicCircle:
    def __init__(self, x, y, start_images, idle_images):
        self.x = x
        self.y = y

        self.start_images = start_images
        self.idle_images = idle_images

        self.state = "start"

        self.frame = 0
        self.frame_count = 0

        self.radius = 72

        self.damage = 1
        self.damage_wait = 45
        self.damage_timer = 0

        self.life = 240
        self.active = True

    def get_images(self):
        if self.state == "start":
            return self.start_images

        return self.idle_images

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

        if self.frame_count >= 3:
            self.frame_count = 0
            self.frame += 1

            if self.state == "start":
                if self.frame >= len(self.start_images):
                    self.state = "idle"
                    self.frame = 0

            else:
                if self.frame >= len(self.idle_images):
                    self.frame = 0

        if self.state != "idle":
            return

        self.life -= 1

        if self.life <= 0:
            self.active = False
            return

        if self.damage_timer > 0:
            self.damage_timer -= 1

        if self.player_inside(player):
            if self.damage_timer <= 0:
                damage_player(
                    player,
                    self.damage
                )

                self.damage_timer = self.damage_wait

    def draw(self, screen):
        if not self.active:
            return

        images = self.get_images()
        image = images[self.frame]

        draw_x = int(self.x) - image.get_width() // 2
        draw_y = int(self.y) - image.get_height() // 2

        screen.blit(
            image,
            (draw_x, draw_y)
        )

class ThirdBoss:
    def __init__(self, x, y):
        self.phase1_images = {
            "idle": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Idle",
                7,
                (150, 150)
            ),

            "walk": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Walk",
                8,
                (150, 150)
            ),

            "attack1": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Attack01",
                7,
                (150, 150)
            ),

            "attack2": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Attack02",
                13,
                (150, 150)
            ),

            "attack3": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Attack03",
                7,
                (150, 150)
            ),

            "hurt": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Hurt",
                4,
                (150, 150)
            ),

            "die": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Death",
                9,
                (150, 150)
            ),

            "jump": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Jump",
                5,
                (150, 150)
            ),

            "land": load_action(
                "AncientSkeleton",
                "AncientSkeleton",
                "Land",
                4,
                (150, 150)
            )
        }

        self.phase2_images = {
            "idle": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Idle",
                6,
                (150, 150)
            ),

            "walk": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Walk",
                10,
                (150, 150)
            ),

            "attack1": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Attack01",
                10,
                (200, 200)
            ),

            "attack2": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Attack02",
                4,
                (300, 300)
            ),

            "attack3": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Attack03",
                12,
                (200, 200)
            ),

            "hurt": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Hurt",
                4,
                (150, 150)
            ),

            "die": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Death",
                13,
                (150, 150)
            ),

            "jump": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Jump",
                6,
                (150, 150)
            ),

            "land": load_action(
                "SkeletonKing",
                "SkeletonKing",
                "Land",
                4,
                (150, 150)
            )
        }

        self.explosion_images = load_explosion_images(
            "SkeletonWizard/explosion-b.png",
            (160, 96)
        )

        self.magic_start_images = load_sheet_images(
            "SkeletonWizard/Tree_of_Glory-Sheet(1).png",
            31,
            (170, 170)
        )

        self.magic_idle_images = load_sheet_images(
            "SkeletonWizard/tree_of_glory_idle-Sheet(1).png",
            43,
            (170, 170)
        )

        self.x = x
        self.y = y

        self.phase = 1
        self.state = "idle"
        self.direction = "down"

        self.frame = 0
        self.frame_count = 0

        self.hp = 150
        self.max_hp = 150

        self.alive = True
        self.dead_done = False

        self.speed = 1.3
        self.jump_speed = 5
        self.detect_range = 600

        self.attack_range = 110
        self.attack_cooldown = 0
        self.attack_count = 0

        self.damage = 4
        self.damage_done = False

        self.jump_cooldown = 0
        self.jump_time = 0
        self.land_time = 0

        self.jump_dx = 0
        self.jump_dy = 0

        self.hurt_time = 0

        self.magic_range = 50
        self.magic_cooldown = 0
        self.magic_time = 0
        self.casting_magic = False
        self.magic_done = False

        self.magic_circles = []

        self.explosions = []

        self.explosion_cooldown = 0
        self.explosion_time = 0
        self.explosion_done = False

        self.casting_explosion = False
        self.warning_circle = False
        self.warning_radius = 60

        self.target_x = 0
        self.target_y = 0

        self.debug_draw = False

        self.attack_hits_done = set()

        self.hurt_sound = pygame.mixer.Sound("Bosses/BossSounds/Hurt.mp3")
        self.die_sound = pygame.mixer.Sound("Bosses/BossSounds/Die.mp3")
        self.cast_sound = pygame.mixer.Sound("Bosses/BossSounds/Cast.mp3")
        self.dash_sound = pygame.mixer.Sound("Bosses/BossSounds/Dash.mp3")
        self.earth_sound = pygame.mixer.Sound("Bosses/BossSounds/Earth.mp3")
        self.kick_sound = pygame.mixer.Sound("Bosses/BossSounds/Kick.mp3")
        self.slash1_sound = pygame.mixer.Sound("Bosses/BossSounds/Slash1.mp3")
        self.slash2_sound = pygame.mixer.Sound("Bosses/BossSounds/Slash2.mp3")
        self.slash3_sound = pygame.mixer.Sound("Bosses/BossSounds/Slash3.mp3")
        self.explosion_sound = pygame.mixer.Sound("Bosses/BossSounds/Explosion.mp3")
        self.player_hurt_sound = pygame.mixer.Sound("Bosses/BossSounds/Player_Hurt.mp3")

        self.hurt_sound.set_volume(0.4)
        self.die_sound.set_volume(0.4)
        self.cast_sound.set_volume(0.8)
        self.dash_sound.set_volume(0.4)
        self.earth_sound.set_volume(0.4)
        self.kick_sound.set_volume(0.4)
        self.slash1_sound.set_volume(0.3)
        self.slash2_sound.set_volume(0.3)
        self.slash3_sound.set_volume(0.3)
        self.explosion_sound.set_volume(1)
        self.player_hurt_sound.set_volume(0.5)

        # ===== phase transition =====
        self.phase_transition = False
        self.phase_transition_timer = 0

        self.revive_sound_played = False

        self.music_fade = False
        self.music_fade_dir = -1  # -1 fade out, +1 fade in
        self.music_fade_speed = 1 / 60  # 1秒

        self.revive_sound = pygame.mixer.Sound(
            "Bosses/BossSounds/Revive.mp3"
        )
        self.revive_sound.set_volume(0.3)

        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)

        self.chan_main = pygame.mixer.Channel(0)
        self.chan_attack1 = pygame.mixer.Channel(1)
        self.chan_attack2 = pygame.mixer.Channel(2)
        self.chan_attack3 = pygame.mixer.Channel(3)
        self.channel_state = pygame.mixer.Channel(4)


    def set_state(self, state):
        self.state = state
        self.frame = 0
        self.frame_count = 0
        self.damage_done = False

        self.attack_hits_done = set()

    def get_images(self):
        if self.phase == 1:
            images = self.phase1_images[
                self.state
            ][self.direction]

        else:
            images = self.phase2_images[
                self.state
            ][self.direction]

        if self.frame >= len(images):
            self.frame = 0

        return images

    def play_animation(self, speed):
        images = self.get_images()

        if self.phase == 2 and self.state != "die":
            speed -= 1

            if speed < 3:
                speed = 3

        self.frame_count += 1

        if self.frame_count < speed:
            return False

        self.frame_count = 0
        self.frame += 1

        if self.frame < len(images):
            return False

        if self.state == "die":
            self.alive = False
            self.frame = len(images) - 1
            if self.phase == 2:
                self.dead_done = True

        elif self.state in [
            "attack1",
            "attack2",
            "attack3",
            "jump",
            "land"
        ]:
            self.frame = len(images) - 1

        else:
            self.frame = 0

        return True

    def get_player_distance(self, player):
        player_rect = player.get_rect()
        boss_rect = self.get_rect()

        dx = player_rect.centerx - boss_rect.centerx
        dy = player_rect.centery - boss_rect.centery

        distance = math.sqrt(
            dx * dx + dy * dy
        )

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

    def get_rect(self):
        if self.phase == 1:
            return pygame.Rect(
                self.x + 58,
                self.y + 78,
                35,
                35
            )

        return pygame.Rect(
            self.x + 55,
            self.y + 75,
            40,
            38
        )

    def get_hurt_rect(self):
        if self.phase == 1:
            return pygame.Rect(
                self.x + 50,
                self.y + 20,
                50,
                95
            )

        return pygame.Rect(
            self.x + 43,
            self.y + 30,
            65,
            95
        )

    def get_attack_rect(self):
        boss_rect = self.get_rect()

        return pygame.Rect(
            boss_rect.right - 53,
            boss_rect.centery - 34,
            70,
            70
        )

    def get_attack1_rect(self):
        boss = self.get_rect()

        if self.direction == "down":
            return pygame.Rect(
                boss.centerx - 60,
                boss.bottom - 40,
                120,
                90
            )

        if self.direction == "up":
            return pygame.Rect(
                boss.centerx - 60,
                boss.top - 70,
                120,
                90
            )

        if self.direction == "left":
            return pygame.Rect(
                boss.left - 60,
                boss.centery - 90,
                70,
                140
            )

        return pygame.Rect(
            boss.right - 10,
            boss.centery - 90,
            70,
            140
        )

    def get_attack2_rect(self):
        boss = self.get_rect()

        if self.direction == "down":
            return pygame.Rect(
                boss.centerx - 80,
                boss.bottom - 70,
                160,
                110
            )

        if self.direction == "up":
            return pygame.Rect(
                boss.centerx - 80,
                boss.top - 70,
                160,
                110
            )

        if self.direction == "left":
            return pygame.Rect(
                boss.left - 60,
                boss.centery - 105,
                110,
                160
            )

        return pygame.Rect(
            boss.right - 60,
            boss.centery - 105,
            110,
            160
        )

    def get_attack3_rect(self):
        boss = self.get_rect()

        if self.direction == "down":
            return pygame.Rect(
                boss.centerx - 20,
                boss.bottom - 20,
                40,
                70
            )

        if self.direction == "up":
            return pygame.Rect(
                boss.centerx - 20,
                boss.top - 90,
                40,
                70
            )

        if self.direction == "left":
            return pygame.Rect(
                boss.left - 60,
                boss.centery - 55,
                70,
                40
            )

        return pygame.Rect(
            boss.right - 10,
            boss.centery - 55,
            70,
            40
        )

    def get_attack1_rect_1(self):
        boss = self.get_rect()

        if self.direction == "down":
            return pygame.Rect(
                boss.centerx - 90,
                boss.bottom - 90,
                180,
                130
            )

        if self.direction == "up":
            return pygame.Rect(
                boss.centerx - 90,
                boss.top - 130,
                180,
                130
            )

        if self.direction == "left":
            return pygame.Rect(
                boss.left - 80,
                boss.centery - 140,
                130,
                200
            )

        return pygame.Rect(
            boss.right - 50,
            boss.centery - 130,
            130,
            190
        )

    def get_attack2_rect_1(self):
        boss = self.get_rect()

        return pygame.Rect(
            boss.right - 95,
            boss.centery - 110,
            150,
            150
        )

    def get_attack3_rect_1(self):
        boss = self.get_rect()

        return pygame.Rect(
            boss.right - 110,
            boss.centery - 60,
            180,
            120
        )

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
        self.state = "walk"

        move_x = dx / distance * self.speed
        move_y = dy / distance * self.speed

        self.move_and_check_wall(
            move_x,
            move_y,
            walls
        )

        self.play_animation(6)

    def start_attack(self):
        self.casting_explosion = False
        self.warning_circle = False

        self.attack_count += 1

        if self.attack_count % 3 == 1:
            self.set_state("attack1")

        elif self.attack_count % 3 == 2:
            self.set_state("attack2")

        else:
            self.set_state("attack3")

        if self.phase == 1:
            self.attack_cooldown = 110

        else:
            self.attack_cooldown = 75

    def start_explosion_attack(self, player):

        self.chan_main.play(self.cast_sound)

        self.set_state("attack3")

        self.casting_explosion = True
        self.explosion_done = False

        self.explosion_time = 60
        self.explosion_cooldown = 180

        player_rect = player.get_hurt_rect()

        self.target_x = player_rect.centerx
        self.target_y = player_rect.centery

        self.warning_circle = True

    def start_magic_attack(self):

        self.set_state("attack2")

        self.casting_magic = True

        self.magic_done = False

        self.magic_time = 45

        self.magic_cooldown = 240

    def cast_explosion(self):
        if self.explosion_done:
            return

        self.chan_main.play(self.explosion_sound)

        explosion = BossExplosion(
            self.target_x,
            self.target_y,
            self.explosion_images
        )

        self.explosions.append(explosion)

        self.explosion_done = True
        self.warning_circle = False

    def cast_magic_circle(self):

        if self.magic_done:
            return

        boss_rect = self.get_rect()

        circle = WizardMagicCircle(
            boss_rect.centerx,
            boss_rect.bottom,
            self.magic_start_images,
            self.magic_idle_images
        )

        self.magic_circles.append(circle)

        self.magic_done = True

    def update_explosions(self, player):
        for explosion in self.explosions[:]:

            explosion.move(player)

            if not explosion.active:
                self.explosions.remove(explosion)

    def update_magic(self, player):

        for circle in self.magic_circles[:]:

            circle.move(player)

            if not circle.active:
                self.magic_circles.remove(circle)

    def update_music(self):
        if not self.music_fade:
            return

        vol = pygame.mixer.music.get_volume()
        vol += self.music_fade_dir * self.music_fade_speed

        if vol <= 0:
            vol = 0
            self.music_fade = False

        if vol >= 1:
            vol = 1
            self.music_fade = False

        pygame.mixer.music.set_volume(vol)

    def start_jump_attack(self, dx, dy, distance):
        self.casting_explosion = False
        self.warning_circle = False

        self.set_state("jump")

        self.jump_dx = dx / distance
        self.jump_dy = dy / distance

        if self.phase == 1:
            self.channel_state.play(self.dash_sound)
            self.jump_time = 25
            self.land_time = 20
            self.jump_cooldown = 180

        else:
            self.channel_state.play(self.dash_sound)
            self.jump_time = 22
            self.land_time = 15
            self.jump_cooldown = 120

    def handle_phase1_attack(self, player):

        if self.state == "attack1":

            if self.frame == 6 and "a1" not in self.attack_hits_done:

                self.chan_attack1.play(self.slash1_sound)

                if self.get_attack1_rect().colliderect(player.get_hurt_rect()):
                    self.hit_player(player)

                self.attack_hits_done.add("a1")

        if self.state == "attack2":

            for f in [4, 7, 10]:

                key = f"a2_{f}"

                if key in self.attack_hits_done:
                    continue

                # 👉 关键：窗口判定（不是只看==）
                if abs(self.frame - f) <= 1:

                    if f == 4:
                        self.chan_attack1.play(self.slash1_sound)
                    elif f == 7:
                        self.chan_attack2.play(self.slash2_sound)
                    elif f == 10:
                        self.chan_attack3.play(self.slash3_sound)

                    if self.get_attack2_rect().colliderect(player.get_hurt_rect()):
                        player.health -= 2
                        self.channel_state.play(self.player_hurt_sound)

                        player.hp = player.health
                        player.hit = True
                        player.hit_timer = 20
                        player.hit_flash_counter = 0

                    self.attack_hits_done.add(key)

        if self.state == "attack3":

            if self.frame == 6 and "a3" not in self.attack_hits_done:

                self.chan_attack1.play(self.kick_sound)

                if self.get_attack3_rect().colliderect(player.get_hurt_rect()):
                    self.hit_player(player)

                    dx = player.get_rect().centerx - self.get_rect().centerx
                    dy = player.get_rect().centery - self.get_rect().centery

                    dist = math.sqrt(dx * dx + dy * dy) or 1

                    player.x += dx / dist * 50
                    player.y += dy / dist * 50

                    player.stunned = True
                    player.stun_time = int(0.5 * 60)

                self.attack_hits_done.add("a3")

    def handle_phase2_attack(self, player):

        if self.state == "attack1":

            hit_frames = [4, 9]

            for f in hit_frames:
                key = f"a1_{f}"

                if self.frame == f and key not in self.attack_hits_done:

                    if f == 4:
                        self.chan_attack1.play(self.slash1_sound)
                    elif f == 9:
                        self.chan_attack2.play(self.slash2_sound)

                    if self.get_attack1_rect().colliderect(player.get_hurt_rect()):
                        player.health -= 6
                        self.channel_state.play(self.player_hurt_sound)
                        player.hp = player.health
                        player.hit = True
                        player.hit_timer = 20
                        player.hit_flash_counter = 0

                    self.attack_hits_done.add(key)

        if self.state == "attack2":

            if self.frame == 1 and "a2" not in self.attack_hits_done:

                self.chan_attack3.play(self.slash3_sound)

                if self.get_attack2_rect().colliderect(player.get_hurt_rect()):
                    player.health -= 3
                    self.channel_state.play(self.player_hurt_sound)
                    player.hp = player.health
                    player.hit = True
                    player.hit_timer = 20
                    player.hit_flash_counter = 0

                self.attack_hits_done.add("a2")

        if self.state == "attack3":

            if self.frame == 11 and "a3" not in self.attack_hits_done:

                self.chan_main.play(self.earth_sound)

                if self.get_attack3_rect().colliderect(player.get_hurt_rect()):
                    self.hit_player(player)

                    dx = player.get_rect().centerx - self.get_rect().centerx
                    dy = player.get_rect().centery - self.get_rect().centery

                    dist = math.sqrt(dx * dx + dy * dy) or 1

                    player.x += dx / dist * 50
                    player.y += dy / dist * 50

                    player.stunned = True
                    player.stun_time = int(60)

                self.attack_hits_done.add("a3")

        if self.state == "land":

            if self.frame == 0 and "land" not in self.attack_hits_done:
                self.chan_main.play(self.dash_sound)

                if self.get_attack_rect().colliderect(player.get_hurt_rect()):
                    self.hit_player(player)

                self.attack_hits_done.add("land")

    def check_hit_player(self, player):
        if self.damage_done:
            return

        if self.state not in [
            "attack1",
            "attack2",
            "attack3",
            "land"
        ]:
            return

        images = self.get_images()
        hit_frame = len(images) // 2

        if self.frame != hit_frame:
            return

        player_rect = player.get_hurt_rect()

        if self.get_attack_rect().colliderect(player_rect):
            self.hit_player(player)
            self.damage_done = True

    def hit_player(self, player):
        if player.hit:
            return

        player.health -= self.damage
        self.channel_state.play(self.player_hurt_sound)
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

    def count_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        if self.explosion_cooldown > 0:
            self.explosion_cooldown -= 1

        if self.magic_cooldown > 0:
            self.magic_cooldown -= 1

    def start_phase_two(self):
        self.phase = 2

        self.alive = True

        self.hp = 200
        self.max_hp = 200

        self.speed = 1.8
        self.jump_speed = 7

        self.detect_range = 700
        self.attack_range = 120

        self.damage = 6

        self.attack_cooldown = 50
        self.jump_cooldown = 70
        self.explosion_cooldown = 75

        self.casting_explosion = False
        self.warning_circle = False

        self.set_state("hurt")
        self.hurt_time = 50

    def hit(self, damage):
        if not self.alive:
            return

        self.hp -= damage

        self.channel_state.play(self.hurt_sound)

        self.warning_circle = False
        self.casting_explosion = False

        if self.hp <= 0:

            if self.phase == 1:
                self.hp = 0

                self.phase_transition = True
                self.phase_transition_timer = 180  # 3秒

                self.set_state("die")

                # 🎵 开始fade out音乐（1秒）
                self.music_fade = True
                self.music_fade_dir = -1
                self.music_fade_speed = 1 / 60

                return

            self.hp = 0

            self.channel_state.play(self.die_sound)

            self.alive = False
            self.set_state("die")
            return

        self.set_state("hurt")

        if self.phase == 1:
            self.hurt_time = 15

        else:
            self.hurt_time = 10

    def move(self, player, walls):
        self.update_explosions(player)
        self.update_magic(player)

        if self.phase_transition:

            self.play_animation(7)

            self.phase_transition_timer -= 1

            # ===== 第2秒：播放诈尸音 =====

            # ===== 结束：进入P2 =====
            if self.phase_transition_timer <= 0:
                self.phase_transition = False

                self.start_phase_two()
                if not self.revive_sound_played:
                    self.chan_main.play(self.revive_sound)
                    self.channel_state.play(self.die_sound)
                    self.revive_sound_played = True

                # 🎵 开始fade in音乐（1秒）
                self.music_fade = True
                self.music_fade_dir = 1
                self.music_fade_speed = 1 / 60

            return

        if not self.alive:
            self.warning_circle = False
            self.state = "die"
            self.play_animation(7)
            return

        self.count_cooldown()

        if self.state == "hurt":
            self.hurt_time -= 1
            self.play_animation(5)

            if self.hurt_time <= 0:
                self.set_state("idle")

            return

        dx, dy, distance = self.get_player_distance(player)

        if (
                self.phase == 2
                and distance < 50
                and self.magic_cooldown <= 0
        ):
            self.start_magic_attack()
            return

        # 初始化权重
        score_attack = 0
        score_jump = 0
        score_walk = 0
        score_explosion = 0

        if distance < 160:

            score_attack += 120
            score_walk += 30

        elif distance < 350:

            score_walk += 80
            score_attack += 60

            # 中距离有机会放爆炸
            if self.phase == 2:
                score_explosion += 90

        else:

            score_jump += 120

            # 远距离优先爆炸
            if self.phase == 2:
                score_explosion += 180

        if self.phase == 2:
            score_attack += 20
            score_jump += 20

            # 让爆炸有随机性
            score_explosion += random.randint(0, 40)

        if self.attack_cooldown > 0:
            score_attack -= 80

        if self.jump_cooldown > 0:
            score_jump -= 80

        if self.explosion_cooldown > 0:
            score_explosion -= 80

        score_attack += random.randint(0, 25)
        score_jump += random.randint(0, 25)
        score_walk += random.randint(0, 15)

        scores = {
            "attack": score_attack,
            "jump": score_jump,
            "walk": score_walk,
            "explosion": score_explosion
        }

        action = max(scores, key=scores.get)

        self.face_player(dx, dy)

        if self.casting_magic:

            self.magic_time -= 1

            if self.magic_time <= 20:
                self.cast_magic_circle()

            if self.magic_time <= 0:
                self.casting_magic = False

        if self.casting_explosion:
            self.explosion_time -= 1

            self.play_animation(6)

            if self.explosion_time <= 30:
                self.cast_explosion()

            if self.explosion_time <= 0:
                self.casting_explosion = False
                self.warning_circle = False
                self.set_state("idle")

            return

        if self.state in ["attack1", "attack2", "attack3"]:

            if self.phase == 1:
                self.handle_phase1_attack(player)

            else:
                self.handle_phase2_attack(player)

            if self.play_animation(6):
                self.set_state("idle")

            return

        if self.state == "jump":
            self.jump_time -= 1

            move_x = self.jump_dx * self.jump_speed
            move_y = self.jump_dy * self.jump_speed

            self.move_and_check_wall(
                move_x,
                move_y,
                walls
            )

            self.play_animation(5)

            if self.jump_time <= 0:
                self.set_state("land")

            return

        if self.state == "land":
            self.land_time -= 1

            self.check_hit_player(player)

            if (
                self.land_time <= 0
                or self.play_animation(5)
            ):
                self.set_state("idle")

            return


        if action == "attack":
            if self.attack_cooldown <= 0:
                self.start_attack()
            else:
                self.walk_to_player(dx, dy, distance, walls)
            return

        if action == "jump":
            if self.jump_cooldown <= 0:
                self.start_jump_attack(dx, dy, distance)
            else:
                self.walk_to_player(dx, dy, distance, walls)
            return

        if action == "explosion":
            if self.phase == 2 and self.explosion_cooldown <= 0:
                self.start_explosion_attack(player)
            else:
                self.walk_to_player(dx, dy, distance, walls)
            return

        if action == "walk":
            self.walk_to_player(dx, dy, distance, walls)
            return

        # fallback
        self.state = "idle"
        self.play_animation(7)

    def draw_warning_circle(self, screen):
        if not self.warning_circle:
            return

        if not self.alive or self.phase != 2:
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
        if not self.alive or self.state == "die":
            return

        bar_x = self.x + 10
        bar_y = self.y - 15

        width = 130
        height = 10

        current_width = (
            width * self.hp / self.max_hp
        )

        if self.phase == 1:
            color = (180, 30, 30)

        else:
            color = (160, 40, 200)

        pygame.draw.rect(
            screen,
            (40, 40, 40),
            (
                bar_x,
                bar_y,
                width,
                height
            )
        )

        pygame.draw.rect(
            screen,
            color,
            (
                bar_x,
                bar_y,
                current_width,
                height
            )
        )

    def draw(self, screen):
        self.draw_warning_circle(screen)

        for explosion in self.explosions:
            explosion.draw(screen)

        for magic in self.magic_circles:
            magic.draw(screen)

        images = self.get_images()
        image = images[self.frame]

        if self.phase == 2 and self.alive:
            image = image.copy()
            image.fill(
                (35, 0, 45, 0),
                special_flags=pygame.BLEND_RGBA_ADD
            )

        draw_x = self.x + 75 - image.get_width() // 2
        draw_y = self.y + 150 - image.get_height()

        if self.state == "attack2" and self.phase == 2:
            draw_y += 60

        screen.blit(image, (draw_x, draw_y))

        self.draw_health_bar(screen)


        if self.debug_draw:
            # body
            pygame.draw.rect(screen, (0, 120, 255), self.get_rect(), 2)

            # hurt
            pygame.draw.rect(screen, (0, 255, 0), self.get_hurt_rect(), 2)

            # attack1
            pygame.draw.rect(screen, (255, 60, 60), self.get_attack1_rect(), 2)

            # attack2
            pygame.draw.rect(screen, (255, 150, 60), self.get_attack2_rect(), 2)

            # attack3
            pygame.draw.rect(screen, (255, 0, 255), self.get_attack3_rect(), 2)

            pygame.draw.rect(screen, (255, 60, 60), self.get_attack1_rect_1(), 2)

            # attack2
            pygame.draw.rect(screen, (255, 150, 60), self.get_attack2_rect_1(), 2)

            # attack3
            pygame.draw.rect(screen, (255, 0, 255), self.get_attack3_rect_1(), 2)

            # attack3
            pygame.draw.rect(screen, (255, 255, 255), self.get_attack_rect(), 2)

