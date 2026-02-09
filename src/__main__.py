# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'main.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nShulker V2 - The Ultimate Minecraft Account Checker\nPhase 1: Foundation & Authentication\n\nAuthor: steve_gamerrr12\nVersion: 2.0.0\n"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.gui.main_window import ShulkerApp
from src.utils.logger import setup_logger
try:
    from src.utils.security import init_security
    SECURE_MODE = True
except ImportError:
    SECURE_MODE = False
def main():
    """Main entry point"""
    if SECURE_MODE:
        try:
            init_security()
        except Exception as e:
            pass
    logger = setup_logger()
    logger.info('============================================================')
    logger.info('SHULKER V2 - STARTING')
    logger.info('============================================================')
    directories = ['results', 'combos', 'proxies', 'config/profiles']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f'Directory ensured: {directory}')
    notletters_file = 'notletters_emails.txt'
    if not os.path.exists(notletters_file):
        try:
            with open(notletters_file, 'w', encoding='utf-8') as f:
                f.write('# NotLetters Email:Password Pairs\n')
                f.write('# Format: email:password (one per line)\n')
                f.write('# Lines starting with # are comments and will be ignored\n')
                f.write('# Empty lines are also ignored\n')
                f.write('#\n')
                f.write('# Minimum 50 emails required for Auto Mark Lost feature\n')
                f.write('#\n')
                f.write('# Purchase NotLetters emails from:\n')
                f.write('# 1. Website: https://notletters.com/\n')
                f.write('# 2. Discord: someone_known21 (ID: 793101872784867352)\n')
                f.write('#\n')
            logger.info(f'Created {notletters_file} file')
        except Exception as e:
            logger.warning(f'Could not create {notletters_file}: {e}')
    proxies_file = os.path.join('proxies', 'proxies.txt')
    if not os.path.exists(proxies_file):
        try:
            with open(proxies_file, 'w', encoding='utf-8') as f:
                f.write('# Proxy List for Shulker V2\n')
                f.write('# Add one proxy per line\n')
                f.write('# Supported formats:\n')
                f.write('#   - ip:port\n')
                f.write('#   - user:pass@ip:port\n')
                f.write('#\n')
                f.write('# Examples:\n')
                f.write('#   123.45.67.89:8080\n')
                f.write('#   user:password@123.45.67.89:8080\n')
                f.write('#   proxy.example.com:1080\n')
                f.write('#\n')
                f.write('# Supported types: HTTP, SOCKS4, SOCKS5 (auto-detected)\n')
                f.write('# Configure proxy type in config.yaml under \'proxies.type\'\n')
                f.write('#\n')
                f.write('# Add your proxies below (remove these comment lines):\n')
            logger.info(f'Created {proxies_file} file')
        except Exception as e:
            logger.warning(f'Could not create {proxies_file}: {e}')
    try:
        logger.info('Initializing GUI...')
        app = ShulkerApp()
        logger.info('GUI initialized successfully')
        logger.info('Starting main event loop...')
        app.mainloop()
    except KeyboardInterrupt:
        logger.info('Application interrupted by user')
        sys.exit(0)
    except Exception as e:
        logger.critical(f'Fatal error: {e}', exc_info=True)
        print(f'\n{'============================================================'}')
        print(f'FATAL ERROR: {e}')
        print(f'{'============================================================'}')
        print('Check application logs for details')
        input('Press Enter to exit...')
        sys.exit(1)
    logger.info('Application closed normally')
    logger.info('============================================================')
if __name__ == '__main__':
    main()