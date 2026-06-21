import pygame

class HelpUI:
    def __init__(self):
        self.open = False

        self.font = pygame.font.Font(None, 40)

        self.texts = [
            "CONTROLS",
            "",
            "Q = Melee Attack",
            "E = Bow Attack",
            "F = Interact",
            "I = Inventory",
            "WASD = Move",
            "",
            "H = Toggle Help"
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.open = not self.open

    def draw(self, screen):
        if not self.open:
            return

        panel = pygame.Rect(260, 180, 760, 380)

        overlay = pygame.Surface((panel.width, panel.height))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))

        screen.blit(overlay, panel.topleft)
        pygame.draw.rect(screen, (255, 255, 255), panel, 2)

        y = panel.y + 20

        for i, line in enumerate(self.texts):
            color = (255, 255, 0) if i == 0 else (255, 255, 255)
            surf = self.font.render(line, True, color)
            screen.blit(surf, (panel.x + 40, y))
            y += 35