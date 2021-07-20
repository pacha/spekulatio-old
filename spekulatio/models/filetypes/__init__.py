from .filetype_map import FiletypeMap
from .filetype_presets import filetype_presets

# create a default filetype map (used mostly for testing)
default_filetype_map = FiletypeMap()
default_filetype_map.update(filetype_presets)
