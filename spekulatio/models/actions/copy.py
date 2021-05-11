
import shutil

extension_change = None

def extract(node):
    return {}

def build(src_path, dst_path, node, **kwargs):
    """Copy file without transformation"""
    shutil.copy(src_path, dst_path)

