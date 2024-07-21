import cv2
import numpy as np
import math
import csv

class AtomicStructureVisualizer:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def find_element_properties(self, atomic_number):
        with open(self.csv_file, mode='r', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['atomic_number']) == atomic_number:
                    mp = float(row['melting_point']) if row['melting_point'] else ''
                    return {
                        'name': row['name'],
                        'atomic_number': int(row['atomic_number']),
                        'symbol': row['symbol'],
                        'atomic_weight': float(row['atomic_weight']),
                        'appearance': row['appearance'],
                        'group_block': row['group_block'],
                        'element_category': row['element_category'],
                        'electron_configuration': row['electron_configuration'],
                        'melting_point': mp,
                        'boiling_point': float(row['boiling_point']) if row['boiling_point'] else '',
                        'oxidation_states': row['oxidation_states']
                    }
        return None


    def draw_wrapped_text(self,image, text, position, font, font_scale, color, thickness, wrap_width):
    
        x, y = position
        words = text.split(' ')
        line = ''
        lines = []

        for word in words:
            # Add word to the line
            test_line = line + word + ' '
            (test_width, _), _ = cv2.getTextSize(test_line, font, font_scale, thickness)

            # Check if the line width exceeds the wrap width
            if test_width > wrap_width:
                lines.append(line)
                line = word + ' '
            else:
                line = test_line

        # Add the last line
        lines.append(line)

        # Draw each line on the image
        for line in lines:
            cv2.putText(image, line, (x, y), font, font_scale, color, thickness)
            y += int(cv2.getTextSize(line, font, font_scale, thickness)[0][1] * 2)
        return y 

    def draw_atom(self, image, center_x, center_y, nucleus_radius, electron_orbit_radius, element_properties):
        # Define colors
        black = (0, 0, 0)
        blue = (255, 0, 0)
        red = (0, 0, 255)
        
        # Draw the nucleus
        cv2.circle(image, (center_x, center_y), nucleus_radius, (51, 87, 255), -1)
        
        # Number of electrons in each shell
        electron_in_shells = [2, 8, 8, 18, 18, 32]

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
                cv2.circle(image, (electron_x, electron_y), 10, (175, 249, 12), -1)

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
        wrap_width = 600 
        for i, prop in enumerate(properties_text):
            # cv2.putText(image, prop, (prop_start_x, prop_start_y + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, black, 2)
            prop_start_y = self.draw_wrapped_text(image, prop, (prop_start_x, prop_start_y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, black, 1, wrap_width)

    def visualize_element(self, atomic_number):
        # Create a blank white image
        image = np.ones((700, 1400, 3), np.uint8) * 255

        # Find element properties based on atomic number
        element_properties = self.find_element_properties(atomic_number)

        if element_properties:
            # Set the center for the atom diagram
            center_x, center_y = 300, 300
            nucleus_radius = 20
            electron_orbit_radius = 40

            # Draw the atom
            self.draw_atom(image, center_x, center_y, nucleus_radius, electron_orbit_radius, element_properties)

            # Display the image
            cv2.imshow("Atomic Structure", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f"Element with atomic number {atomic_number} not found in the CSV file.")

def main(atomic_number):

    # CSV file path containing periodic elements data
    csv_file = 'periodic_table.csv'

    # Create an instance of the AtomicStructureVisualizer class
    visualizer = AtomicStructureVisualizer(csv_file)

    # Example usage: Visualize element with atomic number 15
    # atomic_number = 15
    visualizer.visualize_element(atomic_number)

# main(15)