import shutil

def copy(root_src_path, src_path, root_dst_path, dst_path):
    """Copy file without transformation"""
    shutil.copy(src_path.absolute(), dst_path.absolute())

