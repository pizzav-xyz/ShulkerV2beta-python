# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\utils\\resource_monitor.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nResource Monitor - Monitor CPU/Memory and auto-adjust threads\nPrevents system from hanging\n"""
import psutil
import time
import threading
from typing import Optional
from src.utils.logger import get_logger
logger = get_logger()
class ResourceMonitor:
    """Monitor system resources and adjust threads"""
    def __init__(self, config: dict):
        """\nInitialize resource monitor\n\nArgs:\n    config: Monitoring configuration\n"""
        self.enabled = config.get('enabled', True)
        self.check_interval = config.get('check_interval', 5.0)
        self.cpu_threshold = config.get('cpu_threshold', 80.0)
        self.memory_threshold = config.get('memory_threshold', 85.0)
        self.auto_adjust = config.get('auto_adjust', True)
        self.monitoring = False
        self.monitor_thread = None
        self._stop_event = threading.Event()
        self.current_cpu = 0.0
        self.current_memory = 0.0
        self.warnings_issued = 0
        logger.info(f'Resource monitor initialized (enabled={self.enabled})')
    def start_monitoring(self):
        """Start background monitoring thread"""
        if not self.enabled or self.monitoring:
            return None
        else:
            self.monitoring = True
            self._stop_event.clear()
            self.monitor_thread = threading.Thread(target=self._monitor_loop, name='ResourceMonitor', daemon=True)
            self.monitor_thread.start()
            logger.info('Resource monitoring started')
    def stop_monitoring(self):
        """Stop monitoring thread"""
        if not self.monitoring:
            return
        else:
            self._stop_event.set()
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2)
            self.monitoring = False
            logger.info('Resource monitoring stopped')
    def _monitor_loop(self):
        """Background monitoring loop"""
        # ***<module>.ResourceMonitor._monitor_loop: Failure: Different control flow
        if not self._stop_event.is_set():
            pass
        while True:
            try:
                self.current_cpu = psutil.cpu_percent(interval=1)
                self.current_memory = psutil.virtual_memory().percent
                if self.current_cpu > self.cpu_threshold:
                    self.warnings_issued += 1
                    logger.warning(f'⚠️  High CPU usage: {self.current_cpu:.1f}%')
                if self.current_memory > self.memory_threshold:
                    self.warnings_issued += 1
                    logger.warning(f'⚠️  High memory usage: {self.current_memory:.1f}%')
                self._stop_event.wait(self.check_interval)
            except Exception as e:
                logger.error(f'Resource monitoring error: {e}')
                time.sleep(self.check_interval)
    def should_reduce_threads(self) -> bool:
        """\nCheck if threads should be reduced\n\nReturns:\n    True if resource usage is too high\n"""
        if not self.enabled or not self.auto_adjust:
            return False
        else:
            return self.current_cpu > self.cpu_threshold or self.current_memory > self.memory_threshold
    def get_recommended_threads(self, current_threads: int) -> int:
        """\nGet recommended thread count based on resources\n\nArgs:\n    current_threads: Current thread count\n\nReturns:\n    Recommended thread count\n"""
        if not self.enabled or not self.auto_adjust:
            return current_threads
        else:
            if self.current_cpu > self.cpu_threshold:
                return max(1, current_threads - 1)
            else:
                if self.current_memory > self.memory_threshold:
                    return max(1, current_threads - 1)
                else:
                    if self.current_cpu < 50 and self.current_memory < 60:
                        return current_threads + 1
                    else:
                        return current_threads
    def get_stats(self) -> dict:
        """Get monitoring statistics"""
        return {'enabled': self.enabled, 'monitoring': self.monitoring, 'cpu_percent': self.current_cpu, 'memory_percent': self.current_memory, 'cpu_threshold': self.cpu_threshold, 'memory_threshold': self.memory_threshold, 'warnings_issued': self.warnings_issued}
    def get_system_info(self) -> dict:
        """Get detailed system information"""
        try:
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            memory = psutil.virtual_memory()
            return {'cpu_count': cpu_count, 'cpu_physical': psutil.cpu_count(logical=False), 'cpu_freq_current': cpu_freq.current if cpu_freq else 0, 'cpu_freq_max': cpu_freq.max if cpu_freq else 0, 'memory_total_gb': memory.total / 1073741824, 'memory_available_gb': memory.available / 1073741824, 'memory_used_gb': memory.used / 1073741824}
        except Exception as e:
            logger.error(f'Failed to get system info: {e}')
            return {}