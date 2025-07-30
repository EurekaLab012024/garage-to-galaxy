
import pygame
import json
import os

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Garage to Galaxy – Garage 2.0 + Journal")

WHITE = (255, 255, 255)
BLUE = (150, 200, 255)
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

vehicle_zone = pygame.Rect(300, 250, 200, 100)
snap_points = {
    "engine": pygame.Rect(370, 250, 60, 40),
    "float_L": pygame.Rect(290, 370, 40, 20),
    "float_R": pygame.Rect(470, 370, 40, 20),
    "propeller": pygame.Rect(380, 350, 40, 20)
}

state = load_state()
vehicle = state.get("current_vehicle", {})
attached_parts = vehicle.get("parts", {})
vehicle_name = vehicle.get("name", "Unnamed Build")
journal_ready = state.get("progress", {}).get("journal", False)

clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, vehicle_zone)

    for key, sp in snap_points.items():
        pygame.draw.rect(screen, (0, 0, 0), sp, 2)
        pname = attached_parts.get(key, "")
        if pname:
            pygame.draw.rect(screen, (200, 255, 255), sp)
            label = FONT.render(pname, True, BLACK)
            screen.blit(label, (sp.x + 2, sp.y + 2))

    # Journal View
    y = 40
    screen.blit(FONT.render("🚀 Transform Journal:", True, BLACK), (30, y))
    y += 30
    screen.blit(FONT.render(f"Name: {vehicle_name}", True, BLACK), (30, y))
    y += 30
    screen.blit(FONT.render(f"Parts Used: {', '.join(attached_parts.values())}", True, BLACK), (30, y))
    y += 30
    screen.blit(FONT.render("Challenge: Remix 1 part and test again!", True, (0, 90, 0)), (30, y))
    y += 30

    if journal_ready:
        screen.blit(FONT.render("✅ Journal Ready – You completed the loop!", True, (0, 150, 0)), (30, y))
    else:
        screen.blit(FONT.render("🔒 Journal Locked – Complete Ocean First", True, (150, 0, 0)), (30, y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
