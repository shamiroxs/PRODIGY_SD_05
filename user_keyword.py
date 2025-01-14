import pygame
import sys
from urllib.parse import quote_plus  # To handle URL formatting

# Initialize Pygame
pygame.init()

# Screen Dimensions and Colors
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
HOVER_COLOR = (0, 200, 200)
GREY = (50, 50, 50)

# Fonts
TITLE_FONT = pygame.font.Font(None, 64)
TEXT_FONT = pygame.font.Font(None, 36)
INPUT_FONT = pygame.font.Font(None, 32)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Webscraping - Keyword Input")

# UI Constants
INPUT_WIDTH = 400
INPUT_HEIGHT = 50
BUTTON_WIDTH = 60
BUTTON_HEIGHT = 50
PADDING = 10

# Input Box
input_box = pygame.Rect((WIDTH - INPUT_WIDTH - BUTTON_WIDTH - PADDING) // 2, 
                        HEIGHT // 2 - INPUT_HEIGHT // 2, 
                        INPUT_WIDTH, 
                        INPUT_HEIGHT)

# Button
button_rect = pygame.Rect(input_box.right + PADDING, 
                          input_box.top, 
                          BUTTON_WIDTH, 
                          BUTTON_HEIGHT)

# Variable to store user input
user_input = ""


def draw_ui():
    """Draw the user interface."""
    screen.fill(BLACK)

    # Draw Title
    title_surface = TITLE_FONT.render("Product name?", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    # Draw Input Box
    pygame.draw.rect(screen, GREY, input_box, border_radius=5)
    text_surface = INPUT_FONT.render(user_input, True, WHITE)
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

    # Draw Button
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HOVER_COLOR, button_rect, border_radius=5)
    else:
        pygame.draw.rect(screen, CYAN, button_rect, border_radius=5)

    # Draw '>' Text on Button
    button_text_surface = INPUT_FONT.render(">", True, BLACK)
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)
    screen.blit(button_text_surface, button_text_rect)


def save_url_to_file(keyword):
    """Generate the Amazon search URL and save it to a file."""
    base_url = "https://www.amazon.com/s?k="
    formatted_keyword = quote_plus(keyword)  # Replace spaces with '+'
    full_url = base_url + formatted_keyword

    with open("url.txt", "w") as file:
        file.write(full_url)
    print(f"URL saved: {full_url}")


def main():
    """Main loop for the keyword input screen."""
    global user_input
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]  # Remove last character
                elif event.key == pygame.K_RETURN:
                    if user_input.strip():  # Save URL if input is not empty
                        save_url_to_file(user_input.strip())
                        return "scrape"
                elif event.unicode.isprintable():
                    user_input += event.unicode  # Add character to input

            # Handle mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    if user_input.strip():  # Save URL if input is not empty
                        save_url_to_file(user_input.strip())
                        return

        # Draw UI
        draw_ui()

        # Update display
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()

