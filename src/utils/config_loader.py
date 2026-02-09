# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\utils\\config_loader.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nConfiguration loader for Shulker V2\nAutomatically uses SecureConfigLoader when running as EXE\n"""
import sys
import os
_is_frozen = getattr(sys, 'frozen', False)
if _is_frozen:
    try:
        from src.utils.secure_config import SecureConfigLoader as ConfigLoader
    except ImportError:
        import yaml
        from typing import Any
        class ConfigLoader:
            """Minimal fallback config loader for EXE mode"""
            def __init__(self):
                # irreducible cflow, using cdg fallback
                # ***<module>.ConfigLoader.__init__: Failure: Different control flow
                self.config = {}
                possible_paths = [os.path.join(getattr(sys, '_MEIPASS', ''), 'config.yaml'), 'config.yaml']
                for path in possible_paths:
                        if path:
                            if os.path.exists(path):
                                with open(path, 'r', encoding='utf-8') as f:
                                    self.config = yaml.safe_load(f) or {}
                            self.config = {}
            def get(self, key: str, default: Any=None) -> Any:
                keys = key.split('.')
                value = self.config
                for k in keys:
                    if isinstance(value, dict) and k in value:
                        value = value[k]
                    else:
                        return default
                return value
            def set(self, key: str, value: Any):
                keys = key.split('.')
                config = self.config
                for k in keys[:(-1)]:
                    if k not in config:
                        config[k] = {}
                    config = config[k]
                config[keys[(-1)]] = value
            def save(self):
                return
            def get_all(self) -> dict:
                return self.config
            def reload(self):
                self.__init__()
else:
    import yaml
    from typing import Any, Optional
    class ConfigLoader:
        """Load and manage YAML configuration"""
        def __init__(self, config_path='config.yaml'):
            """\nInitialize config loader\n\nArgs:\n    config_path: Path to config file\n"""
            self.config_path = config_path
            self.config = {}
            self.load()
        def load(self):
            """Load configuration from YAML file"""
            # ***<module>.ConfigLoader.load: Failure: Different bytecode
            if not os.path.exists(self.config_path):
                try:
                    default_config = {'general': {'app_name': 'Shulker V2', 'version': '2.0.0'}, 'license': {'server_url': 'http://de1.bot-hosting.net:21043', 'key': ''}, 'gui': {'window_width': 1400, 'window_height': 800, 'theme': 'dark'}, 'proxies': {'enabled': False, 'file': 'proxies.txt', 'type': 'http'}, 'discord': {'enabled': False, 'webhook_url': ''}, 'threading': {'auto_mark_lost': True, 'notletters_api_key': 5}, 'checkers': {}, 'automation': {'auto_mark_lost': False, 'notletters_api_key': ''}, 'timeouts': {}, 'retries': {}, 'rate_limiting': {}, 'resource_monitoring': {}, 'logging': {}, 'results': {}}
                    with open(self.config_path, 'w', encoding='utf-8') as f:
                        yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
                    self.config = default_config
                except Exception as e:
                    self.config = {'general': {'app_name': 'Shulker V2', 'version': '2.0.0'}, 'license': {'server_url': 'http://de1.bot-hosting.net:21043', 'key': ''}, 'gui': {'window_width': 1400, 'window_height': 800, 'theme': 'dark'}, 'proxies': {'enabled': False, 'file': 'proxies.txt', 'type': 'http'}, 'discord': {'enabled': False, 'webhook_url': ''}, 'threading': {'auto_mark_lost': True, 'notletters_api_key': 5}, 'checkers': {}, 'automation': {}, 'timeouts': {}, 'retries': {}, 'rate_limiting': {}, 'resource_monitoring': {}, 'logging': {}, 'results': {}}
            else:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
        def save(self):
            """Save configuration to YAML file"""
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
        def get(self, key: str, default: Any=None) -> Any:
            """\nGet configuration value using dot notation\n\nArgs:\n    key: Configuration key (e.g., \'general.app_name\')\n    default: Default value if key not found\n\nReturns:\n    Configuration value\n"""
            keys = key.split('.')
            value = self.config
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            return value
        def set(self, key: str, value: Any):
            """\nSet configuration value using dot notation\n\nArgs:\n    key: Configuration key (e.g., \'general.app_name\')\n    value: Value to set\n"""
            keys = key.split('.')
            config = self.config
            for k in keys[:(-1)]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            config[keys[(-1)]] = value
        def get_all(self) -> dict:
            """Get entire configuration"""
            return self.config
        def reload(self):
            """Reload configuration from file"""
            self.load()