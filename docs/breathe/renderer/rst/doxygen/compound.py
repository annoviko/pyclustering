
from .base import Renderer
from .index import CompoundRenderer

class DoxygenTypeSubRenderer(Renderer):

    def render(self):

        context = self.context.create_child_context(self.data_object.compounddef)
        compound_renderer = self.renderer_factory.create_renderer(context)
        return compound_renderer.render()


class CompoundDefTypeSubRenderer(Renderer):

    # We store both the identified and appropriate title text here as we want to define the order
    # here and the titles for the SectionDefTypeSubRenderer but we don't want the repetition of
    # having two lists in case they fall out of sync
    sections = [
                ("user-defined", "User Defined"),
                ("public-type", "Public Types"),
                ("public-func", "Public Functions"),
                ("public-attrib", "Public Members"),
                ("public-slot", "Public Slots"),
                ("signal", "Signal"),
                ("dcop-func",  "DCOP Function"),
                ("property",  "Property"),
                ("event",  "Event"),
                ("public-static-func", "Public Static Functions"),
                ("public-static-attrib", "Public Static Attributes"),
                ("protected-type",  "Protected Types"),
                ("protected-func",  "Protected Functions"),
                ("protected-attrib",  "Protected Attributes"),
                ("protected-slot",  "Protected Slots"),
                ("protected-static-func",  "Protected Static Functions"),
                ("protected-static-attrib",  "Protected Static Attributes"),
                ("package-type",  "Package Types"),
                ("package-func", "Package Functions"),
                ("package-attrib", "Package Attributes"),
                ("package-static-func", "Package Static Functions"),
                ("package-static-attrib", "Package Static Attributes"),
                ("private-type", "Private Types"),
                ("private-func", "Private Functions"),
                ("private-attrib", "Private Members"),
                ("private-slot",  "Private Slots"),
                ("private-static-func", "Private Static Functions"),
                ("private-static-attrib",  "Private Static Attributes"),
                ("friend",  "Friends"),
                ("related",  "Related"),
                ("define",  "Defines"),
                ("prototype",  "Prototypes"),
                ("typedef",  "Typedefs"),
                ("enum",  "Enums"),
                ("func",  "Functions"),
                ("var",  "Variables"),
                ]

    def render(self):

        nodelist = []    

        if self.data_object.briefdescription:
            context = self.context.create_child_context(self.data_object.briefdescription)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        if self.data_object.detaileddescription:
            context = self.context.create_child_context(self.data_object.detaileddescription)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        section_nodelists = {}

        # Get all sub sections
        for sectiondef in self.data_object.sectiondef:
            context = self.context.create_child_context(sectiondef)
            renderer = self.renderer_factory.create_renderer(context)
            child_nodes = renderer.render()
            if not child_nodes:
                # Skip empty section
                continue
            kind = sectiondef.kind
            node = self.node_factory.container(classes=['breathe-sectiondef'])
            node.document = self.state.document
            node['objtype'] = kind
            node.extend(child_nodes)
            # We store the nodes as a list against the kind in a dictionary as the kind can be
            # 'user-edited' and that can repeat so this allows us to collect all the 'user-edited'
            # entries together
            nodes = section_nodelists.setdefault(kind, [])
            nodes += [node]

        # Order the results in an appropriate manner
        for kind, _ in self.sections:
            nodelist.extend(section_nodelists.get(kind, []))

        # Take care of innerclasses
        for innerclass in self.data_object.innerclass:
            context = self.context.create_child_context(innerclass)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        for innernamespace in self.data_object.innernamespace:
            context = self.context.create_child_context(innernamespace)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist


class SectionDefTypeSubRenderer(Renderer):

    section_titles = dict(CompoundDefTypeSubRenderer.sections)

    def render(self):

        node_list = []

        if self.data_object.description:
            context = self.context.create_child_context(self.data_object.description)
            renderer = self.renderer_factory.create_renderer(context)
            node_list.extend(renderer.render())

        # Get all the memberdef info
        for memberdef in self.data_object.memberdef:
            context = self.context.create_child_context(memberdef)
            renderer = self.renderer_factory.create_renderer(context)
            node_list.extend(renderer.render())

        if node_list:

            text = self.section_titles[self.data_object.kind]

            # Override default name for user-defined sections. Use "Unnamed
            # Group" if the user didn't name the section
            # This is different to Doxygen which will track the groups and name
            # them Group1, Group2, Group3, etc.
            if self.data_object.kind == "user-defined":
                if self.data_object.header:
                    text = self.data_object.header
                else:
                    text = "Unnamed Group"

            # Use rubric for the title because, unlike the docutils element "section",
            # it doesn't interfere with the document structure.
            rubric = self.node_factory.rubric(text=text, classes=['breathe-sectiondef-title'])

            return [rubric] + node_list

        return []


class MemberDefTypeSubRenderer(Renderer):

    def create_doxygen_target(self):
        """Can be overridden to create a target node which uses the doxygen refid information
        which can be used for creating links between internal doxygen elements.

        The default implementation should suffice most of the time.
        """

        refid = "%s%s" % (self.project_info.name(), self.data_object.id)
        return self.target_handler.create_target(refid)

    def create_domain_target(self):
        """Should be overridden to create a target node which uses the Sphinx domain information so
        that it can be linked to from Sphinx domain roles like cpp:func:`myFunc`

        Returns a list so that if there is no domain active then we simply return an empty list
        instead of some kind of special null node value"""

        return []

    def title(self):

        nodes = []

        # Variable type or function return type
        if self.data_object.type_:
            context = self.context.create_child_context(self.data_object.type_)
            renderer = self.renderer_factory.create_renderer(context)
            nodes.extend(renderer.render())

        if nodes:
            nodes.append(self.node_factory.Text(" "))

        nodes.append(self.node_factory.desc_name(text=self.data_object.name))

        return nodes

    def description(self):

        nodes = []

        if self.data_object.briefdescription:
            context = self.context.create_child_context(self.data_object.briefdescription)
            renderer = self.renderer_factory.create_renderer(context)
            nodes.extend(renderer.render())

        if self.data_object.detaileddescription:
            context = self.context.create_child_context(self.data_object.detaileddescription)
            renderer = self.renderer_factory.create_renderer(context)
            nodes.extend(renderer.render())

        return nodes

    def build_signodes(self, targets):
        """Returns a list to account for when we need multiple signature nodes to account for
        multi-line declarations like templated declarations"""

        # Build title nodes
        signode = self.node_factory.desc_signature()
        signode.extend(targets)
        signode.extend(self.title())
        return [signode]

    def objtype(self):

        return self.data_object.kind

    def update_signature(self, signode):
        """Update the signature node if necessary, e.g. add qualifiers."""
        pass

    def render(self, node=None):

        doxygen_target = self.create_doxygen_target()
        if node:
            signode, contentnode = node.children
            self.update_signature(signode)
            signode.insert(0, doxygen_target)
        else:
            # Build targets for linking
            targets = []
            targets.extend(self.create_domain_target())
            targets.extend(doxygen_target)

            signodes = self.build_signodes(targets)

            # Build description nodes
            contentnode = self.node_factory.desc_content()

            node = self.node_factory.desc()
            node.document = self.state.document
            node['objtype'] = self.objtype()
            node.extend(signodes)
            node.append(contentnode)

        contentnode.extend(self.description())
        return [node]


class FuncMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def create_domain_target(self):

        return self.domain_handler.create_function_target(self.data_object)

    def update_signature(self, signode):

        # Note whether a member function is virtual
        if self.data_object.virt != 'non-virtual':
            signode.insert(0, self.node_factory.Text('virtual '))

        # Add CV-qualifiers
        if self.data_object.const == 'yes':
            signode.append(self.node_factory.Text(' const'))
        # The doxygen xml output doesn't seem to properly register 'volatile' as the xml attribute
        # 'volatile' so we have to check the argsstring for the moment. Maybe it'll change in
        # doxygen at some point. Registered as bug:
        #     https://bugzilla.gnome.org/show_bug.cgi?id=733451
        if self.data_object.volatile == 'yes' or self.data_object.argsstring.endswith('volatile'):
            signode.append(self.node_factory.Text(' volatile'))

        # Add `= 0` for pure virtual members.
        if self.data_object.virt == 'pure-virtual':
            signode.append(self.node_factory.Text(' = 0'))

    def build_signodes(self, targets):

        template_node = self.create_template_node(self.data_object)
        signodes = [template_node] if template_node else []
        title_node = self.node_factory.desc_signature()
        title_node.extend(self.title())
        signodes.append(title_node)
        for target in reversed(targets):
            signodes[0].insert(0, target)
        return signodes

    def title(self):

        nodes = []

        # Get the function type and name
        nodes.extend(MemberDefTypeSubRenderer.title(self))

        # Get the function arguments
        paramlist = self.node_factory.desc_parameterlist()
        for i, parameter in enumerate(self.data_object.param):
            param = self.node_factory.desc_parameter('', '', noemph=True)
            context = self.context.create_child_context(parameter)
            renderer = self.renderer_factory.create_renderer(context)
            param.extend(renderer.render())
            paramlist.append(param)
        nodes.append(paramlist)

        self.update_signature(nodes)
        return nodes

    def render(self, node=None):
        result = MemberDefTypeSubRenderer.render(self, node)
        if node:
            template_node = self.create_template_node(self.data_object)
            if template_node:
                node.insert(0, template_node)
        return result


class DefineMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def title(self):

        title = [self.node_factory.strong(text=self.data_object.name)]

        if self.data_object.param:
            title.append(self.node_factory.Text("("))
            for i, parameter in enumerate(self.data_object.param):
                if i: title.append(self.node_factory.Text(", "))
                context = self.context.create_child_context(parameter)
                renderer = self.renderer_factory.create_renderer(context)
                title.extend(renderer.render())
            title.append(self.node_factory.Text(")"))

        return title

    def description(self):

        return MemberDefTypeSubRenderer.description(self)


class EnumMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def title(self):

        if self.data_object.name.startswith("@"):
            # Assume anonymous enum
            name = [self.node_factory.strong(text="[anonymous]")]
        else:
            name = MemberDefTypeSubRenderer.title(self)

        return [self.node_factory.Text("enum ")] + name

    def description(self):

        description_nodes = MemberDefTypeSubRenderer.description(self)

        name = self.node_factory.emphasis("", self.node_factory.Text("Values:"))
        title = self.node_factory.paragraph("", "", name)
        description_nodes.append(title)

        enums = []
        for item in self.data_object.enumvalue:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            enums.extend(renderer.render())

        description_nodes.extend(enums)

        return description_nodes

    def update_signature(self, signode):
        # Replace "type" with "enum" in the signature. This is needed because Sphinx cpp domain doesn't have an enum
        # directive and we use a type directive instead.
        signode.children[0][0] = self.node_factory.Text("enum ")


class TypedefMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def create_domain_target(self):

        return self.domain_handler.create_typedef_target(self.context.node_stack)

    def title(self):

        args = [self.node_factory.Text("typedef ")]
        args.extend(MemberDefTypeSubRenderer.title(self))

        if self.data_object.argsstring:
            context = self.context.create_child_context(self.data_object.argsstring)
            renderer = self.renderer_factory.create_renderer(context)
            args.extend(renderer.render())

        return args


class VariableMemberDefTypeSubRenderer(MemberDefTypeSubRenderer):

    def title(self):

        args = MemberDefTypeSubRenderer.title(self)

        if self.data_object.argsstring:
            context = self.context.create_child_context(self.data_object.argsstring)
            renderer = self.renderer_factory.create_renderer(context)
            args.extend(renderer.render())

        return args


class EnumvalueTypeSubRenderer(MemberDefTypeSubRenderer):

    def create_domain_target(self):

        return self.domain_handler.create_enumvalue_target(self.context.node_stack)

    def title(self):

        nodes = [self.node_factory.desc_name(text=self.data_object.name)]

        if self.data_object.initializer:
            context = self.context.create_child_context(self.data_object.initializer)
            renderer = self.renderer_factory.create_renderer(context)
            nodes.append(self.node_factory.Text(" "))
            nodes.extend(renderer.render())

        return nodes

    def objtype(self):

        return 'enumvalue'

    def update_signature(self, signode):
        # Remove "class" from the signature. This is needed because Sphinx cpp domain doesn't have an enum value
        # directive and we use a class directive instead.
        signode.children.pop(0)


class DescriptionTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Get description in rst_nodes if possible
        for item in self.data_object.content_:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist


class LinkedTextTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        # Recursively process where possible
        for i, entry in enumerate(self.data_object.content_):
            context = self.context.create_child_context(entry)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist


class ParamTypeSubRenderer(Renderer):

    def __init__(
            self,
            output_defname,
            *args
            ):

        Renderer.__init__( self, *args )

        self.output_defname = output_defname

    def render(self):

        nodelist = []

        # Parameter type
        if self.data_object.type_:
            context = self.context.create_child_context(self.data_object.type_)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        # Parameter name
        if self.data_object.declname:
            if nodelist: nodelist.append(self.node_factory.Text(" "))
            nodelist.append(self.node_factory.emphasis(text=self.data_object.declname))

        elif self.output_defname and self.data_object.defname:
            # We only want to output the definition name (from the cpp file) if the declaration name
            # (from header file) isn't present
            if nodelist: nodelist.append(self.node_factory.Text(" "))
            nodelist.append(self.node_factory.emphasis(text=self.data_object.defname))

        # array information
        if self.data_object.array:
            nodelist.append(self.node_factory.Text(self.data_object.array))

        # Default value
        if self.data_object.defval:
            nodelist.append(self.node_factory.Text(" = "))
            context = self.context.create_child_context(self.data_object.defval)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist



class DocRefTextTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        for item in self.data_object.content_:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        for item in self.data_object.para:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        refid = "%s%s" % (self.project_info.name(), self.data_object.refid)
        nodelist = [
                self.node_factory.pending_xref(
                    "",
                    reftype="ref",
                    refdomain="std",
                    refexplicit=True,
                    refid=refid, 
                    reftarget=refid,
                    *nodelist
                    )
                ]

        return nodelist


class DocParaTypeSubRenderer(Renderer):
    """
    <para> tags in the Doxygen output tend to contain either text or a single other tag of interest.
    So whilst it looks like we're combined descriptions and program listings and other things, in
    the end we generally only deal with one per para tag. Multiple neighbouring instances of these
    things tend to each be in a separate neighbouring para tag.
    """

    def render(self):

        nodelist = []
        for item in self.data_object.content:              # Description
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        for item in self.data_object.programlisting:       # Program listings
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        for item in self.data_object.images:               # Images
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        definition_nodes = []
        for item in self.data_object.simplesects:          # Returns, user par's, etc
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            definition_nodes.extend(renderer.render())

        for item in self.data_object.parameterlist:       # Parameters/Exceptions
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            definition_nodes.extend(renderer.render())

        if definition_nodes:
            definition_list = self.node_factory.definition_list("", *definition_nodes)
            nodelist.append(definition_list)

        return [self.node_factory.paragraph("", "", *nodelist)]


class DocImageTypeSubRenderer(Renderer):
    """Output docutils image node using name attribute from xml as the uri"""

    def render(self):

        path_to_image = self.project_info.sphinx_abs_path_to_file(
                self.data_object.name
                )

        options = { "uri" : path_to_image }

        return [self.node_factory.image("", **options)]

class DocMarkupTypeSubRenderer(Renderer):

    def __init__(
            self,
            creator,
            *args
            ):

        Renderer.__init__( self, *args )

        self.creator = creator

    def render(self):

        nodelist = []

        for item in self.data_object.content_:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return [self.creator("", "", *nodelist)]


class DocParamListTypeSubRenderer(Renderer):
    """Parameter/Exception documentation"""

    lookup = {
            "param" : "Parameters",
            "exception" : "Exceptions",
            "templateparam" : "Templates",
            "retval" : "Return Value",
            }

    def render(self):

        nodelist = []
        for item in self.data_object.parameteritem:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        # Fild list entry
        nodelist_list = self.node_factory.bullet_list("", classes=["breatheparameterlist"], *nodelist)

        term_text = self.lookup[self.data_object.kind]
        term = self.node_factory.term("", "", self.node_factory.strong( "", term_text ) )
        definition = self.node_factory.definition('', nodelist_list)

        return [self.node_factory.definition_list_item('', term, definition)]



class DocParamListItemSubRenderer(Renderer):
    """ Parameter Description Renderer  """

    def render(self):

        nodelist = []
        for item in self.data_object.parameternamelist:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        term = self.node_factory.literal("","", *nodelist)

        separator = self.node_factory.Text(" - ")

        nodelist = []

        if self.data_object.parameterdescription:
            context = self.context.create_child_context(self.data_object.parameterdescription)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return [self.node_factory.list_item("", term, separator, *nodelist)]

class DocParamNameListSubRenderer(Renderer):
    """ Parameter Name Renderer """

    def render(self):

        nodelist = []
        for item in self.data_object.parametername:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist

class DocParamNameSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for item in self.data_object.content_:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist

class DocSect1TypeSubRenderer(Renderer):

    def render(self):

        return []


class DocSimpleSectTypeSubRenderer(Renderer):
    """Other Type documentation such as Warning, Note, Returns, etc"""

    def title(self):

        text = self.node_factory.Text(self.data_object.kind.capitalize())

        return [self.node_factory.strong( "", text )]

    def render(self):

        nodelist = []
        for item in self.data_object.para:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.append(self.node_factory.paragraph("", "", *renderer.render()))

        term = self.node_factory.term("", "", *self.title())
        definition = self.node_factory.definition("", *nodelist)

        return [self.node_factory.definition_list_item("", term, definition)]


class ParDocSimpleSectTypeSubRenderer(DocSimpleSectTypeSubRenderer):

    def title(self):

        context = self.context.create_child_context(self.data_object.title)
        renderer = self.renderer_factory.create_renderer(context)

        return [self.node_factory.strong( "", *renderer.render() )]


class DocTitleTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        for item in self.data_object.content_:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist


class DocForumlaTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []

        for item in self.data_object.content_:

            latex = item.getValue()

            # Somewhat hacky if statements to strip out the doxygen markup that slips through

            node = None

            # Either inline
            if latex.startswith("$") and latex.endswith("$"):
                latex = latex[1:-1]

                # If we're inline create a math node like the :math: role
                node = self.node_factory.math()
            else:
                # Else we're multiline
                node = self.node_factory.displaymath()

            # Or multiline
            if latex.startswith("\[") and latex.endswith("\]"):
                latex = latex[2:-2:]

            # Here we steal the core of the mathbase "math" directive handling code from:
            #    sphinx.ext.mathbase
            node["latex"] = latex

            # Required parameters which we don't have values for
            node["label"] = None
            node["nowrap"] = False
            node["docname"] = self.state.document.settings.env.docname

            nodelist.append(node)

        return nodelist


class ListingTypeSubRenderer(Renderer):

    def render(self):

        lines = []
        nodelist = []
        for i, item in enumerate(self.data_object.codeline):
            # Put new lines between the lines. There must be a more pythonic way of doing this
            if i:
                nodelist.append(self.node_factory.Text("\n"))
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        # Add blank string at the start otherwise for some reason it renders
        # the pending_xref tags around the kind in plain text
        block = self.node_factory.literal_block(
                "",
                "",
                *nodelist
                )

        return [block]

class CodeLineTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for item in self.data_object.highlight:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist

class HighlightTypeSubRenderer(Renderer):

    def render(self):

        nodelist = []
        for item in self.data_object.content_:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist

class TemplateParamListRenderer(Renderer):

    def render(self):

        nodelist = []

        for i, item in enumerate(self.data_object.param):
            if i:
                nodelist.append(self.node_factory.Text(", "))
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist

class IncTypeSubRenderer(Renderer):

    def render(self):

        if self.data_object.local == u"yes":
            text = '#include "%s"' % self.data_object.content_[0].getValue()
        else:
            text = '#include <%s>' % self.data_object.content_[0].getValue()

        return [self.node_factory.emphasis(text=text)]


class RefTypeSubRenderer(CompoundRenderer):

    def __init__(self, compound_parser, *args):
        CompoundRenderer.__init__(self, compound_parser, False, *args)

    def get_node_info(self, file_data):
        name = self.data_object.content_[0].getValue()
        name = name.rsplit("::", 1)[-1]
        return name, file_data.compounddef.kind

    def create_domain_target(self):
        return self.domain_handler.create_inner_ref_target(self.data_object)


class VerbatimTypeSubRenderer(Renderer):

    def __init__(self, content_creator, *args):
        Renderer.__init__(self, *args)

        self.content_creator = content_creator

    def render(self):

        if not self.data_object.text.strip().startswith("embed:rst"):

            # Remove trailing new lines. Purely subjective call from viewing results
            text = self.data_object.text.rstrip()

            # Handle has a preformatted text
            return [self.node_factory.literal_block(text, text)]

        # do we need to strip leading asterisks?
        # NOTE: We could choose to guess this based on every line starting with '*'.
        #   However This would have a side-effect for any users who have an rst-block
        #   consisting of a simple bullet list.
        #   For now we just look for an extended embed tag
        if self.data_object.text.strip().startswith("embed:rst:leading-asterisk"):

            lines = self.data_object.text.splitlines()
            # Replace the first * on each line with a blank space
            lines = map(lambda text: text.replace("*", " ", 1), lines)
            self.data_object.text = "\n".join(lines)

        # do we need to strip leading ///?
        elif self.data_object.text.strip().startswith("embed:rst:leading-slashes"):

            lines = self.data_object.text.splitlines()
            # Replace the /// on each line with three blank spaces
            lines = map(lambda text: text.replace("///", "   ", 1), lines)
            self.data_object.text = "\n".join(lines)

        rst = self.content_creator(self.data_object.text)

        # Parent node for the generated node subtree
        node = self.node_factory.paragraph()
        node.document = self.state.document

        # Generate node subtree
        self.state.nested_parse(rst, 0, node)

        return node


class MixedContainerRenderer(Renderer):

    def render(self):
        context = self.context.create_child_context(self.data_object.getValue())
        renderer = self.renderer_factory.create_renderer(context)
        return renderer.render()


class DocListNestedRenderer(object):
    """Decorator for the list type renderer.

    Creates the proper docutils node based on the sub-type
    of the underlying data object. Takes care of proper numbering
    for deeply nested enumerated lists.
    """

    numeral_kind = ['arabic', 'loweralpha', 'lowerroman', 'upperalpha', 'upperroman']

    def __init__(self, f):
        self.__render = f
        self.__nesting_level = 0

    def __get__(self, obj, objtype):
        """ Support instance methods. """
        import functools
        return functools.partial(self.__call__, obj)

    def __call__(self, rend_self):
        """ Call the wrapped render function. Update the nesting level for the enumerated lists. """
        rend_instance = rend_self
        if rend_instance.data_object.node_subtype is "itemized":
            val = self.__render(rend_instance)
            return DocListNestedRenderer.render_unordered(rend_instance, children=val)
        elif rend_instance.data_object.node_subtype is "ordered":
            self.__nesting_level += 1
            val = self.__render(rend_instance)
            self.__nesting_level -= 1
            return DocListNestedRenderer.render_enumerated(rend_instance, children=val,
                                                           nesting_level=self.__nesting_level)

        return []

    @staticmethod
    def render_unordered(renderer, children):
        nodelist_list = renderer.node_factory.bullet_list("", *children)

        return [nodelist_list]

    @staticmethod
    def render_enumerated(renderer, children, nesting_level):
        nodelist_list = renderer.node_factory.enumerated_list("", *children)
        idx = nesting_level % len(DocListNestedRenderer.numeral_kind)
        nodelist_list['enumtype'] = DocListNestedRenderer.numeral_kind[idx]
        nodelist_list['prefix'] = ''
        nodelist_list['suffix'] = '.'

        return [nodelist_list]


class DocListTypeSubRenderer(Renderer):
    """List renderer

    The specifics of the actual list rendering are handled by the
    decorator around the generic render function.
    """

    @DocListNestedRenderer
    def render(self):
        """ Render all the children depth-first. """
        nodelist = []
        for item in self.data_object.listitem:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return nodelist


class DocListItemTypeSubRenderer(Renderer):
    """List item renderer.
    """

    def render(self):
        """ Render all the children depth-first.
            Upon return expand the children node list into a docutils list-item.
        """
        nodelist = []
        for item in self.data_object.para:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return [self.node_factory.list_item("", *nodelist)]


class DocHeadingTypeSubRenderer(Renderer):
    """Heading renderer.

    Renders embedded headlines as emphasized text. Different heading levels
    are not supported.
    """

    def render(self):

        nodelist = []
        for item in self.data_object.content_:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return [self.node_factory.emphasis("", "", *nodelist)]


class DocURLLinkSubRenderer(Renderer):
    """Url Link Renderer"""

    def render(self):

        nodelist = []
        for item in self.data_object.content_:
            context = self.context.create_child_context(item)
            renderer = self.renderer_factory.create_renderer(context)
            nodelist.extend(renderer.render())

        return [self.node_factory.reference("", "", refuri=self.data_object.url, *nodelist)]
