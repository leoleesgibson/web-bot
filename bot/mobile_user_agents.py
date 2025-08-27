"""
Mobile User-Agent dataset for mobile device simulation
Contains actual mobile browser fingerprints collected from real devices
"""
import random

# Real Mobile Chrome User-Agents (Android)
MOBILE_CHROME_ANDROID = [
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G996B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]

# Real Mobile Safari User-Agents (iOS)
MOBILE_SAFARI_IOS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
]

# Real Mobile Edge User-Agents  
MOBILE_EDGE_ANDROID = [
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 EdgA/120.0.0.0",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 EdgA/119.0.0.0",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 EdgA/120.0.0.0"
]

# Real Mobile Firefox User-Agents
MOBILE_FIREFOX_ANDROID = [
    "Mozilla/5.0 (Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
    "Mozilla/5.0 (Mobile; rv:120.0) Gecko/120.0 Firefox/120.0",
    "Mozilla/5.0 (Android 13; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
    "Mozilla/5.0 (Android 12; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0"
]

# Mobile screen resolutions (width x height)
MOBILE_SCREEN_RESOLUTIONS = {
    # Android phones
    "360x800": {"device": "Galaxy S20", "platform": "Android", "memory": 8, "cores": 8},
    "375x812": {"device": "iPhone 12/13", "platform": "iOS", "memory": 6, "cores": 6},
    "390x844": {"device": "iPhone 14", "platform": "iOS", "memory": 6, "cores": 6},
    "393x851": {"device": "Pixel 7", "platform": "Android", "memory": 8, "cores": 8},
    "412x915": {"device": "Galaxy S21", "platform": "Android", "memory": 8, "cores": 8},
    "428x926": {"device": "iPhone 14 Pro Max", "platform": "iOS", "memory": 6, "cores": 6},
    "360x780": {"device": "Galaxy A53", "platform": "Android", "memory": 6, "cores": 8},
    "414x896": {"device": "iPhone 11 Pro", "platform": "iOS", "memory": 4, "cores": 6},
    
    # Tablets
    "768x1024": {"device": "iPad", "platform": "iOS", "memory": 4, "cores": 6},
    "810x1080": {"device": "Galaxy Tab", "platform": "Android", "memory": 6, "cores": 8},
    "820x1180": {"device": "iPad Air", "platform": "iOS", "memory": 8, "cores": 8},
}

def get_mobile_user_agent():
    """Get a random mobile user agent from real device data"""
    
    # Weight distribution based on real mobile market share
    browsers = [
        (MOBILE_CHROME_ANDROID, 0.55, "Chrome Mobile"),    # 55% Chrome Android
        (MOBILE_SAFARI_IOS, 0.35, "Safari Mobile"),        # 35% Safari iOS  
        (MOBILE_EDGE_ANDROID, 0.07, "Edge Mobile"),        # 7% Edge Android
        (MOBILE_FIREFOX_ANDROID, 0.03, "Firefox Mobile")   # 3% Firefox Android
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
    return random.choice(MOBILE_CHROME_ANDROID), "Chrome Mobile"

def get_mobile_screen_resolution(user_agent: str):
    """Get matching mobile screen resolution based on user agent"""
    
    # Determine platform from user agent
    if "iPhone" in user_agent or "iPad" in user_agent:
        # iOS devices
        ios_resolutions = [res for res, info in MOBILE_SCREEN_RESOLUTIONS.items() 
                          if info["platform"] == "iOS"]
        resolution = random.choice(ios_resolutions)
    elif "Android" in user_agent or "Linux" in user_agent:
        # Android devices  
        android_resolutions = [res for res, info in MOBILE_SCREEN_RESOLUTIONS.items() 
                             if info["platform"] == "Android"]
        resolution = random.choice(android_resolutions)
    else:
        # Fallback
        resolution = random.choice(list(MOBILE_SCREEN_RESOLUTIONS.keys()))
    
    width, height = map(int, resolution.split('x'))
    return width, height

def get_mobile_platform_info(user_agent: str):
    """Get matching mobile platform info based on user agent"""
    
    # Get screen resolution first
    width, height = get_mobile_screen_resolution(user_agent)
    resolution_key = f"{width}x{height}"
    
    # Get platform info for that resolution
    if resolution_key in MOBILE_SCREEN_RESOLUTIONS:
        device_info = MOBILE_SCREEN_RESOLUTIONS[resolution_key]
        return {
            "device": device_info["device"],
            "platform": device_info["platform"],
            "memory": device_info["memory"],
            "cores": device_info["cores"]
        }
    
    # Fallback for mobile
    return {
        "device": "Mobile Device",
        "platform": "Android",
        "memory": 6,
        "cores": 8
    }

def get_mobile_touch_capabilities():
    """Get mobile touch capabilities"""
    return {
        "maxTouchPoints": random.choice([1, 5, 10]),  # Single touch or multi-touch
        "touchSupport": True,
        "pointerEvents": True
    }
