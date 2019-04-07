
import logging


def list_sorting(nodes, direction, data):
    """Sort nodes by using an explicit list."""

    reverse = direction == 'desc'
    sorted_nodes = []
    unsorted_nodes = nodes[:]
    path_list = data

    # get the nodes sorted in the same order of the list
    for path in path_list:
        for index, node in enumerate(unsorted_nodes):
            if str(node) == path:
                sorted_nodes.append(unsorted_nodes.pop(index))
                break
        else:
            logging.warning(f"Can't find {path} among the files to sort.")

    # check if there was a 1:1 relationship between list and nodes
    for node in unsorted_nodes:
        logging.warning(f"Not sorting {node.path}. File not in sorting list.")

    # reverse if necessary
    if reverse:
        sorted_nodes.reverse()

    return sorted_nodes

