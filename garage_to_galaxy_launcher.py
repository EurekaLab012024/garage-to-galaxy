
import os

print("🚀 Welcome to Garage to Galaxy Launcher!")
print("Choose a phase to begin:")
print("1 – Garage + Car")
print("2 – Sky")
print("3 – Ocean")
print("4 – Garage 2.0 + Journal")

choice = input("Enter number: ").strip()
scripts = {
    "1": "garage_phase1_state_synced.py",
    "2": "garage_phase2_state_synced.py",
    "3": "garage_phase3_state_synced.py",
    "4": "garage_phase4_state_synced.py"
}
selected = scripts.get(choice)
if selected and os.path.exists(selected):
    os.system(f"python {selected}")
else:
    print("Invalid choice or missing file.")
