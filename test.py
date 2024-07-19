import pygame
from clean_csv import scrub_to_csv as scrub
from details_class import main

pygame.init()

# Each element in order of name, atomic num, symbol, weight , col, row 
dataset = scrub()

fps = 60
WIDTH = 900
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Elemental Explorer')
timer = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 16)
midfont = pygame.font.Font('freesansbold.ttf', 28)
bigfont = pygame.font.Font('freesansbold.ttf', 36)

cols = 18
rows = 10

cell_width = WIDTH / cols
cell_height = HEIGHT / rows

highlight = False

colors = [('alkali metals', 'light blue'),
          ('mettaloids', 'yellow'),
          ('actinides', 'orange'),
          ('alkaline earth metals', 'red'),
          ('reactive nonmetals', 'cyan'),
          ('unknown properties', 'dark grey'),
          ('transition metals', 'purple'),
          ('post-transition metals', 'green'),
          ('noble gases', 'dark red'),
          ('lanthanides', 'light grey')]

groups = [[3, 11, 19, 37, 55, 87],
          [5, 14, 32, 33, 51, 52],
          [89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103],
          [4, 12, 20, 38, 56, 88],
          [1, 6, 7, 8, 9, 15, 16, 17, 34, 35, 53],
          [109, 110, 111, 112, 113, 114, 115, 116, 117, 118],
          [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 39, 40, 41, 42, 43, 44,
           45, 46, 47, 48, 72, 73, 74, 75, 76, 77, 78, 79, 80,
           104, 105, 106, 107, 108],
          [13, 31, 49, 50, 81, 82, 83, 84, 85],
          [2, 10, 18, 36, 54, 86],
          [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]]


def draw_screen(data):
    element_list = []

    for i in range(len(data)):
        elem = data[i]
        # name, atomic num, symbol, weight , col, row 

        for q in range(len(groups)):
            if int(elem[1]) in groups[q]:
                color = colors[q][1]

        if elem[4] < 3:
            x_pos = (elem[4] - 1) * cell_width
        else:
            x_pos = (elem[4] - 2) * cell_width

        y_pos = (elem[5] - 2) * cell_height

        # Manual code to shift the first elements of the actinoid and lathanoid series down a bit 
        if elem[4] == 4 and elem[5] in [7, 8]:
            x_pos = (elem[4] + 12) * cell_width
            y_pos = (elem[5] + 1) * cell_height

        box = pygame.draw.rect(screen, color, [x_pos, y_pos, cell_width - 4, cell_height - 4])

        # Silver frame around the box
        pygame.draw.rect(screen, 'silver', [x_pos - 2, y_pos - 2, cell_width, cell_height], 2)

        screen.blit(font.render(elem[1], True, 'black'), (x_pos + 5, y_pos + 5))
        screen.blit(font.render(elem[2], True, 'black'), (x_pos + 10, y_pos + 25))
        # Was returning i which is the index number and not the atomic number here
        # We are using this to draw the highlights not for the data access 
        element_list.append((box, (i, color)))

        # We add a direction explaining the lanthanoid and actinoid series that are at the bottom of the table 
        pygame.draw.rect(screen, 'white', [cell_width * 2 - 3, cell_height * 5 - 3, cell_width, 2 * cell_height], 3, 5)
        pygame.draw.rect(screen, 'white', [cell_width * 2 - 3, cell_height * 8 - 3, cell_width * 15, 2 * cell_height], 3, 5)
        pygame.draw.line(screen, 'white', (cell_width * 2 - 3, cell_height * 6), (cell_width * 2 - 3, cell_height * 9), 3)

    return element_list


def draw_highlight(stuff):
    classification = ''
    information = dataset[stuff[0]]
    for i in range(len(colors)):
        if colors[i][1] == stuff[1]:
            classification = colors[i][0]

    # Top rect 
    pygame.draw.rect(screen, 'light grey', [cell_width * 3, cell_height * 0.5, cell_width * 8, cell_height * 2], 0, 5)
    # Bottom rect 
    pygame.draw.rect(screen, 'black', [cell_width * 3, cell_height * 1.5, cell_width * 8, cell_height * 0.8], 0, 5)
    # Outline 
    pygame.draw.rect(screen, 'dark grey', [cell_width * 3, cell_height * 0.5, cell_width * 8, cell_height * 2], 8, 5)
    pygame.draw.rect(screen, stuff[1], [cell_width * 3, cell_height * 0.5, cell_width * 8, cell_height * 2], 5, 5)

    screen.blit(bigfont.render(information[1] + '-' + information[2], True, 'black'), (cell_width * 3 + 15, cell_height * 0.5 + 10))
    screen.blit(midfont.render(information[0], True, 'black'), (cell_width * 6 + 20, cell_height * 0.5 + 10))
    screen.blit(midfont.render(information[3], True, 'black'), (cell_width * 6 + 20, cell_height * 0.9 + 10))
    screen.blit(midfont.render(classification, True, stuff[1]), (cell_width * 3 + 20, cell_height * 1.5 + 10))


def draw_buttons():
    # Define button positions and dimensions
    button_radius = 15
    button_spacing = 10
    bottom_right_x = WIDTH - button_radius - 15  # Move buttons slightly to the right
    bottom_right_y = HEIGHT - button_radius - 20

    help_button_center = (bottom_right_x, bottom_right_y - (button_radius * 2 + button_spacing))
    search_button_center = (bottom_right_x, bottom_right_y)

    # Draw buttons
    pygame.draw.circle(screen, 'light grey', help_button_center, button_radius)
    pygame.draw.circle(screen, 'light grey', search_button_center, button_radius)
    pygame.draw.circle(screen, 'black', help_button_center, button_radius, 2)
    pygame.draw.circle(screen, 'black', search_button_center, button_radius, 2)

    # Render button symbols
    screen.blit(midfont.render('?', True, 'black'), (help_button_center[0] - 10, help_button_center[1] - 15))
    screen.blit(midfont.render('🔍', True, 'black'), (search_button_center[0] - 15, search_button_center[1] - 15))

    return pygame.Rect(help_button_center[0] - button_radius, help_button_center[1] - button_radius, button_radius * 2, button_radius * 2), \
           pygame.Rect(search_button_center[0] - button_radius, search_button_center[1] - button_radius, button_radius * 2, button_radius * 2)


def open_help_window():
    help_screen = pygame.display.set_mode([800, 800])
    pygame.display.set_caption('Help')
    running = True
    while running:
        help_screen.fill('white')

        # Instructions about the application
        help_text_lines = [
            "Welcome to Elemental Explorer!",
            "",
            "This application provides an interactive periodic table.",
            "You can view information about various elements by clicking on them.",
            "",
            "Features:",
            "- Displays elements with their names, symbols, and weights.",
            "- When you hover over an element, minimal information will be shown.",
            "- Click on the 'Help' button for instructions.",
            "- Click on the 'Search' button for searching elements.",
            "",
            "Element Classification Colors:",
            "- Alkali Metals: Light Blue",
            "- Metalloids: Yellow",
            "- Actinides: Orange",
            "- Alkaline Earth Metals: Red",
            "- Reactive Nonmetals: Cyan",
            "- Unknown Properties: Dark Grey",
            "- Transition Metals: Purple",
            "- Post-Transition Metals: Green",
            "- Noble Gases: Dark Red",
            "- Lanthanides: Light Grey",
            "",
            "Press ESC to close this window."
        ]

        # Render the help text
        for i, line in enumerate(help_text_lines):
            help_text = font.render(line, True, 'black')
            help_screen.blit(help_text, (20, 20 + i * 20))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()
    pygame.display.set_mode([WIDTH, HEIGHT])



def open_search_window():
    global selected_category
    search_screen = pygame.display.set_mode([1000, 700])
    pygame.display.set_caption('Search')
    font_small = pygame.font.Font(None, 24)
    font_large = pygame.font.Font(None, 30)
    
    categories = [
        ('Alkali Metals', [3, 11, 19, 37, 55, 87]),
        ('Metalloids', [5, 14, 32, 33, 51, 52]),
        ('Actinides', [89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103]),
        ('Alkaline Earth Metals', [4, 12, 20, 38, 56, 88]),
        ('Reactive Nonmetals', [1, 6, 7, 8, 9, 15, 16, 17, 34, 35, 53]),
        ('Unknown Properties', [109, 110, 111, 112, 113, 114, 115, 116, 117, 118]),
        ('Transition Metals', [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 39, 40, 41, 42, 43, 44,
                               45, 46, 47, 48, 72, 73, 74, 75, 76, 77, 78, 79, 80, 
                               104, 105, 106, 107, 108]),
        ('Post-Transition Metals', [13, 31, 49, 50, 81, 82, 83, 84, 85]),
        ('Noble Gases', [2, 10, 18, 36, 54, 86]),
        ('Lanthanides', [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71])
    ]
    
    selected_category = None  # Initialize selected_category
    
    running = True
    while running:
        search_screen.fill('white')

        # Render category buttons
        y_offset = 20
        category_buttons = []
        for category, elements in categories:
            button_rect = pygame.Rect(20, y_offset, 250, 40)
            pygame.draw.rect(search_screen, 'light grey', button_rect)
            pygame.draw.rect(search_screen, 'black', button_rect, 2)
            search_screen.blit(font_large.render(category, True, 'black'), (button_rect.x + 10, button_rect.y + 10))
            category_buttons.append((button_rect, elements))
            y_offset += 50

        # Display selected category elements
        if selected_category:
            y_offset = 20
            pygame.draw.rect(search_screen, 'light grey', [240, 20, 740, 660])
            pygame.draw.rect(search_screen, 'black', [240, 20, 740, 660], 2)
            elements_list = [elem for elem in dataset if int(elem[1]) in selected_category]
            elements_text = [f"{elem[1]} - {elem[2]} - {elem[3]}" for elem in elements_list]
            for i, text in enumerate(elements_text):
                search_screen.blit(font_small.render(text, True, 'black'), (250, y_offset + i * 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button_rect, elements in category_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        selected_category = elements  # Update the selected category
                        break

        pygame.display.flip()
    pygame.display.set_mode([WIDTH, HEIGHT])





run = True

while run:
    screen.fill('black')
    timer.tick(fps)
    elements = draw_screen(dataset)
    help_button, search_button = draw_buttons()  # Draw the buttons

    if highlight:
        draw_highlight(info)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check for button clicks
            if help_button.collidepoint(mouse_pos):
                open_help_window()
            elif search_button.collidepoint(mouse_pos):
                open_search_window()

            # Check for element clicks
            for element in elements:
                rect = element[0]
                if rect.collidepoint(mouse_pos):
                    atnum = int(dataset[element[1][0]][1])
                    main(atnum)

    mouse_pos = pygame.mouse.get_pos()
    highlight = False

    for e in range(len(elements)):
        if elements[e][0].collidepoint(mouse_pos):
            highlight = True
            info = elements[e][1]

    pygame.display.flip()

pygame.quit()
