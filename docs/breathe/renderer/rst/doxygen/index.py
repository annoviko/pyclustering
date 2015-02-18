
from .base import Renderer

class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Process all the compound children
        for compound in self.data_object.get_compound():
            context = self.context.create_child_context(compound)
            compound_renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(compound_renderer.render())

        return nodelist


class CompoundRenderer(Renderer):
    """Base class for CompoundTypeSubRenderer and RefTypeSubRenderer."""

    def __init__(self, compound_parser, render_empty_node, *args):
        self.compound_parser = compound_parser
        self.render_empty_node = render_empty_node
        Renderer.__init__(self, *args)

    def create_doxygen_target(self):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        return self.target_handler.create_target(refid)

    def get_fully_qualified_name(self):

        names = []
        node_stack = self.context.node_stack
        node = node_stack[0]
        if node.node_type == 'enumvalue':
            names.append(node.name)
            # Skip the name of the containing enum because it is not a part of the fully qualified name.
            node_stack = node_stack[2:]

        # If the node is a namespace, use its name because namespaces are skipped in the main loop.
        if node.node_type == 'compound' and node.kind == 'namespace':
            names.append(node.name)

        for node in node_stack:
            if node.node_type == 'ref':
                return node.valueOf_
            if (node.node_type == 'compound' and node.kind not in ['file', 'namespace']) or \
                node.node_type == 'memberdef':
                # We skip the 'file' entries because the file name doesn't form part of the
                # qualified name for the identifier. We skip the 'namespace' entries because if we
                # find an object through the namespace 'compound' entry in the index.xml then we'll
                # also have the 'compounddef' entry in our node stack and we'll get it from that. We
                # need the 'compounddef' entry because if we find the object through the 'file'
                # entry in the index.xml file then we need to get the namespace name from somewhere
                names.insert(0, node.name)
            if (node.node_type == 'compounddef' and node.kind == 'namespace'):
                # Nested namespaces include there parent namespace in there compoundname. ie,
                # compoundname is 'foo::bar' instead of just 'bar' for namespace 'bar' nested in
                # namespace 'foo'. But our node_stack includes 'foo' so we only want 'bar' at
                # this point.
                names.insert(0, node.compoundname.split('::')[-1])

        return '::'.join(names)

    def render_signature(self, file_data, doxygen_target):
        # Defer to domains specific directive.
        name, kind = self.get_node_info(file_data)
        domain_directive = self.renderer_factory.domain_directive_factory.create(
            self.context.domain, [kind] + self.context.directive_args[1:])
        domain_directive.arguments = [self.get_fully_qualified_name()]

        # Translate Breathe's no-link option into the standard noindex option.
        if 'no-link' in self.context.directive_args[2]:
            domain_directive.options['noindex'] = True
        nodes = domain_directive.run()
        node = nodes[1]

        signode, contentnode = node.children
        # The cpp domain in Sphinx doesn't support structs at the moment, so change the text from "class "
        # to the correct kind which can be "class " or "struct ".
        signode[0] = self.node_factory.desc_annotation(kind + ' ', kind + ' ')

        # Filter out outer class names if we are rendering an inner class as a part of its outer class content.
        names = self.context.directive_args[1]
        if len(names) > 0 and names[0] != name:
            signode.children = [n for n in signode.children if not n.tagname == 'desc_addname']

        # Check if there is template information and format it as desired
        template_signode = self.create_template_node(file_data.compounddef)
        if template_signode:
            node.insert(0, template_signode)
        node.children[0].insert(0, doxygen_target)
        return nodes, contentnode

    def render(self, node=None):

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)

        parent_context = self.context.create_child_context(file_data)
        data_renderer = self.renderer_factory.create_renderer(parent_context)
        rendered_data = data_renderer.render()

        if not rendered_data and not self.render_empty_node:
            return []

        file_data = parent_context.node_stack[0]
        new_context = parent_context.create_child_context(file_data.compounddef)

        nodes, contentnode = self.render_signature(file_data, self.create_doxygen_target())

        if file_data.compounddef.includes:
            for include in file_data.compounddef.includes:
                context = new_context.create_child_context(include)
                renderer = self.renderer_factory.create_renderer(context)
                contentnode.extend(renderer.render())

        contentnode.extend(rendered_data)
        return nodes


class CompoundTypeSubRenderer(CompoundRenderer):

    def __init__(self, compound_parser, *args):
        CompoundRenderer.__init__(self, compound_parser, True, *args)

    def get_node_info(self, file_data):
        return self.data_object.name, self.data_object.kind

    def create_domain_target(self):
        """Should be overridden to create a target node which uses the Sphinx domain information so
        that it can be linked to from Sphinx domain roles like cpp:func:`myFunc`

        Returns a list so that if there is no domain active then we simply return an empty list
        instead of some kind of special null node value"""

        return []


class FileRenderer(CompoundTypeSubRenderer):

    def render_signature(self, file_data, doxygen_target):
        # Build targets for linking
        targets = []
        targets.extend(self.create_domain_target())
        targets.extend(doxygen_target)

        title_signode = self.node_factory.desc_signature()
        title_signode.extend(targets)

        # Set up the title
        name, kind = self.get_node_info(file_data)
        title_signode.append(self.node_factory.emphasis(text=kind))
        title_signode.append(self.node_factory.Text(" "))
        title_signode.append(self.node_factory.desc_name(text=name))

        contentnode = self.node_factory.desc_content()

        node = self.node_factory.desc()
        node.document = self.state.document
        node['objtype'] = kind
        node.append(title_signode)
        node.append(contentnode)
        return [node], contentnode
