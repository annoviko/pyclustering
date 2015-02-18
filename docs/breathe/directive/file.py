
from ..renderer.rst.doxygen.base import RenderContext
from ..renderer.rst.doxygen.mask import NullMaskFactory
from ..directive.base import BaseDirective
from ..project import ProjectError
from .base import WarningHandler, create_warning

from docutils.parsers.rst.directives import unchanged_required, flag
from docutils import nodes


class BaseFileDirective(BaseDirective):
    """Base class handle the main work when given the appropriate file and project info to work
    from.
    """

    # We use inheritance here rather than a separate object and composition, because so much
    # information is present in the Directive class from the docutils framework that we'd have to
    # pass way too much stuff to a helper object to be reasonable.

    def handle_contents(self, file_, project_info):

        finder = self.finder_factory.create_finder(project_info)

        finder_filter = self.filter_factory.create_file_finder_filter(file_)

        matches = []
        finder.filter_(finder_filter, matches)

        if len(matches) > 1:
            warning = create_warning(None, self.state, self.lineno, file=file_,
                                     directivename=self.directive_name)
            return warning.warn('{directivename}: Found multiple matches for file "{file} {tail}')

        elif not matches:
            warning = create_warning(None, self.state, self.lineno, file=file_,
                                     directivename=self.directive_name)
            return warning.warn('{directivename}: Cannot find file "{file} {tail}')

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_file_filter(file_, self.options)

        renderer_factory_creator = self.renderer_factory_creator_constructor.create_factory_creator(
            project_info,
            self.state.document,
            self.options,
            target_handler
            )
        node_list = []
        for data_object in matches:

            renderer_factory = renderer_factory_creator.create_factory(
                data_object,
                self.state,
                self.state.document,
                filter_,
                target_handler,
                )

            mask_factory = NullMaskFactory()
            context = RenderContext([data_object, self.root_data_object], mask_factory)
            object_renderer = renderer_factory.create_renderer(context)
            node_list.extend(object_renderer.render())

        return node_list


class DoxygenFileDirective(BaseFileDirective):

    directive_name = 'doxygenfile'

    required_arguments = 0
    optional_arguments = 2
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        }
    has_content = False

    def run(self):
        """Get the file from the argument and the project info from the factory."""

        file_ = self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygenfile: %s' % e)

        return self.handle_contents(file_, project_info)


class AutoDoxygenFileDirective(BaseFileDirective):

    directive_name = 'autodoxygenfile'

    required_arguments = 1
    option_spec = {
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        }
    has_content = False

    def run(self):
        """Get the file from the argument and extract the associated project info for the named
        project given that it is an auto-project.
        """

        file_ = self.arguments[0]

        try:
            project_info = self.project_info_factory.retrieve_project_info_for_auto(self.options)
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('autodoxygenfile: %s' % e)

        return self.handle_contents(file_, project_info)

