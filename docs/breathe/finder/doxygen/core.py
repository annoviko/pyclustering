
from . import index as indexfinder
from . import compound as compoundfinder


class CreateCompoundTypeSubFinder(object):

    def __init__(self, parser_factory, matcher_factory):

        self.parser_factory = parser_factory
        self.matcher_factory = matcher_factory

    def __call__(self, project_info, *args):

        compound_parser = self.parser_factory.create_compound_parser(project_info)
        return indexfinder.CompoundTypeSubItemFinder(self.matcher_factory, compound_parser,
                                                     project_info, *args)


class DoxygenItemFinderFactory(object):

    def __init__(self, finders, project_info):

        self.finders = finders
        self.project_info = project_info

    def create_finder(self, data_object):

        return self.finders[data_object.node_type](self.project_info, data_object, self)


class DoxygenItemFinderFactoryCreator(object):

    def __init__(self, parser_factory, filter_factory):

        self.parser_factory = parser_factory
        self.filter_factory = filter_factory

    def create_factory(self, project_info):

        finders = {
            "doxygen": indexfinder.DoxygenTypeSubItemFinder,
            "compound": CreateCompoundTypeSubFinder(self.parser_factory, self.filter_factory),
            "member": indexfinder.MemberTypeSubItemFinder,
            "doxygendef": compoundfinder.DoxygenTypeSubItemFinder,
            "compounddef": compoundfinder.CompoundDefTypeSubItemFinder,
            "sectiondef": compoundfinder.SectionDefTypeSubItemFinder,
            "memberdef": compoundfinder.MemberDefTypeSubItemFinder,
            "ref": compoundfinder.RefTypeSubItemFinder,
            }

        return DoxygenItemFinderFactory(finders, project_info)



