import pygame
import cv2
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interactive Periodic Table")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)

# Elements (simplified example)
elements = [
    {"symbol": "H", "number": 1, "position": (50, 50), "color": BLUE},
    {"symbol": "He", "number": 2, "position": (150, 50), "color": BLUE},
    # Add more elements as needed
]

# Function to draw elements
def draw_elements():
    for element in elements:
        pygame.draw.rect(screen, element["color"], (*element["position"], 100, 100))
        text = font.render(element["symbol"], True, WHITE)
        screen.blit(text, (element["position"][0] + 20, element["position"][1] + 30))

# Function to show atomic structure using OpenCV
def show_atomic_structure(element):
    # Create a blank image
    img = np.zeros((800, 800, 3), dtype=np.uint8)
    
    # Define nucleus position
    nucleus_position = (400, 400)
    
    # Example radii and angles for electrons (simplified)
    radii = [100, 200, 300]
    angles = [
        [0, 180],
        [i * 45 for i in range(8)],
        [0]
    ]
    
    # Draw nucleus
    cv2.circle(img, nucleus_position, 30, RED, -1)
    cv2.putText(img, element["symbol"], (nucleus_position[0] - 15, nucleus_position[1] + 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)
    
    # Draw electrons in each shell
    for shell in range(len(radii)):
        num_electrons = len(angles[shell])
        for i in range(num_electrons):
            angle = angles[shell][i]
            x = nucleus_position[0] + int(radii[shell] * np.cos(np.radians(angle)))
            y = nucleus_position[1] + int(radii[shell] * np.sin(np.radians(angle)))
            cv2.circle(img, (x, y), 10, WHITE, -1)
        cv2.ellipse(img, nucleus_position, (radii[shell], radii[shell]), 0, 0, 360, (200, 200, 200), 2)
    
    # Show image in OpenCV window
    cv2.imshow(f"Atomic Structure of {element['symbol']}", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Main loop
running = True
while running:
    screen.fill(BLACK)
    draw_elements()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for element in elements:
                rect = pygame.Rect(*element["position"], 100, 100)
                if rect.collidepoint(mouse_pos):
                    show_atomic_structure(element)
    
    pygame.display.flip()

pygame.quit()
