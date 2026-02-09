# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checkers\\minecraft_checker.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nMinecraft Checker\nChecks ownership, profile info, capes, name change availability\nDistinguishes OWNED vs Game Pass access\nWith rate limit handling\n"""
import requests
import time
from typing import Optional, Dict, List, Tuple
from src.utils.logger import get_logger
from src.network.rate_limiter import get_rate_limiter
logger = get_logger()
class MinecraftChecker:
    """Check Minecraft ownership and profile"""
    def __init__(self, session: requests.Session, rate_limiter=None):
        """\nInitialize Minecraft checker\n\nArgs:\n    session: Authenticated requests session\n    rate_limiter: Optional rate limiter instance (uses global if None)\n"""
        self.session = session
        self.rate_limiter = rate_limiter or get_rate_limiter()
    def get_xbox_tokens(self, rps_token: str) -> Optional[tuple]:
        # irreducible cflow, using cdg fallback
        """\nGet Xbox Live and XSTS tokens from RPS token\n\nArgs:\n    rps_token: RPS token from Microsoft OAuth\n\nReturns:\n    (uhs, xsts_token) or None\n"""
        # ***<module>.MinecraftChecker.get_xbox_tokens: Failure: Compilation Error
        logger.debug('Getting Xbox Live token...')
        self.rate_limiter.wait_for_domain('https://user.auth.xboxlive.com/user/authenticate')
        xbox_response = self.session.post('https://user.auth.xboxlive.com/user/authenticate', json={'Properties': {'AuthMethod': 'RPS', 'SiteName': 'user.auth.xboxlive.com', 'RpsTicket': rps_token}, 'RelyingParty': 'http://auth.xboxlive.com', 'TokenType': 'JWT'}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
        if xbox_response.status_code!= 200:
            logger.error(f'Xbox Live auth failed: {xbox_response.status_code}')
                return
            xbox_data = xbox_response.json()
            xbox_token = xbox_data.get('Token')
            uhs = xbox_data['DisplayClaims']['xui'][0]['uhs']
            logger.debug('Getting XSTS token...')
            self.rate_limiter.wait_for_domain('https://xsts.auth.xboxlive.com/xsts/authorize')
            xsts_response = self.session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={'Properties': {'SandboxId': 'RETAIL', 'UserTokens': [xbox_token]}, 'RelyingParty': 'rp://api.minecraftservices.com/', 'TokenType': 'JWT'}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
            if xsts_response.status_code!= 200:
                logger.error(f'XSTS auth failed: {xsts_response.status_code}')
                    return
                xsts_token = xsts_response.json().get('Token')
                logger.debug('✅ Xbox tokens acquired')
                return (uhs, xsts_token)
                except Exception as e:
                        logger.error(f'Xbox token error: {e}')
                            return None
    def get_minecraft_xsts_token(self, user_token: str) -> Tuple[Optional[str], Optional[str]]:
        # irreducible cflow, using cdg fallback
        """\nGet XSTS token specifically scoped for Minecraft services\n\nArgs:\n    user_token: Xbox user token\n\nReturns:\n    (uhs, xsts_token) or (None, None) if failed\n"""
        # ***<module>.MinecraftChecker.get_minecraft_xsts_token: Failure: Compilation Error
        logger.debug('Getting Minecraft-scoped XSTS token...')
        self.rate_limiter.wait_for_domain('https://xsts.auth.xboxlive.com/xsts/authorize')
        response = self.session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={'Properties': {'SandboxId': 'RETAIL', 'UserTokens': [user_token]}, 'RelyingParty': 'rp://api.minecraftservices.com/', 'TokenType': 'JWT'}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
        if response.status_code == 200:
            data = response.json()
            uhs = data.get('DisplayClaims', {}).get('xui', [{}])[0].get('uhs')
            xsts_token = data.get('Token')
            logger.debug('✅ Minecraft XSTS token acquired')
            return (uhs, xsts_token)
            logger.error(f'Minecraft XSTS auth failed: {response.status_code}')
                return (None, None)
                except Exception as e:
                        logger.error(f'Minecraft XSTS token error: {e}')
                            return (None, None)
    def get_minecraft_token(self, rps_token: str) -> Optional[str]:
        # irreducible cflow, using cdg fallback
        """\nGet Minecraft access token with rate limit handling\nUses correct Minecraft-scoped XSTS token like Shulker.py\n\nArgs:\n    rps_token: RPS token from Microsoft OAuth\n\nReturns:\n    Minecraft access token or None\n"""
        # ***<module>.MinecraftChecker.get_minecraft_token: Failure: Compilation Error
        max_retries = 3
        base_delay = 2
        self.rate_limiter.wait_for_domain('https://user.auth.xboxlive.com/user/authenticate')
        xbox_response = self.session.post('https://user.auth.xboxlive.com/user/authenticate', json={'Properties': {'AuthMethod': 'RPS', 'SiteName': 'user.auth.xboxlive.com', 'RpsTicket': rps_token}, 'RelyingParty': 'http://auth.xboxlive.com', 'TokenType': 'JWT'}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
        if xbox_response.status_code!= 200:
            logger.error(f'Xbox user token failed: {xbox_response.status_code}')
                return
            xbox_data = xbox_response.json()
            user_token = xbox_data.get('Token')
            if not user_token:
                logger.error('Failed to get Xbox user token')
                    return
                uhs, xsts_token = self.get_minecraft_xsts_token(user_token)
                if not uhs or not xsts_token:
                    logger.error('Failed to get Minecraft XSTS token')
                        return
                    for attempt in range(max_retries):
                        logger.debug(f'Getting Minecraft access token... (attempt {attempt + 1}/{max_retries})')
                        min_delay = 5.0
                        if self.rate_limiter:
                            domain = 'api.minecraftservices.com'
                            if domain in self.rate_limiter.rate_limited_until:
                                wait_until = self.rate_limiter.rate_limited_until[domain]
                                if time.time() < wait_until:
                                    wait_time = wait_until - time.time()
                                    logger.warning(f'⏰ Minecraft API rate limited. Waiting {wait_time:.1f}s...')
                                    time.sleep(wait_time)
                            self.rate_limiter.wait_for_domain('https://api.minecraftservices.com/authentication/login_with_xbox', min_delay=min_delay)
                        else:
                            time.sleep(min_delay)
                        response = self.session.post('https://api.minecraftservices.com/authentication/login_with_xbox', json={'identityToken': f'XBL3.0 x={uhs};{xsts_token}'}, headers={'Content-Type': 'application/json'}, timeout=15)
                        if response.status_code == 200:
                            mc_token = response.json().get('access_token')
                            logger.debug('✅ Minecraft token acquired')
                            if self.rate_limiter:
                                domain = 'api.minecraftservices.com'
                                if domain in self.rate_limiter.rate_limited_until:
                                    del self.rate_limiter.rate_limited_until[domain]
                            return mc_token
                            if response.status_code == 429:
                                wait_time = min(30 + base_delay * 2 ** attempt, 120)
                                logger.warning(f'⏰ Rate limited (429). Waiting {wait_time}s before retry...')
                                if self.rate_limiter:
                                    domain = 'api.minecraftservices.com'
                                    self.rate_limiter.mark_rate_limited(domain, wait_seconds=int(wait_time))
                                time.sleep(wait_time)
                                logger.error(f'Minecraft auth failed: {response.status_code}')
                                if response.status_code == 401:
                                    logger.error('401 Unauthorized - XSTS token may not be scoped for Minecraft')
                                    return
                        logger.error('❌ Max retries exceeded for Minecraft token')
                except Exception as e:
                        logger.error(f'Xbox token error: {e}')
                            return
                                except Exception as e:
                                        error_str = str(e)
                                        if '429' in error_str and attempt < max_retries - 1:
                                            wait_time = min(30 + base_delay * 2 ** attempt, 120)
                                            logger.warning(f'⏰ Rate limit error. Waiting {wait_time}s before retry...')
                                            if self.rate_limiter:
                                                domain = 'api.minecraftservices.com'
                                                self.rate_limiter.mark_rate_limited(domain, wait_seconds=int(wait_time))
                                            time.sleep(wait_time)
                                            logger.error(f'Minecraft token error: {e}')
                                                return
    def check_ownership(self, mc_token: str) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nCheck Minecraft ownership (Java/Bedrock/Dungeons)\nDistinguishes OWNED vs Game Pass access\n\nArgs:\n    mc_token: Minecraft access token\n\nReturns:\n    Dictionary with ownership info\n"""
        # ***<module>.MinecraftChecker.check_ownership: Failure: Compilation Error
        logger.debug('Checking Minecraft ownership...')
        self.rate_limiter.wait_for_domain('https://api.minecraftservices.com/entitlements/license')
        response = self.session.get('https://api.minecraftservices.com/entitlements/license', headers={'Authorization': f'Bearer {mc_token}'}, timeout=15)
        if response.status_code!= 200:
            logger.error(f'Ownership check failed: {response.status_code}')
            return self._no_ownership()
            data = response.json()
            items = data.get('items', [])
            ownership = {'minecraft_java_owned': False, 'minecraft_bedrock_owned': False, 'minecraft_dungeons_owned': False, 'minecraft_java_gamepass': False, 'minecraft_bedrock_gamepass': False, 'minecraft_dungeons_gamepass': False, 'gamepass_ultimate': False, 'gamepass_pc': False, 'raw_items': [f'{item.get('name', 'unknown')} (source: {item.get('source', 'unknown')})' for item in items]}
            for item in items:
                name = item.get('name', '')
                source = item.get('source', '')
                if name in ['game_minecraft', 'product_minecraft']:
                    if source in ['PURCHASE', 'MCPURCHASE']:
                        ownership['minecraft_java_owned'] = True
                    else:
                        ownership['minecraft_java_gamepass'] = True
                else:
                    if name == 'product_minecraft_bedrock':
                        if source in ['PURCHASE', 'MCPURCHASE']:
                            ownership['minecraft_bedrock_owned'] = True
                        else:
                            ownership['minecraft_bedrock_gamepass'] = True
                    else:
                        if name == 'product_dungeons':
                            if source in ['PURCHASE', 'MCPURCHASE']:
                                ownership['minecraft_dungeons_owned'] = True
                            else:
                                ownership['minecraft_dungeons_gamepass'] = True
                        else:
                            if name == 'product_game_pass_pc':
                                ownership['gamepass_pc'] = True
                            else:
                                if name == 'product_game_pass_ultimate':
                                    ownership['gamepass_ultimate'] = True
            logger.info(f'✅ Ownership checked: Java={ownership['minecraft_java_owned']}, Bedrock={ownership['minecraft_bedrock_owned']}')
            logger.debug(f'Raw items: {ownership['raw_items']}')
            return ownership
                except Exception as e:
                        logger.error(f'Ownership check error: {e}')
                        return self._no_ownership()
    def get_profile(self, mc_token: str) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nGet Minecraft profile (username, UUID, capes, name change)\n\nArgs:\n    mc_token: Minecraft access token\n\nReturns:\n    Dictionary with profile info\n"""
        # ***<module>.MinecraftChecker.get_profile: Failure: Compilation Error
        logger.debug('Getting Minecraft profile...')
        self.rate_limiter.wait_for_domain('https://api.minecraftservices.com/minecraft/profile')
        profile_response = self.session.get('https://api.minecraftservices.com/minecraft/profile', headers={'Authorization': f'Bearer {mc_token}'}, timeout=15)
        if profile_response.status_code!= 200:
            logger.warning(f'Profile fetch failed: {profile_response.status_code}')
            return self._no_profile()
            profile_data = profile_response.json()
            profile = {'username': profile_data.get('name', 'Unknown'), 'uuid': profile_data.get('id', 'Unknown'), 'capes': [], 'name_changeable': None, 'name_change_date': None}
            capes = profile_data.get('capes', [])
            for cape in capes:
                profile['capes'].append({'id': cape.get('id'), 'state': cape.get('state'), 'alias': cape.get('alias')})
            logger.debug(f'Profile: {profile['username']} ({profile['uuid']})')
            try:
                self.rate_limiter.wait_for_domain('https://api.minecraftservices.com/minecraft/profile/namechange')
                namechange_response = self.session.get('https://api.minecraftservices.com/minecraft/profile/namechange', headers={'Authorization': f'Bearer {mc_token}'}, timeout=15)
                if namechange_response.status_code == 200:
                    nc_data = namechange_response.json()
                    profile['name_changeable'] = nc_data.get('nameChangeAllowed', False)
                    profile['name_change_date'] = nc_data.get('changedAt')
                    logger.debug(f'Name changeable: {profile['name_changeable']}')
            except:
                pass
            logger.info(f'✅ Profile retrieved: {profile['username']}')
            return profile
                except Exception as e:
                        logger.error(f'Profile fetch error: {e}')
                        return self._no_profile()
    def _no_ownership(self) -> Dict:
        """Return empty ownership"""
        return {'minecraft_java_owned': False, 'minecraft_bedrock_owned': False, 'minecraft_dungeons_owned': False, 'minecraft_java_gamepass': False, 'minecraft_bedrock_gamepass': False, 'minecraft_dungeons_gamepass': False, 'gamepass_ultimate': False, 'gamepass_pc': False, 'raw_items': []}
    def _no_profile(self) -> Dict:
        """Return empty profile"""
        return {'username': None, 'uuid': None, 'capes': [], 'name_changeable': None, 'name_change_date': None}
    def check_minecraft(self, rps_token: str) -> Optional[Dict]:
        # irreducible cflow, using cdg fallback
        """\nComplete Minecraft check (token + ownership + profile)\nUses correct Minecraft-scoped XSTS token like Shulker.py\n\nArgs:\n    rps_token: RPS token from Microsoft OAuth\n\nReturns:\n    Dictionary with ownership and profile info, or None if failed\n"""
        # ***<module>.MinecraftChecker.check_minecraft: Failure: Compilation Error
        mc_token = self.get_minecraft_token(rps_token)
        if not mc_token:
            logger.warning('Failed to get Minecraft token')
                return
            ownership = self.check_ownership(mc_token)
            profile = None
            if ownership.get('minecraft_java_owned') or ownership.get('minecraft_bedrock_owned'):
                profile = self.get_profile(mc_token)
            else:
                profile = self._no_profile()
            return {'ownership': ownership, 'profile': profile}
                except Exception as e:
                        logger.error(f'Minecraft check error: {e}')
                            return None