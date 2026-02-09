# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checkers\\security_checker.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nSecurity Info Checker\nDetects: pending security change, 2FA enabled, or clean (email/phone only)\n"""
import re
from typing import Optional, Dict
import requests
from src.utils.logger import get_logger
logger = get_logger()
class SecurityChecker:
    """Check Microsoft account security status"""
    def __init__(self, session: requests.Session):
        """\nInitialize security checker\n\nArgs:\n    session: Authenticated requests session\n"""
        self.session = session
    def check_security_info(self) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nCheck account security status\n\nReturns:\n    Dictionary with security info:\n    {\n        \'status\': \'pending_change\' | \'2fa_enabled\' | \'email_phone_only\' | \'unknown\',\n        \'has_2fa\': bool or None,\n        \'recovery_email\': str or None,\n        \'recovery_phone\': str or None,\n        \'mark_lost_chance\': \'will_fail\' | \'possible\' | \'guaranteed\' | \'unknown\'\n    }\n"""
        # ***<module>.SecurityChecker.check_security_info: Failure: Compilation Error
        logger.debug('Checking security info...')
        response = self.session.get('https://account.live.com/proofs/manage', allow_redirects=True, timeout=15)
        if response.status_code!= 200:
            logger.warning(f'Security page returned {response.status_code}')
            return self._unknown_status()
            html = response.text
            if 'security info change is still pending' in html.lower() or 'your security info will be replaced' in html.lower() or 'you requested that your security info be replaced' in html.lower():
                logger.info('🔍 Security Status: PENDING CHANGE detected')
                return {'status': 'pending_change', 'has_2fa': None, 'recovery_email': None, 'recovery_phone': None, 'mark_lost_chance': 'will_fail', 'reason': 'Account has pending security request - Mark Lost will fail'}
                recovery_email = None
                recovery_phone = None
                email_matches = re.findall('[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', html)
                if email_matches:
                    for email in email_matches:
                        if 'microsoft.com' not in email.lower() and 'live.com' not in email.lower():
                                recovery_email = email
                                break
                phone_match = re.search('ending in (\\d{2})', html, re.IGNORECASE)
                if phone_match:
                    recovery_phone = f'***{phone_match.group(1)}'
                logger.info('🔍 Security Status: CLEAN (No login 2FA)')
                return {'status': 'email_phone_only', 'has_2fa': False, 'recovery_email': recovery_email, 'recovery_phone': recovery_phone, 'mark_lost_chance': 'guaranteed', 'reason': 'No login 2FA - Mark Lost guaranteed to work'}
                except Exception as e:
                        logger.error(f'Security check error: {e}')
                        return self._unknown_status()
    def _unknown_status(self) -> Dict:
        """Return unknown status"""
        return {'status': 'error', 'has_2fa': None, 'recovery_email': None, 'recovery_phone': None, 'mark_lost_chance': 'unknown', 'reason': 'Failed to check security status'}
    def format_security_status(self, security_info: Dict) -> str:
        """\nFormat security info for display\n\nArgs:\n    security_info: Security info dictionary\n\nReturns:\n    Formatted string\n"""
        status = security_info['status']
        if status == 'pending_change':
            return '⚠️  PENDING SECURITY CHANGE - Mark Lost will fail'
        else:
            if status == '2fa_enabled':
                return '🔐 2FA ENABLED - Mark Lost possible but not guaranteed'
            else:
                if status == 'email_phone_only':
                    return '✅ CLEAN - No login 2FA, Mark Lost guaranteed!'
                else:
                    return '❓ UNKNOWN - Could not determine security status'