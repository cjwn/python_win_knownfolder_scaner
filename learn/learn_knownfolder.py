import ctypes.wintypes
import ctypes as C
import uuid
import winreg
from uuid import UUID

a = uuid.uuid4()
print(a)

FOLDERID_Downloads = '374DE290-123F-4565-9164-39C4925E467B'
UUID_F_Downloads = UUID(FOLDERID_Downloads)


class LP_GUID(object):
    def __init__(self) -> None:
        value = '{374DE290-123F-4565-9164-39C4925E467B}'


a = LP_GUID()
buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
print(buf, type(buf))
print(type(a))
print(isinstance(a, LP_GUID))


def SHGetFolderPathW():
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 2, None, '{374DE290-123F-4565-9164-39C4925E467B}', buf)
    return buf.value


import ctypes
from ctypes import windll, wintypes

class GUID(ctypes.Structure):
    _fields_ = [
         ('Data1', wintypes.DWORD),
         ('Data2', wintypes.WORD),
         ('Data3', wintypes.WORD),
         ('Data4', wintypes.BYTE * 8)
    ]

    def __init__(self, l, w1, w2, b1, b2, b3, b4, b5, b6, b7, b8):
        """Create a new GUID."""
        self.Data1 = l
        self.Data2 = w1
        self.Data3 = w2
        self.Data4[:] = (b1, b2, b3, b4, b5, b6, b7, b8)

    def __repr__(self):
        b1, b2, b3, b4, b5, b6, b7, b8 = self.Data4
        return 'GUID(%x-%x-%x-%x%x%x%x%x%x%x%x)' % (
                   self.Data1, self.Data2, self.Data3, b1, b2, b3, b4, b5, b6, b7, b8)

# constants to be used according to the version on shell32
CSIDL_PROFILE = 40
FOLDERID_Profile = GUID(0x374DE290, 0x123F, 0x4565, 0x9164, 0xFE, 0xEA, 0x33, 0x17, 0xB6, 0x71, 0x73)

def SHGetKnownFolderPath():
    ptr = ctypes.c_wchar_p()
    ctypes.windll.shell32.SHGetKnownFolderPath(FOLDERID_Profile, 0, None, ctypes.byref(ptr))
    return ptr.value


def showpath():
    info = UUID('{374DE290-123F-4565-9164-39C4925E467B}')
    print(f'GetKnownFolder: {SHGetKnownFolderPath()}')
    print(f'GetFolderPathW: {SHGetFolderPathW()}')
    # for i in range(60):
    #     print(f'getKnownFolder: {SHGetKnownFolderPath(i)}')


showpath()


def get_download_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    print(key)
    return winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]


