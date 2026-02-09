# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\storage\\categorizer.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nSimplified Result Categorizer\nSaves results in simple, easy-to-use format\n"""
import os
import re
from datetime import datetime
from typing import Dict, Optional, Set
from src.utils.logger import get_logger
logger = get_logger()
class SimplifiedCategorizer:
    # ***<module>.SimplifiedCategorizer: Failure detected at line number 113 and instruction offset 120: Different bytecode
    """Simple result categorization - one folder, many txt files"""
    def __init__(self, session_name: Optional[str]=None):
        """Initialize categorizer with simple structure"""
        # ***<module>.SimplifiedCategorizer.__init__: Failure: Compilation Error
        if session_name is None:
            session_name = f'session_{datetime.now().strftime('%Y%m%d_%H%M%S')}'
        self.session_name = session_name
        self.base_path = os.path.join('results', session_name)
        os.makedirs(self.base_path, exist_ok=True)
        logger.info(f'💾 Results folder: {self.base_path}')
        self.files = {'valid': os.path.join(self.base_path, 'valid.txt'), 'minecraft_hits': os.path.join(self.base_path, 'minecraft_hits.txt'), '2fa_hits': os.path.join(self.base_path, '2fa_hits.txt'), 'auto_mark_lost': os.path.join(self.base_path, 'auto_mark_lost.txt'), 'nitro_claimed': os.path.join(self.base_path, 'nitro_claimed.txt'), 'nitro_unclaimed': os.path.join(self.base_path, 'nitro_unclaimed.txt'), 'gamepass': os.path.join(self.base_path, 'gamepass.txt'), 'gamepass_ultimate': os.path.join(self.base_path, 'gamepass_ultimate.txt'), 'xbox_codes': os.path.join(self.base_path, 'xbox_codes.txt'), 'ms_rewards': os.path.join(self.base_path, 'ms_rewards.txt'), 'hypixel_banned': os.path.join(self.base_path, 'hypixel_banned.txt'), 'hypixel_unbanned': os.path.join(self.base_path, '
        self.saved_xbox_codes = set()
        self.saved_hits = set()
        for filepath in self.files.values():
            if not os.path.exists(filepath):
                open(filepath, 'w', encoding='utf-8').close()
    def save_result(self, account_data: Dict):
        # irreducible cflow, using cdg fallback
        """Save account result to appropriate files"""
        # ***<module>.SimplifiedCategorizer.save_result: Failure: Compilation Error
        email = account_data.get('email', 'unknown')
        password = account_data.get('password', '')
        if account_data.get('error'):
            return
            has_minecraft = False
            has_xbox = False
            minecraft_data = account_data.get('minecraft')
            if minecraft_data and isinstance(minecraft_data, dict):
                    minecraft = minecraft_data.get('ownership', {})
                    if minecraft and isinstance(minecraft, dict) and (minecraft.get('minecraft_java_owned') or minecraft.get('minecraft_bedrock_owned') or minecraft.get('minecraft_java_gamepass') or minecraft.get('minecraft_bedrock_gamepass')):
                                has_minecraft = True
            xbox = account_data.get('xbox', {})
            if xbox and isinstance(xbox, dict) and xbox.get('gamertag'):
                        has_xbox = True
            if not has_minecraft and (not has_xbox):
                    self._append_to_file('valid', f'{email}:{password}')
            minecraft_data = account_data.get('minecraft')
            is_minecraft_hit = False
            if minecraft_data and isinstance(minecraft_data, dict):
                    minecraft = minecraft_data.get('ownership', {})
                    if minecraft and isinstance(minecraft, dict) and (minecraft.get('minecraft_java_owned') or minecraft.get('minecraft_bedrock_owned')):
                                is_minecraft_hit = True
                                profile = minecraft_data.get('profile', {})
                                username = profile.get('username', 'N/A') if isinstance(profile, dict) else 'N/A'
                                self._append_to_file('minecraft_hits', f'{email}:{password} | Username: {username}')
                                self._add_to_all_hits(f'{email}:{password}')
            security = account_data.get('security', {})
            if security and isinstance(security, dict) and (security.get('status') == '2fa_enabled'):
                        self._append_to_file('2fa_hits', f'{email}:{password}')
            mark_lost = account_data.get('mark_lost', {})
            if mark_lost and isinstance(mark_lost, dict) and mark_lost.get('success'):
                        recovery_email = mark_lost.get('new_recovery_email', '')
                        recovery_pass = 'ShulkerEmails(n{5})'
                        date = datetime.now().strftime('%Y-%m-%d')
                        self._append_to_file('auto_mark_lost', f'{email}:{password}:{recovery_email}:{recovery_pass}:{date}')
            nitro = account_data.get('nitro', {})
            if nitro and isinstance(nitro, dict) and nitro.get('eligible'):
                        promo_code = nitro.get('promo_code', 'N/A')
                        link = nitro.get('redemption_link', 'N/A')
                        if nitro.get('status') == 'claimed':
                            self._append_to_file('nitro_claimed', f'{email}:{password} | Code: {promo_code} | Link: {link}')
                        else:
                            if nitro.get('status') == 'available':
                                self._append_to_file('nitro_unclaimed', f'{email}:{password} | Link: {link}')
            minecraft_data = account_data.get('minecraft')
            minecraft = {}
            has_gamepass_pc = False
            has_gamepass_ultimate = False
            if minecraft_data and isinstance(minecraft_data, dict):
                    minecraft = minecraft_data.get('ownership', {})
                    if minecraft and isinstance(minecraft, dict):
                            has_gamepass_pc = minecraft.get('gamepass_pc', False)
                            has_gamepass_ultimate = minecraft.get('gamepass_ultimate', False)
            if has_gamepass_ultimate:
                self._append_to_file('gamepass_ultimate', f'{email}:{password}')
                self._add_to_all_hits(f'{email}:{password}')
            else:
                if has_gamepass_pc:
                    self._append_to_file('gamepass', f'{email}:{password}')
                    self._add_to_all_hits(f'{email}:{password}')
                else:
                    if nitro and isinstance(nitro, dict) and nitro.get('eligible'):
                                self._append_to_file('gamepass_ultimate', f'{email}:{password}')
                                self._add_to_all_hits(f'{email}:{password}')
            rewards = account_data.get('rewards', {})
            if rewards and isinstance(rewards, dict) and (rewards.get('available_points', 0) > 0):
                        points = rewards.get('available_points')
                        self._append_to_file('ms_rewards', f'{email}:{password} | Balance: {points} points')
            hypixel = account_data.get('hypixel', {})
            if hypixel and isinstance(hypixel, dict):
                    banned = hypixel.get('banned', False)
                    username = hypixel.get('username') or hypixel.get('hypixel_name') or hypixel.get('name', 'N/A')
                    if username == 'N/A' and minecraft_data and isinstance(minecraft_data, dict):
                                profile = minecraft_data.get('profile', {})
                                if profile and isinstance(profile, dict):
                                        username = profile.get('username', 'N/A')
                    capes_list = []
                    if minecraft_data and isinstance(minecraft_data, dict):
                            profile = minecraft_data.get('profile', {})
                            if profile and isinstance(profile, dict):
                                    capes = profile.get('capes', [])
                                    if capes and isinstance(capes, list):
                                            for cape in capes:
                                                if isinstance(cape, dict):
                                                    alias = cape.get('alias', '')
                                                    if alias:
                                                        capes_list.append(alias)
                    capes_str = ', '.join(capes_list) if capes_list else 'None'
                    if banned and str(banned).lower()!= 'false':
                        self._append_to_file('hypixel_banned', f'{email}:{password} | {username} | {capes_str}')
                    else:
                        if banned == 'False' or (banned is False and hypixel.get('has_joined')):
                            self._append_to_file('hypixel_unbanned', f'{email}:{password} | {username} | {capes_str}')
            donut = account_data.get('donut', {})
            if donut and isinstance(donut, dict):
                    banned = donut.get('banned', False)
                    username = donut.get('username') or donut.get('name', 'N/A')
                    if username == 'N/A' and minecraft_data and isinstance(minecraft_data, dict):
                                profile = minecraft_data.get('profile', {})
                                if profile and isinstance(profile, dict):
                                        username = profile.get('username', 'N/A')
                    capes_list = []
                    if minecraft_data and isinstance(minecraft_data, dict):
                            profile = minecraft_data.get('profile', {})
                            if profile and isinstance(profile, dict):
                                    capes = profile.get('capes', [])
                                    if capes and isinstance(capes, list):
                                            for cape in capes:
                                                if isinstance(cape, dict):
                                                    alias = cape.get('alias', '')
                                                    if alias:
                                                        capes_list.append(alias)
                    capes_str = ', '.join(capes_list) if capes_list else 'None'
                    if banned and str(banned).lower()!= 'false':
                        self._append_to_file('donut_banned', f'{email}:{password} | {username} | {capes_str}')
                    else:
                        if banned == 'False' or banned is False:
                            self._append_to_file('donut_unbanned', f'{email}:{password} | {username} | {capes_str}')
            self._save_capture(account_data)
            except Exception as e:
                    logger.error(f'Failed to save result for {account_data.get('email')}: {e}')
    def _save_capture(self, account_data: Dict):
        """Save detailed capture of all account info"""
        email = account_data.get('email', 'unknown')
        password = account_data.get('password', '')
        capture_text = f'\n{'======================================================================'}\n'
        capture_text += f'ACCOUNT: {email}\n'
        capture_text += f'PASSWORD: {password}\n'
        capture_text += f'CHECKED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n'
        capture_text += f'{'======================================================================'}\n\n'
        security = account_data.get('security', {})
        if security:
            capture_text += '🔒 SECURITY:\n'
            capture_text += f'   Status: {security.get('status', 'N/A')}\n\n'
        minecraft = account_data.get('minecraft', {})
        if minecraft:
            ownership = minecraft.get('ownership', {})
            profile = minecraft.get('profile', {})
            capture_text += '🎮 MINECRAFT:\n'
            capture_text += f'   Java: {('OWNED' if ownership.get('minecraft_java_owned') else 'No')}\n'
            capture_text += f'   Bedrock: {('OWNED' if ownership.get('minecraft_bedrock_owned') else 'No')}\n'
            if ownership.get('minecraft_java_gamepass'):
                capture_text += '   Game Pass: Java\n'
            if ownership.get('minecraft_bedrock_gamepass'):
                capture_text += '   Game Pass: Bedrock\n'
            if profile.get('username'):
                capture_text += f'   Username: {profile.get('username')}\n'
            capes = profile.get('capes', [])
            if capes and isinstance(capes, list):
                cape_names = []
                for cape in capes:
                    if isinstance(cape, dict):
                        alias = cape.get('alias', '')
                        if alias:
                            cape_names.append(alias)
                if cape_names:
                    capture_text += f'   Capes: {', '.join(cape_names)}\n'
                else:
                    capture_text += '   Capes: None\n'
            else:
                if capes:
                    capture_text += f'   Capes: {capes}\n'
            if profile.get('name_change_allowed') is not None:
                capture_text += f'   Can Change Name: {profile.get('name_change_allowed')}\n'
            capture_text += '\n'
        xbox = account_data.get('xbox', {})
        if xbox and xbox.get('gamertag'):
                capture_text += '🎮 XBOX:\n'
                capture_text += f'   Gamertag: {xbox.get('gamertag')}\n\n'
        nitro = account_data.get('nitro', {})
        if nitro and nitro.get('eligible'):
                capture_text += '💜 DISCORD NITRO:\n'
                capture_text += f'   Status: {nitro.get('status', 'N/A').upper()}\n'
                if nitro.get('promo_code'):
                    capture_text += f'   Promo Code: {nitro.get('promo_code')}\n'
                if nitro.get('redemption_link'):
                    capture_text += f'   Link: {nitro.get('redemption_link')}\n'
                capture_text += '\n'
        mark_lost = account_data.get('mark_lost', {})
        if mark_lost and mark_lost.get('success'):
                capture_text += '🔄 AUTO MARK LOST:\n'
                capture_text += '   Status: SUCCESS\n'
                capture_text += f'   New Recovery: {mark_lost.get('new_recovery_email', 'N/A')}\n\n'
        rewards = account_data.get('rewards', {})
        if rewards and rewards.get('available_points', 0) > 0:
                capture_text += '💰 MS REWARDS:\n'
                capture_text += f'   Balance: {rewards.get('available_points')} points\n\n'
        hypixel = account_data.get('hypixel', {})
        if hypixel and isinstance(hypixel, dict):
                capture_text += '⚔️ HYPIXEL:\n'
                level = hypixel.get('level', 'N/A')
                rank = hypixel.get('rank', 'None')
                banned = hypixel.get('banned', False)
                capture_text += f'   Level: {(str(level) if level!= 'N/A' else 'N/A')}\n'
                capture_text += f'   Rank: {(str(rank) if rank!= 'None' else 'None')}\n'
                capture_text += f'   Banned: {str(banned)}\n\n'
        donut = account_data.get('donut', {})
        if donut and isinstance(donut, dict):
                capture_text += '🍩 DONUT SMP:\n'
                balance = donut.get('balance', 0)
                playtime = donut.get('playtime_hours', 0)
                banned = donut.get('banned', False)
                capture_text += f'   Balance: ${str(balance)}\n'
                capture_text += f'   Playtime: {str(playtime)}h\n'
                capture_text += f'   Banned: {str(banned)}\n\n'
        capture_text += f'{'======================================================================'}\n'
        self._append_to_file('capture', capture_text)
    def _append_to_file(self, file_key: str, content: str):
        # irreducible cflow, using cdg fallback
        """Append content to file"""
        # ***<module>.SimplifiedCategorizer._append_to_file: Failure: Compilation Error
        filepath = self.files.get(file_key)
        if filepath:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(content + '\n')
                        except Exception as e:
                                logger.error(f'Failed to write to {file_key}: {e}')
    def _add_to_all_hits(self, email_pass: str):
        """Add email:pass to all_hits.txt with deduplication"""
        normalized = email_pass.lower().strip()
        if normalized and normalized not in self.saved_hits:
                self.saved_hits.add(normalized)
                self._append_to_file('all_hits', email_pass)
    def add_xbox_code(self, code: str, account_email: str=None):
        """Add Xbox code to codes file - only 25-char codes, no duplicates"""
        code_pattern = '([A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5})'
        match = re.search(code_pattern, code.upper())
        if not match:
            matches = re.findall(code_pattern, code.upper())
            if matches:
                extracted_code = matches[0]
            else:
                logger.debug(f'Could not extract Xbox code from: {code}')
                return
        else:
            extracted_code = match.group(1)
        if extracted_code in self.saved_xbox_codes:
            logger.debug(f'Skipping duplicate Xbox code: {extracted_code}')
            return
        else:
            self.saved_xbox_codes.add(extracted_code)
            self._append_to_file('xbox_codes', extracted_code)