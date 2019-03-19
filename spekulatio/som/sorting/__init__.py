
from .none_sorting import none_sorting
from .name_sorting import name_sorting
from .field_sorting import field_sorting
from .list_sorting import list_sorting

sorting_methods = {
    'none': none_sorting,
    'name': name_sorting,
    'field': field_sorting,
    'list': list_sorting,
}

