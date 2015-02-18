
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


# Used below in CompoundTypeSubRenderer and in RefTypeSubRenderer in compound.py so we have split it
# out in a helper function. This feels fairly ugly due to the number of arguments. A forced
# refactoring for the sake of refactoring rather than a beautiful reuse of code.
def render_compound(
    name,
    kind,
    parent_context,
    rendered_data,
    renderer_factory,
    node_factory,
    domain_target,
    doxygen_target,
    document
    ):

    # Build targets for linking
    targets = []
    targets.extend(domain_target)
    targets.extend(doxygen_target)

    title_signode = node_factory.desc_signature()

    file_data = parent_context.node_stack[0]
    new_context = parent_context.create_child_context(file_data.compounddef)

    # Check if there is template information and format it as desired
    template_signode = None
    if file_data.compounddef.templateparamlist:
        context = new_context.create_child_context(file_data.compounddef.templateparamlist)
        renderer = renderer_factory.create_renderer(context)
        template_nodes = [node_factory.Text("template <")]
        template_nodes.extend(renderer.render())
        template_nodes.append(node_factory.Text(">"))
        template_signode = node_factory.desc_signature()
        # Add targets to the template line if it is there
        template_signode.extend(targets)
        template_signode.extend(template_nodes)
    else:
        # Add targets to title line if there is no template line
        title_signode.extend(targets)

    # Set up the title
    title_signode.append(node_factory.emphasis(text=kind))
    title_signode.append(node_factory.Text(" "))
    title_signode.append(node_factory.desc_name(text=name))

    contentnode = node_factory.desc_content()

    if file_data.compounddef.includes:
        for include in file_data.compounddef.includes:
            context = new_context.create_child_context(include)
            renderer = renderer_factory.create_renderer(context)
            contentnode.extend(renderer.render())

    contentnode.extend(rendered_data)

    node = node_factory.desc()
    node.document = document
    node['objtype'] = kind
    if template_signode:
        node.append(template_signode)
    node.append(title_signode)
    node.append(contentnode)

    return [node]


class CompoundTypeSubRenderer(Renderer):

    def __init__(self, compound_parser, *args):
        Renderer.__init__(self, *args)

        self.compound_parser = compound_parser

    def create_doxygen_target(self):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        return self.target_handler.create_target(refid)

    def create_domain_target(self):
        """Should be overridden to create a target node which uses the Sphinx domain information so
        that it can be linked to from Sphinx domain roles like cpp:func:`myFunc`

        Returns a list so that if there is no domain active then we simply return an empty list
        instead of some kind of special null node value"""

        return []


    def render(self):

        # Read in the corresponding xml file and process
        file_data = self.compound_parser.parse(self.data_object.refid)

        context = self.context.create_child_context(file_data)
        data_renderer = self.renderer_factory.create_renderer(context)

        # Defer to function for details
        return render_compound(
                self.data_object.name,
                self.data_object.kind,
                context,
                data_renderer.render(),
                self.renderer_factory,
                self.node_factory,
                self.create_domain_target(),
                self.create_doxygen_target(),
                self.state.document
                )


class ClassCompoundTypeSubRenderer(CompoundTypeSubRenderer):

    def create_domain_target(self):

        return self.domain_handler.create_class_target(self.data_object)

