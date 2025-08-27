"""
Human-like retry logic for failed clicks
"""
import asyncio
import random
import pyautogui

async def human_click_with_retry(page, element, session_id: str, max_retries: int = 3):
    """
    Human-like click with retry logic - like when humans try again after failed clicks
    """
    for attempt in range(max_retries):
        try:
            # Check if element is still attached to DOM
            is_attached = await element.evaluate("element => element.isConnected")
            if not is_attached:
                print(f"[{session_id}] Element disconnected, finding new one...")
                return False
            
            # Get element position
            box = await element.bounding_box()
            if not box:
                print(f"[{session_id}] Element not visible, skipping...")
                return False
            
            # Human-like approach: hover first, then click
            center_x = box['x'] + box['width'] / 2
            center_y = box['y'] + box['height'] / 2
            
            # Add slight randomness to click position (humans don't click exact center)
            x_offset = random.uniform(-0.2, 0.2) * box['width']
            y_offset = random.uniform(-0.2, 0.2) * box['height']
            
            target_x = center_x + x_offset
            target_y = center_y + y_offset
            
            # Hover first (humans often do this)
            print(f"[{session_id}] 🎯 Attempt {attempt + 1}: Hovering then clicking...")
            await element.hover(timeout=5000)
            await asyncio.sleep(random.uniform(0.5, 1.2))
            
            # Try different click strategies based on attempt
            if attempt == 0:
                # First attempt: Normal click
                await element.click(timeout=8000)
                
            elif attempt == 1:
                # Second attempt: Force click with scroll into view
                print(f"[{session_id}] 🎯 Scrolling element into view and force clicking...")
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(random.uniform(0.3, 0.8))
                await element.click(force=True, timeout=8000)
                
            elif attempt == 2:
                # Third attempt: JavaScript click + mouse jitter
                print(f"[{session_id}] 🎯 Using JavaScript click with mouse jitter...")
                
                # Small mouse jitter like frustrated human
                current_x, current_y = pyautogui.position()
                for _ in range(3):
                    jitter_x = current_x + random.randint(-10, 10)
                    jitter_y = current_y + random.randint(-10, 10)
                    pyautogui.moveTo(jitter_x, jitter_y, duration=0.1)
                    await asyncio.sleep(0.1)
                
                # Move to target and click
                pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.3, 0.7))
                await asyncio.sleep(random.uniform(0.2, 0.5))
                
                # JavaScript click as backup
                await element.evaluate("element => element.click()")
            
            # Wait a moment to see if click worked
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
            print(f"[{session_id}] ✅ Click successful on attempt {attempt + 1}")
            return True
            
        except Exception as e:
            print(f"[{session_id}] ❌ Click attempt {attempt + 1} failed: {str(e)[:50]}...")
            
            if attempt < max_retries - 1:
                # Human-like frustration behavior
                wait_time = random.uniform(1.5, 3.0) * (attempt + 1)  # Longer waits as frustration grows
                print(f"[{session_id}] 😤 Human-like pause ({wait_time:.1f}s) before retry...")
                
                # Small mouse movement like frustrated human
                current_x, current_y = pyautogui.position()
                pyautogui.moveTo(
                    current_x + random.randint(-20, 20), 
                    current_y + random.randint(-20, 20), 
                    duration=0.3
                )
                
                await asyncio.sleep(wait_time)
            else:
                print(f"[{session_id}] 😡 All click attempts failed, giving up...")
    
    return False

async def smart_element_finder(page, selectors: list, session_id: str, timeout: int = 10000):
    """
    Find elements with multiple fallback strategies like humans do
    """
    print(f"[{session_id}] 🔍 Smart element search with {len(selectors)} strategies...")
    
    # Strategy 1: Try each selector individually
    for i, selector in enumerate(selectors):
        try:
            element = await page.wait_for_selector(selector, timeout=timeout // len(selectors))
            if element and await element.is_visible():
                print(f"[{session_id}] ✅ Found element with strategy {i+1}: {selector[:30]}...")
                return element
        except:
            continue
    
    # Strategy 2: Look for any clickable element (like humans browsing)
    try:
        print(f"[{session_id}] 🎯 Trying clickable element fallback...")
        clickable_selectors = [
            "a[href*='article']", "a[href*='news']", "a[href*='story']",
            ".article-link", ".news-link", ".story-link", 
            "article a", ".post-title a", "h1 a", "h2 a", "h3 a"
        ]
        
        for selector in clickable_selectors:
            elements = await page.query_selector_all(selector)
            visible_elements = []
            
            for elem in elements[:5]:  # Check first 5 elements
                try:
                    if await elem.is_visible():
                        visible_elements.append(elem)
                except:
                    continue
            
            if visible_elements:
                chosen = random.choice(visible_elements)
                print(f"[{session_id}] ✅ Found clickable fallback: {selector}")
                return chosen
                
    except Exception as e:
        print(f"[{session_id}] ⚠️ Fallback search failed: {e}")
    
    return None

async def intelligent_page_wait(page, session_id: str, expected_change: str = "navigation"):
    """
    Wait for page changes intelligently like humans do
    """
    print(f"[{session_id}] ⏳ Waiting for {expected_change}...")
    
    if expected_change == "navigation":
        # Wait for URL change or new content
        try:
            original_url = page.url
            
            # Wait up to 10 seconds for URL change
            for _ in range(20):
                await asyncio.sleep(0.5)
                if page.url != original_url:
                    print(f"[{session_id}] ✅ Navigation detected: {page.url[:50]}...")
                    await page.wait_for_load_state('load', timeout=10000)
                    return True
            
            # If no URL change, wait for content changes
            print(f"[{session_id}] 🔄 No navigation, checking for content changes...")
            await page.wait_for_load_state('domcontentloaded', timeout=5000)
            return True
            
        except Exception as e:
            print(f"[{session_id}] ⚠️ Page wait timeout: {str(e)[:50]}...")
            return False
    
    return True
