import asyncio
import random
import time
from bot.browser import BrowserManager
from bot.actions import search_and_navigate, browse_like_human, direct_navigate_and_browse
import config

async def run_multiple_sessions_per_ip(proxy_session_number: int, sessions_per_ip: int | None = None):
    """Run multiple browser sessions simultaneously on the same proxy IP"""
    if sessions_per_ip is None:
        sessions_per_ip = config.SESSIONS_PER_IP
        
    print(f"\n{'='*70}")
    print(f"🌐 Starting Proxy Session {proxy_session_number} - {sessions_per_ip} concurrent mobile browsers")
    print(f"{'='*70}")
    
    # Create tasks for all sessions that will run concurrently
    session_tasks = []
    for i in range(sessions_per_ip):
        session_number = f"{proxy_session_number}-{i+1}"
        session_duration = random.randint(config.SESSION_DURATION_MIN, config.SESSION_DURATION_MAX)
        task = asyncio.create_task(
            run_single_mobile_session(session_number, session_duration)
        )
        session_tasks.append(task)
    
    # Run all sessions concurrently and wait for completion
    results = await asyncio.gather(*session_tasks, return_exceptions=True)
    
    # Count successes
    successful = sum(1 for result in results if result is True)
    failed = len(results) - successful
    
    print(f"\n📊 PROXY SESSION {proxy_session_number} COMPLETE:")
    print(f"   ✅ Successful mobile sessions: {successful}/{sessions_per_ip}")
    print(f"   ❌ Failed mobile sessions: {failed}/{sessions_per_ip}")
    
    return successful, failed

async def run_single_mobile_session(session_number: str, session_duration: int):
    """Run a single mobile bot session with randomized duration"""
    session_id = f"Mobile-{session_number}"
    browser_manager = None
    
    try:
        print(f"\n📱 Starting {session_id} (Duration: {session_duration} minutes)")
        
        # Start mobile browser session (proxy will be verified inside BrowserManager)
        print(f"[{session_id}] 🚀 Launching mobile browser...")
        browser_manager = BrowserManager(
            headless=config.HEADLESS_MODE, 
            use_proxy=config.ENABLE_PROXY, 
            session_id=session_id
        )
        
        page = await browser_manager.start()

        search_query = config.SEARCH_QUERY
        target_url = config.TARGET_URL

        # Navigate directly to the target website (no search needed)
        print(f"[{session_id}] 📍 Navigating directly to target website...")
        await direct_navigate_and_browse(page, target_url, session_id)
        
        # Browse the website like a human for the specified duration
        print(f"[{session_id}] 📖 Starting {session_duration}-minute mobile browsing session...")
        start_time = time.time()
        await browse_like_human(page, session_duration_minutes=session_duration, session_id=session_id)
        
        actual_duration = (time.time() - start_time) / 60
        print(f"[{session_id}] ✅ Mobile session completed after {actual_duration:.1f} minutes")
        
        return True
        
    except Exception as e:
        print(f"[{session_id}] ❌ Mobile session failed with error: {str(e)[:100]}...")
        return False
        
    finally:
        # Always clean up browser resources
        if browser_manager:
            try:
                print(f"[{session_id}] 🔄 Closing mobile browser...")
                await browser_manager.close()
                print(f"[{session_id}] ✅ Mobile browser closed successfully")
            except Exception as e:
                print(f"[{session_id}] ⚠️ Error closing mobile browser: {e}")
    session_id = f"Session-{session_number}"
    browser_manager = None
    
    # Randomize session duration if not specified (3-8 minutes)
    if session_duration is None:
        session_duration = random.randint(3, 8)
    
    try:
        print(f"\n{'='*60}")
        print(f"🚀 Starting {session_id} (Duration: {session_duration} minutes)")
        print(f"{'='*60}")
        
        # Start browser session (proxy will be verified inside BrowserManager)
        print(f"[{session_id}] Launching browser...")
        browser_manager = BrowserManager(
            headless=False, 
            use_proxy=True, 
            session_id=session_id
        )
        
        page = await browser_manager.start()

        search_query = "website.com.lr"
        target_url = "https://website.com.lr"

        # Navigate directly to the target website (no search needed)
        print(f"[{session_id}] Navigating directly to target website...")
        await direct_navigate_and_browse(page, target_url, session_id)
        
        # Browse the website like a human for the specified duration
        print(f"[{session_id}] Starting {session_duration}-minute browsing session...")
        start_time = time.time()
        await browse_like_human(page, session_duration_minutes=session_duration, session_id=session_id)
        
        actual_duration = (time.time() - start_time) / 60
        print(f"[{session_id}] Session completed after {actual_duration:.1f} minutes")
        
        return True
        
    except Exception as e:
        print(f"[{session_id}] ❌ Session failed with error: {str(e)[:100]}...")
        return False
        
    finally:
        # Always clean up browser resources
        if browser_manager:
            try:
                print(f"[{session_id}] Closing browser...")
                await browser_manager.close()
                print(f"[{session_id}] ✅ Browser closed successfully")
            except Exception as e:
                print(f"[{session_id}] ⚠️ Error closing browser: {e}")

async def run_continuous_mobile_sessions():
    """
    Run continuous multi-session setups with mobile devices
    Each proxy connection runs 3 concurrent mobile browser sessions
    """
    proxy_session_number = 0
    total_successful_sessions = 0
    total_failed_sessions = 0
    start_time = time.time()
    
    print("🤖 CONTINUOUS MOBILE BOT RUNNER STARTED")
    print("=" * 70)
    print("📱 Mobile device simulation: Android & iOS")
    print("🔄 3 concurrent mobile browsers per proxy connection")
    print("⏰ Session duration: 3-8 minutes per browser (randomized)")
    print("🛡️ Proxy connection will be verified before each session")
    print("🎭 Advanced mobile behaviors and fingerprint spoofing enabled")
    print("🛑 Press Ctrl+C to stop the program")
    print("=" * 70)
    
    try:
        while True:
            proxy_session_number += 1
            
            print(f"\n⏳ Preparing proxy session {proxy_session_number} ({config.SESSIONS_PER_IP} mobile browsers)...")
            
            # Run concurrent mobile sessions on the same proxy IP
            successful, failed = await run_multiple_sessions_per_ip(
                proxy_session_number, 
                sessions_per_ip=config.SESSIONS_PER_IP
            )
            
            total_successful_sessions += successful
            total_failed_sessions += failed
            total_sessions = proxy_session_number * config.SESSIONS_PER_IP
            
            # Show summary statistics
            total_time = (time.time() - start_time) / 60
            print(f"\n📊 SUMMARY AFTER PROXY SESSION {proxy_session_number}:")
            print(f"   ✅ Successful mobile sessions: {total_successful_sessions}")
            print(f"   ❌ Failed mobile sessions: {total_failed_sessions}")
            print(f"   📱 Total mobile browsers launched: {total_sessions}")
            print(f"   ⏱️ Total runtime: {total_time:.1f} minutes")
            print(f"   📈 Success rate: {(total_successful_sessions/total_sessions)*100:.1f}%")
            
            # Randomized pause between proxy sessions (from config)
            pause_minutes = random.uniform(config.IP_ROTATION_PAUSE_MIN, config.IP_ROTATION_PAUSE_MAX)
            pause_seconds = pause_minutes * 60
            print(f"\n⏸️ IP rotation pause: {pause_minutes:.1f} minutes before next proxy session...")
            
            # Show countdown for pauses
            if pause_seconds > 30:
                remaining = pause_seconds
                while remaining > 0:
                    if remaining > 60:
                        print(f"   ⏳ {remaining:.0f} seconds remaining...")
                        sleep_time = min(15, remaining)  # Update every 15 seconds
                    else:
                        print(f"   ⏳ {remaining:.0f} seconds remaining...")
                        sleep_time = remaining
                    
                    await asyncio.sleep(sleep_time)
                    remaining -= sleep_time
            else:
                await asyncio.sleep(pause_seconds)
                        
    except KeyboardInterrupt:
        total_time = (time.time() - start_time) / 60
        total_sessions = proxy_session_number * 3 if proxy_session_number > 0 else 0
        
        print(f"\n\n🛑 Program stopped by user after {total_time:.1f} minutes")
        print("=" * 70)
        print("📊 FINAL STATISTICS:")
        print(f"   🌐 Proxy sessions completed: {proxy_session_number}")
        print(f"   📱 Total mobile browsers: {total_sessions}")
        print(f"   ✅ Successful sessions: {total_successful_sessions}")
        print(f"   ❌ Failed sessions: {total_failed_sessions}")
        if total_sessions > 0:
            print(f"   📈 Overall success rate: {(total_successful_sessions/total_sessions)*100:.1f}%")
        print(f"   ⏱️ Total runtime: {total_time:.1f} minutes")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        print("Program will exit.")

if __name__ == "__main__":
    asyncio.run(run_continuous_mobile_sessions())
