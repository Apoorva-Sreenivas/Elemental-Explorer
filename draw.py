import cv2
import numpy as np
import math

def draw_atom(image, center_x, center_y, nucleus_radius, electron_orbit_radius, element_properties):
    # Define colors
    black = (0, 0, 0)
    blue = (255, 0, 0)
    red = (0, 0, 255)
    
    # Draw the nucleus
    cv2.circle(image, (center_x, center_y), nucleus_radius, red, -1)
    
    # Number of electrons in each shell
    electron_in_shells = [2, 8, 8, 18, 18, 32]

    # Draw electron orbits
    total_electrons = element_properties['Electrons']
    current_electron_count = 0

    for i in range(len(electron_in_shells)):
        if current_electron_count >= total_electrons:
            break
        
        orbit_radius = electron_orbit_radius * (i + 1)
        cv2.circle(image, (center_x, center_y), orbit_radius, black, 1)
        
        electrons_in_current_shell = min(electron_in_shells[i], total_electrons - current_electron_count)
        current_electron_count += electrons_in_current_shell
        
        # Draw electrons in the current shell
        angle_step = 360 / electrons_in_current_shell
        for electron_index in range(electrons_in_current_shell):
            angle = angle_step * electron_index
            radian = math.radians(angle)
            electron_x = int(center_x + orbit_radius * math.cos(radian))
            electron_y = int(center_y + orbit_radius * math.sin(radian))
            cv2.circle(image, (electron_x, electron_y), 10, blue, -1)

    # Display properties of the element on the right
    properties_text = [
        f"Element: {element_properties['Element']}",
        f"Atomic Number: {element_properties['Atomic Number']}",
        f"Symbol: {element_properties['Symbol']}",
        f"Atomic Mass: {element_properties['Atomic Mass']}",
        f"Electrons: {element_properties['Electrons']}",
        f"Protons: {element_properties['Protons']}",
        f"Neutrons: {element_properties['Neutrons']}",
        f"Electron Configuration: {element_properties['Electron Configuration']}"
    ]
    # Set starting coordinates for properties text
    prop_start_x, prop_start_y = 600, 100

    for i, prop in enumerate(properties_text):
        cv2.putText(image, prop, (prop_start_x, prop_start_y + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, black, 2)

# Create a blank white image
image = np.ones((600, 1000, 3), np.uint8) * 255

# Element properties
element_properties = {
    'Element': 'Sodium',
    'Atomic Number': 11,
    'Symbol': 'Na',
    'Atomic Mass': 22.9897,
    'Electrons': 11,
    'Protons': 11,
    'Neutrons': 12,
    'Electron Configuration': '1s2 2s2 2p6 3s1'
}




# Set the center for the atom diagram
center_x, center_y = 300, 300
nucleus_radius = 25
electron_orbit_radius = 50

# Draw the atom
draw_atom(image, center_x, center_y, nucleus_radius, electron_orbit_radius, element_properties)

# Display the image
cv2.imshow("Atomic Diagram and Properties", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
