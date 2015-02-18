
from .base import ItemFinder, stack


class DoxygenTypeSubItemFinder(ItemFinder):

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

    def filter_(self, ancestors, filter_, matches):
        """Finds nodes which match the filter and continues checks to children

        Requires parsing the xml files referenced by the children for which we use the compound
        parser and continue at the top level of that pretending that this node is the parent of the
        top level node of the compound file.
        """

        node_stack = stack(self.data_object, ancestors)

        # Match against compound object
        if filter_.allow(node_stack):
            matches.append(node_stack)

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

            for member_stack in member_matches:
                ref_filter = self.filter_factory.create_id_filter('memberdef', member_stack[0].refid)
                finder.filter_(node_stack, ref_filter, matches)

        else:

            # Read in the xml file referenced by the compound and descend into that as well
            file_data = self.compound_parser.parse(self.data_object.refid)
            finder = self.item_finder_factory.create_finder(file_data)

            finder.filter_(node_stack, filter_, matches)


class MemberTypeSubItemFinder(ItemFinder):

    def filter_(self, ancestors, filter_, matches):

        node_stack = stack(self.data_object, ancestors)

        # Match against member object
        if filter_.allow(node_stack):
            matches.append(node_stack)
