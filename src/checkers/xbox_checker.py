# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checkers\\xbox_checker.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nXbox Token and Profile Checker\nGets Xbox Live tokens and gamertag\nWith rate limiting and retry logic\n"""
import requests
import time
from typing import Optional, Tuple
from src.utils.logger import get_logger
from src.network.rate_limiter import get_rate_limiter
logger = get_logger()
class XboxChecker:
    """Check Xbox profile and get tokens"""
    def __init__(self, session: requests.Session, rate_limiter=None):
        """\nInitialize with requests session\n\nArgs:\n    session: Authenticated requests session\n    rate_limiter: Optional rate limiter instance (uses global if None)\n"""
        self.session = session
        self.rate_limiter = rate_limiter or get_rate_limiter()
    def get_xbox_tokens(self, rps_token: str, max_retries: int=3) -> Tuple[Optional[str], Optional[str]]:
        # irreducible cflow, using cdg fallback
        """\nGet Xbox Live UHS and XSTS tokens with retry logic\n\nArgs:\n    rps_token: RPS token from Microsoft OAuth\n    max_retries: Maximum number of retry attempts\n\nReturns:\n    (uhs, xsts_token) or (None, None) if failed\n"""
        # ***<module>.XboxChecker.get_xbox_tokens: Failure: Compilation Error
        base_delay = 2
        for attempt in range(max_retries):
            pass
        user_token = self._get_user_token(rps_token, attempt)
        if not user_token:
            pass
        if attempt < max_retries - 1:
            wait_time = base_delay * 2 ** attempt
            logger.debug(f'User token failed, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})')
            time.sleep(wait_time)
        else:
            return (None, None)
            break
        uhs, xsts_token = self._get_xsts_token(user_token, attempt)
        if not uhs or not xsts_token:
            pass
        if attempt < max_retries - 1:
            pass
        wait_time = base_delay * 2 ** attempt
        logger.debug(f'XSTS token failed, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})')
        time.sleep(wait_time)
        return (None, None)
        return (uhs, xsts_token)
        return (None, None)
        except Exception as e:
            pass
        if attempt < max_retries - 1:
            pass
        wait_time = base_delay * 2 ** attempt
        logger.warning(f'Xbox tokens error (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s...')
        time.sleep(wait_time)
        logger.error(f'Xbox tokens error after {max_retries} attempts: {e}')
        return (None, None)
    def get_gamertag(self, uhs: str, xsts_token: str) -> Optional[str]:
        # irreducible cflow, using cdg fallback
        """Get Xbox gamertag"""
        # ***<module>.XboxChecker.get_gamertag: Failure: Compilation Error
        auth_header = f'XBL3.0 x={uhs};{xsts_token}'
        response = self.session.get('https://profile.xboxlive.com/users/me/profile/settings', headers={'Authorization': auth_header, 'x-xbl-contract-version': '3'}, params={'settings': 'Gamertag'}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            settings = data.get('profileUsers', [{}])[0].get('settings', [])
            for setting in settings:
                    return setting.get('value')
            return None
                        except Exception as e:
                                logger.error(f'Gamertag fetch error: {e}')
    def _get_user_token(self, rps_token: str, attempt: int=0) -> Optional[str]:
        # irreducible cflow, using cdg fallback
        """\nGet Xbox User Token from RPS token with rate limiting\n\nArgs:\n    rps_token: RPS token from Microsoft OAuth\n    attempt: Current retry attempt number\n"""
        # ***<module>.XboxChecker._get_user_token: Failure: Compilation Error
        if self.rate_limiter:
            self.rate_limiter.wait_for_domain('https://user.auth.xboxlive.com/user/authenticate')
        response = self.session.post('https://user.auth.xboxlive.com/user/authenticate', json={'RelyingParty': 'http://auth.xboxlive.com', 'TokenType': 'JWT', 'Properties': {'AuthMethod': 'RPS', 'SiteName': 'user.auth.xboxlive.com', 'RpsTicket': rps_token}}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            token = data.get('Token')
            if token:
                logger.debug('✅ Xbox user token acquired')
                return token
                logger.warning('⚠️ User token response missing \'Token\' field')
                    return
            if response.status_code == 401:
                logger.warning('⚠️ User token failed: 401 Unauthorized - RPS token may be invalid or expired')
                    error_data = response.json()
                    xerr = None
                    if isinstance(error_data, dict):
                        xerr = error_data.get('XErr')
                        message = error_data.get('Message', '')
                        if xerr:
                            logger.debug(f'Xbox error code: XErr={xerr}, Message={message}')
                            logger.debug(f'Error response: {error_data}')
                                return
                        logger.debug(f'Error response: {error_data}')
                                return None
                if response.status_code == 429:
                    wait_time = 10 + 5 * attempt
                    logger.warning(f'⚠️ User token rate limited (429). Marking domain as rate limited for {wait_time}s')
                    if self.rate_limiter:
                        self.rate_limiter.mark_rate_limited('user.auth.xboxlive.com', wait_seconds=wait_time)
                        return None
                    if response.status_code == 403:
                        logger.warning('⚠️ User token failed: 403 Forbidden - Account may have restrictions')
                            return
                        logger.warning(f'⚠️ User token failed: HTTP {response.status_code}')
                            error_data = response.json()
                            logger.debug(f'Error response: {error_data}')
                                    logger.debug(f'Raw response: {response.text[:200]}')
                                            return
                                logger.debug(f'Error response text: {response.text[:200]}')
                    except requests.exceptions.Timeout:
                        logger.warning('⚠️ User token request timed out')
                        except requests.exceptions.ConnectionError as e:
                                logger.warning(f'⚠️ User token connection error: {e}')
                            except Exception as e:
                                    logger.error(f'User token error: {e}')
    def _get_xsts_token(self, user_token: str, attempt: int=0) -> Tuple[Optional[str], Optional[str]]:
        # irreducible cflow, using cdg fallback
        """\nGet XSTS token from user token with rate limiting\n\nArgs:\n    user_token: Xbox user token\n    attempt: Current retry attempt number\n"""
        # ***<module>.XboxChecker._get_xsts_token: Failure: Compilation Error
        if self.rate_limiter:
            self.rate_limiter.wait_for_domain('https://xsts.auth.xboxlive.com/xsts/authorize')
        response = self.session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={'RelyingParty': 'http://xboxlive.com', 'TokenType': 'JWT', 'Properties': {'UserTokens': [user_token], 'SandboxId': 'RETAIL'}}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            uhs = data.get('DisplayClaims', {}).get('xui', [{}])[0].get('uhs')
            xsts_token = data.get('Token')
            if uhs and xsts_token:
                logger.debug('✅ XSTS token acquired')
                return (uhs, xsts_token)
                logger.warning('⚠️ XSTS token response missing required fields')
                    return (None, None)
            if response.status_code == 401:
                error_data = response.json()
                xerr = None
                message = None
                if isinstance(error_data, dict):
                    xerr = error_data.get('XErr')
                    message = error_data.get('Message', '')
                    if xerr:
                        if xerr == 2148916233:
                            logger.debug('Account doesn\'t have Xbox Live account (XErr: 2148916233)')
                                return (None, None)
                            if xerr == 2148916235:
                                logger.debug('Account region doesn\'t support Xbox Live (XErr: 2148916235)')
                                    return (None, None)
                                if xerr == 2148916236:
                                    logger.debug('Account needs Xbox Live verification (XErr: 2148916236)')
                                        return (None, None)
                                    if xerr == 2148916238:
                                        logger.debug('Account is a child account (XErr: 2148916238)')
                                            return (None, None)
                                        logger.warning(f'XSTS token failed: 401 Unauthorized (XErr: {xerr}) - {message}')
                        if 'xbox' in str(error_data).lower() or 'live' in str(error_data).lower():
                            logger.debug('Account may not have Xbox Live access')
                            logger.debug(f'XSTS token failed: 401 Unauthorized - Error response: {error_data}')
                                return (None, None)
                    logger.debug('XSTS token failed: 401 Unauthorized - Could not parse response')
                                            return (None, None)
                if response.status_code == 429:
                    wait_time = 10 + 5 * attempt
                    logger.warning(f'⚠️ XSTS token rate limited (429). Marking domain as rate limited for {wait_time}s')
                    if self.rate_limiter:
                        self.rate_limiter.mark_rate_limited('xsts.auth.xboxlive.com', wait_seconds=wait_time)
                        return (None, None)
                    if response.status_code == 403:
                        logger.warning('⚠️ XSTS token failed: 403 Forbidden - Account may have restrictions')
                            return (None, None)
                        logger.warning(f'⚠️ XSTS token failed: HTTP {response.status_code}')
                            error_data = response.json()
                            logger.debug(f'Error response: {error_data}')
                                return (None, None)
                                except Exception as e:
                                        logger.debug('XSTS token failed: 401 Unauthorized - Account may not have Xbox Live')
                                            if 'xerr' not in response.text.lower()[:200]:
                                                logger.debug(f'Raw response: {response.text[:200]}')
                                                return (None, None)
                                                    return
                                                        return (None, None)
                                logger.debug(f'Error response text: {response.text[:200]}')
                                    return (None, None)
                                                    except requests.exceptions.Timeout:
                                                        logger.warning('⚠️ XSTS token request timed out')
                                                            return (None, None)
                                                        except requests.exceptions.ConnectionError as e:
                                                                logger.warning(f'⚠️ XSTS token connection error: {e}')
                                                                    return (None, None)
                                                            except Exception as e:
                                                                    logger.error(f'XSTS token error: {e}')
                                                                        return (None, None)