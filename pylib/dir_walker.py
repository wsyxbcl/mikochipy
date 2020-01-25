import os
import re
from pathlib import Path

def walker(rootdir, pattern = re.compile('.*?')):
    ls_filename = []
    ls_subdirs = []
    for subdirs, dirs, files in os.walk(rootdir):
        for file in files:
            if pattern.match(file):
                ls_filename.append(file)
                ls_subdirs.append(subdirs)
    return zip(ls_filename, ls_subdirs)

if __name__ == '__main__':
    # rootdir = os.getcwd()
    rootdir = Path('')
    file_list = []
    count = 0
    for filename, subdir in walker(rootdir):
        file_list.append(Path(subdir).joinpath(Path(filename)))
        # print(subdir)
        count += 1
    for f in file_list:
        print(f)
    print('%d files in total'%count)