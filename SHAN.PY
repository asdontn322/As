import platform
import subprocess

def get_system_info():
    info = {
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
    }
    ram = subprocess.getoutput("wmic memorychip get capacity")
    cpu = subprocess.getoutput("wmic cpu get name")
    gpu = subprocess.getoutput("wmic path win32_VideoController get name")
    
    info["RAM"] = ram
    info["CPU"] = cpu
    info["GPU"] = gpu
    return info

print(get_system_info())
