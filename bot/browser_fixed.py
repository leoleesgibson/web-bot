import random
import os
import asyncio
import tempfile
import uuid
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from .user_agents import get_random_user_agent, get_matching_screen_resolution, get_matching_platform_info

class BrowserManager:
    def __init__(self, headless: bool = False, use_proxy: bool = True, session_id: str | None = None):
        self.headless = headless
        self.use_proxy = use_proxy
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    async def verify_proxy_connection(self):
        """Verify proxy connection before starting browser session - retry forever until it works"""
        if not self.use_proxy:
            return True
            
        print(f"[{self.session_id}] Verifying proxy connection...")
        
        attempt = 0
        while True:
            attempt += 1
            try:
                import requests
                proxies = {
                    "http": "http://zruqbalk-rotate:z29qfcd8flic@p.webshare.io:80",
                    "https": "http://zruqbalk-rotate:z29qfcd8flic@p.webshare.io:80"
                }
                
                response = requests.get(
                    "https://httpbin.org/ip", 
                    proxies=proxies, 
                    timeout=15
                )
                
                if response.status_code == 200:
                    proxy_ip = response.json().get('origin', 'Unknown')
                    print(f"[{self.session_id}] ✅ Proxy verified! IP: {proxy_ip}")
                    return True
                else:
                    raise Exception(f"HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"[{self.session_id}] ❌ Proxy verification failed: {str(e)[:50]}...")
                
                # Progressive backoff: longer waits after more failures  
                if attempt <= 3:
                    wait_time = random.uniform(5, 10)
                elif attempt <= 10:
                    wait_time = random.uniform(10, 20)
                else:
                    wait_time = random.uniform(20, 30)
                
                print(f"[{self.session_id}] Retrying in {wait_time:.1f} seconds...")
                await asyncio.sleep(wait_time)

    async def start(self):
        # Verify proxy connection first
        await self.verify_proxy_connection()
        
        self.playwright = await async_playwright().start()

        # Create a temporary user data directory for each session
        temp_dir = tempfile.mkdtemp(prefix=f"bot_{self.session_id}_")

        # Get realistic user agent and matching system specs
        user_agent, browser_name = get_random_user_agent()
        screen_width, screen_height = get_matching_screen_resolution(user_agent)
        platform_info = get_matching_platform_info(user_agent)
        
        print(f"[{self.session_id}] 🎭 Using {browser_name} fingerprint: {screen_width}x{screen_height}, {platform_info['memory']}GB RAM")

        # Launch browser with fresh session
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-notifications",
                "--disable-popup-blocking",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-extensions-file-access-check",
                "--disable-extensions-http-throttling",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-component-extensions-with-background-pages",
                "--disable-renderer-backgrounding",
                "--disable-field-trial-config",
                "--disable-ipc-flooding-protection",
                "--exclude-switches=enable-automation",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        # Create context with proxy and realistic settings that match user agent
        context_options = {
            "viewport": {
                "width": screen_width,
                "height": screen_height
            },
            "user_agent": user_agent,
            "locale": "en-US",
            "timezone_id": "America/New_York"
        }

        if self.use_proxy:
            context_options["proxy"] = {
                "server": "http://p.webshare.io:80",
                "username": "zruqbalk-rotate",
                "password": "z29qfcd8flic"
            }

        self.context = await self.browser.new_context(**context_options)
        self.page = await self.context.new_page()
        
        # Hide automation detection with comprehensive fingerprint spoofing
        fingerprint_script = f"""
            // Remove webdriver property completely
            delete navigator.__proto__.webdriver;
            Object.defineProperty(navigator, 'webdriver', {{
                get: () => undefined,
            }});
            
            // Override automation detection
            Object.defineProperty(navigator, 'permissions', {{
                get: () => ({{
                    query: () => Promise.resolve({{ state: 'granted' }})
                }})
            }});
            
            // Mock chrome object properly
            window.chrome = {{
                runtime: {{}},
                loadTimes: function() {{}},
                csi: function() {{}},
                app: {{}}
            }};
            
            // Mock plugins with realistic data
            Object.defineProperty(navigator, 'plugins', {{
                get: () => ({{
                    0: {{ name: 'Chrome PDF Plugin' }},
                    1: {{ name: 'Chrome PDF Viewer' }},
                    2: {{ name: 'Native Client' }},
                    length: 3
                }})
            }});
            
            // Mock languages consistently
            Object.defineProperty(navigator, 'languages', {{
                get: () => ['en-US', 'en']
            }});
            
            // Spoof canvas fingerprinting with consistent noise
            const canvasProto = HTMLCanvasElement.prototype;
            const originalToDataURL = canvasProto.toDataURL;
            canvasProto.toDataURL = function(...args) {{
                const context = this.getContext('2d');
                if (context) {{
                    // Add consistent but small noise
                    const imageData = context.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {{
                        imageData.data[i] += Math.floor(Math.sin(i) * 2);
                        imageData.data[i + 1] += Math.floor(Math.cos(i) * 2);
                        imageData.data[i + 2] += Math.floor(Math.sin(i + 1) * 2);
                    }}
                    context.putImageData(imageData, 0, 0);
                }}
                return originalToDataURL.apply(this, args);
            }};
            
            // Spoof WebGL fingerprinting consistently
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return 'Intel Inc.'; // UNMASKED_VENDOR_WEBGL
                if (parameter === 37446) return 'Intel(R) UHD Graphics 620'; // UNMASKED_RENDERER_WEBGL
                if (parameter === 7936) return 'WebGL 1.0 (OpenGL ES 2.0 Chromium)'; // VERSION
                if (parameter === 7937) return 'WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)'; // SHADING_LANGUAGE_VERSION
                return getParameter.apply(this, arguments);
            }};
            
            // Spoof audio context fingerprinting
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {{
                const originalCreateAnalyser = AudioContext.prototype.createAnalyser;
                AudioContext.prototype.createAnalyser = function() {{
                    const analyser = originalCreateAnalyser.apply(this, arguments);
                    const originalGetFloatFrequencyData = analyser.getFloatFrequencyData;
                    analyser.getFloatFrequencyData = function(array) {{
                        const result = originalGetFloatFrequencyData.apply(this, arguments);
                        // Add consistent small noise to audio fingerprinting
                        for (let i = 0; i < array.length; i++) {{
                            array[i] += Math.sin(i * 0.1) * 0.0001;
                        }}
                        return result;
                    }};
                    return analyser;
                }};
            }}
            
            // Consistent timezone spoofing (EST)
            Date.prototype.getTimezoneOffset = () => 300; // -5 hours from UTC
            
            // Spoof hardware specs to match user agent
            Object.defineProperty(navigator, 'deviceMemory', {{
                get: () => {platform_info['memory']}, // Match UA specs
            }});
            Object.defineProperty(navigator, 'hardwareConcurrency', {{
                get: () => {platform_info['cores']}, // Match UA specs  
            }});
            
            // Spoof screen dimensions to match viewport
            Object.defineProperty(screen, 'width', {{ get: () => {screen_width} }});
            Object.defineProperty(screen, 'height', {{ get: () => {screen_height} }});
            Object.defineProperty(screen, 'availWidth', {{ get: () => {screen_width} }});
            Object.defineProperty(screen, 'availHeight', {{ get: () => {screen_height - 40} }});
            Object.defineProperty(screen, 'colorDepth', {{ get: () => 24 }});
            Object.defineProperty(screen, 'pixelDepth', {{ get: () => 24 }});
            
            // Remove automation indicators
            if (navigator.webdriver) {{
                delete navigator.webdriver;
            }}
            
            // Override permission query
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({{ state: 'granted' }}) :
                    originalQuery(parameters)
            );
        """
        
        await self.page.add_init_script(fingerprint_script)
            
        print(f"[{self.session_id}] Fresh browser session started with User Agent: {user_agent[:50]}...")
        
        return self.page

    async def close(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
