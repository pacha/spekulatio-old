import shutil

from spekulatio.exceptions import SpekulatioSkipExtraction

extension_change = None


def extract_values(node, site):
    return {}

def extract_content(node, site):
    return {}

def build(src_path, dst_path, node, site):
    """Copy file without transformation"""
    shutil.copy(src_path, dst_path)
