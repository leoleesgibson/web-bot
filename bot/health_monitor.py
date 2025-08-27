import psutil
import asyncio
import os
import time
from typing import Dict, List

class SystemHealthMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.session_history = []
        self.warning_thresholds = {
            'memory_percent': 85,
            'cpu_percent': 90,
            'disk_percent': 95
        }
    
    def check_system_health(self) -> Dict:
        """Check system resources and return health status"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            
            # CPU usage (average over 1 second)
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Process count
            process_count = len(psutil.pids())
            
            health_status = {
                'memory': {
                    'percent': memory.percent,
                    'available_gb': round(memory.available / (1024**3), 1),
                    'total_gb': round(memory.total / (1024**3), 1)
                },
                'cpu': {
                    'percent': cpu_percent,
                    'cores': psutil.cpu_count()
                },
                'disk': {
                    'percent': round((disk.used / disk.total) * 100, 1),
                    'free_gb': round(disk.free / (1024**3), 1),
                    'total_gb': round(disk.total / (1024**3), 1)
                },
                'processes': process_count,
                'uptime_hours': round((time.time() - self.start_time) / 3600, 1)
            }
            
            # Check for warnings
            warnings = []
            if health_status['memory']['percent'] > self.warning_thresholds['memory_percent']:
                warnings.append(f"High memory usage: {health_status['memory']['percent']:.1f}%")
            
            if health_status['cpu']['percent'] > self.warning_thresholds['cpu_percent']:
                warnings.append(f"High CPU usage: {health_status['cpu']['percent']:.1f}%")
            
            if health_status['disk']['percent'] > self.warning_thresholds['disk_percent']:
                warnings.append(f"Low disk space: {health_status['disk']['percent']:.1f}% used")
            
            health_status['warnings'] = warnings
            health_status['healthy'] = len(warnings) == 0
            
            return health_status
            
        except Exception as e:
            return {
                'error': f"Health check failed: {e}",
                'healthy': False,
                'warnings': [f"Health monitoring error: {e}"]
            }
    
    def should_pause_for_recovery(self) -> bool:
        """Check if system needs a recovery pause"""
        health = self.check_system_health()
        
        if not health.get('healthy', True):
            return True
        
        # Check recent failure rate
        if len(self.session_history) >= 5:
            recent_sessions = self.session_history[-5:]
            failure_rate = sum(1 for s in recent_sessions if not s['success']) / len(recent_sessions)
            
            if failure_rate >= 0.6:  # 60% failure rate
                return True
        
        return False
    
    async def recovery_pause(self, duration_minutes: int = 2):
        """Pause for system recovery"""
        print(f"🏥 System needs recovery - pausing for {duration_minutes} minutes...")
        
        # Clear some system resources
        try:
            # Force garbage collection
            import gc
            gc.collect()
            
            # Clear temporary files
            temp_dirs = ['/tmp', os.path.join(os.getcwd(), 'user_data')]
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        if file.startswith('bot_') and file.endswith('_'):
                            try:
                                file_path = os.path.join(temp_dir, file)
                                if os.path.isdir(file_path):
                                    import shutil
                                    shutil.rmtree(file_path)
                            except:
                                pass
        except:
            pass
        
        await asyncio.sleep(duration_minutes * 60)
        print("🔄 Recovery complete - resuming operations...")
    
    def add_session_result(self, session_num: int, success: bool, duration: float, errors: List = None):
        """Add session result to history"""
        self.session_history.append({
            'session': session_num,
            'success': success,
            'duration': duration,
            'errors': errors or [],
            'timestamp': time.time()
        })
        
        # Keep only last 20 sessions in memory
        if len(self.session_history) > 20:
            self.session_history = self.session_history[-20:]
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""
        if not self.session_history:
            return {}
        
        total_sessions = len(self.session_history)
        successful_sessions = sum(1 for s in self.session_history if s['success'])
        average_duration = sum(s['duration'] for s in self.session_history) / total_sessions
        
        return {
            'total_sessions': total_sessions,
            'success_rate': round((successful_sessions / total_sessions) * 100, 1),
            'average_duration_minutes': round(average_duration, 1),
            'uptime_hours': round((time.time() - self.start_time) / 3600, 1)
        }
