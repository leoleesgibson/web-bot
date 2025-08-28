# ===================================
# 🤖 WEB BOT COMPREHENSIVE CONFIGURATION
# ===================================

# ===================================
# 📱🖥️ DEVICE SIMULATION SETTINGS
# ===================================
# Device simulation modes: "mobile", "desktop", "mixed"
DEVICE_SIMULATION_MODE = "mobile"  # Options: "mobile", "desktop", "mixed"
MOBILE_DEVICE_SIMULATION = True   # Enable mobile device simulation
DESKTOP_DEVICE_SIMULATION = True # Enable desktop device simulation

# Device type distributions (when using "mixed" mode)
DEVICE_TYPE_DISTRIBUTION = {
    "mobile": 0.7,    # 70% mobile traffic
    "desktop": 0.3    # 30% desktop traffic
}

DEVICE_TYPES = ["android", "ios", "windows", "mac", "linux"]  # Supported device types

# ===================================
# 🌐 SESSION & CONCURRENCY SETTINGS  
# ===================================
SESSIONS_PER_IP = 1  # Number of concurrent mobile browsers per proxy IP
SESSION_DURATION_MIN = 3  # Minimum session duration in minutes
SESSION_DURATION_MAX = 8  # Maximum session duration in minutes

# IP Rotation Timing
IP_ROTATION_PAUSE_MIN = 0.5  # Minimum pause between proxy sessions (minutes)
IP_ROTATION_PAUSE_MAX = 2.0  # Maximum pause between proxy sessions (minutes)

# ===================================
# 📰 ARTICLE INTERACTION SETTINGS
# ===================================
# Article clicking behavior
ENABLE_ARTICLE_CLICKING = True
ARTICLE_CLICK_PROBABILITY = 0.7  # 70% chance to click articles
ARTICLES_TO_CLICK_MIN = 1        # Minimum articles to click per session
ARTICLES_TO_CLICK_MAX = 4        # Maximum articles to click per session

# Multi-tab browsing behavior
ENABLE_MULTI_TAB_BROWSING = True
TAB_OPENING_PROBABILITY = 0.4    # 40% chance to open articles in new tabs
MAX_TABS_TO_OPEN = 3            # Maximum number of tabs to open
MIN_TAB_READING_TIME = 15       # Minimum time to spend reading in each tab (seconds)
MAX_TAB_READING_TIME = 90       # Maximum time to spend reading in each tab (seconds)
TAB_CLOSE_PROBABILITY = 0.6     # 60% chance to close tabs after reading

# Article selection preferences
PREFER_RECENT_ARTICLES = True    # Prefer articles with recent dates
ARTICLE_READING_TIME_MIN = 30    # Minimum time to spend reading articles (seconds)
ARTICLE_READING_TIME_MAX = 180   # Maximum time to spend reading articles (seconds)

# ===================================
# 🎯 TARGET WEBSITE SETTINGS
# ===================================
TARGET_URL = "https://blog.com.lr/"
SEARCH_QUERY = "blog.com.lr"
USE_DIRECT_NAVIGATION = True  # True = direct navigation, False = search first

# Additional target URLs for variety (optional)
ALTERNATIVE_TARGETS = [
    {"query": "blog.com.lr news", "url": "https://blog.com.lr/"},
    {"query": "Liberia blog", "url": "https://blog.com.lr/"},
    {"query": "West Africa blog", "url": "https://blog.com.lr/"}
]

# ===================================
# 🌐 PROXY SETTINGS
# ===================================
ENABLE_PROXY = True
PROXY_SERVER = "p.webshare.io:80"
PROXY_USERNAME = "xgdfimdk-rotate"
PROXY_PASSWORD = "o6njj0dzq967"

# Proxy retry configuration
PROXY_RETRY_DELAYS = [5, 10, 20, 30]  # Progressive backoff times in seconds
PROXY_TIMEOUT = 15  # Timeout for proxy verification in seconds
PROXY_VERIFICATION_URL = "https://httpbin.org/ip"

# ===================================
# 🖥️ BROWSER SETTINGS
# ===================================
HEADLESS_MODE = False  # Set to True for headless browsing
BROWSER_TIMEOUT = 90000  # Navigation timeout in milliseconds (90 seconds)

# Mobile browser context settings
MOBILE_VIEWPORT_WIDTHS = [360, 375, 390, 393, 412, 428]  # Common mobile widths
MOBILE_VIEWPORT_HEIGHTS = [780, 800, 812, 844, 851, 896, 915, 926]  # Common mobile heights
DEVICE_SCALE_FACTORS = [1, 2, 3]  # Mobile device pixel ratios

# Desktop browser context settings
DESKTOP_VIEWPORT_WIDTHS = [1366, 1440, 1920, 2560, 3840]  # Common desktop widths
DESKTOP_VIEWPORT_HEIGHTS = [768, 900, 1080, 1440, 2160]   # Common desktop heights
DESKTOP_SCALE_FACTORS = [1, 1.25, 1.5, 2]  # Desktop DPI scaling

# ===================================
# 🎭 HUMAN BEHAVIOR SETTINGS
# ===================================
ENABLE_HUMAN_BEHAVIORS = True
ENABLE_WASTED_ACTIONS = True
ENABLE_MOUSE_MOVEMENTS_MOBILE = False  # Disabled for mobile (touch-based)
ENABLE_MOUSE_MOVEMENTS_DESKTOP = True  # Enabled for desktop (mouse-based)
ENABLE_TYPING_MISTAKES = True

# Device-specific interaction settings
MOBILE_TOUCH_ENABLED = True
DESKTOP_MOUSE_ENABLED = True
DESKTOP_KEYBOARD_SHORTCUTS = True  # Enable Ctrl+C, Ctrl+V, etc.

# Reading behavior timing (seconds)
MIN_READING_TIME = 15
MAX_READING_TIME = 60
MIN_THINKING_PAUSE = 1.0
MAX_THINKING_PAUSE = 5.0

# Click retry settings
MAX_CLICK_RETRIES = 3
CLICK_RETRY_DELAYS = [2.5, 4.0, 6.0]  # Progressive delays between retries

# ===================================
# 📊 BROWSING PATTERNS
# ===================================
ENABLE_MULTI_TAB_BROWSING = True
MAX_TABS_PER_SESSION = 4
TAB_SWITCHING_PROBABILITY = 0.3  # 30% chance to switch tabs

BOUNCE_RATE_PROBABILITY = 0.2  # 20% chance of quick exit (bounce)
BACK_BUTTON_PROBABILITY = 0.15  # 15% chance to use back button

# Page interaction settings
MIN_PAGES_PER_SESSION = 1
MAX_PAGES_PER_SESSION = 5
SCROLL_PROBABILITY = 0.8  # 80% chance to scroll on page

# ===================================
# 🔍 SEARCH ENGINE SETTINGS
# ===================================
USE_SEARCH_ENGINE = False  # Currently using direct navigation
PRIMARY_SEARCH_ENGINE = "google"  # google, duckduckgo, bing

# Alternative search engines (fallback)
ALTERNATIVE_SEARCH_ENGINES = [
    "https://www.google.com",
    "https://www.bing.com", 
    "https://duckduckgo.com"
]

# ===================================
# 📈 STATISTICS & MONITORING
# ===================================
ENABLE_DETAILED_LOGGING = True
SHOW_SUCCESS_RATE = True
SHOW_SESSION_SUMMARIES = True

# Countdown display settings
SHOW_COUNTDOWN_UPDATES = True
COUNTDOWN_UPDATE_INTERVAL = 15  # Update every 15 seconds

# ===================================
# 🛡️ ANTI-DETECTION SETTINGS
# ===================================
ENABLE_FINGERPRINT_SPOOFING = True
ENABLE_USER_AGENT_ROTATION = True
ENABLE_CANVAS_SPOOFING = True
ENABLE_WEBGL_SPOOFING = True

# PyAutoGUI settings
DISABLE_PYAUTOGUI_FAILSAFE = True

# Natural timing variance
USE_GAUSSIAN_TIMING = True  # More realistic timing patterns
TIMING_VARIANCE_FACTOR = 0.3  # 30% variance in timing

# ===================================
# 🚀 PERFORMANCE SETTINGS
# ===================================
MAX_CONCURRENT_SESSIONS = 3  # Same as SESSIONS_PER_IP
ENABLE_BACKGROUND_PROCESSING = True

# Memory and resource limits
MAX_MEMORY_USAGE_MB = 2048  # Per browser instance
CLEANUP_TEMP_FILES = True

# ===================================
# 🐛 DEBUG & TESTING SETTINGS  
# ===================================
DEBUG_MODE = False
VERBOSE_LOGGING = False
SAVE_SCREENSHOTS = False  # Save screenshots on errors
SCREENSHOT_DIR = "screenshots"

# Testing overrides
TEST_MODE = False  # Shorter sessions for testing
TEST_SESSION_DURATION = 1  # 1 minute sessions when in test mode
