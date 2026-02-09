# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checkers\\ms_rewards_checker.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nMS Rewards Checker\nUses separate session for Bing Rewards authentication\nBased on working standalone code\n"""
import requests
import re
import time
from typing import Optional, Dict
from src.utils.logger import get_logger
logger = get_logger()
class MSRewardsChecker:
    """Check Microsoft Rewards points using rewards.bing.com"""
    def __init__(self, session: requests.Session=None):
        """\nInitialize MS Rewards checker\n\nNote: This checker creates its own session for Bing Rewards\n"""
        return
    def check_rewards(self, email: str, password: str) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nCheck Microsoft Rewards points balance\n\nArgs:\n    email: Account email\n    password: Account password\n\nReturns:\n    Dictionary with rewards info\n"""
        # ***<module>.MSRewardsChecker.check_rewards: Failure: Compilation Error
        rewards_session = requests.Session()
        rewards_session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.9'})
        logger.debug('Getting Bing Rewards OAuth tokens...')
        initial_url = 'https://rewards.bing.com/'
        response = rewards_session.get(initial_url, timeout=15, allow_redirects=True)
        signin_url = 'https://rewards.bing.com/Signin?idru=%2F'
        response = rewards_session.get(signin_url, timeout=15, allow_redirects=True)
        text = response.text
        match = re.search('value=\\\\\\\"(.+?)\\\\\\\"', text, re.S) or re.search('value=\"(.+?)\"', text, re.S)
        if not match:
            logger.warning('Could not extract PPFT token for Rewards')
            return self._no_rewards('Could not extract login tokens')
            ppft_token = match.group(1)
            logger.debug(f'PPFT token: {ppft_token[:20]}...')
            match = re.search('\"urlPost\":\"(.+?)\"', text, re.S) or re.search('urlPost:\'(.+?)\'', text, re.S)
            if not match:
                logger.warning('Could not extract URL POST for Rewards')
                return self._no_rewards('Could not extract URL POST')
                url_post = match.group(1)
                logger.debug(f'URL POST: {url_post[:50]}...')
                logger.debug('Performing Rewards login...')
                login_success = self._rewards_login(rewards_session, email, password, url_post, ppft_token)
                if not login_success:
                    logger.warning('Bing Rewards authentication failed')
                    return self._no_rewards('Authentication failed')
                    logger.debug('✅ Rewards authentication successful')
                    logger.debug('Fetching rewards points...')
                    home_response = rewards_session.get('https://rewards.bing.com/', timeout=15, allow_redirects=True)
                    if home_response.status_code!= 200:
                        logger.warning(f'Rewards home page returned {home_response.status_code}')
                        return self._no_rewards('Failed to load rewards page')
                        time.sleep(1)
                        timestamp = int(time.time() * 1000)
                        api_url = f'https://rewards.bing.com/api/getuserinfo?type=1&X-Requested-With=XMLHttpRequest&_={timestamp}'
                        response = rewards_session.get(api_url, headers={'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://rewards.bing.com/'}, timeout=15)
                        if response.status_code == 200:
                            data = response.json()
                            dashboard = data.get('dashboard', {})
                            user_status = dashboard.get('userStatus', {})
                            available_points = user_status.get('availablePoints', 0)
                            lifetime_points = user_status.get('lifetimePoints', 0)
                            lifetime_redeemed = user_status.get('lifetimePointsRedeemed', 0)
                            logger.info(f'✅ MS Rewards: {available_points:,} points available')
                            return {'available_points': available_points, 'lifetime_points': lifetime_points, 'redeemed_points': lifetime_redeemed, 'error': None}
                            logger.warning(f'Rewards API returned {response.status_code}')
                            return self._no_rewards(f'API returned {response.status_code}')
                except Exception as e:
                        logger.error(f'MS Rewards check error: {e}')
                        return self._no_rewards(f'Error: {str(e)}')
    def _rewards_login(self, session: requests.Session, email: str, password: str, url_post: str, ppft_token: str, max_retries: int=3) -> bool:
        # irreducible cflow, using cdg fallback
        """\nPerform Microsoft login specifically for Rewards\n"""
        # ***<module>.MSRewardsChecker._rewards_login: Failure: Compilation Error
        tries = 0
        if tries < max_retries:
            data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': ppft_token}
            login_request = session.post(url_post, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=True, timeout=15)
            if 'rewards.bing.com' in login_request.url:
                logger.debug('Successfully authenticated with Bing Rewards')
                    return True
                if 'post.srf' in login_request.url:
                    logger.debug('Found intermediate post.srf, following redirect...')
                    if 'fmHF' in login_request.text or 'DoSubmit' in login_request.text:
                        action_match = re.search('action=[\"\\\']([^\"\\\']+)[\"\\\']', login_request.text)
                        if action_match:
                            action_url = action_match.group(1).replace('&amp;', '&')
                            form_data = {}
                            for field in ['code', 'id_token', 'state', 'session_state', 'correlation_id']:
                                match = re.search(f'name=[\"\']?{field}[\"\']?.*?value=[\"\']([^\"\']*)[\"\']', login_request.text, re.DOTALL)
                                if match:
                                    form_data[field] = match.group(1)
                            if form_data:
                                redirect = session.post(action_url, data=form_data, allow_redirects=True, timeout=15)
                                if 'rewards.bing.com' in redirect.url:
                                    logger.debug('Successfully authenticated after post.srf')
                                        return True
                    if 'cancel?mkt=' in login_request.text:
                        logger.debug('Handling security prompt...')
                            data = {'ipt': re.search('(?<=\"ipt\" value=\").+?(?=\">)', login_request.text).group(), 'pprid': re.search('(?<=\"pprid\" value=\").+?(?=\">)', login_request.text).group(), 'uaid': re.search('(?<=\"uaid\" value=\").+?(?=\">)', login_request.text).group()}
                            action_url = re.search('(?<=id=\"fmHF\" action=\").+?(?=\" )', login_request.text).group()
                            ret = session.post(action_url, data=data, allow_redirects=True, timeout=15)
                            return_url = re.search('(?<=\"recoveryCancel\":{\"returnUrl\":\").+?(?=\",)', ret.text).group()
                            fin = session.get(return_url, allow_redirects=True, timeout=15)
                            if 'rewards.bing.com' in fin.url:
                                logger.debug('Successfully authenticated after security prompt')
                                    return True
                                    tries += 1
                                    time.sleep(1)
            return False
                                        pass
                    except Exception as e:
                            logger.debug(f'Login attempt {tries + 1} exception: {e}')
                            tries += 1
                            time.sleep(1)
    def _no_rewards(self, reason: str='Unknown') -> Dict:
        """Return empty rewards data"""
        return {'available_points': 0, 'lifetime_points': 0, 'redeemed_points': 0, 'error': reason}