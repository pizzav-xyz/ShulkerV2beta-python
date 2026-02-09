# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\auth\\session_manager.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global _session_manager
# ***<module>: Failure: Different bytecode
"""\nSession manager with connection pooling\nManages HTTP sessions efficiently\n"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional
import threading
from src.utils.logger import get_logger
logger = get_logger()
class SessionManager:
    """Manage HTTP sessions with connection pooling"""
    def __init__(self, pool_connections: int=10, pool_maxsize: int=20):
        """\nInitialize session manager\n\nArgs:\n    pool_connections: Number of connection pools\n    pool_maxsize: Maximum connections per pool\n"""
        self.pool_connections = pool_connections
        self.pool_maxsize = pool_maxsize
        self.sessions = {}
        self.lock = threading.Lock()
    def get_session(self, thread_id: Optional[int]=None) -> requests.Session:
        """\nGet or create session for current thread\n\nArgs:\n    thread_id: Thread ID (uses current thread if None)\n\nReturns:\n    Requests session\n"""
        if thread_id is None:
            thread_id = threading.get_ident()
        with self.lock:
            if thread_id not in self.sessions:
                self.sessions[thread_id] = self._create_session()
                logger.debug(f'Created new session for thread {thread_id}')
        return self.sessions[thread_id]
    def _create_session(self) -> requests.Session:
        """\nCreate new session with optimized settings\n\nReturns:\n    Configured requests session\n"""
        session = requests.Session()
        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=['HEAD', 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE'])
        adapter = HTTPAdapter(pool_connections=self.pool_connections, pool_maxsize=self.pool_maxsize, max_retries=retry_strategy, pool_block=False)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 'DNT': '1', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1'})
        return session
    def clear_session(self, thread_id: Optional[int]=None):
        """\nClear session for thread (reset cookies, etc.)\n\nArgs:\n    thread_id: Thread ID (uses current thread if None)\n"""
        if thread_id is None:
            thread_id = threading.get_ident()
        with self.lock:
            if thread_id in self.sessions:
                session = self.sessions[thread_id]
                session.cookies.clear()
                logger.debug(f'Cleared session for thread {thread_id}')
    def close_session(self, thread_id: Optional[int]=None):
        """\nClose and remove session for thread\n\nArgs:\n    thread_id: Thread ID (uses current thread if None)\n"""
        if thread_id is None:
            thread_id = threading.get_ident()
        with self.lock:
            if thread_id in self.sessions:
                self.sessions[thread_id].close()
                del self.sessions[thread_id]
                logger.debug(f'Closed session for thread {thread_id}')
    def close_all(self):
        """Close all sessions"""
        with self.lock:
            for thread_id, session in self.sessions.items():
                session.close()
                logger.debug(f'Closed session for thread {thread_id}')
            self.sessions.clear()
            logger.info('All sessions closed')
    def set_proxy(self, proxy: str, thread_id: Optional[int]=None):
        """\nSet proxy for session\n\nArgs:\n    proxy: Proxy string (e.g., \'http://ip:port\' or \'socks5://ip:port\')\n    thread_id: Thread ID (uses current thread if None)\n"""
        # ***<module>.SessionManager.set_proxy: Failure: Different bytecode
        session = self.get_session(thread_id)
        session.proxies = {'http': proxy, 'https': proxy}
        logger.debug(f'Set proxy for thread {thread_id or threading.get_ident()}: {proxy}')
    def clear_proxy(self, thread_id: Optional[int]=None):
        """\nClear proxy for session\n\nArgs:\n    thread_id: Thread ID (uses current thread if None)\n"""
        session = self.get_session(thread_id)
        session.proxies = {}
        logger.debug(f'Cleared proxy for thread {thread_id or threading.get_ident()}')
_session_manager = None
def get_session_manager() -> SessionManager:
    """Get global session manager instance"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager