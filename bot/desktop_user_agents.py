"""
Desktop User-Agent dataset for desktop device simulation
Contains actual desktop browser fingerprints collected from real devices
"""
import random

# Real Desktop Chrome User-Agents (Windows, Mac, Linux)
DESKTOP_CHROME_WINDOWS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

DESKTOP_CHROME_MAC = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

DESKTOP_CHROME_LINUX = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

# Real Desktop Edge User-Agents
DESKTOP_EDGE_WINDOWS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
]

DESKTOP_EDGE_MAC = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
]

# Real Desktop Firefox User-Agents
DESKTOP_FIREFOX_WINDOWS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

DESKTOP_FIREFOX_MAC = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0"
]

DESKTOP_FIREFOX_LINUX = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

# Real Desktop Safari User-Agents (Mac only)
DESKTOP_SAFARI_MAC = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
]

# Desktop screen resolutions (width x height)
DESKTOP_SCREEN_RESOLUTIONS = {
    # Common desktop resolutions
    "1366x768": {"device": "Laptop HD", "platform": "Windows", "memory": 8, "cores": 4},
    "1920x1080": {"device": "Desktop FHD", "platform": "Windows", "memory": 16, "cores": 8},
    "1440x900": {"device": "MacBook Pro", "platform": "Mac", "memory": 16, "cores": 8},
    "2560x1440": {"device": "Desktop QHD", "platform": "Windows", "memory": 32, "cores": 12},
    "3840x2160": {"device": "Desktop 4K", "platform": "Windows", "memory": 32, "cores": 16},
    "2560x1600": {"device": "MacBook Pro 16", "platform": "Mac", "memory": 32, "cores": 10},
    "1680x1050": {"device": "Desktop WSXGA+", "platform": "Linux", "memory": 16, "cores": 6},
    "2880x1800": {"device": "MacBook Pro Retina", "platform": "Mac", "memory": 16, "cores": 8}
}

def get_desktop_user_agent():
    """Get a random desktop user agent from real browser data"""
    
    # Weight distribution based on real desktop market share
    browsers = [
        (DESKTOP_CHROME_WINDOWS, 0.35, "Chrome Windows"),
        (DESKTOP_CHROME_MAC, 0.15, "Chrome Mac"),
        (DESKTOP_CHROME_LINUX, 0.05, "Chrome Linux"),
        (DESKTOP_EDGE_WINDOWS, 0.15, "Edge Windows"),
        (DESKTOP_EDGE_MAC, 0.02, "Edge Mac"),
        (DESKTOP_FIREFOX_WINDOWS, 0.08, "Firefox Windows"),
        (DESKTOP_FIREFOX_MAC, 0.03, "Firefox Mac"),
        (DESKTOP_FIREFOX_LINUX, 0.02, "Firefox Linux"),
        (DESKTOP_SAFARI_MAC, 0.15, "Safari Mac")
    ]
    
    # Weighted random selection
    rand = random.random()
    cumulative = 0
    
    for user_agents, weight, browser_name in browsers:
        cumulative += weight
        if rand <= cumulative:
            user_agent = random.choice(user_agents)
            return user_agent, browser_name
    
    # Fallback
    return random.choice(DESKTOP_CHROME_WINDOWS), "Chrome Windows"

def get_desktop_screen_resolution(user_agent: str):
    """Get matching desktop screen resolution based on user agent"""
    
    # Determine platform from user agent
    if "Windows" in user_agent:
        # Windows desktops/laptops
        windows_resolutions = [res for res, info in DESKTOP_SCREEN_RESOLUTIONS.items() 
                             if info["platform"] == "Windows"]
        resolution = random.choice(windows_resolutions)
    elif "Macintosh" in user_agent or "Mac OS X" in user_agent:
        # Mac desktops/laptops
        mac_resolutions = [res for res, info in DESKTOP_SCREEN_RESOLUTIONS.items() 
                         if info["platform"] == "Mac"]
        resolution = random.choice(mac_resolutions)
    elif "Linux" in user_agent or "X11" in user_agent:
        # Linux desktops
        linux_resolutions = [res for res, info in DESKTOP_SCREEN_RESOLUTIONS.items() 
                           if info["platform"] == "Linux"]
        if not linux_resolutions:
            linux_resolutions = ["1920x1080", "1366x768"]  # Fallback
        resolution = random.choice(linux_resolutions)
    else:
        # Fallback
        resolution = random.choice(list(DESKTOP_SCREEN_RESOLUTIONS.keys()))
    
    width, height = map(int, resolution.split('x'))
    return width, height

def get_desktop_platform_info(user_agent: str):
    """Get matching desktop platform info based on user agent"""
    
    # Get screen resolution first
    width, height = get_desktop_screen_resolution(user_agent)
    resolution_key = f"{width}x{height}"
    
    # Get platform info for that resolution
    if resolution_key in DESKTOP_SCREEN_RESOLUTIONS:
        device_info = DESKTOP_SCREEN_RESOLUTIONS[resolution_key]
        return {
            "device": device_info["device"],
            "platform": device_info["platform"], 
            "memory": device_info["memory"],
            "cores": device_info["cores"]
        }
    
    # Fallback for desktop
    return {
        "device": "Desktop PC",
        "platform": "Windows",
        "memory": 16,
        "cores": 8
    }

def get_desktop_mouse_capabilities():
    """Get desktop mouse/keyboard capabilities"""
    return {
        "hasTouch": False,  # Most desktops don't have touch
        "maxTouchPoints": 0,
        "mouseEnabled": True,
        "keyboardEnabled": True,
        "wheelEnabled": True
    }
