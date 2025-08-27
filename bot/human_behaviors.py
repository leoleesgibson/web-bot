"""
Advanced human-like behaviors and wasted actions to avoid bot detection
"""
import asyncio
import random
import pyautogui

async def realistic_typing_with_mistakes(page, text: str, session_id: str):
    """Type text with realistic human mistakes and corrections"""
    print(f"[{session_id}] 🎭 Typing with human-like mistakes...")
    
    # 20% chance to make a typo
    if random.random() < 0.2:
        # Common typing mistakes
        mistakes = {
            'a': 's', 'e': 'r', 'i': 'o', 'o': 'p', 's': 'a', 
            'n': 'm', 't': 'y', 'r': 'e', 'u': 'i', 'h': 'g'
        }
        
        # Find a random position to make mistake
        mistake_pos = random.randint(0, len(text) - 1)
        original_char = text[mistake_pos].lower()
        
        if original_char in mistakes:
            # Type up to mistake position
            await page.keyboard.type(text[:mistake_pos])
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Make the mistake
            await page.keyboard.type(mistakes[original_char])
            await asyncio.sleep(random.uniform(0.2, 0.5))
            
            # Realize mistake (pause)
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Backspace to correct
            await page.keyboard.press('Backspace')
            await asyncio.sleep(random.uniform(0.1, 0.3))
            
            # Type correct character and continue
            await page.keyboard.type(text[mistake_pos:])
            return
    
    # Normal typing with natural pauses
    for char in text:
        await page.keyboard.type(char)
        # Vary typing speed (50-200ms per character)
        await asyncio.sleep(random.uniform(0.05, 0.2))
        
        # Occasional longer pauses (thinking)
        if random.random() < 0.1:
            await asyncio.sleep(random.uniform(0.5, 1.0))

async def random_mouse_movements(session_id: str, duration_seconds: int = 3):
    """Make random mouse movements like a human would"""
    print(f"[{session_id}] 🖱️ Making natural mouse movements...")
    
    end_time = asyncio.get_event_loop().time() + duration_seconds
    
    while asyncio.get_event_loop().time() < end_time:
        # Random small movements
        current_x, current_y = pyautogui.position()
        new_x = current_x + random.randint(-50, 50)
        new_y = current_y + random.randint(-30, 30)
        
        # Ensure we stay within screen bounds
        new_x = max(100, min(pyautogui.size().width - 100, new_x))
        new_y = max(100, min(pyautogui.size().height - 100, new_y))
        
        # Smooth movement
        pyautogui.moveTo(new_x, new_y, duration=random.uniform(0.5, 1.5))
        
        # Pause between movements
        await asyncio.sleep(random.uniform(0.8, 2.0))

async def wasted_click_actions(page, session_id: str):
    """Perform wasted clicking actions like humans do"""
    wasted_actions = [
        "check_scroll_bar",
        "click_empty_space", 
        "highlight_text",
        "right_click_context",
        "hover_elements"
    ]
    
    action = random.choice(wasted_actions)
    print(f"[{session_id}] 🎭 Performing wasted action: {action}")
    
    try:
        if action == "check_scroll_bar":
            # Hover over scroll bar area
            await page.mouse.move(
                pyautogui.size().width - 20, 
                random.randint(200, 600)
            )
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
        elif action == "click_empty_space":
            # Click on empty areas (margins, whitespace)
            viewport = await page.viewport_size()
            empty_areas = [
                (50, 50),  # Top-left corner
                (viewport['width'] - 50, 50),  # Top-right  
                (viewport['width'] // 2, viewport['height'] - 50),  # Bottom center
            ]
            x, y = random.choice(empty_areas)
            await page.mouse.click(x, y)
            await asyncio.sleep(random.uniform(0.5, 1.0))
            
        elif action == "highlight_text":
            # Try to highlight some text (may fail, that's okay)
            try:
                text_elements = await page.query_selector_all('p, h1, h2, h3, span')
                if text_elements:
                    element = random.choice(text_elements)
                    await element.click(click_count=3)  # Triple click to select
                    await asyncio.sleep(random.uniform(1.0, 2.0))
                    # Click elsewhere to deselect
                    await page.mouse.click(100, 100)
            except:
                pass
                
        elif action == "right_click_context":
            # Right click to open context menu, then click away
            try:
                await page.mouse.click(
                    random.randint(200, 600), 
                    random.randint(200, 400), 
                    button='right'
                )
                await asyncio.sleep(random.uniform(1.0, 2.0))
                # Click elsewhere to close context menu
                await page.mouse.click(100, 100)
            except:
                pass
                
        elif action == "hover_elements":
            # Hover over various elements without clicking
            try:
                elements = await page.query_selector_all('a, button, img')
                if elements:
                    for _ in range(random.randint(2, 4)):
                        element = random.choice(elements)
                        await element.hover()
                        await asyncio.sleep(random.uniform(0.8, 1.5))
            except:
                pass
                
    except Exception as e:
        print(f"[{session_id}] ⚠️ Wasted action failed: {e}")

async def human_like_page_exploration(page, session_id: str):
    """Explore page like a human - scroll to different sections, hover elements"""
    print(f"[{session_id}] 🔍 Exploring page like a human...")
    
    try:
        # Get page height for realistic scrolling
        page_height = await page.evaluate('document.body.scrollHeight')
        viewport_height = await page.evaluate('window.innerHeight')
        
        # Scroll to random positions and explore
        positions = [0.1, 0.3, 0.5, 0.7, 0.9]  # 10%, 30%, 50%, 70%, 90% of page
        random.shuffle(positions)
        
        for pos in positions[:3]:  # Visit 3 random positions
            scroll_y = int(page_height * pos)
            
            # Smooth scroll to position
            await page.evaluate(f'''
                window.scrollTo({{
                    top: {scroll_y},
                    behavior: 'smooth'
                }});
            ''')
            
            # Wait for scroll to complete
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            # Hover over some elements at this position
            try:
                visible_elements = await page.query_selector_all('a, button, img, h1, h2, h3')
                for _ in range(random.randint(1, 3)):
                    if visible_elements:
                        element = random.choice(visible_elements)
                        # Check if element is in viewport
                        is_visible = await element.is_visible()
                        if is_visible:
                            await element.hover()
                            await asyncio.sleep(random.uniform(0.8, 2.0))
            except:
                pass
                
            # Sometimes perform a wasted action
            if random.random() < 0.3:
                await wasted_click_actions(page, session_id)
                
    except Exception as e:
        print(f"[{session_id}] ⚠️ Page exploration failed: {e}")

async def simulate_reading_behavior(page, session_id: str, reading_time_seconds: int = 30):
    """Simulate human reading behavior - pauses, scrolling, occasional backtracking"""
    print(f"[{session_id}] 📖 Simulating reading behavior for {reading_time_seconds}s...")
    
    start_time = asyncio.get_event_loop().time()
    end_time = start_time + reading_time_seconds
    
    while asyncio.get_event_loop().time() < end_time:
        # Reading patterns
        actions = [
            ("scroll_small", 0.4),    # 40% - small scrolls while reading
            ("pause_reading", 0.3),   # 30% - pause to read  
            ("scroll_back", 0.15),    # 15% - scroll back to re-read
            ("wasted_action", 0.1),   # 10% - distracted actions
            ("mouse_move", 0.05)      # 5% - random mouse movements
        ]
        
        # Choose action based on weights
        rand = random.random()
        cumsum = 0
        chosen_action = "scroll_small"  # default action
        for action, weight in actions:
            cumsum += weight
            if rand <= cumsum:
                chosen_action = action
                break
        
        try:
            if chosen_action == "scroll_small":
                # Small scroll down (reading)
                await page.evaluate('window.scrollBy(0, window.innerHeight * 0.3)')
                await asyncio.sleep(random.uniform(3.0, 6.0))  # Reading time
                
            elif chosen_action == "pause_reading":
                # Pause without scrolling (reading current section)
                await asyncio.sleep(random.uniform(4.0, 8.0))
                
            elif chosen_action == "scroll_back":
                # Scroll back up (re-reading)
                await page.evaluate('window.scrollBy(0, -window.innerHeight * 0.2)')
                await asyncio.sleep(random.uniform(2.0, 4.0))
                
            elif chosen_action == "wasted_action":
                await wasted_click_actions(page, session_id)
                
            elif chosen_action == "mouse_move":
                await random_mouse_movements(session_id, 2)
                
        except Exception as e:
            print(f"[{session_id}] ⚠️ Reading simulation error: {e}")
            await asyncio.sleep(1.0)  # Continue with basic delay
            
        # Small random delay between actions
        await asyncio.sleep(random.uniform(0.5, 1.5))

async def random_page_interactions(page, session_id: str):
    """Random interactions that humans might do accidentally or out of curiosity"""
    interactions = [
        "try_keyboard_shortcuts",
        "test_zoom", 
        "check_page_source",
        "try_browser_back_forward"
    ]
    
    interaction = random.choice(interactions)
    print(f"[{session_id}] 🎭 Random interaction: {interaction}")
    
    try:
        if interaction == "try_keyboard_shortcuts":
            shortcuts = ['Control+f', 'Control+l', 'F5', 'Control+r']
            shortcut = random.choice(shortcuts)
            await page.keyboard.press(shortcut)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            # Press Escape to cancel any dialogs
            await page.keyboard.press('Escape')
            
        elif interaction == "test_zoom":
            # Zoom in/out slightly then reset
            if random.random() < 0.5:
                await page.keyboard.press('Control+Plus')
            else:
                await page.keyboard.press('Control+Minus')
            await asyncio.sleep(random.uniform(1.0, 3.0))
            await page.keyboard.press('Control+0')  # Reset zoom
            
        elif interaction == "check_page_source":
            await page.keyboard.press('Control+u')
            await asyncio.sleep(random.uniform(2.0, 4.0))
            await page.keyboard.press('Control+w')  # Close source tab
            
        elif interaction == "try_browser_back_forward":
            await page.keyboard.press('Alt+Left')  # Browser back
            await asyncio.sleep(random.uniform(1.0, 2.0))
            await page.keyboard.press('Alt+Right')  # Browser forward
            
    except Exception as e:
        print(f"[{session_id}] ⚠️ Random interaction failed: {e}")
