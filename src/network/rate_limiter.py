# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\network\\rate_limiter.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global _rate_limiter
# ***<module>: Failure: Different bytecode
"""\nSmart Rate Limiter\nHandles 429 errors with exponential backoff and retries\nThread-safe per-domain rate limiting for multi-threaded checking\n"""
import time
import threading
from typing import Callable, Any, Optional, Dict
from src.utils.logger import get_logger
logger = get_logger()
class RateLimiter:
    """Smart rate limiter with exponential backoff and thread-safe per-domain delays"""
    def __init__(self, global_delay: float=0.5, per_domain: Optional[Dict[str, float]]=None):
        """\nInitialize rate limiter\n\nArgs:\n    global_delay: Global delay between all requests (seconds)\n    per_domain: Dictionary mapping domain to delay (e.g., {\'api.minecraftservices.com\': 2.0})\n"""
        self.rate_limited_until = {}
        self.request_counts = {}
        self.last_request = {}
        self.global_delay = global_delay
        self.per_domain = per_domain or {}
        self.lock = threading.Lock()
        self.domain_locks = {}
    def execute_with_retry(self, func: Callable, endpoint_name: str, max_retries: int=5, initial_wait: int=10, max_wait: int=120, *args, **kwargs) -> Any:
        """\nExecute a function with automatic retry on rate limit\n\nArgs:\n    func: Function to execute\n    endpoint_name: Name of endpoint (for tracking)\n    max_retries: Maximum number of retries\n    initial_wait: Initial wait time in seconds\n    max_wait: Maximum wait time in seconds\n    *args: Arguments for func\n    **kwargs: Keyword arguments for func\n\nReturns:\n    Result from func or None if all retries failed\n"""
        wait_time = initial_wait
        for attempt in range(max_retries):
            try:
                if endpoint_name in self.rate_limited_until:
                    wait_until = self.rate_limited_until[endpoint_name]
                    if time.time() < wait_until:
                        remaining = int(wait_until - time.time())
                        logger.warning(f'⏳ {endpoint_name} rate limited - waiting {remaining}s...')
                        time.sleep(remaining + 1)
                result = func(*args, **kwargs)
                if endpoint_name in self.rate_limited_until:
                    del self.rate_limited_until[endpoint_name]
                return result
            except Exception as e:
                error_msg = str(e).lower()
                if '429' in error_msg or 'too many' in error_msg or 'rate limit' in error_msg:
                    logger.warning(f'⚠️  Rate limit hit on {endpoint_name} (attempt {attempt + 1}/{max_retries})')
                    if attempt < max_retries - 1:
                        actual_wait = min(wait_time * 2 ** attempt, max_wait)
                        self.rate_limited_until[endpoint_name] = time.time() + actual_wait
                        logger.info(f'⏳ Waiting {actual_wait}s before retry...')
                        time.sleep(actual_wait)
                    else:
                        logger.error(f'❌ Max retries ({max_retries}) exceeded for {endpoint_name}')
                        raise
                else:
                    raise
            else:
                pass
    def wait_if_needed(self, endpoint_name: str, min_delay: Optional[float]=None):
        """\nWait if needed to respect rate limits (thread-safe)\n\nArgs:\n    endpoint_name: Name of endpoint or domain (e.g., \'api.minecraftservices.com\')\n    min_delay: Minimum delay between requests in seconds (uses per-domain or global if None)\n"""
        if min_delay is None:
            min_delay = self.per_domain.get(endpoint_name, self.global_delay)
        with self.lock:
            if endpoint_name not in self.domain_locks:
                self.domain_locks[endpoint_name] = threading.Lock()
            domain_lock = self.domain_locks[endpoint_name]
        with domain_lock:
            current_time = time.time()
            if endpoint_name in self.last_request:
                elapsed = current_time - self.last_request[endpoint_name]
                if elapsed < min_delay:
                    wait_time = min_delay - elapsed
                    if wait_time > 0:
                        time.sleep(wait_time)
            self.last_request[endpoint_name] = time.time()
    def wait_for_domain(self, url: str, min_delay: Optional[float]=None):
        """\nExtract domain from URL and wait if needed\n\nArgs:\n    url: Full URL (e.g., \'https://api.minecraftservices.com/authentication/login_with_xbox\')\n    min_delay: Override delay (uses per-domain or global if None)\n"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            self.wait_if_needed(domain, min_delay)
        except Exception as e:
            logger.debug(f'Error parsing URL for rate limiting: {e}, using global delay')
            self.wait_if_needed('global', min_delay or self.global_delay)
    def mark_rate_limited(self, endpoint_name: str, wait_seconds: int=60):
        """\nManually mark an endpoint as rate limited\n\nArgs:\n    endpoint_name: Name of endpoint\n    wait_seconds: How long to wait\n"""
        self.rate_limited_until[endpoint_name] = time.time() + wait_seconds
        logger.warning(f'⚠️  {endpoint_name} marked as rate limited for {wait_seconds}s')
_rate_limiter = None
_rate_limiter_lock = threading.Lock()
def get_rate_limiter(config: Optional[Dict]=None) -> RateLimiter:
    """\nGet global rate limiter instance (thread-safe singleton)\n\nArgs:\n    config: Optional config dict with \'global_delay\' and \'per_domain\' keys\n\nReturns:\n    RateLimiter instance\n"""
    global _rate_limiter
    # ***<module>.get_rate_limiter: Failure: Different control flow
    if _rate_limiter is None:
        with _rate_limiter_lock:
            if _rate_limiter is None:
                if config:
                    global_delay = config.get('global_delay', 0.5)
                    per_domain = config.get('per_domain', {})
                    _rate_limiter = RateLimiter(global_delay=global_delay, per_domain=per_domain)
                else:
                    _rate_limiter = RateLimiter()
        return _rate_limiter