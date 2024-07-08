import cv2
import numpy as np

# Create a blank white image
image = np.ones((600, 1000, 3), np.uint8) * 255

# Define colors
black = (0, 0, 0)
blue = (255, 0, 0)
red = (0, 0, 255)

# Set the center for the atom diagram
center_x, center_y = 300, 300
nucleus_radius = 25
electron_orbit_radius = 50

# Draw the nucleus
cv2.circle(image, (center_x, center_y), nucleus_radius, red, -1)

# Draw electron orbits
for i in range(1, 4):  # Drawing 3 orbits for simplicity
    orbit_radius = electron_orbit_radius * i
    cv2.circle(image, (center_x, center_y), orbit_radius, black, 1)
# Draw electrons
electrons = [
    (center_x + electron_orbit_radius, center_y),
    (center_x - electron_orbit_radius, center_y),
    (center_x, center_y + electron_orbit_radius),
    (center_x, center_y - electron_orbit_radius),
    (center_x + int(electron_orbit_radius * 1.5), center_y + int(electron_orbit_radius * 1.5)),
    (center_x - int(electron_orbit_radius * 1.5), center_y - int(electron_orbit_radius * 1.5))
]

for electron in electrons:
    cv2.circle(image, electron, 10, blue, -1)

# Display properties of the element on the right
properties = [
    "Element: Hydrogen",
    "Atomic Number: 1",
    "Symbol: H",
    "Atomic Mass: 1.008",
    "Electrons: 1",
    "Protons: 1",
    "Neutrons: 0",
    "Electron Configuration: 1s1"
]
# Set starting coordinates for properties text
prop_start_x, prop_start_y = 600, 100

for i, prop in enumerate(properties):
    cv2.putText(image, prop, (prop_start_x, prop_start_y + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, black, 2)

# Display the image
cv2.imshow("Atomic Diagram and Properties", image)
cv2.waitKey(0)
cv2.destroyAllWindows()