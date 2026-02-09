# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\automation\\notletters_pool.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nNotLetters Email Pool Manager\nUses pre-generated NotLetters emails from file\n"""
import random
import threading
from typing import Optional, Dict, List
from src.utils.logger import get_logger
logger = get_logger()
class NotLettersPool:
    """Manage pool of pre-generated NotLetters emails"""
    def __init__(self, email_file: str='notletters_emails.txt'):
        """\nInitialize NotLetters pool\n\nArgs:\n    email_file: Path to file with email:password pairs\n"""
        self.email_file = email_file
        self.available_emails = []
        self.used_emails = {}
        self.lock = threading.Lock()
        self.load_emails()
    def load_emails(self):
        """Load emails from file"""
        try:
            with open(self.email_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                else:
                    if ':' in line:
                        email, password = line.split(':', 1)
                        if email.strip() and password.strip():
                                self.available_emails.append({'email': email.strip(), 'password': password.strip()})
            logger.info(f'✅ Loaded {len(self.available_emails)} NotLetters emails from pool')
        except FileNotFoundError:
            logger.error(f'NotLetters email file not found: {self.email_file}')
            self.available_emails = []
        except Exception as e:
            logger.error(f'Error loading NotLetters emails: {e}')
            self.available_emails = []
    def get_email(self, account_email: str) -> Optional[Dict]:
        # irreducible cflow, using cdg fallback
        """\nGet a random email from pool (can be reused)\n\nArgs:\n    account_email: Account this email will be used for\n\nReturns:\n    Dictionary with email and password, or None\n"""
        # ***<module>.NotLettersPool.get_email: Failure: Different control flow
        with self.lock:
            pass
        if not self.available_emails:
            logger.error('No NotLetters emails available in pool!')
            return
            email_data = random.choice(self.available_emails)
            if email_data['email'] not in self.used_emails:
                self.used_emails[email_data['email']] = []
            self.used_emails[email_data['email']].append(account_email)
            usage_count = len(self.used_emails[email_data['email']])
            logger.debug(f'Using NotLetters email: {email_data['email']} (used {usage_count}x)')
            return email_data
    def get_stats(self) -> Dict:
        """Get pool statistics"""
        # ***<module>.NotLettersPool.get_stats: Failure: Different bytecode
        with self.lock:
            total_usage = sum((len(accounts) for accounts in self.used_emails.values()))
            return {'total_emails': len(self.available_emails), 'emails_used_at_least_once': len(self.used_emails), 'total_accounts_processed': total_usage, 'average_reuse': total_usage / len(self.used_emails) if self.used_emails else 0}