# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\network\\proxy_manager.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nImproved Proxy Manager\n- Tests proxies 3-5 times before use\n- Filters dead proxies\n- Actually applies proxies to sessions\n"""
import os
import time
import random
import threading
import requests
from typing import List, Optional, Dict
from src.utils.logger import get_logger
logger = get_logger()
class ProxyManager:
    """Enhanced proxy manager with thorough testing"""
    def __init__(self, config: dict):
        """Initialize proxy manager"""
        self.enabled = config.get('enabled', False)
        self.proxy_file = config.get('file', 'proxies.txt')
        self.proxy_type = config.get('type', 'http')
        self.test_retries = config.get('test_retries', 3)
        self.test_timeout = config.get('test_timeout', 10)
        self.test_url = config.get('test_url', 'https://api.ipify.org')
        self.rotation_mode = config.get('rotation_mode', 'round_robin')
        self.raw_proxies = []
        self.working_proxies = []
        self.failed_proxies = []
        self.proxy_stats = {}
        self.current_index = 0
        self.lock = threading.Lock()
        logger.info(f'🔧 Proxy Manager: {('ENABLED' if self.enabled else 'DISABLED')}')
        if self.enabled:
            self.load_and_test_proxies()
    def load_and_test_proxies(self):
        # irreducible cflow, using cdg fallback
        """Load proxies and test them thoroughly"""
        # ***<module>.ProxyManager.load_and_test_proxies: Failure: Compilation Error
        if not os.path.exists(self.proxy_file):
            logger.error(f'❌ Proxy file not found: {self.proxy_file}')
            logger.error(f'   Create {self.proxy_file} with format: ip:port:user:pass')
            self.enabled = False
            return
        with open(self.proxy_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and (not line.startswith('#'))]
        self.raw_proxies = lines
        logger.info(f'📥 Loaded {len(self.raw_proxies)} proxies from file')
        if not self.raw_proxies:
            logger.error('❌ No proxies found in file!')
            self.enabled = False
                return
            logger.info(f'🧪 Testing proxies ({self.test_retries} attempts each)...')
            logger.info('   This may take a few minutes...')
            tested_count = 0
            for proxy in self.raw_proxies:
                tested_count += 1
                logger.info(f'   Testing proxy {tested_count}/{len(self.raw_proxies)}: {self._mask_proxy(proxy)}')
                if self._test_proxy_thoroughly(proxy):
                    self.working_proxies.append(proxy)
                    logger.info('      ✅ WORKING')
                else:
                    self.failed_proxies.append(proxy)
                    logger.warning('      ❌ DEAD')
            logger.info(f'\n{'======================================================================'}')
            logger.info('🎯 PROXY TEST RESULTS:')
            logger.info(f'   Total: {len(self.raw_proxies)}')
            logger.info(f'   ✅ Working: {len(self.working_proxies)}')
            logger.info(f'   ❌ Dead: {len(self.failed_proxies)}')
            logger.info(f'{'======================================================================'}\n')
            if not self.working_proxies:
                logger.error('❌ NO WORKING PROXIES! Disabling proxy mode.')
                self.enabled = False
                logger.info(f'✅ Ready to use {len(self.working_proxies)} working proxies!')
                except Exception as e:
                        logger.error(f'❌ Failed to load proxies: {e}')
                        self.enabled = False
    def _test_proxy_thoroughly(self, proxy: str) -> bool:
        """Test proxy multiple times (3-5) to ensure it works"""
        success_count = 0
        for attempt in range(self.test_retries):
            if self._test_proxy_once(proxy):
                success_count += 1
            time.sleep(0.5)
        required_success = max(2, self.test_retries - 1)
        return success_count >= required_success
    def _test_proxy_once(self, proxy: str) -> bool:
        # irreducible cflow, using cdg fallback
        """Test proxy once"""
        # ***<module>.ProxyManager._test_proxy_once: Failure: Compilation Error
        proxy_dict = self._format_proxy(proxy)
        response = requests.get(self.test_url, proxies=proxy_dict, timeout=self.test_timeout)
        if response.status_code == 200:
            if proxy not in self.proxy_stats:
                self.proxy_stats[proxy] = {'success': 0, 'failures': 0, 'last_used': 0}
            self.proxy_stats[proxy]['success'] += 1
                return True
            return False
            except Exception:
                    return False
    def get_proxy(self, sticky_key: Optional[str]=None) -> Optional[Dict[str, str]]:
        """\nGet next working proxy\n\nArgs:\n    sticky_key: For sticky mode (same proxy per email)\n\nReturns:\n    Proxy dict for requests, or None if disabled\n"""
        if not self.enabled or not self.working_proxies:
            return None
        else:
            with self.lock:
                if self.rotation_mode == 'round_robin':
                    proxy = self.working_proxies[self.current_index]
                    self.current_index = (self.current_index + 1) % len(self.working_proxies)
                else:
                    if self.rotation_mode == 'random':
                        proxy = random.choice(self.working_proxies)
                    else:
                        if self.rotation_mode == 'sticky' and sticky_key:
                            index = hash(sticky_key) % len(self.working_proxies)
                            proxy = self.working_proxies[index]
                        else:
                            proxy = self.working_proxies[0]
                self.proxy_stats[proxy]['last_used'] = time.time()
                return self._format_proxy(proxy)
    def _format_proxy(self, proxy: str) -> Dict[str, str]:
        """\nFormat proxy for requests library\n\nSupports:\n- ip:port\n- ip:port:user:pass\n- user:pass@ip:port\n\nReturns:\n    {\'http\': \'type://...\', \'https\': \'type://...\'}\n"""
        # ***<module>.ProxyManager._format_proxy: Failure: Different bytecode
        proxy = proxy.strip()
        if '@' in proxy:
            auth, address = proxy.split('@', 1)
            proxy_url = f'{self.proxy_type}://{auth}@{address}'
        else:
            if proxy.count(':') == 3:
                parts = proxy.split(':')
                ip, port, user, password = parts
                proxy_url = f'{self.proxy_type}://{user}:{password}@{ip}:{port}'
            else:
                if proxy.count(':') == 1:
                    proxy_url = f'{self.proxy_type}://{proxy}'
                else:
                    logger.warning(f'⚠️ Invalid proxy format: {self._mask_proxy(proxy)}')
                    proxy_url = f'{self.proxy_type}://{proxy}'
        return {'http': proxy_url, 'https': proxy_url}
    def _mask_proxy(self, proxy: str) -> str:
        """Mask proxy for safe logging"""
        if ':' in proxy:
            parts = proxy.split(':')
            if len(parts) >= 2:
                return f'{parts[0]}:****'
        return proxy[:10] + '****'
    def mark_proxy_failed(self, proxy_dict: Optional[Dict[str, str]]):
        """Mark proxy as failed (for future improvements)"""
        if not proxy_dict:
            return
        else:
            proxy_url = proxy_dict.get('http', '')
            for proxy in self.working_proxies:
                if proxy in proxy_url and proxy in self.proxy_stats:
                        self.proxy_stats[proxy]['failures'] += 1
    def get_stats(self) -> dict:
        """Get proxy statistics"""
        return {'enabled': self.enabled, 'total_loaded': len(self.raw_proxies), 'working': len(self.working_proxies), 'failed': len(self.failed_proxies), 'current_index': self.current_index}