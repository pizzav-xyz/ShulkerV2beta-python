# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\utils\\security.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global _DEBUG_DETECTED
global _SECURITY_ENABLED
# ***<module>: Failure: Different bytecode
"""\nSecurity Module - Anti-debugging, Anti-tampering, and Protection Features\n"""
import sys
import os
import ctypes
import time
import threading
from typing import Optional
_DEBUG_DETECTED = False
_SECURITY_ENABLED = True
def _is_debugger_present() -> bool:
    """Check if debugger is attached (Windows)"""
    if sys.platform!= 'win32':
        return False
    else:
        try:
            kernel32 = ctypes.windll.kernel32
            return bool(kernel32.IsDebuggerPresent())
        except:
            return False
def _check_vm() -> bool:
    # irreducible cflow, using cdg fallback
    """Detect if running in virtual machine"""
    # ***<module>._check_vm: Failure: Compilation Error
    if sys.platform!= 'win32':
        return False
    vm_indicators = ['VMware', 'VirtualBox', 'VBOX', 'QEMU', 'Xen', 'VMW', 'VIRTUAL', 'VM', 'HYPER-V']
        import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum')
            for i in range(10):
                        value = winreg.EnumValue(key, i)[1]
                        if any((indicator in value.upper() for indicator in vm_indicators)):
                            return True
                                            import psutil
                                            for proc in psutil.process_iter(['name']):
                                                    proc_name = proc.info['name'].upper()
                                                    if any((indicator in proc_name for indicator in vm_indicators)):
                                                        return True
                                                        return False
                                    pass
                                        except ImportError:
                                                pass
                                                            return False
                                                                    return False
def _check_debug_tools() -> bool:
    # irreducible cflow, using cdg fallback
    """Check for common debugging tools"""
    # ***<module>._check_debug_tools: Failure: Compilation Error
    if sys.platform!= 'win32':
        return False
    else:
        debug_tools = ['ollydbg.exe', 'x64dbg.exe', 'x32dbg.exe', 'windbg.exe', 'ida.exe', 'ida64.exe', 'idaq.exe', 'idaq64.exe', 'ghidra.exe', 'cheatengine.exe', 'processhacker.exe', 'procmon.exe', 'wireshark.exe', 'fiddler.exe', 'charles.exe', 'httpdebugger.exe', 'httpdebuggerpro.exe', 'fiddler.exe']
    import psutil
    for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()
            if proc_name in debug_tools:
                return True
                return False
                    return False
def _integrity_check() -> bool:
    # irreducible cflow, using cdg fallback
    """Check if executable has been tampered with"""
    # ***<module>._integrity_check: Failure: Compilation Error
    if not getattr(sys, 'frozen', False):
        return True
    exe_path = sys.executable
    if not os.path.exists(exe_path):
        return False
        stat = os.stat(exe_path)
        if stat.st_size < 1024:
            return False
            return True
                return False
def _monitor_debugging():
    # irreducible cflow, using cdg fallback
    """Background thread to monitor for debugging"""
    global _DEBUG_DETECTED
    # ***<module>._monitor_debugging: Failure: Compilation Error
    if _SECURITY_ENABLED:
        if _is_debugger_present():
            _DEBUG_DETECTED = True
            _trigger_protection()
                return
            if _check_debug_tools():
                _DEBUG_DETECTED = True
                _trigger_protection()
                    return
                if not _integrity_check():
                    _DEBUG_DETECTED = True
                    _trigger_protection()
                        return
                    time.sleep(2)
                time.sleep(2)
def _trigger_protection():
    # irreducible cflow, using cdg fallback
    """Trigger protection mechanisms when tampering detected"""
    # ***<module>._trigger_protection: Failure: Compilation Error
    os._exit(1)
            sys.exit(1)
                    return None
def init_security():
    """Initialize security features"""
    if not _SECURITY_ENABLED:
        return
    else:
        if _is_debugger_present():
            _trigger_protection()
            return
        else:
            if _check_vm():
                pass
            if _check_debug_tools():
                _trigger_protection()
            else:
                if not _integrity_check():
                    _trigger_protection()
                else:
                    monitor_thread = threading.Thread(target=_monitor_debugging, daemon=True)
                    monitor_thread.start()
def is_debug_detected() -> bool:
    """Check if debugging was detected"""
    return _DEBUG_DETECTED
def disable_security():
    """Disable security (for testing only)"""
    global _SECURITY_ENABLED
    _SECURITY_ENABLED = False