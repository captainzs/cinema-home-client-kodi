import glob
import os
import shutil

EXCLUDES_FROM_COPY = [".pyc", "tests\\", "mock.xbmc", "tox"]


def is_valid_addon(dir_abs_path):
    if os.path.exists(os.path.join(dir_abs_path, "addon.xml")):
        return True
    return False


def is_valid_file(file_abs_path):
    for EXCLUDE in EXCLUDES_FROM_COPY:
        if EXCLUDE in file_abs_path:
            return False
    return True


def copy_addon(src_abs_path, dst_abs_path):
    for (root, dirs, files) in os.walk(src_abs_path):
        relative_subdir = os.path.relpath(root, src_abs_path)
        for file in files:
            src_file_abs_path = os.path.join(src_abs_path, relative_subdir, file)
            if is_valid_file(src_file_abs_path):
                dst_file_abs_path = os.path.join(dst_abs_path, relative_subdir, file)
                if not os.path.exists(os.path.dirname(dst_file_abs_path)):
                    os.makedirs(os.path.dirname(dst_file_abs_path))
                shutil.copy(src_file_abs_path, dst_file_abs_path)
    return


def reinstall_addons(src_rel_path, dst_abs_path):
    sub_dirs = glob.glob(os.path.join(src_rel_path, "*/"))
    addons_metadata = []
    for addon_src_rel_path in sub_dirs:
        addon_src_abs_path = os.path.abspath(addon_src_rel_path)
        addon_src_dir = os.path.basename(os.path.dirname(addon_src_rel_path))
        addon_dst_abs_path = os.path.abspath(os.path.join(dst_abs_path, addon_src_dir))
        if is_valid_addon(addon_src_abs_path):
            if os.path.exists(addon_dst_abs_path):
                shutil.rmtree(addon_dst_abs_path)
            os.mkdir(addon_dst_abs_path)
            copy_addon(addon_src_abs_path, addon_dst_abs_path)
            print("Deploy Success: {}".format(addon_dst_abs_path))
    return addons_metadata


if __name__ == "__main__":
    destination = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Kodi", "addons")
    reinstall_addons("./", destination)
