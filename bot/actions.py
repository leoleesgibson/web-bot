import asyncio
import random
import pyautogui
import time
import config

# Disable PyAutoGUI fail-safe for automated browsing
pyautogui.FAILSAFE = False

from .human_behaviors import (
    realistic_typing_with_mistakes, 
    random_mouse_movements,
    wasted_click_actions,
    human_like_page_exploration,
    simulate_reading_behavior,
    random_page_interactions
)
from .smart_clicking import human_click_with_retry, smart_element_finder, intelligent_page_wait
from .natural_timing import (
    article_reading_time, page_scanning_time, deep_reading_time,
    thinking_pause_time, scroll_interval_time, get_reading_pattern
)

async def random_scroll(page, duration_seconds=20):
    """
    Simulates human-like scrolling on a page for a given duration.
    Scrolls down, with some upward movements, and random pauses to appear more natural.
    """
    end_time = time.time() + duration_seconds
    while time.time() < end_time:
        # 85% chance to scroll down, 15% to scroll up
        should_scroll_down = random.random() < 0.85
        
        scroll_amount = random.randint(200, 600)
        if not should_scroll_down:
            scroll_amount = -scroll_amount  # Negative value scrolls up

        # To make scrolling appear smoother, it's broken into smaller steps
        steps = random.randint(10, 20)
        for _ in range(steps):
            await page.mouse.wheel(0, scroll_amount / steps)
            await asyncio.sleep(random.uniform(0.01, 0.04))
            
        # A longer pause between scroll actions to simulate reading
        await asyncio.sleep(random.uniform(1.5, 4.0))

async def human_like_click(page, element):
    """
    Performs a human-like click on an element with smooth mouse movement
    """
    try:
        # Check if element is still attached to DOM
        is_attached = await element.evaluate("element => element.isConnected")
        if not is_attached:
            print("Element is no longer attached to DOM, skipping click")
            return
            
        box = await element.bounding_box()
        if box:
            # Add some randomness to click position (not always center)
            x_offset = random.uniform(-0.3, 0.3) * box['width']
            y_offset = random.uniform(-0.3, 0.3) * box['height']
            
            x = box['x'] + box['width'] / 2 + x_offset
            y = box['y'] + box['height'] / 2 + y_offset

            # Simulate human-like mouse movement
            pyautogui.moveTo(x, y, duration=random.uniform(0.7, 1.8))
            await asyncio.sleep(random.uniform(0.1, 0.3))

        # Try different click strategies
        try:
            # First try: Normal click with shorter timeout
            await element.click(timeout=15000)
        except Exception as e1:
            print(f"Normal click failed: {str(e1)[:100]}...")
            try:
                # Second try: Force click
                await element.click(force=True, timeout=10000)
            except Exception as e2:
                print(f"Force click failed: {str(e2)[:100]}...")
                try:
                    # Third try: JavaScript click
                    await element.evaluate("element => element.click()")
                except Exception as e3:
                    print(f"JavaScript click failed: {str(e3)[:100]}...")
                    # Fourth try: Navigate directly using href
                    href = await element.get_attribute('href')
                    if href and href.startswith('http'):
                        print(f"Direct navigation to: {href[:50]}...")
                        await page.goto(href, timeout=90000)  # 90 seconds for proxy
                        await page.wait_for_load_state('load')
                    else:
                        raise Exception("All click methods failed")
        
        await asyncio.sleep(random.uniform(1.0, 2.5))
        
    except Exception as e:
        print(f"Click completely failed: {str(e)[:100]}...")
        raise e

async def smart_click_random_article(page, session_id: str):
    """
    Enhanced article clicking with smart retry and multiple fallbacks
    Uses configuration settings for behavior customization
    """
    if not config.ENABLE_ARTICLE_CLICKING:
        print(f"[{session_id}] ⚠️ Article clicking disabled in config")
        return False
        
    # Check probability of clicking articles
    if random.random() > config.ARTICLE_CLICK_PROBABILITY:
        print(f"[{session_id}] 🎲 Skipping article click based on probability")
        return False
    
    # Multiple strategies for finding articles with preference for recent ones
    base_selectors = [
        "a[href*='article']", "a[href*='news']", "a[href*='story']", 
        ".article-title a", ".news-title a", ".post-title a",
        "article a", ".entry-title a", "h1 a", "h2 a", "h3 a",
        "[class*='headline'] a", "[class*='title'] a"
    ]
    
    # Add date-based selectors if preferring recent articles
    if config.PREFER_RECENT_ARTICLES:
        current_year = time.strftime('%Y')
        recent_selectors = [
            f"a[href*='/{current_year}/']",
            f"a[href*='-{current_year}-']",
            "a[href*='/20']",  # Generic recent date pattern
        ]
        article_selectors = recent_selectors + base_selectors
    else:
        article_selectors = base_selectors
    
    print(f"[{session_id}] 🎯 Looking for articles to click...")
    
    # Try smart element finder
    target_element = await smart_element_finder(page, article_selectors, session_id, timeout=8000)
    
    if not target_element:
        print(f"[{session_id}] ❌ No articles found with smart finder")
        return False
    
    # Get article URL for logging
    try:
        article_url = await target_element.get_attribute('href')
        article_text = await target_element.text_content()
        print(f"[{session_id}] 📰 Found article: {(article_text or 'No title')[:50]}...")
        if article_url:
            print(f"[{session_id}] 🔗 URL: {article_url[:80]}...")
    except:
        pass
    
    # Try human-like click with retry
    success = await human_click_with_retry(page, target_element, session_id, max_retries=3)
    
    if success:
        # Wait for navigation intelligently
        await intelligent_page_wait(page, session_id, "navigation")
        print(f"[{session_id}] ✅ Successfully navigated to article")
        return True
    
    print(f"[{session_id}] ❌ Failed to click article after all retries")
    return False

async def multi_tab_article_reading(page, session_id: str):
    """
    Enhanced multi-tab browsing simulation with configurable behavior
    Opens multiple articles in tabs like real users do
    """
    if not config.ENABLE_MULTI_TAB_BROWSING:
        print(f"[{session_id}] ⚠️ Multi-tab browsing disabled in config")
        return False
    
    # Check probability of using tabs
    if random.random() > config.TAB_OPENING_PROBABILITY:
        print(f"[{session_id}] 🎲 Skipping multi-tab based on probability")
        return False
        
    print(f"[{session_id}] 📑 Starting multi-tab browsing simulation...")
    
    try:
        # Find multiple articles with enhanced selectors
        article_selectors = [
            "a[href*='article']", "a[href*='news']", "a[href*='story']",
            "article a", ".entry-title a", ".post-title a", ".article-title a",
            "h1 a", "h2 a", "h3 a", "[class*='headline'] a", "[class*='title'] a"
        ]
        
        # Get all article links
        all_links = []
        for selector in article_selectors:
            try:
                links = await page.query_selector_all(selector)
                all_links.extend(links)
                if len(all_links) >= config.MAX_TABS_TO_OPEN * 2:  # Get more options than needed
                    break
            except:
                continue
        
        if len(all_links) < 2:
            print(f"[{session_id}] ❌ Not enough articles found for multi-tab (found {len(all_links)})")
            return False
        
        # Determine number of tabs to open
        tabs_to_open = min(random.randint(2, config.MAX_TABS_TO_OPEN), len(all_links))
        print(f"[{session_id}] 📑 Planning to open {tabs_to_open} tabs from {len(all_links)} available articles")
        
        opened_tabs = 0
        
        # Open articles in new tabs
        for i in range(tabs_to_open):
            try:
                # Select a random article from remaining links
                if i < len(all_links):
                    link = all_links[i]
                    
                    # Get article info for logging
                    try:
                        href = await link.get_attribute('href')
                        text = await link.text_content()
                        print(f"[{session_id}] 📑 Opening tab {i+1}: {(text or 'No title')[:40]}...")
                        if href:
                            print(f"[{session_id}] � Tab URL: {href[:60]}...")
                    except:
                        pass
                    
                    # Open in new tab with Ctrl+Click
                    await link.click(modifiers=['Control'])
                    opened_tabs += 1
                    
                    # Wait between tab openings
                    await asyncio.sleep(random.uniform(1.0, 2.5))
                    
            except Exception as e:
                print(f"[{session_id}] ⚠️ Failed to open tab {i+1}: {str(e)[:100]}")
                continue
        
        if opened_tabs == 0:
            print(f"[{session_id}] ❌ No tabs were successfully opened")
            return False
            
        print(f"[{session_id}] ✅ Successfully opened {opened_tabs} tabs")
        
        # Simulate realistic tab browsing behavior
        await simulate_tab_switching_behavior(page, session_id, opened_tabs)
        
        return True
        
    except Exception as e:
        print(f"[{session_id}] ❌ Multi-tab simulation failed: {str(e)[:100]}")
        return False

async def simulate_tab_switching_behavior(page, session_id: str, num_tabs: int):
    """
    Simulate realistic tab switching and reading behavior
    """
    print(f"[{session_id}] 🔄 Simulating tab switching behavior for {num_tabs} tabs...")
    
    for i in range(num_tabs):
        try:
            # Switch to next tab (Ctrl+Tab)
            print(f"[{session_id}] 🔄 Switching to tab {i+1}...")
            await page.keyboard.press('Control+Tab')
            await asyncio.sleep(random.uniform(0.5, 1.2))
            
            # Wait for page to load
            try:
                await page.wait_for_load_state('networkidle', timeout=10000)
            except:
                await asyncio.sleep(2)  # Fallback wait
            
            # Read the article with configurable time
            read_time = random.randint(config.MIN_TAB_READING_TIME, config.MAX_TAB_READING_TIME)
            print(f"[{session_id}] 📖 Reading tab {i+1} for {read_time}s...")
            await simulate_reading_behavior(page, session_id, read_time)
            
            # Sometimes scroll during reading
            if random.random() < 0.7:
                scroll_time = min(read_time // 3, 20)  # Scroll for part of reading time
                await random_scroll(page, scroll_time)
            
            # Decide whether to close this tab
            should_close = random.random() < config.TAB_CLOSE_PROBABILITY
            if should_close and i < num_tabs - 1:  # Don't close the last tab
                print(f"[{session_id}] ❌ Closing tab {i+1}...")
                await page.keyboard.press('Control+w')
                await asyncio.sleep(random.uniform(0.3, 0.8))
            
        except Exception as e:
            print(f"[{session_id}] ⚠️ Tab {i+1} switching error: {str(e)[:100]}")
            continue
    
    print(f"[{session_id}] ✅ Completed tab browsing simulation")

async def click_random_article(page, session_id="session"):
    """Legacy function - now uses smart clicking"""
    return await smart_click_random_article(page, session_id)

async def click_multiple_articles(page, session_id: str):
    """
    Click multiple articles in sequence during a single session
    Uses configuration to determine how many articles to click
    """
    if not config.ENABLE_ARTICLE_CLICKING:
        return 0
        
    # Determine how many articles to click
    articles_to_click = random.randint(config.ARTICLES_TO_CLICK_MIN, config.ARTICLES_TO_CLICK_MAX)
    print(f"[{session_id}] 🎯 Planning to click {articles_to_click} articles this session")
    
    successful_clicks = 0
    
    for i in range(articles_to_click):
        try:
            print(f"[{session_id}] 📰 Attempting to click article {i+1}/{articles_to_click}...")
            
            success = await smart_click_random_article(page, session_id)
            
            if success:
                successful_clicks += 1
                
                # Read the article for a realistic amount of time
                read_time = random.randint(config.ARTICLE_READING_TIME_MIN, config.ARTICLE_READING_TIME_MAX)
                print(f"[{session_id}] 📖 Reading article {i+1} for {read_time}s...")
                await simulate_reading_behavior(page, session_id, read_time)
                
                # Sometimes scroll during reading
                if random.random() < 0.8:
                    scroll_duration = min(read_time // 3, 30)
                    await random_scroll(page, scroll_duration)
                
                # Navigate back to main page for next article (unless it's the last one)
                if i < articles_to_click - 1:
                    try:
                        print(f"[{session_id}] ⬅️ Navigating back to find more articles...")
                        await page.go_back()
                        await page.wait_for_load_state('networkidle', timeout=10000)
                        await asyncio.sleep(random.uniform(1.0, 2.0))
                    except Exception as e:
                        print(f"[{session_id}] ⚠️ Failed to go back, navigating to main page: {str(e)[:50]}")
                        await page.goto(config.TARGET_URL)
                        await page.wait_for_load_state('networkidle', timeout=15000)
                        await asyncio.sleep(random.uniform(2.0, 3.0))
                        
            else:
                print(f"[{session_id}] ❌ Failed to click article {i+1}, continuing...")
                
            # Add natural pause between article clicks
            if i < articles_to_click - 1:
                pause_time = random.uniform(3.0, 8.0)
                print(f"[{session_id}] ⏳ Pausing {pause_time:.1f}s before next article...")
                await asyncio.sleep(pause_time)
                
        except Exception as e:
            print(f"[{session_id}] ❌ Error clicking article {i+1}: {str(e)[:100]}")
            continue
    
    print(f"[{session_id}] 📊 Article clicking session complete: {successful_clicks}/{articles_to_click} successful")
    return successful_clicks

async def browse_like_human(page, session_duration_minutes=5, session_id="session"):
    """
    Enhanced human browsing with natural timing patterns and realistic depth variation
    """
    # Get natural reading pattern for this session
    reading_pattern = get_reading_pattern()
    
    # Use natural session duration instead of fixed time
    actual_duration = reading_pattern['session_duration'] if session_duration_minutes == 5 else session_duration_minutes
    session_end_time = time.time() + (actual_duration * 60)
    
    print(f"[{session_id}] 🎭 Natural browsing session: {actual_duration}min, {reading_pattern['pages_to_visit']} pages planned")
    print(f"[{session_id}] 📊 Pattern: bounce={reading_pattern['will_bounce_early']}, tabs={reading_pattern['will_use_tabs']}, back_btn={reading_pattern['prefers_back_button']}")
    
    pages_visited = 0
    max_pages = reading_pattern['pages_to_visit']
    
    # Initial page exploration (like a human getting oriented)
    scan_time = page_scanning_time()
    print(f"[{session_id}] 👀 Initial page scan for {scan_time}s...")
    await simulate_reading_behavior(page, session_id, scan_time)
    
    # Early bounce behavior (30% of users)
    if reading_pattern['will_bounce_early']:
        print(f"[{session_id}] 🏃 Early bounce behavior - quick exit")
        quick_time = random.randint(10, 30)
        await simulate_reading_behavior(page, session_id, quick_time)
        print(f"[{session_id}] 📊 Bounce session completed. Visited {pages_visited + 1} pages.")
        return
    
    while time.time() < session_end_time and pages_visited < max_pages:
        
        # Natural thinking pause
        thinking_time = thinking_pause_time()
        print(f"[{session_id}] 🤔 Natural thinking pause ({thinking_time:.1f}s)...")
        await asyncio.sleep(thinking_time)
        
        # Decide on action with enhanced natural probabilities
        action_choice = random.random()
        
        # Enhanced article interaction - 50% chance
        if action_choice < 0.5 and pages_visited < max_pages:
            
            # Decide between single article click, multi-article session, or multi-tab browsing
            interaction_type = random.random()
            
            if interaction_type < 0.3 and reading_pattern['will_use_tabs']:
                # Multi-tab browsing (30% of article interactions)
                print(f"[{session_id}] 📑 Attempting multi-tab article browsing...")
                tab_success = await multi_tab_article_reading(page, session_id)
                if tab_success:
                    pages_visited += 3  # Count as visiting multiple pages
                else:
                    # Fallback to single article click
                    success = await smart_click_random_article(page, session_id)
                    if success:
                        pages_visited += 1
                        read_time = random.randint(config.ARTICLE_READING_TIME_MIN, config.ARTICLE_READING_TIME_MAX)
                        print(f"[{session_id}] 📰 Reading article #{pages_visited} for {read_time}s...")
                        await simulate_reading_behavior(page, session_id, read_time)
                        
            elif interaction_type < 0.6:
                # Multi-article session (30% of article interactions)
                print(f"[{session_id}] 📚 Attempting multi-article reading session...")
                articles_read = await click_multiple_articles(page, session_id)
                pages_visited += articles_read
                
            else:
                # Single article click (40% of article interactions)
                success = await smart_click_random_article(page, session_id)
                if success:
                    pages_visited += 1
                    # Use configurable reading time
                    read_time = random.randint(config.ARTICLE_READING_TIME_MIN, config.ARTICLE_READING_TIME_MAX)
                    print(f"[{session_id}] 📰 Reading article #{pages_visited} for {read_time}s...")
                    await simulate_reading_behavior(page, session_id, read_time)
                    
                    # Sometimes do wasted actions while reading
                    if random.random() < 0.25:
                        await wasted_click_actions(page, session_id)
                        
                    # Sometimes scroll during reading
                    if random.random() < 0.8:
                        scroll_time = min(read_time // 3, 30)
                        await random_scroll(page, scroll_time)
                else:
                    # No article found - do page exploration instead
                    explore_time = page_scanning_time() 
                    print(f"[{session_id}] 🔍 No articles found, exploring page for {explore_time}s...")
                    await simulate_reading_behavior(page, session_id, explore_time)
        
        elif action_choice < 0.7:  # 20% - Deep reading of current page
            deep_time = deep_reading_time()
            print(f"[{session_id}] 📖 Deep reading session for {deep_time}s...")
            await simulate_reading_behavior(page, session_id, deep_time)
            
        elif action_choice < 0.85 and reading_pattern['prefers_back_button']:  # 15% - Back button navigation
            print(f"[{session_id}] 🔙 Using back button (preferred pattern)...")
            try:
                await page.go_back()
                await intelligent_page_wait(page, session_id, "navigation")
                
                # Scan the previous page briefly
                scan_time = page_scanning_time()
                await simulate_reading_behavior(page, session_id, scan_time)
            except:
                print(f"[{session_id}] ⚠️ Back navigation failed")
        
        elif action_choice < 0.95:  # 10% - Wasted/distracted actions
            await wasted_click_actions(page, session_id)
            # Skip mouse movements for mobile (touch-based)
            try:
                await random_mouse_movements(session_id, random.randint(2, 5))
            except Exception as e:
                print(f"[{session_id}] 📱 Skipping mouse movement (mobile device): {str(e)[:50]}...")
            
        else:  # 5% - Random page interactions
            await random_page_interactions(page, session_id)
        
        # Occasionally do random mouse movements (fidgeting) - mobile safe
        if random.random() < 0.15:
            try:
                await random_mouse_movements(session_id, random.randint(1, 3))
            except Exception as e:
                print(f"[{session_id}] 📱 Skipping mouse movement (mobile device): {str(e)[:50]}...")
    
    # End of session - final human-like action
    if random.random() < 0.3:
        print(f"[{session_id}] 🎭 Final human-like action before leaving...")
        await wasted_click_actions(page, session_id)
    
    print(f"[{session_id}] 📊 Natural browsing completed. Visited {pages_visited} pages (planned: {max_pages}).")

async def click_first_link(page):
    links = await page.query_selector_all("a")
    if links:
        link = links[0]
        await human_like_click(page, link)

async def search_and_navigate(page, search_query, target_url, session_id="session"):
    """
    Enhanced Google search with advanced anti-detection and human-like behavior
    """
    print(f"[{session_id}] 🔍 Starting Google search for: {search_query}")
    
    # Navigate to Google with extended timeout for proxy connections
    await page.goto("https://www.google.com", timeout=90000)  # 90 seconds for proxy
    await asyncio.sleep(random.uniform(2.5, 4.5))
    
    # Handle potential cookie consent (common on Google)
    try:
        cookie_buttons = await page.query_selector_all('button')
        for button in cookie_buttons:
            text = await button.text_content()
            if text and any(word in text.lower() for word in ['accept', 'agree', 'ok', 'got it', 'i agree']):
                print(f"[{session_id}] 🍪 Accepting cookies...")
                await human_click_with_retry(page, button, session_id, max_retries=2)
                await asyncio.sleep(random.uniform(1.0, 2.0))
                break
    except:
        pass
    
    # Find Google search box with multiple strategies
    search_selectors = [
        'input[name="q"]',           # Standard Google search
        'textarea[name="q"]',        # New Google search textarea
        '[data-ved] input',          # Google input with data-ved
        'input[title*="Search"]',    # Search input by title
        '#searchboxinput',           # Alternative Google ID
        '.gLFyf'                     # Google search box class
    ]
    
    search_box = await smart_element_finder(page, search_selectors, session_id, timeout=10000)
    
    if not search_box:
        print(f"[{session_id}] ❌ Could not find Google search box")
        return
    
    # Human-like typing with potential mistakes
    print(f"[{session_id}] ⌨️ Typing search query with human behavior...")
    await realistic_typing_with_mistakes(page, search_query, session_id)
    
    # Natural pause before hitting enter
    thinking_time = thinking_pause_time()
    print(f"[{session_id}] 🤔 Thinking pause ({thinking_time:.1f}s) before search...")
    await asyncio.sleep(thinking_time)
    
    # Press Enter to search
    await page.keyboard.press("Enter")
    
    # Wait for Google search results with multiple fallback selectors
    google_result_selectors = [
        '#search',                   # Main search results container
        '.g',                        # Individual search result
        '[data-ved]',                # Google result with tracking
        '.yuRUbf',                   # Google result link container
        '.tF2Cxc',                   # Google result item
        '.hlcw0c',                   # Alternative Google result
        '#rso'                       # Results container
    ]
    
    results_loaded = False
    for selector in google_result_selectors:
        try:
            await page.wait_for_selector(selector, timeout=12000)
            print(f"[{session_id}] ✅ Google results loaded with: {selector}")
            results_loaded = True
            break
        except:
            continue
    
    if not results_loaded:
        print(f"[{session_id}] ⚠️ Could not confirm results loaded, continuing...")
        await asyncio.sleep(random.uniform(3, 6))
    
    # Enhanced target link finding with multiple strategies
    target_domain = target_url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
    
    # Try multiple link finding strategies
    link_strategies = [
        f'a[href*="{target_domain}"]',                    # Domain match
        f'a[href*="{search_query.replace(" ", "")}"]',    # Query match
        f'h3:has-text("{search_query}") + a',            # Title-based match
        f'cite:has-text("{target_domain}") ~ a',         # Citation-based match
    ]
    
    print(f"[{session_id}] 🎯 Searching for target: {target_domain}")
    
    target_link = None
    for strategy in link_strategies:
        try:
            links = await page.query_selector_all(strategy)
            for link in links:
                href = await link.get_attribute('href')
                if href and target_domain in href.lower():
                    target_link = link
                    print(f"[{session_id}] ✅ Found target link: {href[:50]}...")
                    break
            if target_link:
                break
        except:
            continue
    
    # Fallback: Search through all links manually
    if not target_link:
        print(f"[{session_id}] 🔍 Manual link search fallback...")
        all_links = await page.query_selector_all('a')
        
        for link in all_links[:15]:  # Check first 15 links
            try:
                href = await link.get_attribute('href')
                text = await link.text_content()
                
                if href and (target_domain in href.lower() or 
                           (text and any(word in text.lower() for word in search_query.lower().split()))):
                    target_link = link
                    print(f"[{session_id}] 🎯 Found fallback link: {href[:50]}...")
                    break
            except:
                continue
    
    # Click the target link with smart retry
    if target_link:
        print(f"[{session_id}] 🖱️ Clicking target link...")
        
        # Small pre-click delay (human hesitation)
        await asyncio.sleep(random.uniform(1.0, 2.5))
        
        success = await human_click_with_retry(page, target_link, session_id, max_retries=3)
        
        if success:
            print(f"[{session_id}] ✅ Successfully navigated to target")
            await intelligent_page_wait(page, session_id, "navigation")
            
            # Post-navigation human behavior
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            # Sometimes do a quick page scan after landing
            if random.random() < 0.4:
                scan_time = page_scanning_time()
                print(f"[{session_id}] 👀 Initial page scan ({scan_time}s)...")
                await simulate_reading_behavior(page, session_id, scan_time)
        else:
            print(f"[{session_id}] ❌ Failed to click target link, trying direct navigation...")
            await page.goto(target_url, timeout=90000)  # 90 seconds for proxy
            await asyncio.sleep(random.uniform(3.0, 6.0))
    else:
        print(f"[{session_id}] ❌ Target link not found in Google results, going direct...")
        await page.goto(target_url, timeout=90000)  # 90 seconds for proxy
        await asyncio.sleep(random.uniform(3.0, 6.0))


async def direct_navigate_and_browse(page, target_url: str, session_id: str):
    """
    Navigate directly to target URL without search - much more reliable
    """
    from .natural_timing import thinking_pause_time
    
    print(f"[{session_id}] 🎯 Navigating directly to: {target_url}")
    
    # Add natural thinking pause before navigation
    think_time = thinking_pause_time()
    print(f"[{session_id}] 🤔 Thinking for {think_time:.1f}s before navigation...")
    await asyncio.sleep(think_time)
    
    try:
        # Direct navigation with extended timeout for proxy
        await page.goto(target_url, timeout=90000)
        print(f"[{session_id}] ✅ Successfully reached target website")
        
        # Wait for page to load - using domcontentloaded which is more reliable than networkidle
        try:
            await page.wait_for_load_state('domcontentloaded', timeout=30000)
            print(f"[{session_id}] 📄 Page DOM loaded successfully")
        except Exception as load_error:
            print(f"[{session_id}] ⚠️ DOM load timeout, but continuing anyway: {str(load_error)[:50]}...")
            
        # Additional wait for any remaining resources (but don't fail if it times out)
        try:
            await page.wait_for_load_state('networkidle', timeout=15000)  # Shorter timeout
            print(f"[{session_id}] 🌐 Network reached idle state")
        except Exception as network_error:
            print(f"[{session_id}] ⚠️ Network still loading, but proceeding: {str(network_error)[:50]}...")
        
        # Natural pause after landing
        landing_pause = random.uniform(2.5, 5.0)
        print(f"[{session_id}] 👀 Taking {landing_pause:.1f}s to look around...")
        await asyncio.sleep(landing_pause)
        
        # Optional: Simulate some initial page interaction
        try:
            # Scroll down a bit to simulate reading
            await page.evaluate("window.scrollTo(0, window.innerHeight * 0.3)")
            await asyncio.sleep(random.uniform(1.5, 3.0))
            
            # Scroll back up
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
        except Exception as scroll_error:
            print(f"[{session_id}] Minor scroll interaction failed: {str(scroll_error)[:50]}...")
        
    except Exception as e:
        print(f"[{session_id}] ❌ Direct navigation failed: {str(e)[:100]}...")
        raise e
