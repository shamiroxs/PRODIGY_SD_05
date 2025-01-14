import pygame
import sys
import csv
import time
from bs4 import BeautifulSoup
import requests
import os

# Initialize Pygame
pygame.init()

# Screen Dimensions and Colors
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GREY = (105, 105, 105)

# Fonts
TITLE_FONT = pygame.font.Font(None, 64)
TEXT_FONT = pygame.font.Font(None, 36)
TITLE_HEIGHT = 124

# File Paths
URL_FILE = "url.txt"
OUTPUT_FILE = "information.txt"

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Web Scraping")

# Scroll offset to handle mouse wheel scrolling
scroll_offset = 0

def load_url():
    """Load the URL from the 'url.txt' file."""
    try:
        with open(URL_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def display_loading(blink):
    """Display a blinking 'Loading...' text on the screen."""
    screen.fill(BLACK)
    title = TITLE_FONT.render("Loading...", True, CYAN if blink else GREY)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(title, title_rect)
    pygame.display.flip()

def scrape_products(url):
    """Scrape product data from the given URL and save it to a CSV file."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        )
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    products = []
    product_containers = soup.find_all("div", class_="s-widget-container")[2:7]

    for product in product_containers:
        try:
            # Extract product title
            title_element = product.find(
                "h2", class_="a-size-base-plus a-spacing-none a-color-base a-text-normal"
            )
            title = title_element.text.strip() if title_element else "N/A"
            
            # Extract product price
            price_element = product.find("span", class_="a-offscreen")
            price = price_element.text.strip() if price_element else "N/A"
            
            # Extract product rating
            rating_element = product.find("span", class_="a-icon-alt")
            rating = rating_element.text.strip() if rating_element else "N/A"

            products.append((title, price, rating))
        except Exception as e:
            print(f"Error extracting product data: {e}")
            continue
    
    return products

def save_to_csv(products):
    """Save scraped product data to 'information.txt'."""
    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Rating"])
        writer.writerows(products)

def wrap_text(text, font, max_width):
    """Wrap the text to fit within the given max_width."""
    words = text.split(" ")
    lines = []
    current_line = words[0]

    for word in words[1:]:
        # Check if adding the word would exceed the max_width
        test_line = current_line + " " + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)  # Add the last line
    return lines

def display_results(products):
    """Display the scraped results on the screen with scroll functionality."""
    screen.fill(BLACK)
    y_offset = 100 + scroll_offset  # Add scroll offset to the vertical position

    # Display each product's title, price, and rating with labels
    for i, product in enumerate(products, start=1):
        # Display the "PRODUCT X" label
        label_text = f"PRODUCT {i}"
        label_surface = TEXT_FONT.render(label_text, True, WHITE)
        screen.blit(label_surface, (50, y_offset))
        y_offset += 40

        # Wrap and display the title, price, and rating for each product
        title_lines = wrap_text("Title: " + product[0], TEXT_FONT, WIDTH - 100)
        price_lines = wrap_text("Price: " + product[1], TEXT_FONT, WIDTH - 100)
        rating_lines = wrap_text("Rating: " + product[2], TEXT_FONT, WIDTH - 100)
        
        # Display the title
        for line in title_lines:
            title_surface = TEXT_FONT.render(line, True, WHITE)
            screen.blit(title_surface, (50, y_offset))
            y_offset += 40
        
        # Display the price
        for line in price_lines:
            price_surface = TEXT_FONT.render(line, True, WHITE)
            screen.blit(price_surface, (50, y_offset))
            y_offset += 40
        
        # Display the rating
        for line in rating_lines:
            rating_surface = TEXT_FONT.render(line, True, WHITE)
            screen.blit(rating_surface, (50, y_offset))
            y_offset += 40

        # Add some spacing between products
        y_offset += 20

    # Draw the '>' button with hover effect
    button_rect = pygame.Rect(WIDTH - 50, 10, 40, 40)  # Button at top-right
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Check if the mouse is hovering over the button
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, GREY, button_rect)  # Cyan button on hover
    else:
        pygame.draw.rect(screen, CYAN, button_rect)  # Grey button by default
    
    # Draw the '>' text in the button
    button_text = TEXT_FONT.render(">", True, BLACK)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    
    pygame.display.flip()

    return button_rect  # Return the button rect for click detection

def main():
    """Main function for scraping and displaying product data."""
    global scroll_offset
    clock = pygame.time.Clock()
    blink = True
    url = load_url()

    if not url:
        print("Error: 'url.txt' not found or empty.")
        sys.exit()

    # Remove existing CSV file if it exists
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    # Display loading screen while scraping
    loading = True
    start_time = time.time()

    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display loading animation
        if time.time() - start_time > 0.5:
            blink = not blink
            start_time = time.time()

        display_loading(blink)

        # Perform scraping in the background
        products = scrape_products(url)
        if products:
            save_to_csv(products)
            loading = False

    # Display results after scraping is complete
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse wheel scroll
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_offset += 30  # Scroll up by 30 pixels
                elif event.button == 5:  # Scroll down
                    scroll_offset -= 30  # Scroll down by 30 pixels

        # Display results and '>' button
        button_rect = display_results(products)
        
        # Check if the '>' button is clicked to close the program
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                return  "user_keyword"
        
        clock.tick(30)

if __name__ == "__main__":
    main()

