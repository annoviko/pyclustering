
from .base import ItemFinder, stack


class DoxygenTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):
        """Search with MatcherStack functionality - deprecated in favour of the filter approach"""

        compound_finder = self.item_finder_factory.create_finder(self.data_object.compounddef)
        return compound_finder.find(matcher_stack)

    def filter_(self, ancestors, filter_, matches):
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = stack(self.data_object, ancestors)

        compound_finder = self.item_finder_factory.create_finder(self.data_object.compounddef)
        compound_finder.filter_(node_stack, filter_, matches)


class CompoundDefTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):
        """Search with MatcherStack functionality - deprecated in favour of the filter approach"""

        results = []
        for sectiondef in self.data_object.sectiondef:
            finder = self.item_finder_factory.create_finder(sectiondef)
            results.extend(finder.find(matcher_stack))

        return results

    def filter_(self, ancestors, filter_, matches):
        """Finds nodes which match the filter and continues checks to children"""

        node_stack = stack(self.data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(self.data_object)

        for sectiondef in self.data_object.sectiondef:
            finder = self.item_finder_factory.create_finder(sectiondef)
            finder.filter_(node_stack, filter_, matches)

        for innerclass in self.data_object.innerclass:
            finder = self.item_finder_factory.create_finder(innerclass)
            finder.filter_(node_stack, filter_, matches)


class SectionDefTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):
        """Search with MatcherStack functionality - deprecated in favour of the filter approach"""

        results = []
        for memberdef in self.data_object.memberdef:
            finder = self.item_finder_factory.create_finder(memberdef)
            results.extend(finder.find(matcher_stack))

        return results

    def filter_(self, ancestors, filter_, matches):
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        node_stack = stack(self.data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(self.data_object)

        for memberdef in self.data_object.memberdef:
            finder = self.item_finder_factory.create_finder(memberdef)
            finder.filter_(node_stack, filter_, matches)


class MemberDefTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):
        """Search with MatcherStack functionality - deprecated in favour of the filter approach"""

        if matcher_stack.match("member", self.data_object):
            return [self.data_object]
        else:
            return []

    def filter_(self, ancestors, filter_, matches):

        node_stack = stack(self.data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(self.data_object)


class RefTypeSubItemFinder(ItemFinder):

    def filter_(self, ancestors, filter_, matches):

        node_stack = stack(self.data_object, ancestors)

        if filter_.allow(node_stack):
            matches.append(self.data_object)

