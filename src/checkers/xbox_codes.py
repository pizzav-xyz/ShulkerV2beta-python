# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checkers\\xbox_codes.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nXbox Game Pass Codes Fetcher\nFetches Xbox redeem codes from Game Pass perks\nBased on working testing.py implementation\n"""
import requests
import time
import random
import string
from typing import Dict, List, Optional
from src.utils.logger import get_logger
logger = get_logger()
class XboxCodesFetcher:
    """Fetch Xbox Game Pass codes"""
    def __init__(self, session: requests.Session):
        """Initialize with requests session"""
        self.session = session
    def fetch_codes(self, uhs: str, xsts_token: str) -> List[Dict]:
        # irreducible cflow, using cdg fallback
        """\nFetch all Xbox codes from Game Pass perks\n\nArgs:\n    uhs: Xbox UHS token\n    xsts_token: XSTS token\n\nReturns:\n    List of codes with details:\n    [\n        {\n            \'code\': \'ABC123...\',\n            \'offer_id\': \'...\',\n            \'status\': \'claimed\' or \'available\',\n            \'claimed_date\': \'2024-12-09\'\n        },\n        ...\n    ]\n"""
        # ***<module>.XboxCodesFetcher.fetch_codes: Failure: Compilation Error
        logger.debug('🎁 Fetching Xbox Game Pass perks...')
        perks_data = self._get_perks_list(uhs, xsts_token)
        if not perks_data:
            logger.debug('No perks data returned')
            return []
            all_codes = []
            offers = perks_data.get('offers', [])
            logger.debug(f'Found {len(offers)} perks total')
            xbox_code_offers = [offer for offer in offers if offer.get('resourceType') == 'store-token']
            logger.debug(f'Found {len(xbox_code_offers)} Xbox code offers')
            for offer in xbox_code_offers:
                offer_id = offer.get('offerId')
                status = offer.get('offerStatus')
                detailed_offer = self._get_offer_details(uhs, xsts_token, offer_id)
                if detailed_offer:
                    code = detailed_offer.get('resource')
                    code_status = detailed_offer.get('offerStatus', status)
                    claimed_date = detailed_offer.get('claimedDate')
                    code_info = {'code': code if code else 'N/A', 'offer_id': offer_id, 'status': code_status, 'claimed_date': claimed_date[:10] if claimed_date else None}
                    if str(code_info['status']).lower() == 'available':
                        claimed_code = self._claim_offer(uhs, xsts_token, offer_id)
                        if claimed_code:
                            code_info['code'] = claimed_code
                            code_info['status'] = 'claimed'
                        time.sleep(1)
                    else:
                        if str(code_info.get('status', '')).lower() == 'claimed' and code_info.get('code') and (code_info['code']!= 'N/A'):
                                    logger.debug(f'✅ Already claimed code: {code_info['code'][:20]}...')
                    all_codes.append(code_info)
                else:
                    code_info = {'code': offer.get('resource', 'N/A'), 'offer_id': offer_id, 'status': status, 'claimed_date': offer.get('claimedDate', '')[:10] if offer.get('claimedDate') else None}
                    if str(code_info['status']).lower() == 'available':
                        claimed_code = self._claim_offer(uhs, xsts_token, offer_id)
                        if claimed_code:
                            code_info['code'] = claimed_code
                            code_info['status'] = 'claimed'
                        time.sleep(1)
                    all_codes.append(code_info)
            claimed_count = len([c for c in all_codes if str(c.get('status', '')).lower() == 'claimed' and c.get('code') and (c.get('code')!= 'N/A')])
            available_count = len([c for c in all_codes if str(c.get('status', '')).lower() == 'available'])
            if all_codes:
                logger.info(f'🎁 Xbox Codes: {len(all_codes)} total ({claimed_count} claimed, {available_count} available)')
                for code_info in all_codes:
                    if code_info.get('status') == 'claimed' and code_info.get('code') and (code_info.get('code')!= 'N/A'):
                                logger.info(f'   ✅ Code: {code_info['code']}')
                return all_codes
                logger.debug('No Xbox codes found')
                return all_codes
                except Exception as e:
                        logger.error(f'Xbox codes fetch error: {e}')
                        return []
    def _get_perks_list(self, uhs: str, xsts_token: str) -> Optional[Dict]:
        # irreducible cflow, using cdg fallback
        """Get list of all perks"""
        # ***<module>.XboxCodesFetcher._get_perks_list: Failure: Compilation Error
        auth_header = f'XBL3.0 x={uhs};{xsts_token}'
        response = self.session.get('https://profile.gamepass.com/v2/offers', headers={'Authorization': auth_header, 'Content-Type': 'application/json', 'User-Agent': 'okhttp/4.12.0'}, timeout=30)
        if response.status_code == 200:
            return response.json()
            logger.warning(f'Perks list failed: {response.status_code}')
                return
                except Exception as e:
                        logger.error(f'Get perks list error: {e}')
    def _get_offer_details(self, uhs: str, xsts_token: str, offer_id: str) -> Optional[Dict]:
        # irreducible cflow, using cdg fallback
        """Get detailed info for specific offer"""
        # ***<module>.XboxCodesFetcher._get_offer_details: Failure: Compilation Error
        auth_header = f'XBL3.0 x={uhs};{xsts_token}'
        response = self.session.get(f'https://profile.gamepass.com/v2/offers/{offer_id}', headers={'Authorization': auth_header, 'Content-Type': 'application/json', 'User-Agent': 'okhttp/4.12.0'}, timeout=30)
        if response.status_code == 200:
            return response.json()
            return None
                except Exception as e:
                        logger.debug(f'Get offer details error: {e}')
                            return None
    def _claim_offer(self, uhs: str, xsts_token: str, offer_id: str) -> Optional[str]:
        # irreducible cflow, using cdg fallback
        """Claim an available offer and get the code (EXACT copy of testing.py claim_perk)"""
        # ***<module>.XboxCodesFetcher._claim_offer: Failure: Compilation Error
        auth_header = f'XBL3.0 x={uhs};{xsts_token}'
        cv_base = ''.join(random.choices(string.ascii_letters + string.digits, k=22))
        ms_cv = f'{cv_base}.0'
        original_headers = dict(self.session.headers)
        self.session.headers.clear()
            response = self.session.post(f'https://profile.gamepass.com/v2/offers/{offer_id}', headers={'Authorization': auth_header, 'content-type': 'application/json', 'User-Agent': 'okhttp/4.12.0', 'ms-cv': ms_cv, 'Accept-Encoding': 'gzip', 'Connection': 'Keep-Alive', 'Host': 'profile.gamepass.com', 'Content-Length': '0'}, data='', timeout=30)
                self.session.headers.clear()
                self.session.headers.update(original_headers)
                if response.status_code == 200:
                    data = response.json()
                    code = data.get('resource')
                    if code:
                        logger.debug(f'✅ Claimed code: {code}')
                        return code
                        logger.warning(f'⚠️ Claim succeeded but no code in response: {data}')
                            return
                    error_text = response.text[:300] if response.text else 'No response body'
                    logger.warning(f'❌ Claim failed with status {response.status_code}: {error_text}')
                            except Exception as e:
                                    logger.error(f'Claim offer error: {e}')
                                    import traceback
                                    logger.debug(f'Traceback: {traceback.format_exc()}')