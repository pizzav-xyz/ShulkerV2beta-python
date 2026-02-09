# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\checkers\\hypixel_checker.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nHypixel Checker - EXACT CODE FROM SHULKER.PY\nStats from Plancke.io + Separate ban check function\n"""
import requests
import re
import json
import uuid as uuid_module
import time
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
class HypixelChecker:
    """Check Hypixel stats and ban status - EXACT Shulker.py implementation"""
    def __init__(self, session: requests.Session=None):
        """\nInitialize Hypixel checker\n\nArgs:\n    session: Optional requests session\n"""
        self.session = session or requests.Session()
    def check_player(self, username: str) -> Dict:
        # irreducible cflow, using cdg fallback
        """\nCheck Hypixel stats using Plancke.io (EXACT Shulker.py code)\nThis is STATS ONLY - ban check is separate!\n\nArgs:\n    username: Minecraft username\n\nReturns:\n    Dictionary with Hypixel stats (NO ban status)\n"""
        # ***<module>.HypixelChecker.check_player: Failure: Compilation Error
        stats = {'has_joined': False, 'hypixel_name': None, 'network_level': None, 'first_login': None, 'last_login': None, 'bedwars_stars': None, 'skyblock_coins': None, 'error': None}
        logger.debug(f'Fetching Hypixel stats from Plancke.io for: {username}')
        tx = requests.get(f'https://plancke.io/hypixel/player/stats/{username}', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}, verify=False, timeout=15).text
        if 'Player not found' in tx or 'never joined' in tx.lower():
            logger.info('Player has never joined Hypixel')
            stats['error'] = 'Never joined Hypixel'
            return stats
            stats['has_joined'] = True
            try:
                stats['hypixel_name'] = re.search('(?<=content=\"Plancke\" /><meta property=\"og:locale\" content=\"en_US\" /><meta property=\"og:description\" content=\").+?(?=\")', tx).group()
            except:
                pass
            try:
                stats['network_level'] = re.search('(?<=Level:</b> ).+?(?=<br/><b>)', tx).group()
            except:
                pass
            try:
                stats['first_login'] = re.search('(?<=<b>First login: </b>).+?(?=<br/><b>)', tx).group()
            except:
                pass
            try:
                stats['last_login'] = re.search('(?<=<b>Last login: </b>).+?(?=<br/>)', tx).group()
            except:
                pass
            try:
                stats['bedwars_stars'] = re.search('(?<=<li><b>Level:</b> ).+?(?=</li>)', tx).group()
            except:
                pass
            try:
                req = requests.get(f'https://sky.shiiyu.moe/stats/{username}', verify=False, timeout=15)
                stats['skyblock_coins'] = re.search('(?<= Networth: ).+?(?=\n)', req.text).group()
            except:
                pass
            logger.info(f'✅ Hypixel: Level {stats['network_level']}, BW Stars {stats['bedwars_stars']}')
            return stats
                except Exception as e:
                        logger.error(f'Hypixel check error: {e}')
                        stats['error'] = str(e)
                        return stats
    def check_ban(self, username: str, access_token: str, uuid: str) -> str:
        # irreducible cflow, using cdg fallback
        """\nCheck Hypixel ban status - SEPARATE function like Shulker.py\nEXACT CODE FROM SHULKER.PY def ban() method\n\nArgs:\n    username: Minecraft username\n    access_token: Minecraft access token\n    uuid: Minecraft UUID\n\nReturns:\n    \"False\" if not banned, ban message if banned, None if error\n"""
        # ***<module>.HypixelChecker.check_ban: Failure: Compilation Error
        if not MINECRAFT_LIB_AVAILABLE:
            logger.warning('Minecraft library not available - ban check disabled')
                return
            result = self._do_hypixel_ban_check(username, access_token, uuid)
            if result == 'False':
                logger.info(f'✅ [Hypixel] {username}: NOT BANNED')
                return result
                if result:
                    logger.warning(f'🚫 [Hypixel] {username}: BANNED - {result}')
                return result
                    except Exception as e:
                            logger.debug(f'[Hypixel] Ban check error: {e}')
                except Exception as e:
                        logger.error(f'Ban check error: {e}')
                        import traceback
                        logger.error(traceback.format_exc())
    def _do_hypixel_ban_check(self, username: str, access_token: str, uuid: str) -> str:
        # irreducible cflow, using cdg fallback
        """\nInternal method to perform Hypixel ban check\nEXACT CODE FROM SHULKER.PY def ban() method\n"""
        # ***<module>.HypixelChecker._do_hypixel_ban_check: Failure: Compilation Error
        auth_token = AuthenticationToken(username=username, access_token=access_token, client_token=uuid_module.uuid4().hex)
        auth_token.profile = Profile(id_=uuid, name=username)
        banned_status = None
        max_retries = 5
        tries = 0
        if tries < max_retries:
            connection = Connection('alpha.hypixel.net', 25565, auth_token=auth_token, initial_version=47, allowed_versions={'1.8', 47})
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
                # ***<module>.HypixelChecker._do_hypixel_ban_check.login_disconnect: Failure: Compilation Error
                data = json.loads(str(packet.json_data))
                if 'Suspicious activity' in str(data):
                    banned_status = f'[Permanently] Suspicious activity has been detected on your account. Ban ID: {data['extra'][6]['text'].strip()}'
                    if 'temporarily banned' in str(data):
                        banned_status = f'[{data['extra'][1]['text']}] {data['extra'][4]['text'].strip()} Ban ID: {data['extra'][8]['text'].strip()}'
                        if 'You are permanently banned from this server!' in str(data):
                            banned_status = f'[Permanently] {data['extra'][2]['text'].strip()} Ban ID: {data['extra'][6]['text'].strip()}'
                            if 'The Hypixel Alpha server is currently closed!' in str(data):
                                banned_status = 'False'
                                if 'Failed cloning your SkyBlock data' in str(data):
                                    banned_status = 'False'
                                    banned_status = ''.join((item['text'] for item in data['extra']))
                        except Exception as e:
                                logger.error(f'[Ban Check] Error in disconnect handler: {e}')
                                import traceback
                                logger.debug(f'[Ban Check] Disconnect handler traceback: {traceback.format_exc()}')
            @connection.listener(clientbound.play.JoinGamePacket, early=True)
            def joined_server(packet):
                nonlocal banned_status
                # ***<module>.HypixelChecker._do_hypixel_ban_check.joined_server: Failure: Compilation Error
                if banned_status is None:
                    banned_status = 'False'
                original_stderr = sys.stderr
                stderr_capture = StringIO()
                sys.stderr = stderr_capture
                connection_established = False
                connection_error = None
                try:
                    connection.connect()
                    connection_established = True
                except Exception as e:
                    connection_error = str(e)
                    logger.debug(f'[Ban Check] Connection failed: {e}')
                    stderr_content = stderr_capture.getvalue()
                    if stderr_content:
                        logger.debug(f'[Ban Check] Connection stderr: {stderr_content[:200]}')
                if connection_established:
                    c = 0
                    max_wait = 1000
                    if banned_status is None or c < max_wait:
                        time.sleep(0.01)
                        c += 1
                        if banned_status is not None and c >= 100:
                            pass
                        try:
                            connection.disconnect()
                        except:
                            pass
                        else:
                            pass
                        sys.stderr = original_stderr
                            sys.stderr = original_stderr
                            if banned_status is not None:
                                return banned_status
                                tries += 1
            return banned_status
                            except LoginDisconnect:
                                    pass
                                except Exception as e:
                                        logger.debug(f'[Ban Check] Connection error: {e}')
                except Exception as e:
                        logger.error(f'Ban check error: {e}')
                        import traceback
                        logger.error(traceback.format_exc())