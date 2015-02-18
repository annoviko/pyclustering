
from .base import ItemFinder, stack


class DoxygenTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):

        compounds = self.data_object.get_compound()

        results = []

        for compound in compounds:

            if matcher_stack.match("compound", compound):
                compound_finder = self.item_finder_factory.create_finder(compound)
                results.extend(compound_finder.find(matcher_stack))

        return results

    def filter_(self, ancestors, filter_, matches):
        """Find nodes which match the filter. Doesn't test this node, only its children"""

        compounds = self.data_object.get_compound()

        node_stack = stack(self.data_object, ancestors)

        for compound in compounds:

            compound_finder = self.item_finder_factory.create_finder(compound)
            compound_finder.filter_(node_stack, filter_, matches)


class CompoundTypeSubItemFinder(ItemFinder):

    def __init__(self, filter_factory, compound_parser, *args):
        ItemFinder.__init__(self, *args)

        self.filter_factory = filter_factory
        self.compound_parser = compound_parser

    def find(self, matcher_stack):

        members = self.data_object.get_member()

        member_results = []

        for member in members:
            if matcher_stack.match("member", member):
                member_finder = self.item_finder_factory.create_finder(member)
                member_results.extend(member_finder.find(matcher_stack))

        results = []

        # If there are members in this compound that match the criteria
        # then load up the file for this compound and get the member data objects
        if member_results:

            file_data = self.compound_parser.parse(self.data_object.refid)
            finder = self.item_finder_factory.create_finder(file_data)

            for member_data in member_results:
                results.extend(finder.find(matcher_stack))

        elif matcher_stack.full_match("compound", self.data_object):
            results.append(self.data_object)

        return results

    def filter_(self, ancestors, filter_, matches):
        """Finds nodes which match the filter and continues checks to children

        Requires parsing the xml files referenced by the children for which we use the compound
        parser and continue at the top level of that pretending that this node is the parent of the
        top level node of the compound file.
        """

        node_stack = stack(self.data_object, ancestors)

        # Match against compound object
        if filter_.allow(node_stack):
            matches.append(self.data_object)

        # Descend to member children
        members = self.data_object.get_member()
        member_matches = []
        for member in members:
            member_finder = self.item_finder_factory.create_finder(member)
            member_finder.filter_(node_stack, filter_, member_matches)

        results = []

        # If there are members in this compound that match the criteria
        # then load up the file for this compound and get the member data objects
        if member_matches:

            file_data = self.compound_parser.parse(self.data_object.refid)
            finder = self.item_finder_factory.create_finder(file_data)

            for member_data in member_matches:
                ref_filter = self.filter_factory.create_id_filter('memberdef', member_data.refid)
                finder.filter_(node_stack, ref_filter, matches)

        else:

            # Read in the xml file referenced by the compound and descend into that as well
            file_data = self.compound_parser.parse(self.data_object.refid)
            finder = self.item_finder_factory.create_finder(file_data)

            finder.filter_(node_stack, filter_, matches)


class MemberTypeSubItemFinder(ItemFinder):

    def find(self, matcher_stack):

        if matcher_stack.full_match("member", self.data_object):
            return [self.data_object]
        else:
            return []

    def filter_(self, ancestors, filter_, matches):

        node_stack = stack(self.data_object, ancestors)

        # Match against member object
        if filter_.allow(node_stack):
            matches.append(self.data_object)


