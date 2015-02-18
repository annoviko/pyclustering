
from ..renderer.rst.doxygen.base import RenderContext
from ..renderer.rst.doxygen import format_parser_error
from ..renderer.rst.doxygen.mask import NullMaskFactory
from ..parser import ParserError, FileIOError
from ..project import ProjectError
from ..finder.core import NoMatchesError

from docutils.parsers import rst
from docutils.parsers.rst.directives import unchanged_required, flag
from docutils import nodes

class WarningHandler(object):

    def __init__(self, state, context):
        self.state = state
        self.context = context

    def warn(self, raw_text, rendered_nodes=None):
        raw_text = self.format(raw_text)
        if rendered_nodes is None:
            rendered_nodes = [nodes.paragraph("", "", nodes.Text(raw_text))]
        return [
            nodes.warning("", *rendered_nodes),
            self.state.document.reporter.warning(raw_text, line=self.context['lineno'])
            ]

    def format(self, text):
        return text.format(**self.context)


def create_warning(project_info, state, lineno, **kwargs):

    tail = ''
    if project_info:
        tail = 'in doxygen xml output for project "{project}" from directory: {path}'.format(
            project=project_info.name(),
            path=project_info.project_path()
            )

    context = dict(
        lineno=lineno,
        tail=tail,
        **kwargs
        )

    return WarningHandler(state, context)


class BaseDirective(rst.Directive):

    def __init__(self, root_data_object, renderer_factory_creator_constructor, finder_factory,
                 matcher_factory, project_info_factory, filter_factory, target_handler_factory,
                 *args):
        rst.Directive.__init__(self, *args)

        self.root_data_object = root_data_object
        self.renderer_factory_creator_constructor = renderer_factory_creator_constructor
        self.finder_factory = finder_factory
        self.matcher_factory = matcher_factory
        self.project_info_factory = project_info_factory
        self.filter_factory = filter_factory
        self.target_handler_factory = target_handler_factory

    def render(self, data_object, project_info, options, filter_, target_handler, mask_factory):
        "Standard render process used by subclasses"

        renderer_factory_creator = self.renderer_factory_creator_constructor.create_factory_creator(
            project_info,
            self.state.document,
            options,
            target_handler
            )

        try:
            renderer_factory = renderer_factory_creator.create_factory(
                data_object,
                self.state,
                self.state.document,
                filter_,
                target_handler,
                )
        except ParserError as e:
            return format_parser_error("doxygenclass", e.error, e.filename, self.state,
                                       self.lineno, True)
        except FileIOError as e:
            return format_parser_error("doxygenclass", e.error, e.filename, self.state, self.lineno)

        context = RenderContext([data_object, self.root_data_object], mask_factory)
        object_renderer = renderer_factory.create_renderer(context)
        node_list = object_renderer.render()

        return node_list


class DoxygenBaseDirective(BaseDirective):

    required_arguments = 1
    optional_arguments = 1
    option_spec = {
        "path": unchanged_required,
        "project": unchanged_required,
        "outline": flag,
        "no-link": flag,
        }
    has_content = False

    def run(self):

        try:
            namespace, name = self.arguments[0].rsplit("::", 1)
        except ValueError:
            namespace, name = "", self.arguments[0]

        try:
            project_info = self.project_info_factory.create_project_info(self.options)
        except ProjectError as e:
            warning = create_warning(None, self.state, self.lineno)
            return warning.warn('doxygen%s: %s' % (self.kind, e))

        finder = self.finder_factory.create_finder(project_info)

        matcher_stack = self.create_matcher_stack(namespace, name)

        try:
            data_object = finder.find_one(matcher_stack)
        except NoMatchesError as e:
            display_name = "%s::%s" % (namespace, name) if namespace else name
            warning = create_warning(project_info, self.state, self.lineno, name=display_name,
                                     kind=self.kind)
            return warning.warn('doxygen{kind}: Cannot find {kind} "{name}" {tail}')

        target_handler = self.target_handler_factory.create_target_handler(
            self.options, project_info, self.state.document)
        filter_ = self.filter_factory.create_outline_filter(self.options)

        mask_factory = NullMaskFactory()
        return self.render(data_object, project_info, self.options, filter_, target_handler,
                           mask_factory)

