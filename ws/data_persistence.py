# https://github.com/usc-isi-i2/dig-etl-engine/issues/92

import json
import threading
import os
import codecs


# 1.acquire file write lock
# 2.write to file.new
# 3.acquire replace lock
# 4.rename file to file.old
# 5.rename file.new to file
# 6.release replace lock and write lock
# 7.remove file.old
def dump_data(data, file_path, write_lock, replace_lock):
    new_path = file_path + '.new'
    old_path = file_path + '.old'

    try:
        write_lock.acquire()
        with codecs.open(new_path, 'w') as f:
            f.write(data)

        replace_lock.acquire()
        # https://docs.python.org/2/library/os.html#os.rename
        # On Unix, if dst exists and is a file,
        # it will be replaced silently if the user has permission.
        os.rename(file_path, old_path)
        os.rename(new_path, file_path)
        os.remove(old_path)
    except Exception as e:
        print e
    finally:
        write_lock.release()
        replace_lock.release()


# when starting:
# if only file exists, correct.
# if both file.new and file.old exist, ignore file.old and rename file.new to file (shut down in the middle of replacing, file.new is complete)
# if both file.new and file exist, ignore file.new (shut down in the middle of generating file.new).
# if only file.new exists, error (user deletion)
# if only file.old exists, error (user deletion)
# if three of them exists, error (user operation, system error
def prepare_data_file(file_path):
    new_path = file_path + '.new'
    old_path = file_path + '.old'
    has_file = os.path.exists(file_path)
    has_new = os.path.exists(new_path)
    has_old = os.path.exists(old_path)

    if has_file and not has_new and not has_old:
        pass
    elif not has_file and has_old and has_new:
        os.remove(old_path)
        os.rename(new_path, file_path)
    elif has_file and not has_old and has_new:
        os.remove(new_path)
    else:
        pass

