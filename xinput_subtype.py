import ctypes
from ctypes import wintypes

# Load xinput1_4.dll (fallback to xinput1_3 or xinput9_1_0 if needed)
for dll in ("xinput1_4.dll", "xinput1_3.dll", "xinput9_1_0.dll"):
    try:
        xinput = ctypes.WinDLL(dll)
        break
    except OSError:
        xinput = None
if xinput is None:
    raise OSError("No XInput DLL found")

# Types and structures
XINPUT_DEVTYPE_GAMEPAD = 0x01

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", wintypes.WORD),
        ("bLeftTrigger", wintypes.BYTE),
        ("bRightTrigger", wintypes.BYTE),
        ("sThumbLX", ctypes.c_short),
        ("sThumbLY", ctypes.c_short),
        ("sThumbRX", ctypes.c_short),
        ("sThumbRY", ctypes.c_short),
    ]

class XINPUT_CAPABILITIES(ctypes.Structure):
    _fields_ = [
        ("Type", wintypes.BYTE),
        ("SubType", wintypes.BYTE),
        ("Flags", wintypes.WORD),
        ("Gamepad", XINPUT_GAMEPAD),
        ("Vibration", wintypes.WORD * 2),  # placeholder for XINPUT_VIBRATION
    ]

# Function prototype
XInputGetCapabilities = xinput.XInputGetCapabilities
XInputGetCapabilities.argtypes = (wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(XINPUT_CAPABILITIES))
XInputGetCapabilities.restype = wintypes.DWORD

# Known subtypes (common ones)
SUBTYPE_NAMES = {
    0x00: "Unknown",
    0x01: "Gamepad",
    0x02: "Wheel",
    0x03: "ArcadeStick",
    0x04: "FlightStick",
    0x05: "DancePad",
    0x06: "Guitar",
    0x07: "GuitarAlternate",
    0x08: "Drums",
    0x09: "GuitarBass",
    0x0A: "ArcadePad",
}

def get_controller_subtype(user_index=0):
    caps = XINPUT_CAPABILITIES()
    res = XInputGetCapabilities(user_index, XINPUT_DEVTYPE_GAMEPAD, ctypes.byref(caps))
    if res != 0:
        return None  # controller not connected or error
    return caps.SubType

if __name__ == "__main__":
    for i in range(4):
        subtype = get_controller_subtype(i)
        if subtype is None:
            print(f"Controller {i}: not connected")
        else:
            name = SUBTYPE_NAMES.get(subtype, f"Unknown (0x{subtype:02X})")
            print(f"Controller {i}: subtype=0x{subtype:02X} -> {name}")
