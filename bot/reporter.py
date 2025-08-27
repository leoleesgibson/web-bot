import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List

class SessionReporter:
    def __init__(self):
        self.stats_file = os.path.join(os.getcwd(), 'session_stats.json')
        self.daily_stats = {}
        self.load_existing_stats()
    
    def load_existing_stats(self):
        """Load existing statistics from file"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    self.daily_stats = json.load(f)
        except:
            self.daily_stats = {}
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.daily_stats, f, indent=2)
        except Exception as e:
            print(f"Failed to save stats: {e}")
    
    def record_session(self, session_data: Dict):
        """Record session data"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today not in self.daily_stats:
            self.daily_stats[today] = {
                'sessions': [],
                'summary': {
                    'total_sessions': 0,
                    'successful_sessions': 0,
                    'failed_sessions': 0,
                    'total_duration_minutes': 0,
                    'total_pages_visited': 0,
                    'unique_ips': set()
                }
            }
        
        # Add session data
        self.daily_stats[today]['sessions'].append(session_data)
        
        # Update summary
        summary = self.daily_stats[today]['summary']
        summary['total_sessions'] += 1
        
        if session_data.get('success', False):
            summary['successful_sessions'] += 1
        else:
            summary['failed_sessions'] += 1
        
        summary['total_duration_minutes'] += session_data.get('duration', 0)
        summary['total_pages_visited'] += session_data.get('pages_visited', 0)
        
        if session_data.get('proxy_ip'):
            if isinstance(summary['unique_ips'], set):
                summary['unique_ips'].add(session_data['proxy_ip'])
            else:
                summary['unique_ips'] = {session_data['proxy_ip']}
        
        # Convert set to list for JSON serialization
        if isinstance(summary['unique_ips'], set):
            summary['unique_ips'] = list(summary['unique_ips'])
        
        self.save_stats()
    
    def generate_daily_report(self, date: str | None = None) -> str:
        """Generate daily report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if date not in self.daily_stats:
            return f"No data available for {date}"
        
        data = self.daily_stats[date]
        summary = data['summary']
        
        success_rate = 0
        if summary['total_sessions'] > 0:
            success_rate = (summary['successful_sessions'] / summary['total_sessions']) * 100
        
        avg_duration = 0
        if summary['successful_sessions'] > 0:
            avg_duration = summary['total_duration_minutes'] / summary['successful_sessions']
        
        unique_ips = summary.get('unique_ips', [])
        if isinstance(unique_ips, set):
            unique_ips = list(unique_ips)
        
        report = f"""
📊 DAILY REPORT - {date}
{'='*50}
🔢 Total Sessions: {summary['total_sessions']}
✅ Successful: {summary['successful_sessions']}
❌ Failed: {summary['failed_sessions']}
📈 Success Rate: {success_rate:.1f}%

⏱️ Total Runtime: {summary['total_duration_minutes']:.1f} minutes
⏱️ Average Session: {avg_duration:.1f} minutes
📄 Pages Visited: {summary['total_pages_visited']}
🌐 Unique IPs: {len(unique_ips)}

🔗 IP Addresses Used:
{chr(10).join(f'   • {ip}' for ip in unique_ips)}
{'='*50}
        """
        
        return report.strip()
    
    def generate_weekly_summary(self) -> str:
        """Generate weekly summary"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        weekly_data = {
            'total_sessions': 0,
            'successful_sessions': 0,
            'failed_sessions': 0,
            'total_duration': 0,
            'total_pages': 0,
            'unique_ips': set()
        }
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            if date_str in self.daily_stats:
                summary = self.daily_stats[date_str]['summary']
                weekly_data['total_sessions'] += summary['total_sessions']
                weekly_data['successful_sessions'] += summary['successful_sessions']
                weekly_data['failed_sessions'] += summary['failed_sessions']
                weekly_data['total_duration'] += summary['total_duration_minutes']
                weekly_data['total_pages'] += summary['total_pages_visited']
                
                unique_ips = summary.get('unique_ips', [])
                if isinstance(unique_ips, list):
                    weekly_data['unique_ips'].update(unique_ips)
            
            current_date += timedelta(days=1)
        
        success_rate = 0
        if weekly_data['total_sessions'] > 0:
            success_rate = (weekly_data['successful_sessions'] / weekly_data['total_sessions']) * 100
        
        report = f"""
📊 WEEKLY SUMMARY ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})
{'='*60}
🔢 Total Sessions: {weekly_data['total_sessions']}
✅ Successful: {weekly_data['successful_sessions']}
❌ Failed: {weekly_data['failed_sessions']}
📈 Success Rate: {success_rate:.1f}%

⏱️ Total Runtime: {weekly_data['total_duration']:.1f} minutes ({weekly_data['total_duration']/60:.1f} hours)
📄 Total Pages Visited: {weekly_data['total_pages']}
🌐 Unique IP Addresses: {len(weekly_data['unique_ips'])}
📅 Average Sessions/Day: {weekly_data['total_sessions']/7:.1f}
{'='*60}
        """
        
        return report.strip()
