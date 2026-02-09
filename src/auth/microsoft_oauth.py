# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\auth\\microsoft_oauth.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nMicrosoft OAuth authentication\nWITH EXTENSIVE DEBUGGING\n"""
import requests
import re
import time
from urllib.parse import urlparse, parse_qs
from typing import Optional, Tuple
from src.utils.logger import get_logger
logger = get_logger()
MICROSOFT_OAUTH_URL = 'https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en'
class MicrosoftAuthenticator:
    """Handle Microsoft OAuth authentication"""
    def __init__(self, session: Optional[requests.Session]=None):
        """\nInitialize authenticator\n\nArgs:\n    session: Optional requests session (will create new if None)\n"""
        self.session = session or requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'})
    def get_oauth_tokens(self) -> Tuple[Optional[str], Optional[str]]:
        # irreducible cflow, using cdg fallback
        """\nGet OAuth tokens (PPFT and URL POST) from Microsoft\n\nReturns:\n    (url_post, ppft_token) or (None, None) on failure\n"""
        # ***<module>.MicrosoftAuthenticator.get_oauth_tokens: Failure: Compilation Error
        logger.debug('🔍 DEBUG: Fetching OAuth page...')
        response = self.session.get(MICROSOFT_OAUTH_URL, timeout=15)
        logger.debug(f'🔍 DEBUG: OAuth page status: {response.status_code}')
        text = response.text
        logger.debug(f'🔍 DEBUG: Response length: {len(text)} chars')
        match = re.search('value=\\\\\\\"(.+?)\\\\\\\"', text, re.S) or re.search('value=\"(.+?)\"', text, re.S)
        if match:
            ppft_token = match.group(1)
            logger.debug(f'🔍 DEBUG: PPFT token found: {ppft_token[:20]}...')
            match = re.search('\"urlPost\":\"(.+?)\"', text, re.S) or re.search('urlPost:\'(.+?)\'', text, re.S)
            if match:
                url_post = match.group(1)
                logger.debug(f'🔍 DEBUG: URL POST found: {url_post}')
                return (url_post, ppft_token)
                logger.error('🔍 DEBUG: URL POST not found in response')
                    return (None, None)
            logger.error('🔍 DEBUG: PPFT token not found in response')
                return (None, None)
                except Exception as e:
                        logger.error(f'🔍 DEBUG: OAuth tokens error: {e}')
                            return (None, None)
    def login(self, email: str, password: str, url_post: str, ppft_token: str, max_retries: int=3) -> Optional[str]:
        # irreducible cflow, using cdg fallback
        """\nPerform Microsoft login and get RPS token\n\nArgs:\n    email: Microsoft account email\n    password: Account password\n    url_post: POST URL from OAuth\n    ppft_token: PPFT token from OAuth\n    max_retries: Maximum retry attempts\n\nReturns:\n    RPS token string or None on failure\n"""
        # ***<module>.MicrosoftAuthenticator.login: Failure: Compilation Error
        tries = 0
        if tries < max_retries:
            logger.debug(f'🔍 DEBUG: Login attempt {tries + 1}/{max_retries}')
            data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': ppft_token}
            logger.debug(f'🔍 DEBUG: Posting to: {url_post}')
            login_request = self.session.post(url_post, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=True, timeout=15)
            logger.debug(f'🔍 DEBUG: Login response status: {login_request.status_code}')
            logger.debug(f'🔍 DEBUG: Final URL: {login_request.url}')
            logger.debug(f'🔍 DEBUG: Response length: {len(login_request.text)} chars')
            if '#' in login_request.url:
                logger.debug('🔍 DEBUG: Found # in URL - checking for token')
                fragment = urlparse(login_request.url).fragment
                logger.debug(f'🔍 DEBUG: Fragment: {fragment[:100]}...')
                token = parse_qs(fragment).get('access_token', ['None'])[0]
                if token!= 'None':
                    logger.info(f'✅ Login successful - RPS token acquired: {token[:30]}...')
                    return token
                    logger.warning('🔍 DEBUG: Token in fragment was \'None\'')
                logger.debug('🔍 DEBUG: No # in URL')
                        if 'cancel?mkt=' in login_request.text:
                            logger.debug('🔍 DEBUG: Security prompt detected - attempting bypass')
                                ipt_match = re.search('(?<=\"ipt\" value=\").+?(?=\">)', login_request.text)
                                pprid_match = re.search('(?<=\"pprid\" value=\").+?(?=\">)', login_request.text)
                                uaid_match = re.search('(?<=\"uaid\" value=\").+?(?=\">)', login_request.text)
                                action_match = re.search('(?<=id=\"fmHF\" action=\").+?(?=\" )', login_request.text)
                                if ipt_match and pprid_match and uaid_match and action_match:
                                    data = {'ipt': ipt_match.group(), 'pprid': pprid_match.group(), 'uaid': uaid_match.group()}
                                    action_url = action_match.group()
                                    logger.debug(f'🔍 DEBUG: Posting security cancel to: {action_url}')
                                    ret = self.session.post(action_url, data=data, allow_redirects=True, timeout=15)
                                    return_url_match = re.search('(?<=\"recoveryCancel\":{\"returnUrl\":\").+?(?=\",)', ret.text)
                                    if return_url_match:
                                        return_url = return_url_match.group()
                                        logger.debug(f'🔍 DEBUG: Following return URL: {return_url}')
                                        fin = self.session.get(return_url, allow_redirects=True, timeout=15)
                                        if '#' in fin.url:
                                            token = parse_qs(urlparse(fin.url).fragment).get('access_token', ['None'])[0]
                                            if token!= 'None':
                                                logger.info(f'✅ Login successful (via security bypass) - RPS token: {token[:30]}...')
                                                return token
                                    logger.warning('🔍 DEBUG: Could not extract security form fields')
                                            if 'password is incorrect' in login_request.text.lower():
                                                logger.warning('🔍 DEBUG: Incorrect password detected')
                                                    return
                                                if 'account doesn\'t exist' in login_request.text.lower():
                                                    logger.warning('🔍 DEBUG: Account doesn\'t exist')
                                                        return
                                                    if 'too many' in login_request.text.lower() or 'slow down' in login_request.text.lower():
                                                        logger.warning('🔍 DEBUG: Rate limited!')
                                                        time.sleep(5)
                                                    tries += 1
                                                    time.sleep(1)
                                        logger.warning(f'❌ Login failed after {max_retries} attempts')
                                                    except Exception as e:
                                                            logger.warning(f'🔍 DEBUG: Security prompt handling failed: {e}')
                        except Exception as e:
                                logger.error(f'🔍 DEBUG: Login attempt {tries + 1} exception: {e}')
                                tries += 1
                                time.sleep(1)
    def authenticate(self, email: str, password: str) -> Optional[str]:
        """\nComplete authentication flow (get tokens + login)\n\nArgs:\n    email: Microsoft account email\n    password: Account password\n\nReturns:\n    RPS token or None on failure\n"""
        logger.info(f'Authenticating: {email}')
        logger.debug('🔍 DEBUG: Starting authentication flow')
        logger.debug('🔍 DEBUG: Step 1 - Getting OAuth tokens')
        url_post, ppft_token = self.get_oauth_tokens()
        if not url_post or not ppft_token:
            logger.error('🔍 DEBUG: Failed to get OAuth tokens - cannot proceed')
            return
        else:
            logger.debug('🔍 DEBUG: OAuth tokens acquired successfully')
            logger.debug('🔍 DEBUG: Step 2 - Attempting login')
            rps_token = self.login(email, password, url_post, ppft_token)
            if rps_token:
                logger.debug('🔍 DEBUG: Authentication completed successfully')
                return rps_token
            else:
                logger.debug('🔍 DEBUG: Authentication failed')
                return rps_token