
class FakeParentNode(object):

    node_type = "fakeparent"


class Finder(object):

    def __init__(self, root, item_finder_factory):

        self._root = root
        self.item_finder_factory = item_finder_factory

    def filter_(self, filter_, matches):
        """Adds all nodes which match the filter into the matches list"""

        item_finder = self.item_finder_factory.create_finder(self._root)
        item_finder.filter_([FakeParentNode()], filter_, matches)

    def root(self):

        return self._root


class FinderFactory(object):

    def __init__(self, parser, item_finder_factory_creator):

        self.parser = parser
        self.item_finder_factory_creator = item_finder_factory_creator

    def create_finder(self, project_info):

        root = self.parser.parse(project_info)
        item_finder_factory = self.item_finder_factory_creator.create_factory(project_info)

        return Finder(root, item_finder_factory)

    def create_finder_from_root(self, root, project_info):

        item_finder_factory = self.item_finder_factory_creator.create_factory(project_info)

        return Finder(root, item_finder_factory)


