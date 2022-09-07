import ctypes
from uuid import UUID
from ctypes import wintypes, Structure, windll

# print(0x374DE290)
# bx = '0x'+PURE[0]
# by = bytes(bx, 'UTF-8')
# print(by)


from tools import GUID, ToGUID

# from learn_knownfolder import GUID


int_ = int
DOWNLOADS_GUID_str = '{374DE290-123F-4565-9164-39C4925E467B}'
PURE = DOWNLOADS_GUID_str.strip('{}').split('-')
a = ToGUID(DOWNLOADS_GUID_str)
print(0, a)


CSIDL_PROFILE = 40
FOLDERID_Profile = GUID(0x5E6C858F, 0x0E22, 0x4760, 0x9A, 0xFE, 0xEA, 0x33, 0x17, 0xB6, 0x71, 0x73)
print(1, FOLDERID_Profile)
cloned_FOLDERID_Profile = GUID(0x374DE290, 0x123F, 0x4565, 0x91, 0x64, 0x39, 0xC4, 0x92, 0x5E, 0x46, 0x7B)
print(2, cloned_FOLDERID_Profile)
# temp4 = '9A'
# print(f'temp4:{wintypes.BYTE(int(temp4, 16))}')
# temp2 = wintypes.BYTE(0x9A)
# print(f'9A:{temp2}')


def expand_user():
    # get the function that we can find from Vista up, not the one in XP
    get_folder_path = getattr(windll.shell32, 'SHGetKnownFolderPath', None)
    if get_folder_path is not None:
        # ok, we can use the new function which is recommended by the msdn
        ptr = ctypes.c_wchar_p()
        get_folder_path(ctypes.byref(a), 0, 0, ctypes.byref(ptr))
        return ptr.value
    else:
        # use the deprecated one found in XP and on for compatibility reasons
       get_folder_path = getattr(windll.shell32, 'SHGetSpecialFolderPathW', None)
       buf = ctypes.create_unicode_buffer(300)
       get_folder_path(None, buf, CSIDL_PROFILE, False)
       return buf.value


print(expand_user())

# print(getattr(a, 'bytes'))
# print(getattr(a, 'bytes_le'))
# print(getattr(a, 'fields'))
# print("time_low", wintypes.DWORD(getattr(a, 'time_low')))
# print("time_mid", wintypes.WORD(getattr(a, 'time_mid')))
# print("time_hi_version", wintypes.WORD(getattr(a, 'time_hi_version')))
# print("clock_seq_hi_variant", wintypes.BYTE(getattr(a, 'clock_seq_hi_variant')))
# print(getattr(a, 'clock_seq_low'))
# print(getattr(a, 'node'))
# print(getattr(a, 'int'))
# hex_int = DOWNLOADS_GUID_str.strip('{}').replace('-', '')
# hex_int = int_(hex_int, 32)
# print(hex_int)