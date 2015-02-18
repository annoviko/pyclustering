
class ItemFinder(object):

    def __init__(self, project_info, data_object, item_finder_factory):

        self.data_object = data_object
        self.item_finder_factory = item_finder_factory
        self.project_info = project_info


def stack(element, list_):
    """Stack an element on to the start of a list and return as a new list"""

    # Copy list first so we have a new list to insert into
    output = list_[:]
    output.insert(0, element)
    return output

