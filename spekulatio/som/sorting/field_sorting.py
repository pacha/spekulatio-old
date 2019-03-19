
import logging


def field_sorting(nodes, direction, data):
    """Sort nodes according to one of their data fields."""
    reverse = direction == 'desc'
    field = data

    # classify nodes according if they have the required field or not
    nodes_without_field = []
    nodes_with_field = []
    for node in nodes:
        if field in node.data:
            nodes_with_field.append(node)
        else:
            nodes_without_field.append(node)
            logging.warning(f"Can't sort {node} because it doesn't have a field '{field}'")

    # get sorted nodes
    try:
        sorted_nodes = sorted(nodes_with_field, reverse=reverse, key=lambda n: n.data[field])
    except Exception as err:
        logging.warning(f"Can't sort pages by field {field}: {err}")
        sorted_nodes = nodes_with_field

    # return sorted nodes first, unsorted last
    return sorted_nodes + nodes_without_field

