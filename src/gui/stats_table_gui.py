# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\gui\\stats_table_gui.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nStats Table GUI Component\nDisplays detailed account statistics in a table format\n"""
import customtkinter as ctk
from typing import Dict
DARK_THEME = {'background': '#0F111A', 'surface': '#1E2433', 'surface_hover': '#252E42', 'border': '#2A3441', 'text_primary': '#E8F0F8', 'text_secondary': '#9CA3AF'}
class StatsTable(ctk.CTkScrollableFrame):
    # ***<module>.StatsTable: Failure: Different bytecode
    """Detailed stats table for GUI"""
    def __init__(self, parent, **kwargs):
        # ***<module>.StatsTable.__init__: Failure: Compilation Error
        kwargs.setdefault('fg_color', DARK_THEME['background'])
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        title = ctk.CTkLabel(self, text='📊 Account Statistics', font=('Segoe UI', 18, 'bold'), text_color=DARK_THEME['text_primary'])
        title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20), sticky='w')
        self.stat_labels = {}
        self.stats_config = [('📧 Email Domains', [('hotmail_accounts', 'Hotmail'), ('outlook_accounts', 'Outlook'), ('live_accounts', 'Live'), ('gmail_accounts', 'Gmail'), ('other_accounts', 'Other')]), ('🎮 Minecraft Ownership', [('minecraft_java_owned', 'Java Only'), ('minecraft_bedrock_owned', 'Bedrock Only'), ('minecraft_both_owned', 'Java + Bedrock'), ('gamepass_only', 'Game Pass Only'), ('no_minecraft', 'No Minecraft')]), ('🔒 Security Status', [('clean_accounts', 'Clean (No 2FA)'), ('2fa_enabled', '2FA Enabled'), ('security_pending', 'Pending Changes')]), ('🔄 Auto Mark Lost', [('mark_lost_success', 'Success'), ('mark_lost_failed', 'Failed'), ('mark_lost_skipped', 'Skipped (No Java)')]), ('💰 MS Rewards', [('high_rewards', 'High Points (500+)')]), ('⚔️ Hypixel', [(
        self._build_table()
    def _build_table(self):
        """Build the stats table"""
        # ***<module>.StatsTable._build_table: Failure: Different bytecode
        current_row = 1
        for category, stats in self.stats_config:
            header_frame = ctk.CTkFrame(self, fg_color=DARK_THEME['surface'], corner_radius=5, border_width=1, border_color=DARK_THEME['border'])
            header_frame.grid(row=current_row, column=0, columnspan=2, padx=5, pady=(15, 5), sticky='ew')
            header = ctk.CTkLabel(header_frame, text=category, font=('Segoe UI', 14, 'bold'), text_color=DARK_THEME['text_primary'])
            header.pack(padx=10, pady=5)
            current_row += 1
            for stat_key, stat_name in stats:
                name_label = ctk.CTkLabel(self, text=f'  {stat_name}:', font=('Segoe UI', 12), anchor='w', text_color=DARK_THEME['text_secondary'])
                name_label.grid(row=current_row, column=0, padx=10, pady=2, sticky='w')
                value_label = ctk.CTkLabel(self, text='0', font=('Segoe UI', 12, 'bold'), anchor='e', text_color=DARK_THEME['text_primary'])
                value_label.grid(row=current_row, column=1, padx=10, pady=2, sticky='e')
                self.stat_labels[stat_key] = value_label
                current_row += 1
    def update_stats(self, stats: Dict):
        # irreducible cflow, using cdg fallback
        """\nUpdate all stats\n\nArgs:\n    stats: Stats dictionary from checker engine\n"""
        # ***<module>.StatsTable.update_stats: Failure: Compilation Error
        if not stats:
            return
            for stat_key, label in self.stat_labels.items():
                value = stats.get(stat_key, 0)
                label.configure(text=str(value))
            except Exception as e:
                    return None
class CompactStatsDisplay(ctk.CTkFrame):
    """Compact stats display for main GUI window"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.stat_frames = {}
        self._create_stat_displays()
    def _create_stat_displays(self):
        """Create compact stat display boxes"""
        stats_config = [[('valid', '✅ Valid', 'green'), ('invalid', '❌ Invalid', 'red'), ('checked', '📊 Checked', 'blue')], [('minecraft_java_owned', '🎮 Java Owned', 'green'), ('minecraft_both_owned', '🎮 Both Owned', 'orange'), ('gamepass_only', '🎮 Game Pass', 'yellow')], [('mark_lost_success', '✅ Mark Lost', 'green'), ('nitro_claimed', '🎁 Nitro Claimed', 'purple'), ('clean_accounts', '🔓 Clean', 'cyan')]]
        for row_idx, row_stats in enumerate(stats_config):
            for col_idx, (stat_key, stat_label, color) in enumerate(row_stats):
                frame = self._create_stat_box(stat_label, color)
                frame.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky='ew')
                self.stat_frames[stat_key] = frame
    def _create_stat_box(self, label: str, color: str):
        """Create a single stat box"""
        # ***<module>.CompactStatsDisplay._create_stat_box: Failure: Different bytecode
        frame = ctk.CTkFrame(self, fg_color=DARK_THEME['surface'], corner_radius=8, border_width=1, border_color=DARK_THEME['border'])
        frame.grid_columnconfigure(0, weight=1)
        label_widget = ctk.CTkLabel(frame, text=label, font=('Segoe UI', 11), text_color=DARK_THEME['text_primary'])
        label_widget.grid(row=0, column=0, padx=10, pady=(8, 2))
        value_widget = ctk.CTkLabel(frame, text='0', font=('Segoe UI', 20, 'bold'), text_color=DARK_THEME['text_primary'])
        value_widget.grid(row=1, column=0, padx=10, pady=(2, 8))
        frame.value_label = value_widget
        return frame
    def update_stats(self, stats: Dict):
        """Update stats display"""
        for stat_key, frame in self.stat_frames.items():
            value = stats.get(stat_key, 0)
            frame.value_label.configure(text=str(value))