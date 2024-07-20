import cv2
import numpy as np
import math
import csv

def draw_atom(image, center_x, center_y, nucleus_radius, electron_orbit_radius, element_properties):
    # Define colors
    black = (0, 0, 0)
    blue = (255, 0, 0)
    red = (0, 0, 255)
    
    # Draw the nucleus
    cv2.circle(image, (center_x, center_y), nucleus_radius, red, -1)
    
    # Number of electrons in each shell
    electron_in_shells = [2, 8, 18, 32, 32, 18, 8]

    # Draw electron orbits
    total_electrons = element_properties['atomic_number']
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
        f"Element: {element_properties['name']}",
        f"Atomic Number: {element_properties['atomic_number']}",
        f"Symbol: {element_properties['symbol']}",
        f"Atomic Weight: {element_properties['atomic_weight']}",
        f"Appearance: {element_properties['appearance']}",
        f"Group Block: {element_properties['group_block']}",
        f"Element Category: {element_properties['element_category']}",
        f"Electron Configuration: {element_properties['electron_configuration']}",
        f"Melting Point: {element_properties['melting_point']}",
        f"Boiling Point: {element_properties['boiling_point']}",
        f"Oxidation States: {element_properties['oxidation_states']}"
    ]

    # Set starting coordinates for properties text
    prop_start_x, prop_start_y = 600, 100

    for i, prop in enumerate(properties_text):
        cv2.putText(image, prop, (prop_start_x, prop_start_y + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, black, 2)

def find_element_properties(atomic_number, csv_file):
    with open(csv_file, mode='r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['atomic_number']) == atomic_number:
                return {
                    'name': row['name'],
                    'atomic_number': int(row['atomic_number']),
                    'symbol': row['symbol'],
                    'atomic_weight': float(row['atomic_weight']),
                    'appearance': row['appearance'],
                    'group_block': row['group_block'],
                    'element_category': row['element_category'],
                    'electron_configuration': row['electron_configuration'],
                    'melting_point': float(row['melting_point']),
                    'boiling_point': float(row['boiling_point']),
                    'oxidation_states': row['oxidation_states']
                }
    return None

# Create a blank white image
image = np.ones((600, 1000, 3), np.uint8) * 255

# Prompt for atomic number
atomic_number = int(input("Enter the atomic number: "))

# CSV file path containing periodic elements data
csv_file = 'periodic_table.csv'

# Find element properties based on atomic number
element_properties = find_element_properties(atomic_number, csv_file)

if element_properties:
    # Set the center for the atom diagram
    center_x, center_y = 300, 300
    nucleus_radius = 25
    electron_orbit_radius = 50

    # Draw the atom
    draw_atom(image, center_x, center_y, nucleus_radius, electron_orbit_radius, element_properties)

    # Save the image
    output_image_path = 'atomic_diagram.png'
    cv2.imwrite(output_image_path, image)
    print(f"Image saved as {output_image_path}.")
else:
    print(f"Element with atomic number {atomic_number} not found in the CSV file.")
