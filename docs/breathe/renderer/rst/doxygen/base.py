
class Renderer(object):

    def __init__(self,
            project_info,
            context,
            renderer_factory,
            node_factory,
            state,
            document,
            domain_handler,
            target_handler,
            domain_directive_factory,
            ):

        self.project_info = project_info
        self.context = context
        self.data_object = context.node_stack[0]
        self.renderer_factory = renderer_factory
        self.node_factory = node_factory
        self.state = state
        self.document = document
        self.domain_handler = domain_handler
        self.target_handler = target_handler
        self.domain_directive_factory = domain_directive_factory

        if self.context.domain == '':
            self.context.domain = self.get_domain()

    def get_domain(self):
        """Returns the domain for the current node."""

        def get_filename(node):
            """Returns the name of a file where the declaration represented by node is located."""
            try:
                return node.location.file
            except AttributeError:
                return None

        node_stack = self.context.node_stack
        node = node_stack[0]
        # An enumvalue node doesn't have location, so use its parent node for detecting the domain instead.
        if type(node) == unicode or node.node_type == "enumvalue":
            node = node_stack[1]
        filename = get_filename(node)
        if not filename and node.node_type == "compound":
            file_data = self.compound_parser.parse(node.refid)
            filename = get_filename(file_data.compounddef)
        return self.project_info.domain_for_file(filename) if filename else ''

    def create_template_node(self, decl):
        """Creates a node for the ``template <...>`` part of the declaration."""
        if not decl.templateparamlist:
            return None
        context = self.context.create_child_context(decl.templateparamlist)
        renderer = self.renderer_factory.create_renderer(context)
        nodes = [self.node_factory.Text("template <")]
        nodes.extend(renderer.render())
        nodes.append(self.node_factory.Text(">"))
        signode = self.node_factory.desc_signature()
        signode.extend(nodes)
        return signode


class RenderContext(object):

    def __init__(self, node_stack, mask_factory, directive_args, domain=''):
        self.node_stack = node_stack
        self.mask_factory = mask_factory
        self.directive_args = directive_args
        self.domain = domain

    def create_child_context(self, data_object):

        node_stack = self.node_stack[:]
        node_stack.insert(0, self.mask_factory.mask(data_object))
        return RenderContext(node_stack, self.mask_factory, self.directive_args, self.domain)
