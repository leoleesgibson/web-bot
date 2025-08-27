# Bot Configuration Settings

# Session Settings
SESSION_DURATION_MINUTES = 5
PAUSE_BETWEEN_SESSIONS_SECONDS = 10

# Search Settings  
SEARCH_QUERY = "FrontPageAfrica"
TARGET_URL = "frontpageafricaonline.com"

# Proxy Settings
PROXY_USERNAME = "zruqbalk-rotate"
PROXY_PASSWORD = "z29qfcd8flic" 
PROXY_SERVER = "p.webshare.io:80"

# Browser Settings
HEADLESS_MODE = False
ENABLE_PROXY = True

# Retry Settings
PROXY_RETRY_DELAYS = [5, 10, 20, 30]  # Progressive backoff times
PROXY_TIMEOUT = 15

# Alternative Search Engines (if DuckDuckGo fails)
ALTERNATIVE_SEARCH_ENGINES = [
    "https://www.startpage.com",
    "https://www.searx.org", 
    "https://www.bing.com"
]

# Target Websites (for variety)
ALTERNATIVE_TARGETS = [
    {"query": "FrontPageAfrica news", "url": "frontpageafricaonline.com"},
    {"query": "Liberia news", "url": "frontpageafricaonline.com"},
    {"query": "West Africa news", "url": "frontpageafricaonline.com"}
]
