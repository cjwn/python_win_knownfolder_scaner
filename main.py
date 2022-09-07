import os
import json

from pathlib import Path
import ctypes.wintypes

from specs import KNOWNFOLDERID_LIST
from tools import Folders, Scan



# def SHGetKnownFolderPath(fid):
#     buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
#     ctypes.windll.shell32.SHGetKnownFolderPath(fid, 0, None, buf)
#     return buf.value


class MyFolders(object):

    def __init__(self) -> None:
        self.user_root = ''
        self.pictures = ""
        self.videos = ""
        self.documents = ''
        self.downloads = ''
        self.music = ''
        self.desktop = ''

    def get_my_foders():
        pass

    def get_user_root(self):
        home = str(Path.home())
        self.user_root = home


def get_doc_path(CSIDL_PERSONAL):
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, 0, buf)
    return buf.value


# def scanfolder(dir, alias=None):
#     folders = []
#     for i in os.scandir(dir):
#         if alias == 'Documents' and (i.name in("My Music","My Pictures", "My Videos")) :
#             continue
#         if i.is_dir():
#             # if alias == 'Documents':
#             #     print(i)
#             scanfolder(i)
#             folders.append(i.path)
#         else:
#             folders.append(i.path)


#     return folders




def test():
    cwd = os.getcwd()
    for i in os.scandir(cwd):
        print(i.path, i.stat().st_size / 1024 / 1024)
        break


def make_json():
    path_list = []
    total_size = 0
    total_files_count = 0
    a = Folders()
    for i in range(60):
         # 获取个人文件夹的地址及别名
        if not a.set_some_folder(i):
            continue
        s = Scan()
        s.scan(a.path, a.alias)
        subfolders_list = s.d
        file_dict = {'path': a.path, "name": a.alias,
                     "subfolders": subfolders_list, "size": s.s}
        path_list.append(file_dict)
        total_size += s.s
        total_files_count += s.files_count
    a.get_known_folder(KNOWNFOLDERID_LIST)
    s = Scan()
    s.scan(a.path, a.alias)
    subfolders_list = s.d
    file_dict = {'path': a.path, "name": a.alias,
                 "subfolders": subfolders_list, "size": s.s}
    path_list.append(file_dict)
    total_size += s.s
    total_files_count += s.files_count
    total_info = {"st_size": total_size, "size": StrOfSize(
        total_size), "files": total_files_count, "path_list": path_list}
    with open('folders.json', 'w', encoding='utf-8') as f:
        json.dump(total_info, f, ensure_ascii=False)
        info = f'{StrOfSize(total_size)}, total {total_files_count} files'
    return info


def StrOfSize(size):
    '''
    递归实现，精确为最大单位值 + 小数点后三位
    '''

    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'K', 'M', 'G', 'T', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level + 1 > len(units):
        level = -1
    return ('{}.{:>03d}{}'.format(integer, remainder, units[level]))


if __name__ == "__main__":
    print(make_json())

    # test()
