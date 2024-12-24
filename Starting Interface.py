import pygame
import pygame_menu

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

# Load assets (replace these with actual file paths for your assets)
bg = pygame.image.load('bg.png')  # Background image
bg = pygame.transform.scale(bg, (1000, 1000))

# Function to start the game
def start_the_game():
    print("Starting the game...")
    # Your game logic goes here
    # You can move to the next part of the game or game loop

# Function to exit the game
def exit_game():
    pygame.quit()
    quit()

# Create the main menu
def create_menu():
    menu = pygame_menu.Menu('Welcome to Space Invaders', 1000, 1000,
                            theme=pygame_menu.themes.THEME_DARK)

    # Set background for the menu using theme (background image)
    menu.get_theme().background_color = (0, 0, 0)  # Optional if you want a solid color
    # You can also set other properties for the background here if needed

    # Add start button
    menu.add.button('Play', start_the_game)

    # Add exit button
    menu.add.button('Quit', exit_game)

    # Display the menu with background image (by drawing it separately)
    while True:
        screen.blit(bg, (0, 0))  # Draw the background image
        menu.update(pygame.event.get())  # Update the menu
        menu.draw(screen)  # Draw the menu
        pygame.display.update()  # Update the display

# Call the menu function
create_menu()

# Main game loop (can be replaced with your actual game loop)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)  # Limit to 60 FPS
