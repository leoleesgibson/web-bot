# Webshare proxy configuration
WEBSHARE_PROXY = {
    "server": "socks5://p.webshare.io:80",
    "username": "zruqbalk-rotate",
    "password": "z29qfcd8flic"
}

# Test proxy with requests (for verification)
import requests

def test_proxy_connection():
    """Test the proxy connection using requests"""
    try:
        proxies = {
            "http": "socks5://zruqbalk-rotate:z29qfcd8flic@p.webshare.io:80/",
            "https": "socks5://zruqbalk-rotate:z29qfcd8flic@p.webshare.io:80/"
        }
        
        response = requests.get(
            "https://ipv4.webshare.io/",
            proxies=proxies,
            timeout=10
        )
        
        print("Proxy test successful!")
        print("Response:", response.text)
        return True
    except Exception as e:
        print(f"Proxy test failed: {e}")
        return False

if __name__ == "__main__":
    test_proxy_connection()
