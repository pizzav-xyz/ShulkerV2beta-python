# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'src\\license\\hwid.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""\nHardware ID (HWID) generator for license system\nCross-platform: Windows & Linux\n"""
import hashlib
import uuid
import platform
import subprocess
import os
def get_hwid() -> str:
    """\nGenerate unique hardware ID for this machine\n\nReturns:\n    SHA256 hash of hardware identifiers\n"""
    system = platform.system()
    hwid_components = []
    if system == 'Windows':
        hwid_components = _get_windows_hwid()
    else:
        if system == 'Linux':
            hwid_components = _get_linux_hwid()
        else:
            hwid_components = [str(uuid.getnode())]
    hwid_string = '_'.join(filter(None, hwid_components))
    hwid = hashlib.sha256(hwid_string.encode()).hexdigest()
    return hwid
def _get_windows_hwid() -> list:
    """Get hardware identifiers on Windows"""
    components = []
    try:
        cpu_id = subprocess.check_output('wmic cpu get ProcessorId', shell=True, stderr=subprocess.DEVNULL).decode().split('\n')[1].strip()
        components.append(cpu_id)
    except:
        pass
    try:
        disk_serial = subprocess.check_output('wmic diskdrive get SerialNumber', shell=True, stderr=subprocess.DEVNULL).decode().split('\n')[1].strip()
        components.append(disk_serial)
    except:
        pass
    try:
        mb_serial = subprocess.check_output('wmic baseboard get SerialNumber', shell=True, stderr=subprocess.DEVNULL).decode().split('\n')[1].strip()
        components.append(mb_serial)
    except:
        pass
    if not components:
        components.append(str(uuid.getnode()))
    return components
def _get_linux_hwid() -> list:
    # irreducible cflow, using cdg fallback
    """Get hardware identifiers on Linux"""
    # ***<module>._get_linux_hwid: Failure: Compilation Error
    components = []
    with open('/etc/machine-id', 'r') as f:
        machine_id = f.read().strip()
        components.append(machine_id)
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'Serial' in line:
                            cpu_serial = line.split(':')[1].strip()
                            components.append(cpu_serial)
                            break
                        try:
                            disk_serial = subprocess.check_output('lsblk -o SERIAL -n | head -1', shell=True, stderr=subprocess.DEVNULL).decode().strip()
                            if disk_serial:
                                components.append(disk_serial)
                        except:
                            pass
                        if not components:
                            components.append(str(uuid.getnode()))
                        return components
                    pass
                        pass
def get_system_info() -> dict:
    """\nGet system information for debugging\n\nReturns:\n    Dictionary with system info\n"""
    return {'platform': platform.system(), 'platform_release': platform.release(), 'platform_version': platform.version(), 'architecture': platform.machine(), 'processor': platform.processor(), 'hostname': platform.node(), 'hwid': get_hwid()}
if __name__ == '__main__':
    print('System Info:')
    info = get_system_info()
    for key, value in info.items():
        print(f'  {key}: {value}')
    print(f'\nHWID: {get_hwid()}')