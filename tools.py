import ctypes
import os
from ctypes import wintypes, Structure


class GUID(Structure):
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


class ToGUID(Structure):
    _fields_ = [
        ('Data1', wintypes.DWORD),
        ('Data2', wintypes.WORD),
        ('Data3', wintypes.WORD),
        ('Data4', wintypes.BYTE * 8)
    ]

    def __init__(self, info):
        """Convert to a new GUID."""
        data4 = []
        pure = info.strip('{}').split('-')
        self.Data1 = int(pure[0], 16)
        self.Data2 = int(pure[1], 16)
        self.Data3 = int(pure[2], 16)
        data4.append(int(pure[3][0:2], 16))
        data4.append(int(pure[3][2:4], 16))
        temp1 = pure[4]
        res = [int(temp1[i:i + 2], 16) for i in range(0, len(temp1), 2)]
        data4.extend(res)
        self.Data4[:] = data4

    def __repr__(self):
        b1, b2, b3, b4, b5, b6, b7, b8 = self.Data4
        x = None
        # x = 'GUID(%x-%x-%x-%x%x%x%x%x%x%x%x)' % (
        #          self.Data1, self.Data2, self.Data3, b1, b2, b3, b4, b5, b6, b7, b8)
        return f'{x}+GUID({self.Data1}-{self.Data2}-{self.Data3}-{b1}{b2}{b3}{b4}{b5}{b6}{b7}{b8})'


class Folders(object):
    def __init__(self, name=None, path=None, files_count=None, folders_count=None, size=None, software=None, alias=None,
                 subfolders=None) -> None:
        self.name = name
        self.path = path
        self.files_count = files_count
        self.folders_count = folders_count
        self.size = size
        self.software = software
        self.alias = alias
        self.subfolders = subfolders

    def get_folder_size():
        pass

    def get_files_count():
        pass

    def set_some_folder(self, path_type_id):
        alias = ""
        match path_type_id:
            case 0:
                alias = "Desktop"
            case 5:
                alias = "Documents"
            case 6:
                alias = "Favorites"
            case 13:
                alias = "Music"
            case 14:
                alias = "Videos"
            case 19:
                alias = "Network Shortcuts"
            case 20:
                alias = "Fonts"
            case _:
                return None
        self.path = get_doc_path(path_type_id)
        self.alias = alias
        return True

    def get_known_folder(self, info_dict):
        for key in info_dict:
            self.path = SHGetKnownFolderPath(info_dict[key])
            self.alias = key


class Scan():
    def __init__(self) -> None:
        self.d = []
        self.s = 0
        self.files_count = 0

    def scan(self, dir, alias=None):
        for i in os.scandir(dir):
            if alias == 'Documents' and (i.name in ("My Music", "My Pictures", "My Videos")):
                continue
            if i.is_dir():
                self.scan(i)
            else:
                self.d.append(i.path)
                self.s += i.stat().st_size
                if i.is_file():
                    self.files_count += 1


def get_doc_path(CSIDL_PERSONAL):
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, 0, buf)
    return buf.value


def SHGetKnownFolderPath(info):
    info = ToGUID(info)
    ptr = ctypes.c_wchar_p()
    ctypes.windll.shell32.SHGetKnownFolderPath(info, 0, None, ctypes.byref(ptr))
    return ptr.value

