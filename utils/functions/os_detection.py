from typing import Literal
import platform

OsType = Literal["windows", "linux", "macos", "unknown"]

def os_detection() -> OsType:
    """
    Detect the operating system and return a string representing it.
    """
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    else:
        return "unknown"