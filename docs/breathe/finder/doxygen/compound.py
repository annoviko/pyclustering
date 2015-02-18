
from .base import ItemFinder, stack


class DoxygenTypeSubItemFinder(ItemFinder):

    def filter_(self, ancestors, filter_, matches):
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = stack(self.data_object, ancestors)

        compound_finder = self.item_finder_factory.create_finder(self.data_object.compounddef)
        compound_finder.filter_(node_stack, filter_, matches)


class CompoundDefTypeSubItemFinder(ItemFinder):

    def filter_(self, ancestors, filter_, matches):
        """Finds nodes which match the filter and continues checks to children"""

        node_stack = stack(self.data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(node_stack)

        for sectiondef in self.data_object.sectiondef:
            finder = self.item_finder_factory.create_finder(sectiondef)
            finder.filter_(node_stack, filter_, matches)

        for innerclass in self.data_object.innerclass:
            finder = self.item_finder_factory.create_finder(innerclass)
            finder.filter_(node_stack, filter_, matches)


class SectionDefTypeSubItemFinder(ItemFinder):

    def filter_(self, ancestors, filter_, matches):
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = stack(self.data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(node_stack)

        for memberdef in self.data_object.memberdef:
            finder = self.item_finder_factory.create_finder(memberdef)
            finder.filter_(node_stack, filter_, matches)


class MemberDefTypeSubItemFinder(ItemFinder):

    def filter_(self, ancestors, filter_, matches):

        data_object = self.data_object
        node_stack = stack(data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(node_stack)

        if data_object.kind == 'enum':
            for value in data_object.enumvalue:
                value_stack = stack(value, node_stack)
                if filter_.allow(value_stack):
                    matches.append(value_stack)


class RefTypeSubItemFinder(ItemFinder):

    def filter_(self, ancestors, filter_, matches):

        node_stack = stack(self.data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(node_stack)

