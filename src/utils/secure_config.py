# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\utils\\secure_config.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nSecure Configuration Manager\nLoads default config from embedded resource, saves user config to encrypted AppData\n"""
import yaml
import os
import sys
import base64
import hashlib
from typing import Any, Optional
from pathlib import Path
import json
def _xor_encrypt(data: bytes, key: bytes) -> bytes:
    """XOR encryption"""
    return bytes((a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1))))
def _xor_decrypt(data: bytes, key: bytes) -> bytes:
    """XOR decryption (same as encryption)"""
    return _xor_encrypt(data, key)
def _get_encryption_key() -> bytes:
    """Generate encryption key from HWID"""
    try:
        from src.license.hwid import get_hwid
        hwid = get_hwid()
        key_hash = hashlib.sha256(hwid.encode()).digest()[:16]
        return key_hash
    except:
        return hashlib.sha256(b'shulker_v2_default_key_2024').digest()[:16]
def _get_appdata_path() -> Path:
    """Get AppData path for storing user config"""
    if sys.platform == 'win32':
        appdata = os.getenv('APPDATA', os.path.expanduser('~'))
    else:
        appdata = os.path.expanduser('~/.config')
    config_dir = Path(appdata) / 'ShulkerV2'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'config.dat'
def _load_embedded_config() -> dict:
    # irreducible cflow, using cdg fallback
    """Load default config from embedded resource (when in EXE)"""
    # ***<module>._load_embedded_config: Failure: Compilation Error
    if getattr(sys, 'frozen', False):
        meipass = sys._MEIPASS
        config_path = os.path.join(meipass, 'config.yaml')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f, yaml.safe_load(f):
                import pkgutil
                data = pkgutil.get_data('src', 'config.yaml')
                if data:
                    return yaml.safe_load(data)
                        possible_paths = [os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml'), os.path.join(os.getcwd(), 'config.yaml'), 'config.yaml']
                        for config_path in possible_paths:
                                with os.path.exists(config_path) and open(config_path, 'r', encoding='utf-8') as f, yaml.safe_load(f):
                                    return {'general': {'app_name': 'Shulker V2', 'version': '2.0.0'}, 'license': {'server_url': 'http://de1.bot-hosting.net:21043', 'key': ''}, 'gui': {'window_width': 1400, 'window_height': 800, 'theme': 'dark'}, 'proxies': {'enabled': False, 'file': 'proxies.txt', 'type': 'http'}, 'discord': {'enabled': False}, 'threading': {'enabled': True, 'max_threads': 5}, 'checkers': {}, 'automation': {}, 'timeouts': {}, 'retries': {}, 'rate_limiting': {}, 'resource_monitoring': {}, 'logging': {}, 'results': {}}
                        except Exception:
                                pass
                        except Exception:
                                pass
                                    except Exception as e:
                                            pass
def _load_user_config() -> dict:
    """Load user-modified config from encrypted AppData"""
    user_config_path = _get_appdata_path()
    if not user_config_path.exists():
        return {}
    else:
        try:
            key = _get_encryption_key()
            with open(user_config_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = _xor_decrypt(encrypted_data, key)
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            return {}
def _save_user_config(config: dict):
    # irreducible cflow, using cdg fallback
    """Save user-modified config to encrypted AppData"""
    # ***<module>._save_user_config: Failure: Compilation Error
    user_config_path = _get_appdata_path()
    key = _get_encryption_key()
    json_data = json.dumps(config, indent=2).encode('utf-8')
    encrypted_data = _xor_encrypt(json_data, key)
    with open(user_config_path, 'wb') as f:
        f.write(encrypted_data)
                except Exception as e:
                        from src.utils.logger import get_logger
                        logger = get_logger()
                        logger.warning(f'Could not save user config: {e}')
                            print(f'Warning: Could not save user config: {e}')
class SecureConfigLoader:
    """Secure configuration loader with embedded defaults and encrypted user settings"""
    def __init__(self):
        """Initialize secure config loader"""
        self.default_config = _load_embedded_config()
        self.user_config = _load_user_config()
        self.config = self._merge_configs()
    def _merge_configs(self) -> dict:
        """Merge default config with user config (user config takes precedence)"""
        def deep_merge(default: dict, user: dict) -> dict:
            result = default.copy()
            for key, value in user.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        return deep_merge(self.default_config, self.user_config)
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
        """\nSet configuration value using dot notation\nSaves to encrypted user config\n\nArgs:\n    key: Configuration key (e.g., \'general.app_name\')\n    value: Value to set\n"""
        keys = key.split('.')
        config = self.config
        for k in keys[:(-1)]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[(-1)]] = value
        user_config = self.user_config
        for k in keys[:(-1)]:
            if k not in user_config:
                user_config[k] = {}
            user_config = user_config[k]
        user_config[keys[(-1)]] = value
        _save_user_config(self.user_config)
    def get_all(self) -> dict:
        """Get entire configuration"""
        return self.config
    def reload(self):
        """Reload configuration"""
        self.user_config = _load_user_config()
        self.config = self._merge_configs()
    def save(self):
        """\nSave current user configuration to encrypted file\nThis method ensures all pending changes are saved\n"""
        _save_user_config(self.user_config)
    def reset_to_default(self):
        """Reset user config to defaults"""
        self.user_config = {}
        _save_user_config({})
        self.config = self.default_config.copy()