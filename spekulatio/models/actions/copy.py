
import shutil

from spekulatio.exceptions import SpekulatioSkipExtraction

extension_change = None

def extract(node):
    raise SpekulatioSkipExtraction()

def build(src_path, dst_path, node, **kwargs):
    """Copy file without transformation"""
    shutil.copy(src_path, dst_path)

