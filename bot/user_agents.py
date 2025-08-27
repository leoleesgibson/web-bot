"""
Real User-Agent dataset for anti-detection
Contains actual browser fingerprints collected from real users
"""
import random

# Real Chrome User-Agents (Windows, Mac, Linux)
CHROME_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

# Real Edge User-Agents
EDGE_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
]

# Real Firefox User-Agents  
FIREFOX_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

# Real Safari User-Agents (Mac only)
SAFARI_USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
]

def get_random_user_agent():
    """Get a random but realistic user agent from real browser data"""
    
    # Weight distribution based on real market share
    browsers = [
        (CHROME_USER_AGENTS, 0.65),    # 65% Chrome
        (EDGE_USER_AGENTS, 0.20),      # 20% Edge  
        (FIREFOX_USER_AGENTS, 0.10),   # 10% Firefox
        (SAFARI_USER_AGENTS, 0.05)     # 5% Safari
    ]
    
    # Choose browser based on market share weights
    rand = random.random()
    cumulative = 0
    
    for user_agents, weight in browsers:
        cumulative += weight
        if rand <= cumulative:
            selected_ua = random.choice(user_agents)
            browser_name = "Chrome" if "Chrome/" in selected_ua and "Edg/" not in selected_ua else \
                          "Edge" if "Edg/" in selected_ua else \
                          "Firefox" if "Firefox/" in selected_ua else "Safari"
            
            return selected_ua, browser_name
    
    # Fallback to Chrome if something goes wrong
    return random.choice(CHROME_USER_AGENTS), "Chrome"

def get_matching_screen_resolution(user_agent):
    """Get realistic screen resolution based on OS in user agent"""
    
    if "Windows NT 10.0" in user_agent or "Windows NT 11.0" in user_agent:
        # Common Windows resolutions
        resolutions = [
            (1920, 1080),   # Most common
            (1366, 768),    # Laptops
            (2560, 1440),   # High-end monitors
            (1536, 864),    # Scaled displays
            (1440, 900)     # MacBook Air equivalent on Windows
        ]
        return random.choice(resolutions)
        
    elif "Macintosh" in user_agent:
        # Mac resolutions
        resolutions = [
            (2560, 1600),   # MacBook Pro 16"
            (2560, 1664),   # MacBook Pro 14" 
            (2880, 1800),   # MacBook Pro 15"
            (2560, 1440),   # iMac 27"
            (1920, 1080)    # External monitor
        ]
        return random.choice(resolutions)
        
    else:  # Linux
        # Linux desktop resolutions
        resolutions = [
            (1920, 1080),
            (2560, 1440), 
            (1366, 768),
            (1600, 900)
        ]
        return random.choice(resolutions)

def get_matching_platform_info(user_agent):
    """Get platform-specific info that matches the user agent"""
    
    if "Windows NT 10.0" in user_agent:
        return {
            'platform': 'Win32',
            'os': 'Windows 10',
            'memory': random.choice([4, 8, 16]),  # GB
            'cores': random.choice([4, 6, 8, 12])
        }
    elif "Windows NT 11.0" in user_agent:
        return {
            'platform': 'Win32', 
            'os': 'Windows 11',
            'memory': random.choice([8, 16, 32]),  # Windows 11 usually has more RAM
            'cores': random.choice([6, 8, 12, 16])
        }
    elif "Macintosh" in user_agent:
        return {
            'platform': 'MacIntel',
            'os': 'macOS',
            'memory': random.choice([8, 16, 32]),  # Macs typically have good specs
            'cores': random.choice([4, 6, 8, 10])
        }
    else:  # Linux
        return {
            'platform': 'Linux x86_64',
            'os': 'Linux',
            'memory': random.choice([4, 8, 16]),
            'cores': random.choice([4, 6, 8])
        }
