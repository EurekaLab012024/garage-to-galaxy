
import pygame
import json
import os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Garage Phase 1 – State Synced")

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
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

# Setup
vehicle_zone = pygame.Rect(300, 250, 200, 100)
snap_points = {
    "tire_L": pygame.Rect(300, 340, 30, 30),
    "tire_R": pygame.Rect(470, 340, 30, 30),
    "engine": pygame.Rect(370, 250, 60, 40),
    "light": pygame.Rect(470, 260, 20, 20),
    "wing": pygame.Rect(350, 230, 100, 20)
}

# Parts
class Part:
    def __init__(self, name, color, pos):
        self.name = name
        self.rect = pygame.Rect(*pos, 40, 40)
        self.color = color
        self.dragging = False

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        label = FONT.render(self.name, True, BLACK)
        surf.blit(label, (self.rect.x + 2, self.rect.y + 2))

parts = [
    Part("Tire", GRAY, (50, 100)),
    Part("Engine", BLUE, (50, 160)),
    Part("Light", (255, 255, 0), (50, 220)),
    Part("Wing", (150, 255, 150), (50, 280))
]

# State init/load
state = load_state()
vehicle_data = state.get("current_vehicle", {"name": "Unnamed", "parts": {}, "notes": {"worked": "", "failed": ""}})
progress = state.get("progress", {"garage": True, "sky": False, "ocean": False, "journal": False})

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, vehicle_zone)

    for key, sp in snap_points.items():
        pygame.draw.rect(screen, BLACK, sp, 2)

    for part in parts:
        part.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for part in parts:
                if part.rect.collidepoint(event.pos):
                    part.dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = part.rect.x - mouse_x
                    offset_y = part.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            for part in parts:
                if part.dragging:
                    part.dragging = False
                    for snap_key, sp in snap_points.items():
                        if part.rect.colliderect(sp):
                            part.rect.topleft = sp.topleft
                            vehicle_data["parts"][snap_key] = part.name
                            if part.name == "Wing" and snap_key == "wing":
                                progress["sky"] = True  # Unlock Sky phase
                            # Save new state
                            state["current_vehicle"] = vehicle_data
                            state["progress"] = progress
                            save_state(state)

        elif event.type == pygame.MOUSEMOTION:
            for part in parts:
                if part.dragging:
                    part.rect.x = event.pos[0] + offset_x
                    part.rect.y = event.pos[1] + offset_y

    # Display vehicle name + progress status
    screen.blit(FONT.render(f"Vehicle: {vehicle_data['name']}", True, BLACK), (10, 10))
    screen.blit(FONT.render("Sky Unlocked" if progress["sky"] else "Sky Locked - Add Wing!", True, BLACK), (10, 40))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
