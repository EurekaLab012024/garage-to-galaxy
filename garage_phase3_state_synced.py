
import pygame
import json
import os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Garage to Galaxy – Phase 3: Ocean")

WHITE = (255, 255, 255)
OCEAN_BLUE = (70, 130, 180)
BLUE = (100, 150, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Arial", 20)
FPS = 60

STATE_FILE = "gg_state.json"
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Setup
vehicle_zone = pygame.Rect(300, 250, 200, 100)
snap_points = {
    "float_L": pygame.Rect(290, 370, 40, 20),
    "float_R": pygame.Rect(470, 370, 40, 20),
    "propeller": pygame.Rect(380, 350, 40, 20),
    "cockpit": pygame.Rect(360, 260, 80, 40)
}

class Part:
    def __init__(self, name, color, pos, buoyant=False):
        self.name = name
        self.rect = pygame.Rect(*pos, 40, 40)
        self.color = color
        self.dragging = False
        self.buoyant = buoyant

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        label = FONT.render(self.name, True, BLACK)
        surf.blit(label, (self.rect.x + 2, self.rect.y + 2))

parts = [
    Part("Floaty L", (135, 206, 250), (50, 100), buoyant=True),
    Part("Floaty R", (135, 206, 250), (50, 160), buoyant=True),
    Part("Propeller", (180, 180, 255), (50, 220)),
    Part("Cockpit", (255, 255, 255), (50, 280))
]

state = load_state()
vehicle = state.get("current_vehicle", {})
attached = vehicle.get("parts", {})
progress = state.get("progress", {})
ocean_unlocked = progress.get("ocean", False)

clock = pygame.time.Clock()
running = True
msg = ""

while running:
    screen.fill(OCEAN_BLUE)

    pygame.draw.rect(screen, BLUE, vehicle_zone)
    for key, sp in snap_points.items():
        pygame.draw.rect(screen, BLACK, sp, 2)

    for part in parts:
        part.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and ocean_unlocked:
            for part in parts:
                if part.rect.collidepoint(event.pos):
                    part.dragging = True
                    offset_x = event.pos[0] - part.rect.x
                    offset_y = event.pos[1] - part.rect.y

        elif event.type == pygame.MOUSEBUTTONUP:
            for part in parts:
                if part.dragging:
                    part.dragging = False
                    for snap_key, sp in snap_points.items():
                        if part.rect.colliderect(sp):
                            part.rect.topleft = sp.topleft
                            attached[snap_key] = part.name
                            vehicle["parts"] = attached
                            vehicle["name"] = vehicle.get("name", "OceanX Proto")
                            state["current_vehicle"] = vehicle
                            progress["journal"] = True
                            state["progress"] = progress
                            save_state(state)

        elif event.type == pygame.MOUSEMOTION:
            for part in parts:
                if part.dragging:
                    part.rect.x = event.pos[0] - offset_x
                    part.rect.y = event.pos[1] - offset_y

    if not ocean_unlocked:
        lock = FONT.render("Ocean Scene Locked – Complete Sky Phase!", True, (255, 0, 0))
        screen.blit(lock, (180, 250))
    else:
        screen.blit(FONT.render("Add floaties to balance your sub!", True, BLACK), (20, 20))
        fL = "float_L" in attached
        fR = "float_R" in attached
        if fL and fR:
            status = "✅ Stable floatation!"
        elif fL or fR:
            status = "⚠️ Sub is tilting!"
        else:
            status = "❌ You're sinking!"
        screen.blit(FONT.render(status, True, WHITE), (20, 60))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
