# scrape.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def test_depop_access():
    url = "https://www.depop.com/search/?q=birkenstock+clogs&conditions=brand_new&brands=353"
    
    try:        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = context.new_page()
            
            print("Loading page...")
            response = page.goto(url, timeout=30000, wait_until='domcontentloaded')
            
            if response and response.status == 200:
                print("Successfully loaded page!")
                
                time.sleep(3)

                try:
                    page.wait_for_selector('a[href*="/products/"]', timeout=10000)
                    
                    print("Scrolling to load more products...")
                    previous_count = 0
                    scroll_attempts = 0
                    max_scrolls = 20 
                    
                    while scroll_attempts < max_scrolls:
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(2) 
                        
                        products = page.query_selector_all('a[href*="/products/"]')
                        current_count = len(products)
                        
                        print(f"Scroll {scroll_attempts + 1}: Found {current_count} products")
                        
                        if current_count == previous_count:
                            print("No new products loaded, reached end of results")
                            break
                        
                        previous_count = current_count
                    
                    print(f"\nTotal products found: {len(products)}")
                    return True
                    
                except Exception as e:
                    print(f"Could not find product listings: {e}")
                    return True
                    
            else:
                print(f"Failed to access - Status code: {response.status if response else 'No response'}")
                return False
                
            browser.close()
            
    except Exception as e:
        print(f"Browser automation failed: {e}")
        return False

test_depop_access()