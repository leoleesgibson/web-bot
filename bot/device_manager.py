"""
Unified Device Manager for both Mobile and Desktop simulation
Automatically selects appropriate device type based on configuration
"""
import random
import config
from .mobile_user_agents import get_mobile_user_agent, get_mobile_screen_resolution, get_mobile_platform_info, get_mobile_touch_capabilities
from .desktop_user_agents import get_desktop_user_agent, get_desktop_screen_resolution, get_desktop_platform_info, get_desktop_mouse_capabilities

def get_device_simulation_settings():
    """
    Get device simulation settings based on configuration
    Returns device type, user agent, screen resolution, platform info, and input capabilities
    """
    
    # Determine device type based on configuration
    if config.DEVICE_SIMULATION_MODE == "mobile":
        device_type = "mobile"
    elif config.DEVICE_SIMULATION_MODE == "desktop":
        device_type = "desktop"
    elif config.DEVICE_SIMULATION_MODE == "mixed":
        # Use probability distribution to choose device type
        rand = random.random()
        if rand <= config.DEVICE_TYPE_DISTRIBUTION["mobile"]:
            device_type = "mobile"
        else:
            device_type = "desktop"
    else:
        # Default fallback
        device_type = "mobile"
    
    # Get device-specific settings
    if device_type == "mobile":
        user_agent, browser_name = get_mobile_user_agent()
        screen_width, screen_height = get_mobile_screen_resolution(user_agent)
        platform_info = get_mobile_platform_info(user_agent)
        input_capabilities = get_mobile_touch_capabilities()
        
        browser_context_options = {
            "is_mobile": True,
            "has_touch": True,
            "device_scale_factor": random.choice(config.DEVICE_SCALE_FACTORS)
        }
        
    else:  # desktop
        user_agent, browser_name = get_desktop_user_agent()
        screen_width, screen_height = get_desktop_screen_resolution(user_agent)
        platform_info = get_desktop_platform_info(user_agent)
        input_capabilities = get_desktop_mouse_capabilities()
        
        browser_context_options = {
            "is_mobile": False,
            "has_touch": False,
            "device_scale_factor": random.choice(config.DESKTOP_SCALE_FACTORS)
        }
    
    return {
        "device_type": device_type,
        "user_agent": user_agent,
        "browser_name": browser_name,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "platform_info": platform_info,
        "input_capabilities": input_capabilities,
        "browser_context_options": browser_context_options
    }

def get_device_emoji(device_type: str):
    """Get appropriate emoji for device type"""
    return "📱" if device_type == "mobile" else "🖥️"

def get_device_description(device_info: dict):
    """Get human-readable device description"""
    device_type = device_info["device_type"]
    browser_name = device_info["browser_name"] 
    platform_info = device_info["platform_info"]
    screen_width = device_info["screen_width"]
    screen_height = device_info["screen_height"]
    
    emoji = get_device_emoji(device_type)
    
    return f"{emoji} Using {browser_name}: {platform_info['device']} ({screen_width}x{screen_height}), {platform_info['memory']}GB RAM"

def should_enable_mouse_movements(device_type: str):
    """Determine if mouse movements should be enabled based on device type"""
    if device_type == "mobile":
        return config.ENABLE_MOUSE_MOVEMENTS_MOBILE
    else:  # desktop
        return config.ENABLE_MOUSE_MOVEMENTS_DESKTOP
