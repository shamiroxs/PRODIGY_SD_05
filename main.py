import user_keyword
import scrape

def main():
    """Main function to run the Guessing Game."""
    current_screen = "user_keyword"  
    
    while True:
        if current_screen == "user_keyword":
            current_screen = user_keyword.main()
        
        elif current_screen == "scrape":
            current_screen = scrape.main()
        

if __name__ == "__main__":
    main()
