# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checkers\\donut_checker.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nDonut SMP Checker - EXACT CODE FROM SHULKER.PY\nUses donutstats.net API\n"""
import requests
import time
import json
import uuid as uuid_module
from io import StringIO
import sys
from typing import Optional, Dict
from src.utils.logger import get_logger
try:
    from minecraft.networking.connection import Connection
    from minecraft.authentication import AuthenticationToken, Profile
    from minecraft.networking.packets import clientbound
    from minecraft.exceptions import LoginDisconnect
    MINECRAFT_LIB_AVAILABLE = True
except ImportError:
    MINECRAFT_LIB_AVAILABLE = False
    LoginDisconnect = None
    logger = None
logger = get_logger()
class DonutChecker:
    """Check Donut SMP stats - EXACT Shulker.py implementation"""
    def __init__(self, session: requests.Session=None):
        """\nInitialize Donut SMP checker\n\nArgs:\n    session: Optional requests session\n"""
        self.session = session or requests.Session()
    def check_player(self, username: str) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nCheck Donut SMP stats using donutstats.net API\nEXACT CODE FROM SHULKER.PY line 302-382\n\nArgs:\n    username: Minecraft username\n\nReturns:\n    Dictionary with Donut SMP stats\n"""
        # ***<module>.DonutChecker.check_player: Failure: Compilation Error
        stats = {'has_joined': False, 'banned': None, 'money': None, 'playtime': None, 'playtime_hours': 0, 'shards': None, 'kills': None, 'deaths': None, 'blocks_placed': None, 'blocks_broken': None, 'mobs_killed': None, 'error': None}
        time.sleep(0.5)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        max_retries = 3
        tries = 0
        if tries < max_retries:
            response = requests.get(f'https://donutstats.net/api/stats/{username}', headers=headers, verify=False, timeout=10)
            if response.status_code == 200:
                result = response.json()
                stats = self._process_donut_stats(result)
                stats['has_joined'] = True
                logger.info(f'✅ Donut SMP: {stats['money']}, {stats['playtime']}')
                    return stats
                if response.status_code == 404:
                    logger.info('Player has never joined Donut SMP')
                    stats['error'] = 'Never joined Donut SMP'
                        return stats
                    if response.status_code == 400:
                        stats['error'] = 'Invalid username format'
                            return stats
                        tries += 1
                        if tries < max_retries:
                            time.sleep(1)
                            stats['error'] = f'API returned {response.status_code}'
            return stats
                    except requests.exceptions.Timeout:
                        tries += 1
                        if tries < max_retries:
                            time.sleep(1)
                            stats['error'] = 'Request timeout'
                        except Exception as e:
                                tries += 1
                                if tries >= max_retries:
                                    stats['error'] = str(e)
                except Exception as e:
                        logger.error(f'Donut SMP check error: {e}')
                        stats['error'] = str(e)
                        return stats
    def _process_donut_stats(self, result: Dict) -> Dict:
        """\nProcess DonutSMP API stats data (NO BAN CHECKING)\nEXACT CODE FROM SHULKER.PY line 383-418\n"""
        stats = {'has_joined': False, 'banned': None, 'money': None, 'playtime': None, 'playtime_hours': 0, 'shards': None, 'kills': None, 'deaths': None, 'blocks_placed': None, 'blocks_broken': None, 'mobs_killed': None, 'error': None}
        if 'money' in result:
            money_value = result['money']
            try:
                money_int = int(money_value)
                stats['money'] = f'${money_int:,}'
            except:
                stats['money'] = f'${money_value}'
        if 'playtime' in result:
            playtime_ms = int(result['playtime'])
            total_minutes = playtime_ms // 60000
            hours = total_minutes // 60
            minutes = total_minutes % 60
            stats['playtime'] = f'{hours}h {minutes}m'
            stats['playtime_hours'] = hours + minutes / 60.0
        if 'shards' in result:
            stats['shards'] = result['shards']
        if 'kills' in result:
            stats['kills'] = result['kills']
        if 'deaths' in result:
            stats['deaths'] = result['deaths']
        if 'placed_blocks' in result:
            stats['blocks_placed'] = f'{int(result['placed_blocks']):,}'
        if 'broken_blocks' in result:
            stats['blocks_broken'] = f'{int(result['broken_blocks']):,}'
        if 'mobs_killed' in result:
            stats['mobs_killed'] = result['mobs_killed']
        return stats
    def check_ban(self, username: str, access_token: str, uuid: str) -> str:
        # irreducible cflow, using cdg fallback
        """\nCheck DonutSMP ban status by attempting to connect to the server\nEXACT CODE FROM SHULKER.PY def donutban() method (line 567-760)\n\nArgs:\n    username: Minecraft username\n    access_token: Minecraft access token\n    uuid: Minecraft UUID\n\nReturns:\n    \"False\" if not banned, ban message if banned, None if error\n"""
        # ***<module>.DonutChecker.check_ban: Failure: Compilation Error
        if not MINECRAFT_LIB_AVAILABLE:
            logger.warning('Minecraft library not available - ban check disabled')
                return
            result = self._do_donut_ban_check(username, access_token, uuid)
            if result == 'False':
                logger.info(f'✅ [Donut] {username}: NOT BANNED')
                return result
                if result:
                    logger.warning(f'🚫 [Donut] {username}: BANNED - {result}')
                return result
                    except Exception as e:
                            logger.debug(f'[Donut] Ban check error: {e}')
                                return
                except Exception as e:
                        logger.error(f'Donut ban check error: {e}')
                        import traceback
                        logger.error(traceback.format_exc())
    def _do_donut_ban_check(self, username: str, access_token: str, uuid: str) -> str:
        # irreducible cflow, using cdg fallback
        """\nInternal method to perform DonutSMP ban check\nEXACT CODE FROM SHULKER.PY def donutban() method (line 567-760)\n"""
        # ***<module>.DonutChecker._do_donut_ban_check: Failure: Compilation Error
        auth_token = AuthenticationToken(username=username, access_token=access_token, client_token=uuid_module.uuid4().hex)
        auth_token.profile = Profile(id_=uuid, name=username)
        banned_status = None
        max_retries = 5
        tries = 0
        donut_protocol_versions = [393, 401, 404, 477, 498, 573, 575, 578, 735, 736, 751, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763]
        if tries < max_retries:
            for protocol_version in donut_protocol_versions:
                    connection = Connection('donutsmp.net', 25565, auth_token=auth_token, initial_version=protocol_version, allowed_versions={protocol_version})
                    def suppress_login_disconnect(exc_type, exc_value, exc_traceback):
                        if exc_type == LoginDisconnect:
                            return
                        else:
                            sys.__excepthook__(exc_type, exc_value, exc_traceback)
                    connection.exception_handler = suppress_login_disconnect
                    @connection.listener(clientbound.login.DisconnectPacket, early=True)
                    def login_disconnect(packet):
                        # irreducible cflow, using cdg fallback
                        nonlocal banned_status
                        # ***<module>.DonutChecker._do_donut_ban_check.login_disconnect: Failure: Compilation Error
                        data = json.loads(str(packet.json_data))
                        disconnect_message = ''
                        if 'extra' in data and isinstance(data['extra'], list):
                            disconnect_message = ''.join((str(item.get('text', '')) for item in data['extra']))
                        else:
                            if 'text' in data:
                                disconnect_message = str(data['text'])
                            else:
                                disconnect_message = str(data)
                        if 'only compatible with minecraft 1.13' in disconnect_message.lower():
                            logger.debug(f'[Ban Check] Protocol {protocol_version} incompatible, trying next version...')
                                return
                            message_lower = disconnect_message.lower()
                            not_banned_indicators = ['whitelist', 'server is full', 'outdated client', 'outdated server', 'already online', 'restarting your game']
                            is_not_banned = any((indicator in message_lower for indicator in not_banned_indicators))
                            ban_indicators = ['discord.gg/donutsmp', 'banned', 'suspended', 'blacklisted', 'you are not allowed', 'appeal at']
                            is_banned = any((indicator in message_lower for indicator in ban_indicators))
                            if is_banned:
                                banned_status = 'Banned'
                                if is_not_banned:
                                    banned_status = 'False'
                                    banned_status = disconnect_message
                                except Exception as e:
                                        logger.error(f'[Ban Check] Error in Donut disconnect handler: {e}')
                                        import traceback
                                        logger.debug(f'[Ban Check] Disconnect handler traceback: {traceback.format_exc()}')
                                        banned_status = f'Error: {str(e)}'
                    @connection.listener(clientbound.play.JoinGamePacket, early=True)
                    def joined_server(packet):
                        nonlocal banned_status
                        # ***<module>.DonutChecker._do_donut_ban_check.joined_server: Failure: Compilation Error
                        if banned_status is None:
                            banned_status = 'False'
                        original_stderr = sys.stderr
                        sys.stderr = StringIO()
                            connection.connect()
                            wait_cycles = 0
                            max_wait = 1000
                            if banned_status is None and wait_cycles < max_wait:
                                time.sleep(0.01)
                                wait_cycles += 1
                                if banned_status is not None and wait_cycles >= 100:
                                    pass
                                connection.disconnect()
                                    sys.stderr = original_stderr
                                            if banned_status is not None:
                                                    if banned_status is not None:
                                                        return banned_status
                                                        tries += 1
            return banned_status
                                        pass
                                            except LoginDisconnect:
                                                    pass
                                                except Exception as e:
                                                        logger.debug(f'[Ban Check] Connection error: {e}')
                            except Exception as e:
                                    logger.debug(f'[Ban Check] Outer connection error: {e}')
                except Exception as e:
                        logger.error(f'Donut ban check error: {e}')
                        import traceback
                        logger.error(traceback.format_exc())