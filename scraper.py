from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re

class IMDbScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Setup WebDriver
        self.driver = webdriver.Chrome(
            options=chrome_options
        )
        
        self.url = "https://www.imdb.com/chart/top/"

    def scroll_and_load_page(self):
        """
        Simulate scrolling to trigger lazy loading of content
        """
        try:
            self.driver.get(self.url)
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ipc-metadata-list"))
            )
            time.sleep(2)

        except Exception as e:
            print(f"Scrolling error: {e}")
            raise
    
    def get_director(self, item):
        """
        Click to open the movie's modal and extract the director's name
        """
        try:
            # Locate the button to open the modal (the button might be an anchor tag or a button)
            modal_button = item.find_element(By.CSS_SELECTOR, "div.cli-post-element")
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(modal_button))
        
            try:
                modal_button.click()
            except:
                # If it's not clickable, scroll it into view and then click
                self.driver.execute_script("arguments[0].scrollIntoView(true);", modal_button)
                time.sleep(1)  # Wait a bit to ensure the element is fully in view
                modal_button.click()
            
            # Wait for modal to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-1582ce06-3"))
            )        

            # Extract the director's name from the modal
            director_elems = self.driver.find_elements(By.CSS_SELECTOR, "div[data-testid='p_ct_dr'] a")
            directors = [director_elem.get_attribute('textContent') for director_elem in director_elems]
            
            # Close the modal
            self.driver.find_element(By.CSS_SELECTOR, "div.ipc-promptable-base__close").click()  # Adjust if modal close button has different class

            return directors
        
        except Exception as e:
            print(f"Could not retrieve director info: {e}")
            return "Unknown"

    def scrape_top_250(self):
        try:
            self.driver.get(self.url)
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ipc-metadata-list"))
            )
            time.sleep(2)

            # Find all movie list items
            movie_items = self.driver.find_elements(By.CSS_SELECTOR, "ul.ipc-metadata-list li")
            
            movies = []
            for index, item in enumerate(movie_items[:250], 1):
                try:
                    directors = self.get_director(item)
                    
                    title_elem = item.find_element(By.CSS_SELECTOR, "h3.ipc-title__text")
                    title = re.sub(r'^\d+\.\s*', '', title_elem.text.strip())
     
                    metadata_items = item.find_elements(By.CSS_SELECTOR, "span.cli-title-metadata-item")
                    
                    year = metadata_items[0].text.strip() if metadata_items else 'N/A'

                    
                    movie_info = {
                        'title': title,
                        'year': year,
                        'directors': directors
                    }
                    
                    movies.append(movie_info)
                    
                except Exception as e:
                    print(f"Could not parse movie at index {index}: {e}")

            return movies

        except Exception as e:
            print(f"Scraping failed: {e}")
            raise
        finally:
            self.driver.quit()

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass