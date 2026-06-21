import pygame
import random
from Character import Player
import pytmx
from Arrow import Arrow, load_arrow_images
from MeleeWeapon import MeleeWeapon, load_melee_images
from Enemy import Enemy
from Dialogue import DialogueSystem
from NPCs import NPC
from Buttons import Button
from Inventory import Inventory, InventoryUI, Consumable
from Animal import Animal
from Chest import Chest
from Sprite import SpriteObject
from SavePoint import SavePoint
from Boss import Boss
from SecondBoss import SecondBoss, MiniSecondBoss
from ThirdBoss import ThirdBoss
from SkeletonSoldier import SkeletonSoldier
from SkeletonBoxer import SkeletonBoxer
from SkeletonSword import SkeletonSword
from SkeletonWizard import SkeletonWizard
from SkeletonWizard2 import SkeletonWizard2
from StorageChest import StorageChest
from StorageChestUI import StorageChestUI
from RandomNPC import RandomNPC
from SaveSystem import (
    save_game,
    load_game,
    apply_save_data,
    respawn_from_save,
    reset_save_data,
    make_sword,
    make_key,
    make_axe,
    make_bow,
    make_bow_2,
    make_bow_3,
    make_head_1,
    make_chest_1,
    make_legs_1,
    make_hands_1,
    make_head_2,
    make_chest_2,
    make_legs_2,
    make_hands_2,
    make_head_3,
    make_chest_3,
    make_legs_3,
    make_hands_3,
    make_sword_1,
    make_sword_2,
    make_bayonet,
    make_apple,
    make_fish,
    make_bread,
    make_potato,
    make_tomato,
    make_pieapple,
    make_moonshine,
    make_potion,
    make_truth_1,
    make_truth_2,
    make_watermelon,
)
from Hint import HintAnimation
from HelpUI import HelpUI

pygame.init()

Screen1 = pygame.display.set_mode((1280, 768))
pygame.display.set_caption("Major 2")

icon = pygame.image.load("Graphics/icon.png")
pygame.display.set_icon(icon)

f_icon = pygame.image.load("Graphics/F.png").convert_alpha()
f_icon = pygame.transform.scale(f_icon, (30, 30))

river = pygame.mixer.Sound("SoundEffects/River.mp3")
river.set_volume(0.01)

bird = pygame.mixer.Sound("SoundEffects/Bird.mp3")
bird.set_volume(0.1)

def draw_save_message(screen, text):

    box = pygame.Rect(390, 560, 500, 100)

    pygame.draw.rect(screen, (25, 25, 25), box, border_radius=15)
    pygame.draw.rect(screen, (230, 220, 180), box, 3, border_radius=15)

    font = pygame.font.Font(None, 42)

    message = font.render(text, True, (240, 235, 210))

    screen.blit(
        message,
        (
            box.centerx - message.get_width() // 2,
            box.centery - message.get_height() // 2
        )
    )

def create_arrow_from_bow(player, arrows, arrow_images, arrow_sound):
    shot = player.take_arrow_shot()

    if shot is None:
        return

    x, y, direction = shot
    arrows.append(Arrow(x, y, direction, arrow_images))
    arrow_sound.play()

def eldermoor_npcs():
    npcs = []

    npcs.append(RandomNPC(
        "npc1",
        800,
        300,
        image_path="RandomNPCs/Male/Male1.png",
        lines=[
            "You looks tired my fellow traveller",
            "Please take my goodwill",
            "Hope these apple will be useful on your journey."
        ],
        gift_item=make_apple(),
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc2",
        512,
        704,
        image_path="RandomNPCs/Male/Male2.png",
        lines=[
            "Welcome to Eldermoor",
            "Try not to cause trouble",
            "We already have enough trouble.",
            "We just can not remeber where we put it."
        ],
        gift_item=None,
        can_move=False,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc3",
        1088,
        672,
        image_path="RandomNPCs/Male/Male3.png",
        lines=[
            "The cows keep walking toward the northern road",
            "I bring them back every morning",
            "Maybe they remember something I do not."
        ],
        gift_item=None,
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc4",
        896,
        110,
        image_path="RandomNPCs/Female/Female1.png",
        lines=[
            "I come here every day",
            "I think I used to wait for someone",
            "I just can not remember who",
            "Take this fish",
            "They will be useful."
        ],
        gift_item=make_fish(),
        can_move=True,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc5",
        384,
        320,
        image_path="RandomNPCs/Male/Male4.png",
        lines=[
            "I buy old weapons, broken rings, unreadable letters — anything with a past",
            "New things are cheaper",
            "They have fewer ghosts attached."
        ],
        gift_item=None,
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc6",
        160,
        110,
        image_path="RandomNPCs/Female/Female2.png",
        lines=[
            "I made twelve loaves this morning",
            "But there are only eleven people in my family",
            "Take this extra bread",
            "As my gift."
        ],
        gift_item=make_bread(),
        can_move=True,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc7",
        928,
        416,
        image_path="RandomNPCs/Male/Male5.png",
        lines=[
            "Do you have a name?",
            "My mother says everyone has one",
            "She also forgets mine sometimes"
        ],
        gift_item=None,
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc8",
        320,
        480,
        image_path="RandomNPCs/Male/Male6.png",
        lines=[
            "I used to serve in the army",
            "I do not remember which war",
            "That probably means we won",
            "Take these supplies my fellow",
            "Use them wisely on your way."
        ],
        gift_item=make_potato(),
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc9",
        618,
        472,
        image_path="RandomNPCs/Female/Female3.png",
        lines=[
            "The save stone remembers where you stood",
            "It remembers your wounds and your belongings",
            "Do not ask what it forgets in return."
        ],
        gift_item=None,
        can_move=False,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc10",
        64,
        320,
        image_path="RandomNPCs/Female/Female4.png",
        lines=[
            "Several pages are missing from every history book in the city",
            "The strange part is that the sentences continue normally",
            "As if the missing years were never needed."
        ],
        gift_item=None,
        can_move=True,
        gender="female"
    ))

    return npcs

def irohouse_npcs():
    npcs = []

    npcs.append(RandomNPC(
        "npc11",
        696,
        376,
        image_path="RandomNPCs/Female/Female5.png",
        lines=[
            "Hi there",
            "My name is Verelia",
            "This the house your father used to own",
            "Take it as your temporary shelter",
            "Also take these tomato",
            "I found them on the ground",
            "Just kidding",
            "I bought them in grocery stores",
            "Wish you all the best."
        ],
        gift_item=make_tomato(),
        can_move=False,
        gender="female"
    ))

    return npcs

def irohome_npcs():
    npcs = []

    npcs.append(RandomNPC(
        "npc12",
        696,
        440,
        image_path="RandomNPCs/Male/Male7.png",
        lines=[
            "Come here my fellow",
            "Hundreds years ago",
            "An evil force took everyone's memory and turned peace into chaos",
            "And three monster were formed in three regions",
            "These three route connects to the three regions --",
            "The land of snow with a giant stone monster;",
            "The land of sand with a bone eater;",
            "And the land of the Lava with the origin of the evil force.",
            "Your destiny is to save all three of them",
            "Due to a mysterious force",
            "You can not enter the Lava land before saving the two other region",
            "Anyways",
            "My son",
            "Take my goodwill",
            "Good Luck"
        ],
        gift_item=make_chest_1(),
        can_move=False,
        gender="male"
    ))

    return npcs

def snowvillage_npcs():
    npcs = []

    npcs.append(RandomNPC(
        "npc13",
        1176,
        216,
        image_path="RandomNPCs/Male/Male8.png",
        lines=[
            "The storm never stops.",
            "We stopped asking why a long time ago.",
            "It saves time",
            "Take this apple pie",
            "My mom made it."
        ],
        gift_item=make_pieapple(),
        can_move=False,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc14",
        24,
        280,
        image_path="RandomNPCs/Male/Male9.png",
        lines=[
            "The ice maze speak every night.",
            "I once heard it.",
            "It was telling me to not to get any closer."
        ],
        gift_item=None,
        can_move=False,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc15",
        632,
        88,
        image_path="RandomNPCs/Male/Male10.png",
        lines=[
            "I repair armor found inside the maze.",
            "Every piece has the same old symbol.",
            "No army in our records ever used it."
        ],
        gift_item=None,
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc16",
        248,
        88,
        image_path="RandomNPCs/Female/Female6.png",
        lines=[
            "Travelers do not stay long.",
            "They complain about voices beneath the floor.",
            "The rooms are cheaper because of it."
        ],
        gift_item=None,
        can_move=True,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc17",
        408,
        408,
        image_path="RandomNPCs/Male/Male11.png",
        lines=[
            "The guardian protects us from the plague.",
            "That is what the captain says.",
            "The plague ended hundreds of years ago, but orders are orders.",
            "My friend,",
            "This potato is for you",
            "For everyone that helped us."
        ],
        gift_item=make_potato(),
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc18",
        56,
        88,
        image_path="RandomNPCs/Female/Female7.png",
        lines=[
            "I dream about a locked gate.",
            "It locates in the deepest of the maze.",
            "The dream tells me to find a silver key."
        ],
        gift_item=None,
        can_move=True,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc19",
        856,
        472,
        image_path="RandomNPCs/Female/Female8.png",
        lines=[
            "We do not bury people here.",
            "The ground is too hard.",
            "We carve names into the ice instead.",
            "Take this liquor",
            "It keeps you warm."
        ],
        gift_item=make_moonshine(),
        can_move=True,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc20",
        472,
        120,
        image_path="RandomNPCs/Female/Female9.png",
        lines=[
            "The general saved the north.",
            "That sentence appears in every medical record from the old plague.",
            "None of them say who he saved it from."
            "Take this potion",
            "Leave it until the moment that you'll die."
        ],
        gift_item=make_potion(),
        can_move=True,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc21",
        632,
        248,
        image_path="RandomNPCs/Male/Male12.png",
        lines=[
            "There are fish frozen beneath the lake.",
            "Sometimes their eyes move.",
            "I no longer fish there.",
            "This fish is fresh",
            "Bring it with you"
        ],
        gift_item=make_fish(),
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc22",
        1088,
        408,
        image_path="RandomNPCs/Female/Female10.png",
        lines=[
            "I hear people whispering under the snow.",
            "They keep saying their names.",
            "I tried to remember them all, but there were too many."
        ],
        gift_item=None,
        can_move=True,
        gender="female"
    ))

    return npcs

def desertvillage_npcs():
    npcs = []

    npcs.append(RandomNPC(
        "npc23",
        478,
        670,
        36,
        image_path="RandomNPCs/Male/Male13.png",
        lines=[
            "The desert keeps everything.",
            "Bones, weapons, cities.",
            "Mostly because returning them would require effort."
        ],
        gift_item=None,
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc24",
        30,
        382,
        36,
        image_path="RandomNPCs/Male/Male14.png",
        lines=[
            "Do not follow footprints after sunset.",
            "Some of them belong to soldiers who died centuries ago.",
            "They still know where they are going."
        ],
        gift_item=None,
        can_move=False,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc25",
        766,
        382,
        36,
        image_path="RandomNPCs/Female/Female11.png",
        lines=[
            "I collect equipment from the ruins.",
            "Every piece carries the same symbol.",
            "No history book recognizes it.",
            "The beast inside is afraid of consecutive attack",
            "I found this on a dead body last time in the Maze",
            "Good Luck."
        ],
        gift_item=make_bayonet(),
        can_move=True,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc26",
        958,
        478,
        36,
        image_path="RandomNPCs/Male/Male15.png",
        lines=[
            "I remember fighting in the south.",
            "I also remember being born two hundred years later.",
            "One of those memories must belong to someone else.",
            "Take this watermelon",
            "It shall keep you cool."
        ],
        gift_item=make_watermelon(),
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc27",
        894,
        30,
        36,
        image_path="RandomNPCs/Male/Male16.png",
        lines=[
            "When the skeleton mages draw a red circle, move.",
            "It is not fire.",
            "The world simply stops remembering whatever stands inside it."
        ],
        gift_item=None,
        can_move=False,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc28",
        542,
        382,
        36,
        image_path="RandomNPCs/Male/Male17.png",
        lines=[
            "There was once a city beneath these dunes.",
            "The king's army erased it.",
            "Then the king erased the army."
        ],
        gift_item=None,
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc29",
        542,
        478,
        36,
        image_path="RandomNPCs/Female/Female12.png",
        lines=[
            "The bone beast is made from many soldiers.",
            "Their bodies formed the shell.",
            "Their fear formed everything else."
        ],
        gift_item=None,
        can_move=True,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc30",
        318,
        414,
        36,
        image_path="RandomNPCs/Male/Male18.png",
        lines=[
            "I do not discuss the old war.",
            "I was not there.",
            "I saw nothing.",
            "Take these potato",
            "Use them wisely."
        ],
        gift_item=make_potato(),
        can_move=True,
        gender="male"
    ))

    npcs.append(RandomNPC(
        "npc31",
        638,
        688,
        36,
        image_path="RandomNPCs/Female/Female13.png",
        lines=[
            "The three spirits have simple names.",
            "Obedience. Fear. Silence.",
            "Most wars require all three."
        ],
        gift_item=None,
        can_move=False,
        gender="female"
    ))

    npcs.append(RandomNPC(
        "npc32",
        414,
        574,
        36,
        image_path="RandomNPCs/Female/Female14.png",
        lines=[
            "The first king erased the past to prevent another war.",
            "It worked.",
            "For a while."
        ],
        gift_item=None,
        can_move=True,
        gender="female"
    ))

    return npcs

def preroom_npcs():
    npcs = []
    npcs.append(RandomNPC(
        "npc33",
        1080,
        536,
        image_path="RandomNPCs/Male/Male7.png",
        lines=[
            "Good to see you again my friend",
            "The entry leads you to the beast",
            "It does ranged attacks so be aware",
            "The bones he throw are quiet fragile",
            "Here are some supplies",
            "Good Luck."
        ],
        gift_item=make_potato(),
        can_move=False,
        gender="male"
    ))

    return npcs

def preroom1_npcs():
    npcs = []
    npcs.append(RandomNPC(
        "npc34",
        1112,
        280,
        image_path="RandomNPCs/Male/Male7.png",
        lines=[
            "Come'on son",
            "Kill that evil creature",
            "And people shall regain their memory",
            "Take this Bow",
            "Good Luck."
        ],
        gift_item=make_bow_3(),
        can_move=False,
        gender="male"
    ))

    return npcs


def menu(player, game_data):
    pygame.mixer.music.stop()
    pygame.mixer.stop()

    pygame.mixer.music.load("Musics/Menu.mp3")
    pygame.mixer.music.play(loops=-1)
    Dragon = pygame.mixer.Sound("SoundEffects/DragonDeep.mp3")
    Dragon.set_volume(0.1)
    Dragon.play()
    ScaryCave = pygame.mixer.Sound("SoundEffects/ScaryCave.mp3")
    ScaryCave.set_volume(0.1)
    ScaryCave.play(loops=-1)
    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)
    sound = pygame.mixer.Sound("Musics/Hover.mp3")
    sound.set_volume(0.2)

    start_button = Button("Graphics/image.png", "Graphics/Hovered_Start.png", (253, 430))
    quit_button = Button("Graphics/image2.png", "Graphics/Hovered_Quit.png", (250, 580))

    regular_buttons = pygame.sprite.Group()
    regular_buttons.add(start_button)
    regular_buttons.add(quit_button)

    Background = pygame.image.load("Graphics/Menu.jpeg").convert()
    Background = pygame.transform.scale(Background, (1280, 768))

    clock = pygame.time.Clock()
    Game_active = True

    while Game_active:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(mouse_pos):
                    click.play()

                    save_data = load_game()

                    if save_data is not None:
                        return apply_save_data(player, game_data, save_data)

                    player.set_position(250, 330)
                    player.health = player.max_health
                    player.hp = player.health
                    player.weapon = None

                    game_data["loaded_position"] = False
                    game_data["looted_chests"] = set()
                    game_data["first_boss_dead"] = False
                    game_data["second_boss_dead"] = False

                    return "first_scene"

                if quit_button.is_clicked(mouse_pos):
                    return "quit"

            if event.type == pygame.MOUSEMOTION:
                for x in regular_buttons.sprites():
                    if x.rect.collidepoint(mouse_pos):
                        x.image = x.Image_list[1]

                        if not x.hovered:
                            sound.play()
                            x.hovered = True
                    else:
                        x.image = x.Image_list[0]
                        x.hovered = False


        Screen1.blit(Background, (0, 0))

        regular_buttons.draw(Screen1)

        pygame.display.update()
        clock.tick(60)

def first_scene(player, game_data):
    player.can_attack = True

    if not game_data["loaded_position"]:
        player.set_position(250, 330)
    elif game_data["Scene_Back"]:
        player.set_position(1178, 50)
        game_data["Scene_Back"] = False
    else:
        game_data["loaded_position"] = False

    pygame.mixer.music.stop()
    pygame.mixer.stop()

    last_melee_time = 0

    enemies = [
        Enemy(1000, 200),
        Enemy(950, 300),
        Enemy(1100, 250)
    ]

    chest = Chest(
        816,
        384,
        "cave_chest"
    )

    chest.set_loot(make_sword())

    chest.load_state(game_data)

    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group()
    regular_buttons.add(MenuButton)

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_hit = pygame.mixer.Sound("SoundEffects/Melee_slash.mp3")
    melee_hit.set_volume(0.1)

    melee_sounds = []

    for i in range(1, 4):
        s = pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        s.set_volume(0.1)
        melee_sounds.append(s)

    ChangeScene = pygame.mixer.Sound("SoundEffects/ChangeScene.mp3")

    CaveWater = pygame.mixer.Sound("SoundEffects/CaveWater.mp3")
    CaveWater.set_volume(0.4)
    CaveWater.play()

    pygame.mixer.music.load("Musics/Cave.mp3")
    pygame.mixer.music.play(-1, fade_ms=2000)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    tiled_map = pytmx.load_pygame(
        "Maps/first scene.tmx",
        pixelalpha=True
    )

    b1 = pygame.Surface((1280, 768)).convert_alpha()

    def draw_map(surf):

        for layer in tiled_map.visible_layers:

            if isinstance(layer, pytmx.TiledTileLayer):

                for x, y, gid in layer:

                    img = tiled_map.get_tile_image_by_gid(gid)

                    if img:
                        surf.blit(
                            img,
                            (
                                x * tiled_map.tilewidth,
                                y * tiled_map.tileheight
                            )
                        )

        return surf

    SF = draw_map(b1)

    walls = []

    ice_rects = []

    for obj in tiled_map.get_layer_by_name("collision"):

        walls.append(
            pygame.Rect(
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
        )

    walls.append(chest.hitbox)

    scene_change_rect = pygame.Rect(1210, 40, 60, 60)

    save_point = SavePoint("cave_save")

    walls.append(save_point.get_rect())

    save_message_timer = 0
    save_message_text = ""

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fade_alpha = 0
    fading = False
    fade_start = 0

    Game_active = True

    while Game_active:

        near_save_point = save_point.is_near(player)

        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        chest_open = chest.state == "opened"

        freeze_world = ui_open or chest_open or fading

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if MenuButton.is_clicked(mouse_pos):

                    click.play()

                    return "menu"

            if event.type == pygame.MOUSEMOTION:

                for x in regular_buttons.sprites():

                    if x.rect.collidepoint(mouse_pos):

                        x.image = x.Image_list[1]

                        if not x.hovered:
                            click.play()
                            x.hovered = True

                    else:
                        x.image = x.Image_list[0]
                        x.hovered = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if event.key == pygame.K_p:

                    if near_save_point:

                        save_game(
                            player,
                            "first_scene",
                            game_data,
                            save_point.save_point_id
                        )

                        save_message_timer = 120
                        save_message_text = "Progress saved."

                if event.key == pygame.K_r:

                    if near_save_point:
                        return reset_save_data(player, game_data)

                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if event.key == pygame.K_f:

                    if chest.state == "opened":
                        chest.close_ui()

                if inventory_ui.open:

                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)

                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)

                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)

                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:

                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        if not freeze_world:

            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )

            for enemy in enemies:
                enemy.move(player, walls)

        chest.update(player)

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False



        if not freeze_world:

            for arrow in arrows[:]:

                if not arrow.update() or arrow.off_screen(1280, 768):

                    arrows.remove(arrow)

                    continue

                for enemy in enemies:

                    if enemy.alive and arrow.hit_enemy(enemy.get_rect()):

                        damage = 1
                        if player.bow:
                            damage = player.bow.damage

                        enemy.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break

            for weapon in melee_weapons[:]:

                if not weapon.update():

                    melee_weapons.remove(weapon)

                    continue

                for enemy in enemies:

                    if enemy.alive and weapon.hit_enemy(enemy):

                        damage = 1

                        if player.weapon:
                            damage = player.weapon.attack

                        enemy.hit(damage)

                        melee_hit.play()

            for enemy in enemies:

                if enemy.alive and enemy.get_rect().colliderect(
                    player.get_hurt_rect()
                ):
                    player.take_hit(1)

            if player.health <= 0:
                player.dead = True

            if player.dead:

                white = pygame.Surface(Screen.get_size())
                white.fill((255, 255, 255))

                old_screen = Screen.copy()

                for alpha in range(0, 255, 8):

                    Screen.blit(old_screen, (0, 0))

                    white.set_alpha(alpha)

                    Screen.blit(white, (0, 0))

                    pygame.display.update()

                    clock.tick(60)

                pygame.mixer.music.stop()
                pygame.mixer.stop()

                return respawn_from_save(player, game_data)

        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        chest.draw(Screen)

        player.draw(Screen)

        regular_buttons.draw(Screen)

        for enemy in enemies:
            enemy.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if player.get_rect().colliderect(scene_change_rect) and not fading:

            fading = True

            fade_start = now

            ChangeScene.play()

            pygame.mixer.music.fadeout(1000)

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        font = pygame.font.Font(None, 32)

        text = font.render("H = Toggle Help", True, (255, 255, 0))

        x = 1080
        y = 768 - text.get_height() - 20

        bg_rect = pygame.Rect(x - 10, y - 5, text.get_width() + 20, text.get_height() + 10)

        pygame.draw.rect(Screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(Screen, (255, 255, 0), bg_rect, 2)

        Screen.blit(text, (x, y))

        if fading:

            elapsed = now - fade_start

            fade_alpha = min(
                255,
                int(elapsed / 2000 * 255)
            )

            fade_surface.set_alpha(fade_alpha)

            Screen.blit(fade_surface, (0, 0))

            if elapsed >= 2000:

                CaveWater.stop()

                return "second_scene"

        if save_message_timer > 0:

            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        game_data["help_ui"].draw(Screen)



        pygame.display.update()

        clock.tick(60)

def second_scene(player, game_data):
    player.can_attack = False

    if game_data.get("Scene_Back"):
        player.set_position(570, -80)
        game_data["Scene_Back"] = False
    else:
        player.set_position(570, 652)

    pygame.mixer.music.stop()
    pygame.mixer.stop()

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    pygame.mixer.music.load("Musics/Main World.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, fade_ms=2000)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    dialogue = DialogueSystem()

    animals = [
        Animal(100, 10, "Cow", "cow", size=(72,72)),
        Animal(900, 20, "Sheep", "sheep"),
        Animal(300, 30, "Cow", "cow", size=(72,72)),
        Animal(1100, 15, "Sheep", "sheep"),
        Animal(250, 5, "Cow", "cow", size=(72,72)),
        Animal(1000, 20, "Sheep", "sheep"),
        Animal(50, 10, "Cow", "cow", size=(72,72)),
        Animal(1150, 15, "Sheep", "sheep"),
    ]

    tiled_map = pytmx.load_pygame("Maps/untitled.tmx", pixelalpha=True)

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_image_layers(n):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        n.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return n

    SF = draw_image_layers(b1)

    npc = NPC(720, 450)

    npc_gift_given = game_data.get("npc_gift_given", False)
    npc_gift = game_data.get("npc_gift", False)

    save_point = SavePoint("village_save")

    walls = [
        npc.get_rect(),
        save_point.get_rect()
    ]

    ice_rects = []

    Change_Scene = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fading = False
    fade_start = 0

    scene_change_rect = pygame.Rect(0, -10, 1280, 10)

    Game_active = True

    while Game_active:

        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        dialogue_active = dialogue.active
        freeze_world = ui_open or fading or dialogue_active

        near_save_point = save_point.is_near(player)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            if event.type == pygame.MOUSEMOTION:

                for x in regular_buttons.sprites():

                    if x.rect.collidepoint(mouse_pos):

                        x.image = x.Image_list[1]

                        if not x.hovered:
                            click.play()
                            x.hovered = True

                    else:
                        x.image = x.Image_list[0]
                        x.hovered = False

            if event.type == pygame.KEYDOWN:

                # ================= SAVE =================
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "second_scene",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ================= INVENTORY =================
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                # F = 使用物品（你新系统）
                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ================= COMBAT =================
                # ================= DIALOGUE =================
                if event.key == pygame.K_f:
                    if dialogue.active:
                        dialogue.next_line()
                    elif player.get_rect().inflate(40, 40).colliderect(npc.get_rect()):
                        npc.sound[0].play()
                        dialogue.start([
                            "You came out of that cave…?!",
                            "That place is extremely dangerous.",
                            "You shouldn’t go back there again.",
                            "You look exhausted…",
                            "Eldermoor City is just ahead.",
                            "You can rest there for a while."
                        ])
                        npc_gift = True

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

        near_npc = player.get_rect().inflate(40, 40).colliderect(npc.get_rect())

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        # ================= RENDER =================
        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        npc.draw(Screen)

        for animal in animals:
            animal.draw(Screen, walls)

        player.draw(Screen)


        regular_buttons.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        dialogue.update()
        dialogue.draw(Screen)

        if near_npc:
            offset_y = -30 + int(3 * pygame.time.get_ticks() / 300 % 2)
            Screen.blit(f_icon, (npc.x + 8, npc.y + offset_y))

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        # ================= SCENE CHANGE =================
        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                game_data["Scene_Back"] = True
                return "first_scene"

        if player.get_rect().colliderect(scene_change_rect):
            return "eldermoor_scene"

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)
            save_message_timer -= 1

        # ================= NPC GIFT =================
        if not dialogue.active and not npc_gift_given and npc_gift:
            apple = Consumable(
                "Apple",
                "Items/Apple.png",
                "An apple that restore 2 health.",
                heal=2,
                quantity=5
            )

            game_data["inventory"].add_item(apple)

            npc_gift_given = True
            game_data["npc_gift_given"] = True

            save_message_timer = 120
            save_message_text = "Received Apple!"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)

def eldermoor_scene(player, game_data):
    player.can_attack = False

    if "npc_gifts" not in game_data:
        game_data["npc_gifts"] = set()

    if game_data.get("Scene_Back"):
        player.set_position(570, 0)
        pygame.mixer.music.load("Musics/Main World.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, fade_ms=2000)
        game_data["Scene_Back"] = False
    elif game_data["scene"] == "eldermoor_scene":
        pygame.mixer.music.load("Musics/Main World.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, fade_ms=2000)
        player.set_position(570, 450)
    else:
        player.set_position(570, 650)

    bird.play(-1)
    river.play(-1)

    npcs = eldermoor_npcs()
    dialogue = DialogueSystem()

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrows = []
    melee_weapons = []

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Eldermoor/Eldermoor City.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("eldermoor_save")

    # ================= UI =================
    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    houses = [

        SpriteObject(
            352,
            416,
            "Graphics/House.png",
            size=(192, 256)
        ),

        SpriteObject(
            736,
            416,
            "Graphics/House.png",
            size=(192, 256)
        ),

        SpriteObject(
            -32,
            64,
            "Graphics/House.png",
            size=(192, 256)
        ),

        SpriteObject(
            160,
            64,
            "Graphics/House.png",
            size=(192, 256)
        ),

        SpriteObject(
            352,
            64,
            "Graphics/House.png",
            size=(192, 256)
        ),

        SpriteObject(
            736,
            64,
            "Graphics/House.png",
            size=(192, 256)
        ),

        SpriteObject(
            928,
            64,
            "Graphics/House.png",
            size=(192, 256)
        ),

        SpriteObject(
            1120,
            64,
            "Graphics/House.png",
            size=(192, 256)
        )

    ]

    # ================= COLLISION =================
    walls = [save_point.get_rect()]

    ice_rects = []

    Change_Scene = []

    Change_Scene_1 = []

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        freeze_world = ui_open or dialogue.active

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= UI BUTTON =================
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "eldermoor_scene",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if event.key == pygame.K_f and not inventory_ui.open:
                    if dialogue.active:
                        dialogue.next_line()
                    else:
                        for npc in npcs:
                            npc.talk(
                                player,
                                dialogue,
                                inventory,
                                game_data
                            )

                # ===== COMBAT =====
        # ================= UPDATE =================
        if not freeze_world:
            npc_rects = [npc.get_rect() for npc in npcs]

            player.move(
                keys,
                walls + npc_rects,
                ice_rects
            )

            for i, npc in enumerate(npcs):

                npc_walls = walls.copy()
                npc_walls.append(player.get_rect())

                for j, other in enumerate(npcs):
                    if i != j:
                        npc_walls.append(other.get_rect())

                npc.move(npc_walls)


        for npc in npcs:
            npc.near_player = npc.is_near(player)

        dialogue.update()


        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        # ================= RENDER =================
        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        for npc in npcs:
            npc.draw(Screen)

        player.draw(Screen)

        for i in houses:
            i.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        dialogue.draw(Screen)

        for npc in npcs:
            if npc.near_player and not dialogue.active:
                offset_y = -30 + int(
                    3 * pygame.time.get_ticks() / 300 % 2
                )

                Screen.blit(
                    f_icon,
                    (npc.x + 8, npc.y + offset_y)
                )

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        regular_buttons.draw(Screen)

        if save_message_timer > 0:

            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                return "IroHouse"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                game_data["Scene_Back"] = True
                pygame.mixer.stop()
                return "second_scene"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def IroHouse(player, game_data):
    player.can_attack = False

    if "npc_gifts" not in game_data:
        game_data["npc_gifts"] = set()

    if game_data.get("House_Out"):
        player.set_position(1046, 220)
        game_data["House_Out"] = False
    elif game_data.get("Scene_Back"):
        player.set_position(570, 0)
        pygame.mixer.music.load("Musics/Home.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, fade_ms=2000)
        game_data["Scene_Back"] = False
    else:
        player.set_position(570, 650)
        pygame.mixer.music.load("Musics/Home.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, fade_ms=2000)

    npcs = irohouse_npcs()
    dialogue = DialogueSystem()

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrows = []
    melee_weapons = []

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Home/IroHouse.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("IroHouse_save")

    # ================= UI =================
    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    # ================= COLLISION =================
    walls = [save_point.get_rect()]

    ice_rects = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    Change_Scene = []

    Change_Scene_1 = []

    House = []

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("House"):
        House.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        freeze_world = ui_open or dialogue.active

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= UI BUTTON =================
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "IroHouse",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if event.key == pygame.K_f and not inventory_ui.open:
                    if dialogue.active:
                        dialogue.next_line()
                    else:
                        for npc in npcs:
                            npc.talk(
                                player,
                                dialogue,
                                inventory,
                                game_data
                            )

        # ================= UPDATE =================
        if not freeze_world:
            npc_rects = [npc.get_rect() for npc in npcs]

            player.move(
                keys,
                walls + npc_rects,
                ice_rects
            )

            for i, npc in enumerate(npcs):

                npc_walls = walls.copy()
                npc_walls.append(player.get_rect())

                for j, other in enumerate(npcs):
                    if i != j:
                        npc_walls.append(other.get_rect())

                npc.move(npc_walls)

        for npc in npcs:
            npc.near_player = npc.is_near(player)

        dialogue.update()

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        # ================= RENDER =================
        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        for npc in npcs:
            npc.draw(Screen)

        player.draw(Screen)


        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        dialogue.draw(Screen)

        for npc in npcs:
            if npc.near_player and not dialogue.active:
                offset_y = -30 + int(
                    3 * pygame.time.get_ticks() / 300 % 2
                )

                Screen.blit(
                    f_icon,
                    (npc.x + 8, npc.y + offset_y)
                )

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        regular_buttons.draw(Screen)

        if save_message_timer > 0:

            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                print("Going to IroHome")
                return "IroHome"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                game_data["Scene_Back"] = True
                return "eldermoor_scene"

        for rect in House:
            if player.get_rect().colliderect(rect):
                return "InHouse"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        game_data["help_ui"].draw(Screen)


        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def InHouse(player, game_data):
    player.can_attack = False
    player.set_position(715, 420)

    open_sound = pygame.mixer.Sound(
        "SoundEffects/OpenChest.mp3"
    )

    close_sound = pygame.mixer.Sound(
        "SoundEffects/CloseChest.mp3"
    )

    transfer_sound = pygame.mixer.Sound(
        "SoundEffects/Equip.mp3"
    )

    open_sound.set_volume(0.3)
    close_sound.set_volume(0.3)
    transfer_sound.set_volume(0.3)

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    opened_this_frame = False

    storage = StorageChest(
        544,
        288,
        "chest_1",
        game_data
    )

    storage_ui = StorageChestUI(
        inventory,
        storage.inventory
    )

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Home/InHouse.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= UI =================
    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    # ================= COLLISION =================
    walls = []

    ice_rects = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    Change_Scene = []

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )
    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        freeze_world = ui_open

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                storage.save()
                pygame.quit()
                exit()

            # ================= UI BUTTON =================
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if (
                        event.key == pygame.K_f
                        and storage.can_interact(player)
                        and not inventory_ui.open
                        and not storage_ui.open
                ):

                    open_sound.play()

                    storage_ui.open = True
                    storage.ui_open = True

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if (
                        storage_ui.open
                        and not opened_this_frame
                ):

                    if event.key == pygame.K_TAB:
                        storage_ui.switch_focus()

                    if event.key == pygame.K_LEFT:
                        storage_ui.move_cursor(-1, 0)

                    if event.key == pygame.K_RIGHT:
                        storage_ui.move_cursor(1, 0)

                    if event.key == pygame.K_UP:
                        storage_ui.move_cursor(0, -1)

                    if event.key == pygame.K_DOWN:
                        storage_ui.move_cursor(0, 1)

                    if event.key == pygame.K_ESCAPE:
                        close_sound.play()
                        storage_ui.open = False
                        storage.ui_open = False
                        storage.save()

                    if event.key == pygame.K_t:

                        mods = pygame.key.get_mods()

                        if mods & pygame.KMOD_SHIFT:
                            storage_ui.transfer_stack()
                            storage.save()
                            transfer_sound.play()
                        else:
                            storage_ui.transfer_one()
                            storage.save()
                            transfer_sound.play()

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

        # ================= RENDER =================
        Screen.blit(SF, (0, 0))

        player.draw(Screen)

        storage.draw_prompt(
            Screen,
            player
        )

        if storage.ui_open:
            storage_ui.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        regular_buttons.draw(Screen)

        if save_message_timer > 0:

            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                game_data["House_Out"] = True
                return "IroHouse"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def IroHome(player, game_data):
    player.can_attack = False

    if "npc_gifts" not in game_data:
        game_data["npc_gifts"] = set()

    if game_data["Scene_Back"]:
        player.set_position(-40, 300)
        game_data["Scene_Back"] = False
    elif game_data["Scene_Back_1"]:
        player.set_position(570, -40)
        game_data["Scene_Back_1"] = False
    elif game_data["Scene_Back_2"]:
        player.set_position(1200, 300)
        game_data["Scene_Back_2"] = False
    else:
        player.set_position(570, 653)

    pygame.mixer.music.stop()
    pygame.mixer.stop()

    npcs = irohome_npcs()
    dialogue = DialogueSystem()

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    pygame.mixer.music.load("Musics/Main World.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, fade_ms=2000)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Home/IroHome.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("IroHome_save")

    # ================= UI =================
    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    # ================= COLLISION =================
    walls = [save_point.get_rect()]

    ice_rects = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    Change_Scene = []

    Change_Scene_1 = []

    Change_Scene_2 = []

    Change_Scene_3 = []

    collision2 = []

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene_2"):
        Change_Scene_2.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene_3"):
        Change_Scene_3.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("collision2"):
        if not game_data["Boss1"] or not game_data["Boss2"]:
            walls.append(
                pygame.Rect(
                    obj.x * SCALE,
                    obj.y * SCALE,
                    obj.width * SCALE,
                    obj.height * SCALE
                )
            )

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        freeze_world = ui_open or dialogue.active

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= UI BUTTON =================
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "IroHouse",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if event.key == pygame.K_f and not inventory_ui.open:
                    if dialogue.active:
                        dialogue.next_line()
                    else:
                        for npc in npcs:
                            npc.talk(
                                player,
                                dialogue,
                                inventory,
                                game_data
                            )

        # ================= UPDATE =================
        if not freeze_world:
            npc_rects = [npc.get_rect() for npc in npcs]

            player.move(
                keys,
                walls + npc_rects,
                ice_rects
            )

            for i, npc in enumerate(npcs):

                npc_walls = walls.copy()
                npc_walls.append(player.get_rect())

                for j, other in enumerate(npcs):
                    if i != j:
                        npc_walls.append(other.get_rect())

                npc.move(npc_walls)

        for npc in npcs:
            npc.near_player = npc.is_near(player)

        dialogue.update()

        # ================= RENDER =================
        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        for npc in npcs:
            npc.draw(Screen)

        player.draw(Screen)

        dialogue.draw(Screen)

        for npc in npcs:
            if npc.near_player and not dialogue.active:
                offset_y = -30 + int(
                    3 * pygame.time.get_ticks() / 300 % 2
                )

                Screen.blit(
                    f_icon,
                    (npc.x + 8, npc.y + offset_y)
                )

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        regular_buttons.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                game_data["Scene_Back"] = True
                return "IroHouse"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                return "SnowVillage"

        for rect in Change_Scene_2:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                return "DesertVillage"

        for rect in Change_Scene_3:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                return "Entry"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def SnowVillage(player, game_data):
    # ================= INIT =================
    player.can_attack = False

    if "npc_gifts" not in game_data:
        game_data["npc_gifts"] = set()

    if game_data.get("Scene_Back"):
        player.set_position(-50, 350)
        game_data["Scene_Back"] = False
    else:
        player.set_position(1200, 220)
        if not game_data["Boss1"]:
            pygame.mixer.music.load("Musics/SnowyDark.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
        else:
            pygame.mixer.music.load("Musics/Snowy.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)

    npcs = snowvillage_npcs()
    dialogue = DialogueSystem()

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/First Boss/SnowVillage.tmx",
        pixelalpha=True
    )

    SCALE = 1

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("SnowVillage_save")

    # ================= UI =================
    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    # ================= COLLISION =================
    walls = [save_point.get_rect()]

    ice_rects = []

    Change_Scene = []

    Change_Scene_1 = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Ice"):
        ice_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        freeze_world = ui_open or dialogue.active

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= UI BUTTON =================
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "SnowVillage",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if event.key == pygame.K_f and not inventory_ui.open:
                    if dialogue.active:
                        dialogue.next_line()
                    else:
                        for npc in npcs:
                            npc.talk(
                                player,
                                dialogue,
                                inventory,
                                game_data
                            )

        # ================= UPDATE =================
        if not freeze_world:
            npc_rects = [npc.get_rect() for npc in npcs]

            player.move(
                keys,
                walls + npc_rects,
                ice_rects
            )

            for i, npc in enumerate(npcs):

                npc_walls = walls.copy()
                npc_walls.append(player.get_rect())

                for j, other in enumerate(npcs):
                    if i != j:
                        npc_walls.append(other.get_rect())

                npc.move(npc_walls)

        for npc in npcs:
            npc.near_player = npc.is_near(player)

        dialogue.update()

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        for npc in npcs:
            npc.draw(Screen)

        player.draw(Screen)


        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        dialogue.draw(Screen)

        for npc in npcs:
            if npc.near_player and not dialogue.active:
                offset_y = -30 + int(
                    3 * pygame.time.get_ticks() / 300 % 2
                )

                Screen.blit(
                    f_icon,
                    (npc.x + 8, npc.y + offset_y)
                )

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        regular_buttons.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                if game_data["MazeSolved"]:
                    return "Maze_Solved"
                else:
                    return "Maze"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                game_data["Scene_Back"] = True
                return "IroHome"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Maze(player, game_data):
    # ================= INIT =================
    player.can_attack = True

    if game_data["scene"] == "Maze":
        player.set_position(90, 440)
        if not game_data["Boss1"]:
            pygame.mixer.music.load("Musics/SnowyDark.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
        else:
            pygame.mixer.music.load("Musics/Snowy.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
    else:
        player.set_position(1200, 350)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    metal = pygame.mixer.Sound("SoundEffects/Metal.mp3")
    metal.set_volume(0.2)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    skeletons = []

    skeletons.append(SkeletonSoldier(544, 192))
    skeletons.append(SkeletonSoldier(832, 192))
    skeletons.append(SkeletonSoldier(544, 416))
    skeletons.append(SkeletonSoldier(832, 416))
    skeletons.append(SkeletonSoldier(544, 640))
    skeletons.append(SkeletonSoldier(832, 640))

    chest = Chest(
        1008,
        176,
        "maze_chest"
    )

    chest.set_loot(make_key())

    chest.load_state(game_data)

    chest1 = Chest(
        1168,
        656,
        "maze_chest_1"
    )

    chest1.set_loot(make_axe())

    chest1.load_state(game_data)

    chest2 = Chest(
        400,
        656,
        "maze_chest_2"
    )

    chest2.set_loot(make_head_1())

    chest2.load_state(game_data)

    chest3 = Chest(
        144,
        96,
        "maze_chest_3"
    )

    chest3.set_loot(make_hands_1())

    chest3.load_state(game_data)

    chest4 = Chest(
        1232,
        16,
        "maze_chest_4"
    )

    chest4.set_loot(make_legs_1())

    chest4.load_state(game_data)

    hint = HintAnimation(
        x=1002,
        y=130
    )

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/First Boss/Maze.tmx",
        pixelalpha=True
    )

    SCALE = 1

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("Maze_save")

    # ================= COLLISION =================
    walls = [save_point.get_rect()]

    walls.append(chest.hitbox)
    walls.append(chest1.hitbox)
    walls.append(chest2.hitbox)
    walls.append(chest3.hitbox)
    walls.append(chest4.hitbox)

    ice_rects = []

    Change_Scene = []

    save_message_timer = 0
    save_message_text = ""

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fade_alpha = 0
    fading = False
    fade_start = 0

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Ice"):
        ice_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        chest_open = (
                chest.state == "opened"
                or
                chest1.state == "opened"
                or
                chest2.state == "opened"
                or
                chest3.state == "opened"
                or
                chest4.state == "opened"
        )

        freeze_world = ui_open or chest_open or fading

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if event.key == pygame.K_f:

                    if chest.state == "opened":
                        chest.close_ui()

                        fading = True
                        fade_start = now

                        game_data["MazeSolved"] = True

                        pygame.mixer.music.fadeout(2000)

                    if chest1.state == "opened":
                        chest1.close_ui()
                    if chest2.state == "opened":
                        chest2.close_ui()
                    if chest3.state == "opened":
                        chest3.close_ui()
                    if chest4.state == "opened":
                        chest4.close_ui()

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "Maze",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )
            chest.update(player)
            chest1.update(player)
            chest2.update(player)
            chest3.update(player)
            chest4.update(player)

            for sk in skeletons:
                sk.move(player, walls)

                for weapon in melee_weapons:

                    for skeleton in skeletons:
                        for arrow in skeleton.arrows[:]:

                            if weapon.attack_rect.colliderect(arrow.get_rect()):
                                metal.play()
                                arrow.active = False
                                skeleton.arrows.remove(arrow)

                    if weapon.hit_enemy(sk) and sk.alive:

                        damage = 0

                        if player.weapon:
                            damage = player.weapon.attack

                        sk.hit(damage)

                for arrow in arrows[:]:

                    if sk.alive and arrow.hit_enemy(sk.get_hurt_rect()):

                        damage = 0

                        if player.bow:
                            damage = player.bow.damage

                        sk.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        if chest1.give_loot:

            if chest1.loot_item:
                inventory.add_item(chest1.loot_item)

            game_data["looted_chests"].add(
                chest1.chest_id
            )

            chest1.give_loot = False

        if chest2.give_loot:

            if chest2.loot_item:
                inventory.add_item(chest2.loot_item)

            game_data["looted_chests"].add(
                chest2.chest_id
            )

            chest2.give_loot = False

        if chest3.give_loot:

            if chest3.loot_item:
                inventory.add_item(chest3.loot_item)

            game_data["looted_chests"].add(
                chest3.chest_id
            )

            chest3.give_loot = False

        if chest4.give_loot:

            if chest4.loot_item:
                inventory.add_item(chest4.loot_item)

            game_data["looted_chests"].add(
                chest4.chest_id
            )

            chest4.give_loot = False

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        hint.update()
        hint.draw(Screen)

        chest.draw(Screen)
        chest1.draw(Screen)
        chest2.draw(Screen)
        chest3.draw(Screen)
        chest4.draw(Screen)

        for sk in skeletons:
            sk.draw(Screen)

        player.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if chest1.state == "opened":
            chest1.draw_loot_ui(Screen)

        if chest2.state == "opened":
            chest2.draw_loot_ui(Screen)

        if chest3.state == "opened":
            chest3.draw_loot_ui(Screen)

        if chest4.state == "opened":
            chest4.draw_loot_ui(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                game_data["Scene_Back"] = True
                return "SnowVillage"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if fading:

            elapsed = now - fade_start

            fade_alpha = min(
                255,
                int(elapsed / 2000 * 255)
            )

            fade_surface.set_alpha(fade_alpha)

            Screen.blit(fade_surface, (0, 0))

            if elapsed >= 2000:
                pygame.mixer.music.stop()
                game_data["Maze_Solved"] = True
                game_data["Scene_Back_1"] = True
                return "Maze_Solved"

        if player.health <= 0:
            player.dead = True

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Maze_Solved(player, game_data):
    # ================= INIT =================
    player.can_attack = True

    if game_data["Scene_Back"]:
        player.set_position(-40, 350)
        if not game_data["Boss1"]:
            pygame.mixer.music.load("Musics/SnowyDark.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
        else:
            pygame.mixer.music.load("Musics/Snowy.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
        game_data["Scene_Back"] = False

    elif game_data["Scene_Back_1"]:
        player.set_position(90, 440)
        if not game_data["Boss1"]:
            pygame.mixer.music.load("Musics/SnowyDark.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
        else:
            pygame.mixer.music.load("Musics/Snowy.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
        game_data["Scene_Back_1"] = False

    elif game_data["scene"] == "Maze_Solved":
        player.set_position(90, 440)
        if not game_data["Boss1"]:
            pygame.mixer.music.load("Musics/SnowyDark.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
        else:
            pygame.mixer.music.load("Musics/Snowy.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1, fade_ms=2000)
        game_data["Scene_Back_1"] = False
    else:
        player.set_position(1200, 350)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    metal = pygame.mixer.Sound("SoundEffects/Metal.mp3")
    metal.set_volume(0.2)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    skeletons = []

    skeletons.append(SkeletonSoldier(544, 192))
    skeletons.append(SkeletonSoldier(832, 192))
    skeletons.append(SkeletonSoldier(544, 416))
    skeletons.append(SkeletonSoldier(832, 416))
    skeletons.append(SkeletonSoldier(544, 640))
    skeletons.append(SkeletonSoldier(832, 640))

    chest = Chest(
        1008,
        176,
        "maze_chest"
    )

    chest.set_loot(make_key())

    chest.load_state(game_data)

    chest1 = Chest(
        1168,
        656,
        "maze_chest_1"
    )

    chest1.set_loot(make_axe())

    chest1.load_state(game_data)

    chest2 = Chest(
        400,
        656,
        "maze_chest_2"
    )

    chest2.set_loot(make_head_1())

    chest2.load_state(game_data)

    chest3 = Chest(
        144,
        96,
        "maze_chest_3"
    )

    chest3.set_loot(make_chest_1())

    chest3.load_state(game_data)

    chest4 = Chest(
        1232,
        16,
        "maze_chest_4"
    )

    chest4.set_loot(make_legs_1())

    chest4.load_state(game_data)

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/First Boss/Maze_Soved.tmx",
        pixelalpha=True
    )

    SCALE = 1

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("MazeSolved_save")

    # ================= COLLISION =================
    walls = [save_point.get_rect()]

    walls.append(chest.hitbox)
    walls.append(chest1.hitbox)
    walls.append(chest2.hitbox)
    walls.append(chest3.hitbox)
    walls.append(chest4.hitbox)


    ice_rects = []

    Change_Scene = []

    Change_Scene_1 = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Ice"):
        ice_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        chest_open = (
                chest.state == "opened"
                or
                chest1.state == "opened"
                or
                chest2.state == "opened"
                or
                chest3.state == "opened"
                or
                chest4.state == "opened"
        )

        freeze_world = ui_open or chest_open

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if event.key == pygame.K_f:

                    if chest.state == "opened":
                        chest.close_ui()
                    if chest1.state == "opened":
                        chest1.close_ui()
                    if chest2.state == "opened":
                        chest2.close_ui()
                    if chest3.state == "opened":
                        chest3.close_ui()
                    if chest4.state == "opened":
                        chest4.close_ui()

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "Maze_Solved",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )
            chest.update(player)
            chest1.update(player)
            chest2.update(player)
            chest3.update(player)
            chest4.update(player)

            for sk in skeletons:
                sk.move(player, walls)

                for weapon in melee_weapons:

                    for skeleton in skeletons:
                        for arrow in skeleton.arrows[:]:

                            if weapon.attack_rect.colliderect(arrow.get_rect()):
                                metal.play()
                                arrow.active = False
                                skeleton.arrows.remove(arrow)

                    if weapon.hit_enemy(sk) and sk.alive:

                        damage = 0

                        if player.weapon:
                            damage = player.weapon.attack

                        sk.hit(damage)

                for arrow in arrows[:]:

                    if sk.alive and arrow.hit_enemy(sk.get_hurt_rect()):

                        damage = 0

                        if player.bow:
                            damage = player.bow.damage

                        sk.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break



        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        if chest1.give_loot:

            if chest1.loot_item:
                inventory.add_item(chest1.loot_item)

            game_data["looted_chests"].add(
                chest1.chest_id
            )

            chest1.give_loot = False

        if chest2.give_loot:

            if chest2.loot_item:
                inventory.add_item(chest2.loot_item)

            game_data["looted_chests"].add(
                chest2.chest_id
            )

            chest2.give_loot = False

        if chest3.give_loot:

            if chest3.loot_item:
                inventory.add_item(chest3.loot_item)

            game_data["looted_chests"].add(
                chest3.chest_id
            )

            chest3.give_loot = False

        if chest4.give_loot:

            if chest4.loot_item:
                inventory.add_item(chest4.loot_item)

            game_data["looted_chests"].add(
                chest4.chest_id
            )

            chest4.give_loot = False


        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        for sk in skeletons:
            sk.draw(Screen)

        player.draw(Screen)

        chest.draw(Screen)
        chest1.draw(Screen)
        chest2.draw(Screen)
        chest3.draw(Screen)
        chest4.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if chest1.state == "opened":
            chest1.draw_loot_ui(Screen)

        if chest2.state == "opened":
            chest2.draw_loot_ui(Screen)

        if chest3.state == "opened":
            chest3.draw_loot_ui(Screen)

        if chest4.state == "opened":
            chest4.draw_loot_ui(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.stop()
                game_data["Scene_Back"] = True
                return "SnowVillage"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                if not game_data["Boss1"]:
                    pygame.mixer.music.stop()
                game_data["Scene_Back"] = True
                return "First_Boss"

        if player.health <= 0:
            player.dead = True

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def First_Boss(player, game_data):
    # ================= INIT =================
    player.can_attack = True
    player.set_position(1200, 350)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    if not game_data["Boss1"]:
        pygame.mixer.music.load("Musics/FirstBoss.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    chest = None

    if game_data["Boss1"]:
        chest = Chest(
            304,
            368,
            "boss1_chest"
        )

        chest.set_loot(make_truth_1())
        chest.load_state(game_data)


    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    boss = Boss(400, 200)

    boss_leave_warning = False

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/First Boss/Boss.tmx",
        pixelalpha=True
    )

    SCALE = 1

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    if chest:
        walls.append(chest.hitbox)

    ice_rects = []

    Change_Scene = []

    fading = False
    fade_start = 0

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Ice"):
        ice_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open

        if chest:
            chest_open = chest.state == "opened"
            freeze_world = ui_open or boss_leave_warning or chest_open
        else:
            freeze_world = ui_open or boss_leave_warning

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if boss_leave_warning:

                    if event.key == pygame.K_y:
                        pygame.mixer.music.fadeout(1000)
                        game_data["Scene_Back"] = True
                        return "Maze_Solved"

                    elif event.key == pygame.K_n:
                        boss_leave_warning = False
                        player.x -= 50

                    continue

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if chest:
                    if event.key == pygame.K_f:
                        if chest.state == "opened":
                            chest.close_ui()

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================


        for weapon in melee_weapons:

            if weapon.hit_enemy(boss) and boss.alive and not game_data["Boss1"]:

                damage = 0

                if player.weapon:
                    damage = player.weapon.attack

                boss.hit(damage)

        for arrow in arrows:

            if boss.alive and arrow.hit_enemy(boss.get_rect()) and not game_data["Boss1"]:

                damage = 0

                if player.bow:
                    damage = player.bow.damage

                boss.hit(damage)

                arrows.remove(arrow)

                arrow_hit.play()

                break


        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )

            if chest:
                chest.update(player)

            if not game_data["Boss1"]:
                boss.move(player, walls)

            if boss.alive and not game_data["Boss1"]:
                if boss.get_rect().colliderect(player.get_hurt_rect()):
                    player.take_hit(boss.damage)

        if chest:
            if chest.give_loot:

                if chest.loot_item:
                    inventory.add_item(chest.loot_item)

                game_data["looted_chests"].add(
                    chest.chest_id
                )

                chest.give_loot = False

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        if chest:
            chest.draw(Screen)

        player.draw(Screen)

        if chest:
            if chest.state == "opened":
                chest.draw_loot_ui(Screen)

        if not game_data["Boss1"]:
            boss.draw(Screen)

        if boss.dead_done and not fading:
            fading = True
            fade_start = pygame.time.get_ticks()

            # 所有声音淡出
            pygame.mixer.music.fadeout(1500)

            game_data["Boss1"] = True

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:

            if player.get_rect().colliderect(rect):

                if not game_data["Boss1"]:

                    boss_leave_warning = True
                else:

                    pygame.mixer.music.fadeout(1000)
                    game_data["Scene_Back"] = True
                    return "Maze_Solved"

        if boss_leave_warning:
            panel = pygame.Rect(240, 250, 800, 200)

            pygame.draw.rect(Screen, (20, 20, 20), panel, border_radius=12)
            pygame.draw.rect(Screen, (255, 255, 255), panel, 2, border_radius=12)

            font = pygame.font.Font(None, 42)

            text1 = font.render(
                "You have not defeated the boss.",
                True,
                (255, 255, 255)
            )

            text2 = font.render(
                "Are you sure you want to leave?",
                True,
                (255, 255, 255)
            )

            text3 = font.render(
                "[Y] Yes    [N] No",
                True,
                (255, 255, 0)
            )

            Screen.blit(
                text1,
                (panel.centerx - text1.get_width() // 2, panel.y + 40)
            )

            Screen.blit(
                text2,
                (panel.centerx - text2.get_width() // 2, panel.y + 90)
            )

            Screen.blit(
                text3,
                (panel.centerx - text3.get_width() // 2, panel.y + 145)
            )

        if player.health <= 0:
            player.dead = True

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.dead:

            game_data["Scene_back"] = True

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        if fading:
            elapsed = pygame.time.get_ticks() - fade_start

            if elapsed >= 3000:
                return "First_Boss"

            alpha = min(
                255,
                int(elapsed / 3000 * 255)
            )

            fade_surface = pygame.Surface(
                (Screen.get_width(), Screen.get_height())
            )

            fade_surface.fill((255, 255, 255))

            fade_surface.set_alpha(alpha)

            Screen.blit(fade_surface, (0, 0))

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def DesertVillage(player, game_data):
    # ================= INIT =================
    player.can_attack = False

    if "npc_gifts" not in game_data:
        game_data["npc_gifts"] = set()

    if game_data.get("Scene_Back"):
        player.set_position(778, -40)
        game_data["Scene_Back"] = False
    else:
        player.set_position(-40, 362)
        pygame.mixer.music.load("Musics/DesertVillage.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1, fade_ms=2000)

    npcs = desertvillage_npcs()
    dialogue = DialogueSystem()

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Second Boss/DesertVillage.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("DesertVillage_save")

    chest = Chest(
        96,
        544,
        "desert_chest_1"
    )

    chest.set_loot(make_bow())
    chest.load_state(game_data)

    # ================= UI =================
    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    # ================= COLLISION =================
    walls = [
        save_point.get_rect(),
        chest.hitbox
    ]

    Spikes = []

    ice_rects = []

    Change_Scene = []

    Change_Scene_1 = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Spike"):
        Spikes.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        freeze_world = ui_open or dialogue.active

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= UI BUTTON =================
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if chest.state == "opened":
                        chest.close_ui()

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "DesertVillage",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if event.key == pygame.K_f and not inventory_ui.open:
                    if dialogue.active:
                        dialogue.next_line()
                    else:
                        for npc in npcs:
                            npc.talk(
                                player,
                                dialogue,
                                inventory,
                                game_data
                            )

        # ================= UPDATE =================
        if not freeze_world:
            npc_rects = [npc.get_rect() for npc in npcs]

            player.move(
                keys,
                walls + npc_rects,
                ice_rects
            )

            chest.update(player)

            for rect in Spikes:
                if player.get_rect().colliderect(rect):
                    player.take_hit(1)

            for i, npc in enumerate(npcs):

                npc_walls = walls.copy()
                npc_walls.append(player.get_rect())

                for j, other in enumerate(npcs):
                    if i != j:
                        npc_walls.append(other.get_rect())

                npc.move(npc_walls)

        for npc in npcs:
            npc.near_player = npc.is_near(player)

        dialogue.update()

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        chest.draw(Screen)

        save_point.draw(Screen, near_save_point)

        for npc in npcs:
            npc.draw(Screen)

        player.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        dialogue.draw(Screen)

        for npc in npcs:
            if npc.near_player and not dialogue.active:
                offset_y = -30 + int(
                    3 * pygame.time.get_ticks() / 300 % 2
                )

                Screen.blit(
                    f_icon,
                    (npc.x + 8, npc.y + offset_y)
                )

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        regular_buttons.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                    return "DesertMaze"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                game_data["Scene_Back_2"] = True
                return "IroHome"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)


        pygame.display.update()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.mixer.stop()

def DesertMaze(player, game_data):
    # ================= INIT =================
    player.can_attack = True

    if game_data["Scene_Back"]:
        player.set_position(970, -40)
        game_data["Scene_Back"] = False
    else:
        player.set_position(778, 660)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    Wind = pygame.mixer.Sound("SoundEffects/Wind.mp3")
    Wind.set_volume(0.3)
    Wind.play(-1)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    skeletons = []

    skeletons.append(SkeletonWizard2(1104, 314))
    skeletons.append(SkeletonWizard2(-16, 122))
    skeletons.append(SkeletonWizard2(-16 , 218))
    skeletons.append(SkeletonWizard2(-16, 378))
    skeletons.append(SkeletonWizard2(656, 698))
    skeletons.append(SkeletonWizard2(720, 602))

    chest = Chest(
        0,
        0,
        "desert_maze_chest"
    )

    chest.set_loot(make_chest_2())

    chest.load_state(game_data)

    chest1 = Chest(
        928,
        576,
        "desert_maze_chest_1"
    )

    chest1.set_loot(make_hands_2())

    chest1.load_state(game_data)

    chest2 = Chest(
        1248,
        288,
        "desert_maze_chest_2"
    )

    chest2.set_loot(make_head_2())

    chest2.load_state(game_data)

    chest3 = Chest(
        0,
        736,
        "desert_maze_chest_3"
    )

    chest3.set_loot(make_legs_2())

    chest3.load_state(game_data)

    chest4 = Chest(
        992,
        256,
        "desert_maze_chest_4"
    )

    chest4.set_loot(make_sword_1())

    chest4.load_state(game_data)

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Second Boss/DesertMaze.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    walls.append(chest.hitbox)
    walls.append(chest1.hitbox)
    walls.append(chest2.hitbox)
    walls.append(chest3.hitbox)
    walls.append(chest4.hitbox)

    ice_rects = []

    Change_Scene = []

    Change_Scene_1 = []

    save_message_timer = 0
    save_message_text = ""

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fade_alpha = 0
    fading = False
    fade_start = 0

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        chest_open = (
                chest.state == "opened"
                or
                chest1.state == "opened"
                or
                chest2.state == "opened"
                or
                chest3.state == "opened"
                or
                chest4.state == "opened"
        )

        freeze_world = ui_open or chest_open or fading

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if event.key == pygame.K_f:

                    if chest.state == "opened":
                        chest.close_ui()
                    if chest1.state == "opened":
                        chest1.close_ui()
                    if chest2.state == "opened":
                        chest2.close_ui()
                    if chest3.state == "opened":
                        chest3.close_ui()
                    if chest4.state == "opened":
                        chest4.close_ui()

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )
            chest.update(player)
            chest1.update(player)
            chest2.update(player)
            chest3.update(player)
            chest4.update(player)

            for sk in skeletons:
                sk.move(player, walls)

                for weapon in melee_weapons:

                    if weapon.hit_enemy(sk) and sk.alive:

                        damage = 0

                        if player.weapon:
                            damage = player.weapon.attack

                        sk.hit(damage)

                for arrow in arrows:

                    if sk.alive and arrow.hit_enemy(sk.get_rect()):

                        damage = 0

                        if player.bow:
                            damage = player.bow.damage

                        sk.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        if chest1.give_loot:

            if chest1.loot_item:
                inventory.add_item(chest1.loot_item)

            game_data["looted_chests"].add(
                chest1.chest_id
            )

            chest1.give_loot = False

        if chest2.give_loot:

            if chest2.loot_item:
                inventory.add_item(chest2.loot_item)

            game_data["looted_chests"].add(
                chest2.chest_id
            )

            chest2.give_loot = False

        if chest3.give_loot:

            if chest3.loot_item:
                inventory.add_item(chest3.loot_item)

            game_data["looted_chests"].add(
                chest3.chest_id
            )

            chest3.give_loot = False

        if chest4.give_loot:

            if chest4.loot_item:
                inventory.add_item(chest4.loot_item)

            game_data["looted_chests"].add(
                chest4.chest_id
            )

            chest4.give_loot = False

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        chest.draw(Screen)
        chest1.draw(Screen)
        chest2.draw(Screen)
        chest3.draw(Screen)
        chest4.draw(Screen)

        for sk in skeletons:
            sk.draw(Screen)

        player.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if chest1.state == "opened":
            chest1.draw_loot_ui(Screen)

        if chest2.state == "opened":
            chest2.draw_loot_ui(Screen)

        if chest3.state == "opened":
            chest3.draw_loot_ui(Screen)

        if chest4.state == "opened":
            chest4.draw_loot_ui(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                game_data["Scene_Back"] = True
                return "DesertVillage"

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                return "PreRoom"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.health <= 0:
            player.dead = True

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def PreRoom(player, game_data):
    # ================= INIT =================
    player.can_attack = False

    if "npc_gifts" not in game_data:
        game_data["npc_gifts"] = set()

    if game_data.get("Scene_Back"):
        player.set_position(810, -40)
        game_data["Scene_Back"] = False
        pygame.mixer.music.load("Musics/DesertVillage.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1, fade_ms=2000)
    else:
        player.set_position(970, 660)

    if game_data["scene"] == "PreRoom":
        pygame.mixer.music.load("Musics/DesertVillage.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1, fade_ms=2000)

    npcs = preroom_npcs()
    dialogue = DialogueSystem()

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Second Boss/PreRoom.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("PreRoom_save")

    # ================= UI =================
    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    # ================= COLLISION =================
    walls = [
        save_point.get_rect(),
    ]

    Spikes = []

    ice_rects = []

    Change_Scene = []

    Change_Scene_1 = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Spike"):
        Spikes.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        freeze_world = ui_open or dialogue.active

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= UI BUTTON =================
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "PreRoom",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if event.key == pygame.K_f and not inventory_ui.open:
                    if dialogue.active:
                        dialogue.next_line()
                    else:
                        for npc in npcs:
                            npc.talk(
                                player,
                                dialogue,
                                inventory,
                                game_data
                            )

        # ================= UPDATE =================
        if not freeze_world:
            npc_rects = [npc.get_rect() for npc in npcs]

            player.move(
                keys,
                walls + npc_rects,
                ice_rects
            )

            for rect in Spikes:
                if player.get_rect().colliderect(rect):
                    player.take_hit(1)

            for i, npc in enumerate(npcs):

                npc_walls = walls.copy()
                npc_walls.append(player.get_rect())

                for j, other in enumerate(npcs):
                    if i != j:
                        npc_walls.append(other.get_rect())

                npc.move(npc_walls)

        for npc in npcs:
            npc.near_player = npc.is_near(player)

        dialogue.update()

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        for npc in npcs:
            npc.draw(Screen)

        player.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        dialogue.draw(Screen)

        for npc in npcs:
            if npc.near_player and not dialogue.active:
                offset_y = -30 + int(
                    3 * pygame.time.get_ticks() / 300 % 2
                )

                Screen.blit(
                    f_icon,
                    (npc.x + 8, npc.y + offset_y)
                )

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        regular_buttons.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.stop()
                return "Second_Boss"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                game_data["Scene_Back"] = True
                return "DesertMaze"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)


        pygame.display.update()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Second_Boss(player, game_data):
    # ================= INIT =================
    player.can_attack = True
    player.set_position(810, 660)

    music_fading_down = False
    music_fade_start = 0

    music_fading_up = False
    music_fade_up_start = 0

    ending_started = False
    boss_phase1_done = False

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    bone1 = pygame.mixer.Sound("BoneBoss/Sounds/BoneCrack.mp3")
    bone1.set_volume(0.5)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    if not game_data["Boss2"]:
        pygame.mixer.music.load("Musics/SecondBoss.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)


    chest = Chest(
        32,
        480,
        "boss2_chest"
    )

    chest.set_loot(make_truth_2())
    chest.load_state(game_data)

    skeletons = []

    skeletons.append(SkeletonWizard2(300, 75))
    skeletons.append(SkeletonWizard2(900, 75))

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    boss = SecondBoss(-50, 300)

    mini_bosses = []

    mini_spawned = False

    boss_leave_warning = False

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Second Boss/Boss.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    walls.append(chest.hitbox)

    ice_rects = []

    Change_Scene = []

    Spikes = []

    fading = False
    fade_start = 0

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Spike"):
        Spikes.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open

        chest_open = chest.state == "opened"
        freeze_world = ui_open or boss_leave_warning or chest_open

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if boss_leave_warning:

                    if event.key == pygame.K_y:
                        pygame.mixer.music.fadeout(1500)
                        game_data["Scene_Back"] = True
                        return "PreRoom"

                    elif event.key == pygame.K_n:
                        boss_leave_warning = False
                        player.y -= 50

                    continue

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if event.key == pygame.K_f:
                    if chest.state == "opened":
                        chest.close_ui()

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================

        for weapon in melee_weapons[:]:

            for bone in boss.bones[:]:

                if weapon.hit_enemy(bone):
                    bone1.play()
                    boss.bones.remove(bone)
                    break

            for mini in mini_bosses:

                for bone in mini.bones[:]:

                    if weapon.hit_enemy(bone):
                        bone1.play()
                        mini.bones.remove(bone)
                        break

            for mini in mini_bosses:

                if weapon.hit_enemy(mini) and mini.alive:
                    damage = player.weapon.attack

                    mini.hit(damage)

            if weapon.hit_enemy(boss) and boss.alive and not game_data["Boss2"]:

                damage = 0

                if player.weapon:
                    damage = player.weapon.attack

                boss.hit(damage)

        for arrow in arrows:

            for mini in mini_bosses:

                if mini.alive and arrow.hit_enemy(mini.get_rect()):
                    damage = player.bow.damage

                    mini.hit(damage)

                    arrows.remove(arrow)

                    arrow_hit.play()

                    break

            if boss.alive and arrow.hit_enemy(boss.get_rect()) and not game_data["Boss2"]:

                damage = 0

                if player.bow:
                    damage = player.bow.damage

                boss.hit(damage)

                arrows.remove(arrow)

                arrow_hit.play()

                break


        if not freeze_world:
            player.move(keys, walls, ice_rects)



            if not mini_spawned and not game_data["Boss2"]:
                for sk in skeletons:
                    sk.move(player, walls)

                    for weapon in melee_weapons:

                        if weapon.hit_enemy(sk) and sk.alive:

                            damage = 0

                            if player.weapon:
                                damage = player.weapon.attack

                            sk.hit(damage)

                    for arrow in arrows[:]:

                        if sk.alive and arrow.hit_enemy(sk.get_hurt_rect()):

                            damage = 0

                            if player.bow:
                                damage = player.bow.damage

                            sk.hit(damage)

                            arrows.remove(arrow)

                            arrow_hit.play()

                            break

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )

            for rect in Spikes:
                if player.get_rect().colliderect(rect):
                    player.take_hit(1)

            if boss.dead_done:
                chest.update(player)

            if not mini_spawned and not game_data["Boss2"]:
                boss.move(player, walls)

            for mini in mini_bosses:
                mini.move(player, walls)

        if (
                mini_spawned
                and not ending_started
                and all(not mini.alive for mini in mini_bosses)
        ):
            ending_started = True

            fading = True
            fade_start = now

            pygame.mixer.music.fadeout(3000)

            game_data["Boss2"] = True

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        if (
                boss_phase1_done
                and chest.state == "opened"
                and not mini_spawned
        ):
            music_fading_up = True
            music_fade_up_start = now

            mini_bosses.append(
                MiniSecondBoss(
                    300, 250
                )
            )

            mini_bosses.append(
                MiniSecondBoss(
                    500, 250
                )
            )

            mini_bosses.append(
                MiniSecondBoss(
                    700, 250
                )
            )

            mini_spawned = True

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        if chest:
            chest.draw(Screen)

        player.draw(Screen)

        if not mini_spawned and not game_data["Boss2"]:
            boss.draw(Screen)
            for sk in skeletons:
                sk.draw(Screen)

        for mini in mini_bosses:
            mini.draw(Screen)

        if (
                boss.dead_done
                and not boss_phase1_done
        ):
            boss_phase1_done = True

            music_fading_down = True
            music_fade_start = now

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:

            if player.get_rect().colliderect(rect):

                if not game_data["Boss2"]:

                    boss_leave_warning = True
                else:

                    pygame.mixer.music.fadeout(1000)
                    game_data["Scene_Back"] = True
                    return "PreRoom"

        if boss_leave_warning:
            panel = pygame.Rect(240, 250, 800, 200)

            pygame.draw.rect(Screen, (20, 20, 20), panel, border_radius=12)
            pygame.draw.rect(Screen, (255, 255, 255), panel, 2, border_radius=12)

            font = pygame.font.Font(None, 42)

            text1 = font.render(
                "You have not defeated the boss.",
                True,
                (255, 255, 255)
            )

            text2 = font.render(
                "Are you sure you want to leave?",
                True,
                (255, 255, 255)
            )

            text3 = font.render(
                "[Y] Yes    [N] No",
                True,
                (255, 255, 0)
            )

            Screen.blit(
                text1,
                (panel.centerx - text1.get_width() // 2, panel.y + 40)
            )

            Screen.blit(
                text2,
                (panel.centerx - text2.get_width() // 2, panel.y + 90)
            )

            Screen.blit(
                text3,
                (panel.centerx - text3.get_width() // 2, panel.y + 145)
            )

        if player.health <= 0:
            player.dead = True

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        if fading:

            elapsed = now - fade_start

            if elapsed >= 3000:
                pygame.mixer.music.stop()
                game_data["Scene_Back"] = True
                return "PreRoom"

            alpha = min(
                255,
                int(elapsed / 3000 * 255)
            )

            fade_surface = pygame.Surface(
                (Screen.get_width(), Screen.get_height())
            )

            fade_surface.fill((255, 255, 255))

            fade_surface.set_alpha(alpha)

            Screen.blit(fade_surface, (0, 0))

        if music_fading_down:

            elapsed = now - music_fade_start

            volume = max(
                0.0,
                0.4 - elapsed / 2000 * 0.4
            )

            pygame.mixer.music.set_volume(volume)

            if elapsed >= 2000:
                music_fading_down = False
                pygame.mixer.music.set_volume(0)

        if music_fading_up:

            elapsed = now - music_fade_up_start

            volume = min(
                0.4,
                elapsed / 1500 * 0.4
            )

            pygame.mixer.music.set_volume(volume)

            if elapsed >= 1500:
                music_fading_up = False
                pygame.mixer.music.set_volume(0.4)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Entry(player, game_data):
    # ================= INIT =================
    player.can_attack = True
    lava = pygame.mixer.Sound("SoundEffects/Lava.mp3")
    lava.set_volume(0.4)

    if game_data["Scene_Back_1"]:
        player.set_position(-40, 150)
        game_data["Scene_Back_1"] = False
    elif game_data["Scene_Back"]:
        player.set_position(1200, 150)
        game_data["Scene_Back"] = False
    else:
        player.set_position(570, 660)
        pygame.mixer.music.load("Musics/Fight.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        lava.play(-1)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    metal = pygame.mixer.Sound("SoundEffects/Metal.mp3")
    metal.set_volume(0.2)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    skeletons = []

    skeletons.append(SkeletonSword(50, 180))
    skeletons.append(SkeletonBoxer(40, 120))
    skeletons.append(SkeletonBoxer(40, 240))
    skeletons.append(SkeletonSword(1186, 180))
    skeletons.append(SkeletonBoxer(1196, 120))
    skeletons.append(SkeletonBoxer(1196, 240))

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Third Boss/Entry.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    ice_rects = []

    Change_Scene = []

    Change_Scene_1 = []

    Change_Scene_2 = []

    save_message_timer = 0
    save_message_text = ""

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fading = False
    fade_start = 0

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_2"):
        Change_Scene_2.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open

        freeze_world = ui_open or fading

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )

            for sk in skeletons:
                sk.move(player, walls)

                for weapon in melee_weapons:

                    if weapon.hit_enemy(sk) and sk.alive:

                        damage = 0

                        if player.weapon:
                            damage = player.weapon.attack

                        sk.hit(damage)

                for arrow in arrows[:]:

                    if sk.alive and arrow.hit_enemy(sk.get_hurt_rect()):

                        damage = 0

                        if player.bow:
                            damage = player.bow.damage

                        sk.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        for sk in skeletons:
            sk.draw(Screen)

        player.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                return "Room1"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                return "Room2"

        for rect in Change_Scene_2:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.stop()
                game_data["Scene_Back_1"] = True
                return "IroHome"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.health <= 0:
            player.dead = True

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Room1(player, game_data):
    # ================= INIT =================
    player.can_attack = True

    player.set_position(1200, 150)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    metal = pygame.mixer.Sound("SoundEffects/Metal.mp3")
    metal.set_volume(0.2)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    skeletons = []

    skeletons.append(SkeletonSword(510, 590))
    skeletons.append(SkeletonBoxer(490, 640))
    skeletons.append(SkeletonSword(605, 590))
    skeletons.append(SkeletonBoxer(625, 640))

    chest = Chest(
        576,
        672,
        "Lava_chest_1"
    )

    chest.set_loot(make_legs_3())
    chest.load_state(game_data)

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Third Boss/Room1.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    walls.append(chest.hitbox)

    ice_rects = []

    Change_Scene = []

    save_message_timer = 0
    save_message_text = ""

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fading = False
    fade_start = 0

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open

        chest_open = chest.state == "opened"

        freeze_world = ui_open or fading or chest_open

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if event.key == pygame.K_f:
                    if chest.state == "opened":
                        chest.close_ui()

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )
            chest.update(player)

            for sk in skeletons:
                sk.move(player, walls)

                for weapon in melee_weapons:

                    if weapon.hit_enemy(sk) and sk.alive:

                        damage = 0

                        if player.weapon:
                            damage = player.weapon.attack

                        sk.hit(damage)

                for arrow in arrows[:]:

                    if sk.alive and arrow.hit_enemy(sk.get_hurt_rect()):

                        damage = 0

                        if player.bow:
                            damage = player.bow.damage

                        sk.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        for sk in skeletons:
            sk.draw(Screen)

        player.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        chest.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                game_data["Scene_Back_1"] = True
                return "Entry"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.health <= 0:
            player.dead = True

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Room2(player, game_data):
    # ================= INIT =================
    player.can_attack = True

    if game_data["Scene_Back_1"]:
        player.set_position(1200, 150)
        game_data["Scene_Back_1"] = False
    elif game_data["Scene_Back"]:
        player.set_position(570, -40)
        game_data["Scene_Back"] = False
    elif game_data["Scene_Back_2"]:
        player.set_position(570, 660)
        game_data["Scene_Back_2"] = False
    else:
        player.set_position(-40, 150)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    metal = pygame.mixer.Sound("SoundEffects/Metal.mp3")
    metal.set_volume(0.2)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    skeletons = []

    skeletons.append(SkeletonSword(555, 590))
    skeletons.append(SkeletonBoxer(535, 640))
    skeletons.append(SkeletonSword(650, 590))
    skeletons.append(SkeletonBoxer(670, 640))

    skeletons.append(SkeletonSword(555, 50))
    skeletons.append(SkeletonBoxer(535, 0))
    skeletons.append(SkeletonSword(650, 50))
    skeletons.append(SkeletonBoxer(670, 0))

    skeletons.append(SkeletonWizard(1186, 180))

    chest = Chest(
        624,
        176,
        "Lava_chest_2"
    )

    chest.set_loot(make_hands_3())
    chest.load_state(game_data)

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Third Boss/Room2.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    walls.append(chest.hitbox)

    ice_rects = []

    Change_Scene = []
    Change_Scene_1 = []
    Change_Scene_2 = []
    Change_Scene_3 = []

    save_message_timer = 0
    save_message_text = ""

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fading = False
    fade_start = 0

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_2"):
        Change_Scene_2.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_3"):
        Change_Scene_3.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))
    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open

        chest_open = chest.state == "opened"

        freeze_world = ui_open or fading or chest_open

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if event.key == pygame.K_f:
                    if chest.state == "opened":
                        chest.close_ui()

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )
            chest.update(player)

            for sk in skeletons:
                sk.move(player, walls)

                for weapon in melee_weapons:

                    if weapon.hit_enemy(sk) and sk.alive:

                        damage = 0

                        if player.weapon:
                            damage = player.weapon.attack

                        sk.hit(damage)

                for arrow in arrows[:]:

                    if sk.alive and arrow.hit_enemy(sk.get_hurt_rect()):

                        damage = 0

                        if player.bow:
                            damage = player.bow.damage

                        sk.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        for sk in skeletons:
            sk.draw(Screen)

        player.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        chest.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene_3:
            if player.get_rect().colliderect(rect):
                game_data["Scene_Back"] = True
                return "Entry"

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                return "Room3"

        for rect in Change_Scene_2:
            if player.get_rect().colliderect(rect):
                return "Room4"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                return "PreRoom_1"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.health <= 0:
            player.dead = True

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Room3(player, game_data):
    # ================= INIT =================
    player.can_attack = True

    player.set_position(570, 660)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    metal = pygame.mixer.Sound("SoundEffects/Metal.mp3")
    metal.set_volume(0.2)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    skeletons = []

    skeletons.append(SkeletonSword(606, 250))
    skeletons.append(SkeletonBoxer(560, 200))
    skeletons.append(SkeletonBoxer(652, 200))
    skeletons.append(SkeletonWizard(400, 150))
    skeletons.append(SkeletonWizard(812, 150))

    chest = Chest(
        624,
        176,
        "Lava_chest_3"
    )

    chest.set_loot(make_head_3())
    chest.load_state(game_data)

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Third Boss/Room3.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    walls.append(chest.hitbox)

    ice_rects = []

    Change_Scene = []

    save_message_timer = 0
    save_message_text = ""

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fading = False
    fade_start = 0

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open

        chest_open = chest.state == "opened"

        freeze_world = ui_open or fading or chest_open

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if event.key == pygame.K_f:
                    if chest.state == "opened":
                        chest.close_ui()

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )
            chest.update(player)

            for sk in skeletons:
                sk.move(player, walls)

                for weapon in melee_weapons:

                    if weapon.hit_enemy(sk) and sk.alive:

                        damage = 0

                        if player.weapon:
                            damage = player.weapon.attack

                        sk.hit(damage)

                for arrow in arrows[:]:

                    if sk.alive and arrow.hit_enemy(sk.get_hurt_rect()):

                        damage = 0

                        if player.bow:
                            damage = player.bow.damage

                        sk.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        for sk in skeletons:
            sk.draw(Screen)

        player.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        chest.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                game_data["Scene_Back"] = True
                return "Room2"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.health <= 0:
            player.dead = True

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Room4(player, game_data):
    # ================= INIT =================
    player.can_attack = True

    player.set_position(570, -40)

    last_arrow_time = 0
    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    metal = pygame.mixer.Sound("SoundEffects/Metal.mp3")
    metal.set_volume(0.2)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    skeletons = []

    skeletons.append(SkeletonSword(558, 600))
    skeletons.append(SkeletonBoxer(538, 640))
    skeletons.append(SkeletonSword(652, 600))
    skeletons.append(SkeletonBoxer(672, 640))

    chest = Chest(
        624,
        672,
        "Lava_chest_4"
    )

    chest.set_loot(make_sword_2())
    chest.load_state(game_data)

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Third Boss/Room4.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    walls.append(chest.hitbox)

    ice_rects = []

    Change_Scene = []

    save_message_timer = 0
    save_message_text = ""

    fade_surface = pygame.Surface((1280, 768))
    fade_surface.fill((255, 255, 255))

    fading = False
    fade_start = 0

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open

        chest_open = chest.state == "opened"

        freeze_world = ui_open or fading or chest_open

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if event.key == pygame.K_f:
                    if chest.state == "opened":
                        chest.close_ui()

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================
        if not freeze_world:
            player.move(keys, walls, ice_rects)

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )
            chest.update(player)

            for sk in skeletons:
                sk.move(player, walls)

                for weapon in melee_weapons:

                    if weapon.hit_enemy(sk) and sk.alive:

                        damage = 0

                        if player.weapon:
                            damage = player.weapon.attack

                        sk.hit(damage)

                for arrow in arrows[:]:

                    if sk.alive and arrow.hit_enemy(sk.get_hurt_rect()):

                        damage = 0

                        if player.bow:
                            damage = player.bow.damage

                        sk.hit(damage)

                        arrows.remove(arrow)

                        arrow_hit.play()

                        break

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        for sk in skeletons:
            sk.draw(Screen)

        player.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if chest.give_loot:

            if chest.loot_item:
                inventory.add_item(chest.loot_item)

            game_data["looted_chests"].add(
                chest.chest_id
            )

            chest.give_loot = False

        chest.draw(Screen)

        if chest.state == "opened":
            chest.draw_loot_ui(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                game_data["Scene_Back_2"] = True
                return "Room2"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.health <= 0:
            player.dead = True

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

def PreRoom_1(player, game_data):
    # ================= INIT =================
    player.can_attack = False

    if "npc_gifts" not in game_data:
        game_data["npc_gifts"] = set()

    lava = pygame.mixer.Sound("SoundEffects/Lava.mp3")
    lava.set_volume(0.4)

    if game_data.get("Scene_Back"):
        player.set_position(1200, 350)
        game_data["Scene_Back"] = False
        pygame.mixer.music.load("Musics/Fight.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1, fade_ms=2000)
        lava.play()
    else:
        player.set_position(-40, 150)

    if game_data["scene"] == "PreRoom_1":
        pygame.mixer.music.load("Musics/Fight.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1, fade_ms=2000)
        lava.play()

    npcs = preroom1_npcs()
    dialogue = DialogueSystem()

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrows = []
    melee_weapons = []

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Third Boss/PreRoom.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= SAVE POINT =================
    save_point = SavePoint("PreRoom_1_save")

    # ================= UI =================
    MenuButton = Button(
        "Graphics/MenuButton.png",
        "Graphics/Hovered_MenuButton.png",
        (20, 680),
        size=(164, 66)
    )

    regular_buttons = pygame.sprite.Group(MenuButton)

    # ================= COLLISION =================
    walls = [
        save_point.get_rect(),
    ]

    ice_rects = []

    Change_Scene = []

    Change_Scene_1 = []

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    for obj in tiled_map.get_layer_by_name("Change_Scene_1"):
        Change_Scene_1.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open
        freeze_world = ui_open or dialogue.active

        keys = pygame.key.get_pressed()

        near_save_point = save_point.is_near(player)

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= UI BUTTON =================
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MenuButton.is_clicked(mouse_pos):
                    click.play()
                    return "menu"

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                # ===== SAVE SYSTEM =====
                if event.key == pygame.K_p and near_save_point:
                    save_game(
                        player,
                        "PreRoom",
                        game_data,
                        save_point.save_point_id
                    )
                    save_message_timer = 120
                    save_message_text = "Progress saved."

                if event.key == pygame.K_r and near_save_point:
                    return reset_save_data(player, game_data)

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                if event.key == pygame.K_f and not inventory_ui.open:
                    if dialogue.active:
                        dialogue.next_line()
                    else:
                        for npc in npcs:
                            npc.talk(
                                player,
                                dialogue,
                                inventory,
                                game_data
                            )
        # ================= UPDATE =================
        if not freeze_world:
            npc_rects = [npc.get_rect() for npc in npcs]

            player.move(
                keys,
                walls + npc_rects,
                ice_rects
            )

            for i, npc in enumerate(npcs):

                npc_walls = walls.copy()
                npc_walls.append(player.get_rect())

                for j, other in enumerate(npcs):
                    if i != j:
                        npc_walls.append(other.get_rect())

                npc.move(npc_walls)

        for npc in npcs:
            npc.near_player = npc.is_near(player)

        dialogue.update()

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        save_point.draw(Screen, near_save_point)

        for npc in npcs:
            npc.draw(Screen)

        player.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        dialogue.draw(Screen)

        for npc in npcs:
            if npc.near_player and not dialogue.active:
                offset_y = -30 + int(
                    3 * pygame.time.get_ticks() / 300 % 2
                )

                Screen.blit(
                    f_icon,
                    (npc.x + 8, npc.y + offset_y)
                )

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        regular_buttons.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:
            if player.get_rect().colliderect(rect):
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.stop()
                return "Third_Boss"

        for rect in Change_Scene_1:
            if player.get_rect().colliderect(rect):
                game_data["Scene_Back_1"] = True
                return "Room2"

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)
        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Third_Boss(player, game_data):
    # ================= INIT =================
    player.can_attack = True
    player.set_position(-40, 350)

    last_melee_time = 0

    inventory = game_data["inventory"]
    inventory_ui = InventoryUI(inventory, player)

    click = pygame.mixer.Sound("Musics/Hover2.mp3")
    click.set_volume(0.2)

    arrow1 = pygame.mixer.Sound("SoundEffects/Arrow1.mp3")
    arrow1.set_volume(0.05)

    arrow_hit = pygame.mixer.Sound("SoundEffects/Arrow_hit.mp3")
    arrow_hit.set_volume(0.05)

    melee_sounds = [
        pygame.mixer.Sound(f"SoundEffects/Melee{i}.mp3")
        for i in range(1, 4)
    ]
    for s in melee_sounds:
        s.set_volume(0.1)

    if not game_data["Boss3"]:
        pygame.mixer.music.load("Musics/FinalFight.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

    chest = None

    if game_data["Boss3"]:
        chest = Chest(
            304,
            368,
            "boss3_chest"
        )

        chest.set_loot(make_chest_3())
        chest.load_state(game_data)


    Screen = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    arrow_images = load_arrow_images()
    melee_images = load_melee_images()

    arrows = []
    melee_weapons = []

    boss = ThirdBoss(1100, 309)

    boss_leave_warning = False

    # ================= MAP =================
    tiled_map = pytmx.load_pygame(
        "Maps/Third Boss/Boss.tmx",
        pixelalpha=True
    )

    SCALE = 2

    b1 = pygame.Surface(
        (
            tiled_map.width * tiled_map.tilewidth * SCALE,
            tiled_map.height * tiled_map.tileheight * SCALE
        )
    ).convert_alpha()

    def draw_map(surface):
        for layer in tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                tiled_map.tilewidth * SCALE,
                                tiled_map.tileheight * SCALE
                            )
                        )
                        surface.blit(tile, (
                            x * tiled_map.tilewidth * SCALE,
                            y * tiled_map.tileheight * SCALE
                        ))
        return surface

    SF = draw_map(b1)

    # ================= COLLISION =================
    walls = []

    if chest:
        walls.append(chest.hitbox)

    ice_rects = []

    Change_Scene = []

    fading = False
    fade_start = 0

    black_fading = False
    black_start = 0
    black_alpha = 0

    save_message_timer = 0
    save_message_text = ""

    for obj in tiled_map.get_layer_by_name("collision"):
        walls.append(
            pygame.Rect(
                obj.x * SCALE,
                obj.y * SCALE,
                obj.width * SCALE,
                obj.height * SCALE
            )
        )

    for obj in tiled_map.get_layer_by_name("Change_Scene"):
        Change_Scene.append(pygame.Rect(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE))

    # ================= GAME LOOP =================
    Game_active = True

    while Game_active:

        # ================= STATE =================
        now = pygame.time.get_ticks()

        ui_open = inventory_ui.open

        if chest:
            chest_open = chest.state == "opened"
            freeze_world = ui_open or boss_leave_warning or chest_open
        else:
            freeze_world = ui_open or boss_leave_warning

        keys = pygame.key.get_pressed()

        # ================= EVENTS =================
        for event in pygame.event.get():

            game_data["help_ui"].handle_event(event)

            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # ================= KEY INPUT =================
            if event.type == pygame.KEYDOWN:

                if boss_leave_warning:

                    if event.key == pygame.K_y:
                        pygame.mixer.music.fadeout(1000)
                        game_data["Scene_Back"] = True
                        return "PreRoom_1"

                    elif event.key == pygame.K_n:
                        boss_leave_warning = False
                        player.x += 50

                    continue

                if event.key == pygame.K_f and inventory_ui.open:
                    inventory_ui.handle_use(player, game_data["inventory"])

                if chest:
                    if event.key == pygame.K_f:
                        if chest.state == "opened":
                            chest.close_ui()

                # ===== INVENTORY =====
                if event.key == pygame.K_i:
                    inventory_ui.open = not inventory_ui.open

                if inventory_ui.open:
                    if event.key == pygame.K_LEFT:
                        inventory_ui.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        inventory_ui.move_cursor(1, 0)
                    if event.key == pygame.K_UP:
                        inventory_ui.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN:
                        inventory_ui.move_cursor(0, 1)

                # ===== COMBAT =====
                if not freeze_world:

                    if event.key == pygame.K_e:
                        if player.start_bow_attack():
                            last_arrow_time = now

                    if event.key == pygame.K_q:

                        if player.weapon is None:
                            continue

                        if now - last_melee_time >= player.weapon.cooldown:
                            x, y = player.get_center()

                            melee_weapons.append(
                                MeleeWeapon(
                                    x,
                                    y,
                                    player.direction,
                                    melee_images
                                )
                            )

                            random.choice(melee_sounds).play()

                            last_melee_time = now

        # ================= UPDATE =================


        for weapon in melee_weapons:

            if weapon.hit_boss(boss) and boss.alive and not game_data["Boss3"]:

                damage = 0

                if player.weapon:
                    damage = player.weapon.attack

                boss.hit(damage)

        for arrow in arrows:

            if boss.alive and arrow.hit_enemy(boss.get_hurt_rect()) and not game_data["Boss3"]:

                damage = 0

                if player.bow:
                    damage = player.bow.damage

                boss.hit(damage)

                arrows.remove(arrow)

                arrow_hit.play()

                break


        if not freeze_world:
            player.move(keys, walls, ice_rects)

            boss.update_music()

            create_arrow_from_bow(
                player, arrows, arrow_images, arrow1
            )

            if chest:
                chest.update(player)

            if not game_data["Boss3"]:
                boss.move(player, walls)

        if chest:
            if chest.give_loot:

                if chest.loot_item:
                    inventory.add_item(chest.loot_item)

                game_data["looted_chests"].add(
                    chest.chest_id
                )

                chest.give_loot = False

        for arrow in arrows[:]:
            if not arrow.update() or arrow.off_screen(1280, 768):
                arrows.remove(arrow)

        for weapon in melee_weapons[:]:
            if not weapon.update():
                melee_weapons.remove(weapon)

        Screen.blit(SF, (0, 0))

        if chest:
            chest.draw(Screen)

        player.draw(Screen)

        if chest:
            if chest.state == "opened":
                chest.draw_loot_ui(Screen)

        if not game_data["Boss3"]:
            boss.draw(Screen)

        for arrow in arrows:
            arrow.draw(Screen)

        for weapon in melee_weapons:
            weapon.draw(Screen)

        if inventory_ui.open:
            inventory_ui.draw(Screen)

        if save_message_timer > 0:
            draw_save_message(Screen, save_message_text)

            save_message_timer -= 1

        for rect in Change_Scene:

            if player.get_rect().colliderect(rect):

                if not game_data["Boss3"]:

                    boss_leave_warning = True
                else:

                    pygame.mixer.music.fadeout(1000)
                    game_data["Scene_Back"] = True
                    return "PreRoom_1"

        if boss_leave_warning:
            panel = pygame.Rect(240, 250, 800, 200)

            pygame.draw.rect(Screen, (20, 20, 20), panel, border_radius=12)
            pygame.draw.rect(Screen, (255, 255, 255), panel, 2, border_radius=12)

            font = pygame.font.Font(None, 42)

            text1 = font.render(
                "You have not defeated the boss.",
                True,
                (255, 255, 255)
            )

            text2 = font.render(
                "Are you sure you want to leave?",
                True,
                (255, 255, 255)
            )

            text3 = font.render(
                "[Y] Yes    [N] No",
                True,
                (255, 255, 0)
            )

            Screen.blit(
                text1,
                (panel.centerx - text1.get_width() // 2, panel.y + 40)
            )

            Screen.blit(
                text2,
                (panel.centerx - text2.get_width() // 2, panel.y + 90)
            )

            Screen.blit(
                text3,
                (panel.centerx - text3.get_width() // 2, panel.y + 145)
            )

        if player.health <= 0:
            player.dead = True

        player.draw_health_bar(Screen)
        player.draw_stamina_bar(Screen)

        if player.can_attack:
            player.draw_weapon_cooldowns(Screen)

        if player.dead:

            white = pygame.Surface(Screen.get_size())
            white.fill((255, 255, 255))

            old_screen = Screen.copy()

            for alpha in range(0, 255, 8):
                Screen.blit(old_screen, (0, 0))

                white.set_alpha(alpha)

                Screen.blit(white, (0, 0))

                pygame.display.update()

                clock.tick(60)

            pygame.mixer.music.stop()
            pygame.mixer.stop()

            return respawn_from_save(player, game_data)

        if boss.dead_done and not black_fading:
            black_fading = True
            black_start = pygame.time.get_ticks()

            pygame.mixer.music.fadeout(1500)

        if black_fading:

            elapsed = pygame.time.get_ticks() - black_start

            # ================= FADE TO BLACK =================
            if elapsed < 1500:
                black_alpha = int((elapsed / 1500) * 255)
            else:
                black_alpha = 255

            fade_surface = pygame.Surface(
                (Screen.get_width(), Screen.get_height())
            )

            fade_surface.fill((0, 0, 0))  # ⭐ 黑屏

            fade_surface.set_alpha(black_alpha)

            Screen.blit(fade_surface, (0, 0))

            # ================= HOLD BLACK =================
            if elapsed >= 3000:
                game_data["Boss3"] = True
                return "Final_scene"

        game_data["help_ui"].draw(Screen)

        pygame.display.update()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.mixer.stop()

def Final_scene(screen, clock):

    pygame.mixer.music.load("Musics/FinalFight.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)

    # ================= TEXT =================
    subtitles = [
        "At the moment the King felled",
        "Iro heard a voice:",
        "Iro, my son",
        "You have growed",
        "Stronger",
        "Smarter",
        "And braver",
        "Let me explain to you what actually happend to Eldermoor",
        "Hundreds years ago",
        "The curse named 'Forgotton' took our country",
        "Everyone have forgot who they were",
        "But I was special",
        "I still remember things time to time",
        "And I left the hope of humanity to you",
        "At this point, seems like you did it",
        "I knew you can",
        "Besides that",
        "I am sorry",
        "I did not intended to left you along whe you were young",
        "But the evil force didn't left me a choice",
        "It's nice to see you before the end of my life",
        "You are my successor, Eldermoor III, Iro Eldermoor",
        "With this responsibility, save more people",
        "Iro."
    ]

    font = pygame.font.Font(None, 36)

    # ================= TIMING =================
    fade_in_time = 800
    hold_time = 1200
    fade_out_time = 800

    white_fade_speed = 3

    white_hold_time = 3000  # ⭐ 白屏停留3秒
    white_hold_timer = 0

    WHITE = (255, 255, 255)

    def render_text(text, alpha):
        surf = font.render(text, True, (255, 255, 255))
        surf.set_alpha(alpha)
        return surf

    # ================= STATE =================
    index = 0
    timer = 0
    phase = "subtitle"

    white_alpha = 0

    running = True

    while running:
        dt = clock.tick(60)
        timer += dt

        screen.fill((0, 0, 0))

        # ================= SUBTITLE =================
        if phase == "subtitle":
            text = subtitles[index]

            total = fade_in_time + hold_time + fade_out_time

            if timer < fade_in_time:
                alpha = int(255 * (timer / fade_in_time))
            elif timer < fade_in_time + hold_time:
                alpha = 255
            elif timer < total:
                alpha = int(255 * (1 - (timer - fade_in_time - hold_time) / fade_out_time))
            else:
                timer = 0
                index += 1

                if index >= len(subtitles):
                    phase = "whitefade"
                    pygame.mixer.music.fadeout(3000)  # ⭐ 音乐淡出3秒
                continue

            text_surf = render_text(text, alpha)
            rect = text_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text_surf, rect)

        # ================= WHITE FADE =================
        elif phase == "whitefade":

            # fade to white
            if white_alpha < 255:
                white_alpha += white_fade_speed
                if white_alpha > 255:
                    white_alpha = 255

            # hold white screen for 3 seconds
            else:
                white_hold_timer += dt
                if white_hold_timer >= white_hold_time:
                    pygame.mixer.music.stop()
                    return "menu"

            overlay = pygame.Surface(screen.get_size())
            overlay.fill(WHITE)
            overlay.set_alpha(white_alpha)
            screen.blit(overlay, (0, 0))

        pygame.display.flip()

player = Player(spawn_x=297, spawn_y=389)

inventory = Inventory(cols=6, rows=3)

game_data = {
    "loaded_position": False,
    "looted_chests": set(),
    "npc_gifts": set(),
    "npc_gift_given": False,
    "npc_gift": False,
    "Scene_Back": False,
    "Scene_Back_1": False,
    "Scene_Back_2": False,
    "inventory": inventory,
    "scene": menu,
    "MazeSolved": False,
    "Boss1": False,
    "Boss2": False,
    "Boss3": False,

    "storage_chests": {}
}

game_data["help_ui"] = HelpUI()


current_scene = "menu"

while True:

    if current_scene == "menu":
        current_scene = menu(player, game_data)

    elif current_scene == "first_scene":
        current_scene = first_scene(player, game_data)

    elif current_scene == "second_scene":
        current_scene = second_scene(player, game_data)

    elif current_scene == "eldermoor_scene":
        current_scene = eldermoor_scene(player, game_data)

    elif current_scene == "Maze":
        current_scene = Maze(player, game_data)

    elif current_scene == "SnowVillage":
        current_scene = SnowVillage(player, game_data)

    elif current_scene == "IroHouse":
        current_scene = IroHouse(player, game_data)

    elif current_scene == "IroHome":
        current_scene = IroHome(player, game_data)

    elif current_scene == "InHouse":
        current_scene = InHouse(player, game_data)

    elif current_scene == "Maze_Solved":
        current_scene = Maze_Solved(player, game_data)

    elif current_scene == "First_Boss":
        current_scene = First_Boss(player, game_data)

    elif current_scene == "DesertVillage":
        current_scene = DesertVillage(player, game_data)

    elif current_scene == "DesertMaze":
        current_scene = DesertMaze(player, game_data)

    elif current_scene == "PreRoom":
        current_scene = PreRoom(player, game_data)

    elif current_scene == "Second_Boss":
        current_scene = Second_Boss(player, game_data)

    elif current_scene == "Entry":
        current_scene = Entry(player, game_data)

    elif current_scene == "Room1":
        current_scene = Room1(player, game_data)

    elif current_scene == "Room2":
        current_scene = Room2(player, game_data)

    elif current_scene == "Room3":
        current_scene = Room3(player, game_data)

    elif current_scene == "Room4":
        current_scene = Room4(player, game_data)

    elif current_scene == "PreRoom_1":
        current_scene = PreRoom_1(player, game_data)

    elif current_scene == "Third_Boss":
        current_scene = Third_Boss(player, game_data)

    elif current_scene == "Final_scene":
        current_scene = Final_scene(Screen1, clock = pygame.time.Clock())

    elif current_scene == "quit":
        break

pygame.quit()

