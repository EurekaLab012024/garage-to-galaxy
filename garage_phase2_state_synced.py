
import pygame
import json
import os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Garage to Galaxy – Phase 2 (Sky)")

WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
BLUE = (100, 150, 255)
BLACK = (0, 0, 0)
FPS = 60
FONT = pygame.font.SysFont("Arial", 20)

STATE_FILE = "gg_state.json"
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Vehicle zone + snap points
vehicle_zone = pygame.Rect(300, 250, 200, 100)
snap_points = {
    "balloon": pygame.Rect(330, 200, 40, 40),
    "parachute": pygame.Rect(400, 200, 40, 40),
    "tailfin": pygame.Rect(370, 330, 60, 20),
    "splash": pygame.Rect(350, 400, 60, 20)
}

# Part class
class Part:
    def __init__(self, name, color, pos):
        self.name = name
        self.rect = pygame.Rect(*pos, 40, 40)
        self.color = color
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        label = FONT.render(self.name, True, BLACK)
        surface.blit(label, (self.rect.x + 2, self.rect.y + 2))

# Parts for sky
sky_parts = [
    Part("Balloon", (255, 105, 180), (50, 100)),
    Part("Parachute", (255, 165, 0), (50, 160)),
    Part("Tail Fin", (120, 60, 255), (50, 220)),
    Part("Splash", (0, 0, 255), (50, 280))
]

# Load state
state = load_state()
progress = state.get("progress", {})
vehicle = state.get("current_vehicle", {})
attached = vehicle.get("parts", {})
sky_unlocked = progress.get("sky", False)

clock = pygame.time.Clock()
running = True
msg = ""

while running:
    screen.fill(SKY_BLUE)

    pygame.draw.rect(screen, BLUE, vehicle_zone)
    for key, sp in snap_points.items():
        pygame.draw.rect(screen, BLACK, sp, 2)

    for part in sky_parts:
        part.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and sky_unlocked:
            for part in sky_parts:
                if part.rect.collidepoint(event.pos):
                    part.dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = part.rect.x - mouse_x
                    offset_y = part.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            for part in sky_parts:
                if part.dragging:
                    part.dragging = False
                    for snap_key, sp in snap_points.items():
                        if part.rect.colliderect(sp):
                            part.rect.topleft = sp.topleft
                            # Track part in vehicle
                            attached[snap_key] = part.name
                            vehicle["parts"] = attached
                            if part.name == "Splash":
                                progress["ocean"] = True  # Unlock ocean phase
                            state["current_vehicle"] = vehicle
                            state["progress"] = progress
                            save_state(state)

        elif event.type == pygame.MOUSEMOTION:
            for part in sky_parts:
                if part.dragging:
                    part.rect.x = event.pos[0] + offset_x
                    part.rect.y = event.pos[1] + offset_y

    if not sky_unlocked:
        msg = "Sky Scene Locked – Add Wing in Garage First!"
        lock_msg = FONT.render(msg, True, (255, 0, 0))
        screen.blit(lock_msg, (150, 250))
    else:
        label = FONT.render("Sky Scene Active – Add parts or parachute to continue!", True, BLACK)
        screen.blit(label, (100, 20))
        if progress.get("ocean", False):
            screen.blit(FONT.render("✅ Ocean Unlocked!", True, BLACK), (100, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
