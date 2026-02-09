# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checkers\\nitro_checker.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nDiscord Nitro Checker with Promo Code Fetcher\nEnhanced version that extracts actual Nitro promo codes\n"""
import requests
import re
from typing import Optional, Dict
from src.utils.logger import get_logger
logger = get_logger()
class NitroChecker:
    """Check Discord Nitro perk and fetch promo codes"""
    def __init__(self, session: requests.Session):
        """\nInitialize Nitro checker\n\nArgs:\n    session: Authenticated requests session\n"""
        self.session = session
    def check_nitro_perk(self, has_gpu: bool, uhs: str=None, xsts_token: str=None) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nCheck Discord Nitro perk availability and fetch promo code\n\nArgs:\n    has_gpu: Whether account has Game Pass Ultimate\n    uhs: Xbox UHS (required if has_gpu=True)\n    xsts_token: Xbox Live XSTS token (required if has_gpu=True)\n\nReturns:\n    Dictionary with Nitro info including promo code\n"""
        # ***<module>.NitroChecker.check_nitro_perk: Failure: Compilation Error
        if not has_gpu:
            logger.debug('Account doesn\'t have Game Pass Ultimate - skipping Nitro check')
            return {'eligible': False, 'status': 'not_eligible', 'redemption_link': None, 'promo_code': None, 'error': None}
        else:
            if not uhs or not xsts_token:
                logger.warning('Missing Xbox tokens for Nitro check')
                return {'eligible': True, 'status': 'error', 'redemption_link': None, 'promo_code': None, 'error': 'Missing Xbox authentication tokens'}
        logger.debug('Checking Discord Nitro perk...')
        auth_header = f'XBL3.0 x={uhs};{xsts_token}'
        response = self.session.get('https://profile.gamepass.com/v2/offers', headers={'Authorization': auth_header, 'Content-Type': 'application/json', 'User-Agent': 'okhttp/4.12.0'}, timeout=30)
        if response.status_code!= 200:
            logger.warning(f'Game Pass perks API returned {response.status_code}')
            return self._error_result(f'API returned {response.status_code}')
            perks_data = response.json()
            for offer in perks_data.get('offers', []):
                    if offer.get('resourceType') == 'external-link':
                        offer_id = offer.get('offerId', '').lower()
                        resource = offer.get('resource', '')
                        if 'discord' in resource.lower() or 'discord' in offer_id:
                            status = offer.get('offerStatus', '').lower()
                            claimed_date = offer.get('claimedDate')
                            logger.debug(f'Found Discord Nitro perk: {offer_id}')
                            if status == 'claimed':
                                logger.info('✅ Discord Nitro: CLAIMED')
                                promo_code = self._extract_promo_code(resource)
                                return {'eligible': True, 'status': 'claimed', 'redemption_link': resource if resource else None, 'promo_code': promo_code, 'claimed_date': claimed_date[:10] if claimed_date else None, 'error': None}
                                if status == 'available':
                                    logger.info('✅ Discord Nitro: AVAILABLE!')
                                    promo_result = self._claim_and_get_promo(offer, auth_header)
                                    return {'eligible': True, 'status': 'available', 'redemption_link': promo_result.get('link', resource), 'promo_code': promo_result.get('promo_code'), 'error': None}
                                    logger.warning(f'Discord Nitro unknown status: {status}')
                                    return {'eligible': True, 'status': 'unknown', 'redemption_link': resource if resource else None, 'promo_code': None, 'error': f'Unknown status: {status}'}
                    logger.warning('Discord Nitro perk not found in offers')
                    return {'eligible': True, 'status': 'not_found', 'redemption_link': None, 'promo_code': None, 'error': 'Perk not found in Game Pass offers'}
                except Exception as e:
                        logger.error(f'Nitro check error: {e}')
                        return self._error_result(f'Error: {str(e)}')
    def _extract_promo_code(self, redemption_link: str) -> Optional[str]:
        # irreducible cflow, using cdg fallback
        """\nExtract promo code from redemption link\n\nArgs:\n    redemption_link: Discord redemption URL\n\nReturns:\n    Promo code or None\n"""
        # ***<module>.NitroChecker._extract_promo_code: Failure: Compilation Error
        if not redemption_link:
            return
        patterns = ['discord\\.com/billing/promotions/([A-Za-z0-9]+)', 'discord\\.com/gifts/([A-Za-z0-9]+)', 'promos\\.discord\\.gg/([A-Za-z0-9]+)', 'discord\\.gg/promotions/([A-Za-z0-9]+)']
        for pattern in patterns:
                match = re.search(pattern, redemption_link)
                if match:
                    promo_code = match.group(1)
                    logger.debug(f'Extracted promo code: {promo_code}')
                    return promo_code
                if 'discord' in redemption_link.lower():
                    return self._fetch_promo_from_link(redemption_link)
                    return None
                        except Exception as e:
                                logger.error(f'Error extracting promo code: {e}')
                                    return None
    def _fetch_promo_from_link(self, link: str) -> Optional[str]:
        # irreducible cflow, using cdg fallback
        """\nFetch promo code by following redemption link\n\nArgs:\n    link: Redemption URL\n\nReturns:\n    Promo code or None\n"""
        # ***<module>.NitroChecker._fetch_promo_from_link: Failure: Compilation Error
        logger.debug(f'Fetching promo code from link: {link[:50]}...')
        response = self.session.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}, allow_redirects=True, timeout=15)
        if response.status_code!= 200:
            logger.warning(f'Failed to fetch promo link: {response.status_code}')
                return
            patterns = ['discord\\.com/billing/promotions/([A-Za-z0-9]+)', 'discord\\.com/gifts/([A-Za-z0-9]+)', 'promos\\.discord\\.gg/([A-Za-z0-9]+)', 'promotion[\"\\\']?\\s*:\\s*[\"\\\']?([A-Za-z0-9]+)', 'code[\"\\\']?\\s*:\\s*[\"\\\']?([A-Za-z0-9]{16,})']
            content = response.text
            for pattern in patterns:
                    match = re.search(pattern, content)
                    if match:
                        promo_code = match.group(1)
                        logger.debug(f'Found promo code in response: {promo_code}')
                        return promo_code
                    final_url = response.url
                    if final_url!= link:
                        logger.debug(f'Following redirect to: {final_url[:50]}...')
                        return self._extract_promo_code(final_url)
                except Exception as e:
                        logger.error(f'Error fetching promo from link: {e}')
                            return None
    def _claim_and_get_promo(self, offer: Dict, auth_header: str) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nClaim an available Nitro perk and get promo code\n\nArgs:\n    offer: Offer data from API\n    auth_header: Xbox authorization header\n\nReturns:\n    Dictionary with link and promo_code\n"""
        # ***<module>.NitroChecker._claim_and_get_promo: Failure: Compilation Error
        offer_id = offer.get('offerId')
        logger.info(f'Attempting to claim Nitro perk: {offer_id}')
        claim_response = self.session.post(f'https://profile.gamepass.com/v2/offers/{offer_id}/claim', headers={'Authorization': auth_header, 'Content-Type': 'application/json', 'User-Agent': 'okhttp/4.12.0'}, timeout=30)
        if claim_response.status_code == 200:
            claim_data = claim_response.json()
            redemption_link = claim_data.get('resource') or offer.get('resource')
            logger.info('✅ Successfully claimed Nitro perk!')
            promo_code = self._extract_promo_code(redemption_link)
            if promo_code:
                logger.info(f'🎁 Nitro Promo Code: {promo_code}')
            return {'link': redemption_link, 'promo_code': promo_code}
            logger.warning(f'Failed to claim Nitro: {claim_response.status_code}')
            return {'link': offer.get('resource'), 'promo_code': None}
                except Exception as e:
                        logger.error(f'Error claiming Nitro perk: {e}')
                        return {'link': offer.get('resource'), 'promo_code': None}
    def _error_result(self, error_msg: str) -> Dict:
        """Return error result"""
        return {'eligible': False, 'status': 'error', 'redemption_link': None, 'promo_code': None, 'error': error_msg}
    def check_nitro(self, uhs: str, xsts_token: str) -> Dict:
        """\nCheck Discord Nitro (wrapper that auto-detects GPU)\n\nArgs:\n    uhs: Xbox UHS token\n    xsts_token: XSTS token\n\nReturns:\n    Dictionary with Nitro info\n"""
        try:
            auth_header = f'XBL3.0 x={uhs};{xsts_token}'
            response = self.session.get('https://profile.gamepass.com/v2/offers', headers={'Authorization': auth_header, 'Content-Type': 'application/json', 'User-Agent': 'okhttp/4.12.0'}, timeout=30)
            has_gpu = False
            if response.status_code == 200:
                try:
                    perks_data = response.json()
                    if perks_data and isinstance(perks_data, dict):
                            offers = perks_data.get('offers', [])
                            if offers:
                                has_gpu = True
                                logger.debug('Account has Game Pass Ultimate (detected via perks API)')
                except (ValueError, AttributeError) as e:
                    logger.debug(f'Failed to parse perks data: {e}')
                else:
                    pass
            else:
                logger.debug(f'Game Pass perks API returned {response.status_code}, assuming no GPU')
            return self.check_nitro_perk(has_gpu, uhs, xsts_token)
        except Exception as e:
            logger.error(f'Error checking Nitro: {e}')
            return self._error_result(str(e))