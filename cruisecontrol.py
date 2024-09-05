import pygame
import psutil
import win32gui
import win32process
import os

# Initialize pygame
pygame.init()

# Set up the window and graphics configuration (adjusting size to fit the ASCII art)
win_width = 1200
win_height = 400
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Controller Improvement")

# Set up the clock
clock = pygame.time.Clock()

# ASCII art for "Cruise Control"
cruise_control_ascii = r"""
                                __                                                 __                          __ 
                              |  \                                               |  \                        |  \\
  _______   ______   __    __  \$$  _______         _______   ______   _______  _| $$_     ______    ______  | $$  
 /       \ /      \ |  \  |  \|  \ /       \       /       \ /      \ |       \|   $$ \   /      \  /      \ | $$  
|  $$$$$$$|  $$$$$$\| $$  | $$| $$|  $$$$$$$      |  $$$$$$$|  $$$$$$\| $$$$$$$\\$$$$$$  |  $$$$$$\|  $$$$$$\| $$  
| $$      | $$   \$$| $$  | $$| $$ \$$    \       | $$      | $$  | $$| $$  | $$ | $$ __ | $$   \$$| $$  | $$| $$  
| $$_____ | $$      | $$__/ $$| $$ _\$$$$$$\      | $$_____ | $$__/ $$| $$  | $$ | $$|  \| $$      | $$__/ $$| $$  
 \$$     \| $$       \$$    $$| $$|       $$       \$$     \ \$$    $$| $$  | $$  \$$  $$| $$       \$$    $$| $$  
  \$$$$$$$ \$$        \$$$$$$  \$$ \$$$$$$$         \$$$$$$$  \$$$$$$  \$$   \$$   \$$$$  \$$        \$$$$$$  \$$  
"""

# Define the game class
class Game:
    def __init__(self):
        # Initialize variables related to game state
        self.running = True
        self.game_detected = None
        self.is_cloud = False
        self.button_states = {"accel": False, "brake": False, "nitrous": False, "handbrake": False}
        self.accel_sensitivity = 1.2  # Increase sensitivity for acceleration
        self.brake_sensitivity = 1.1  # Increase sensitivity for braking

    def handle_input(self):
        # Handle controller input and process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                is_pressed = event.type == pygame.KEYDOWN
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.button_states["accel"] = is_pressed
                    print(f"Accelerate {'pressed' if is_pressed else 'released'}")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.button_states["brake"] = is_pressed
                    print(f"Brake {'pressed' if is_pressed else 'released'}")
                elif event.key == pygame.K_n:
                    self.button_states["nitrous"] = is_pressed
                    print(f"Nitrous {'pressed' if is_pressed else 'released'}")
                elif event.key == pygame.K_SPACE:
                    self.button_states["handbrake"] = is_pressed
                    print(f"Handbrake {'pressed' if is_pressed else 'released'}")

    def detect_game(self):
        # Get the title of the active window
        hwnd = win32gui.GetForegroundWindow()
        if hwnd == 0:
            self.game_detected = None
            return
        
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid <= 0:
            # If pid is invalid, skip processing
            self.game_detected = None
            return
        
        try:
            # Get the process name
            process = psutil.Process(pid)
            process_name = process.name().lower()
            window_title = win32gui.GetWindowText(hwnd)

            # Detect if the active window is a known car game or a cloud platform
            if "forza" in window_title.lower() or "need for speed" in window_title.lower():
                self.game_detected = "Forza or Need for Speed"
                self.is_cloud = False
            elif "chrome" in process_name or "firefox" in process_name or "msedge" in process_name:
                # Check if using cloud gaming
                if "xbox" in window_title.lower() or "nvidia" in window_title.lower():
                    self.is_cloud = True
                    self.game_detected = "Cloud Gaming (Xbox/Nvidia)"
                else:
                    self.is_cloud = False
                    self.game_detected = None
            else:
                # Add other games or cloud platforms as needed
                self.is_cloud = False
                self.game_detected = None
        except psutil.NoSuchProcess:
            self.game_detected = None
            self.is_cloud = False

    def update(self):
        # Detect what game is being played
        self.detect_game()

    def draw(self, window):
        # Fill the screen with a color (black in this case)
        window.fill((0, 0, 0))

        # Render the ASCII art "Cruise Control"
        font = pygame.font.SysFont('Courier', 18)  # Monospaced font for ASCII art
        y_offset = 50  # Adjust this to properly fit the art in the window
        color_toggle = True
        for line in cruise_control_ascii.splitlines():
            # Alternate between purple and green for each line of ASCII art
            text_surface = font.render(line, True, (128, 0, 128) if color_toggle else (0, 255, 0))
            window.blit(text_surface, (20, y_offset))  # Adjust position as necessary
            y_offset += 30
            color_toggle = not color_toggle

        # Display game detection status
        font = pygame.font.Font(None, 36)
        if self.game_detected:
            text_surface = font.render(f"Detected Game: {self.game_detected}", True, (255, 255, 255))
            window.blit(text_surface, (20, 300))

        if self.is_cloud:
            cloud_text = font.render("Playing on Cloud Gaming", True, (255, 255, 0))
            window.blit(cloud_text, (20, 340))

    def run(self):
        # Start the main game loop
        while self.running:
            # Handle input
            self.handle_input()

            # Update the game state
            self.update()

            # Draw the updated state
            self.draw(win)

            # Update the display
            pygame.display.update()

            # Wait for the next frame
            clock.tick(60)

# Create a Game instance and run the game loop
game = Game()
game.run()

# Quit pygame
pygame.quit()
