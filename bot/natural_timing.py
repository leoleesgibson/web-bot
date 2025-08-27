"""
Natural timing patterns using statistical distributions
Replaces fixed time ranges with realistic human variability
"""
import random
import numpy as np

def gaussian_reading_time(base_seconds: int, variance_factor: float = 0.3) -> int:
    """
    Generate reading time using Gaussian distribution for natural variance
    
    Args:
        base_seconds: Average reading time 
        variance_factor: How much variance (0.1 = 10% variance, 0.3 = 30% variance)
    
    Returns:
        Natural reading time in seconds
    """
    # Calculate standard deviation
    std_dev = base_seconds * variance_factor
    
    # Generate time using normal distribution
    reading_time = np.random.normal(base_seconds, std_dev)
    
    # Ensure it's not negative and within reasonable bounds
    min_time = max(5, base_seconds * 0.3)  # At least 30% of base time
    max_time = base_seconds * 2.5  # At most 250% of base time
    
    return int(max(min_time, min(max_time, reading_time)))

def article_reading_time() -> int:
    """Generate realistic article reading time (30-120 seconds avg)"""
    # Most people read articles for 45-75 seconds
    base_time = random.randint(45, 75)
    return gaussian_reading_time(base_time, variance_factor=0.4)

def page_scanning_time() -> int:
    """Generate time for scanning/skimming a page (15-40 seconds avg)"""
    base_time = random.randint(20, 35)
    return gaussian_reading_time(base_time, variance_factor=0.5)

def deep_reading_time() -> int:
    """Generate time for careful reading (60-180 seconds avg)"""
    base_time = random.randint(80, 140)
    return gaussian_reading_time(base_time, variance_factor=0.3)

def quick_glance_time() -> int:
    """Generate time for quick page glance (5-20 seconds avg)"""
    base_time = random.randint(8, 15)
    return gaussian_reading_time(base_time, variance_factor=0.6)

def thinking_pause_time() -> float:
    """Generate natural thinking pause between actions"""
    # Humans pause 1-8 seconds between major actions
    base_time = random.uniform(2.0, 5.0)
    std_dev = base_time * 0.4
    
    pause = np.random.normal(base_time, std_dev)
    return max(0.5, min(12.0, pause))  # 0.5 to 12 seconds

def scroll_interval_time() -> float:
    """Time between scroll actions during reading"""
    # Humans scroll every 2-8 seconds while reading
    base_time = random.uniform(3.0, 6.0)
    std_dev = base_time * 0.3
    
    interval = np.random.normal(base_time, std_dev)
    return max(1.0, min(15.0, interval))

def human_typing_speed() -> float:
    """Generate natural typing delay per character (40-80 WPM)"""
    # Average typing: 60 WPM = 5 chars/sec = 0.2 sec/char
    # Add natural variance
    base_speed = random.uniform(0.12, 0.25)  # 12-25ms per character
    variance = base_speed * 0.4
    
    speed = np.random.normal(base_speed, variance)
    return max(0.05, min(0.5, speed))

def page_visit_depth() -> int:
    """
    Determine how many pages to visit in a session
    Uses weighted distribution to mimic real user behavior
    """
    # Real user behavior: most people visit 1-3 pages, some go deeper
    depths = [1, 2, 3, 4, 5, 6, 7, 8]
    weights = [0.35, 0.25, 0.20, 0.10, 0.05, 0.03, 0.015, 0.005]  # Most visit 1-3 pages
    
    return np.random.choice(depths, p=weights)

def session_duration_minutes() -> int:
    """
    Generate realistic session duration 
    Most users spend 2-6 minutes, few go longer
    """
    # Use log-normal distribution - most short sessions, few long ones
    mean_log = 1.5  # ln(4.5) ≈ 4.5 minutes average
    sigma_log = 0.4
    
    duration = np.random.lognormal(mean_log, sigma_log)
    
    # Clamp to reasonable bounds (2-12 minutes)
    return int(max(2, min(12, duration)))

def bounce_probability() -> float:
    """
    Probability of bouncing (leaving quickly) based on realistic user behavior
    """
    # 30% of users bounce within first 30 seconds
    return 0.3

def multi_tab_probability() -> float:
    """
    Probability of opening multiple articles in tabs (advanced behavior)
    """
    # 20% of users open multiple tabs
    return 0.2

def back_button_probability() -> float:
    """
    Probability of using back button instead of clicking new links
    """
    # 40% of navigation uses back button
    return 0.4

def scroll_back_probability() -> float:
    """
    Probability of scrolling back up to re-read something
    """
    # 25% of reading sessions include backtracking
    return 0.25

def get_reading_pattern() -> dict:
    """
    Generate a complete reading pattern for a session
    """
    pattern = {
        'session_duration': session_duration_minutes(),
        'pages_to_visit': page_visit_depth(),
        'will_bounce_early': random.random() < bounce_probability(),
        'will_use_tabs': random.random() < multi_tab_probability(),
        'prefers_back_button': random.random() < back_button_probability(),
        'will_scroll_back': random.random() < scroll_back_probability()
    }
    
    # If bouncing early, limit pages and duration
    if pattern['will_bounce_early']:
        pattern['pages_to_visit'] = 1
        pattern['session_duration'] = min(pattern['session_duration'], 2)
    
    return pattern
