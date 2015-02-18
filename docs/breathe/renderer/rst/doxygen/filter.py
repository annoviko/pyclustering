"""
Filters
-------

Filters are an interesting and somewhat challenging part of the code base. They are used for
two different purposes:

 - To figure out which nodes in the xml hierarchy to start rendering from. These are called
   'finder filters' or 'content filters'. This is done before rendering starts.
 - To figure out which nodes under a selected nodes in the xml hierarchy should be rendered. These
   are called 'render filters'. This is done during the render process with a test in the
   DoxygenToRstRendererFactory.


General Implementation
~~~~~~~~~~~~~~~~~~~~~~

Filters are essential just tests to see if a node matches certain parameters that are needed to
decide whether or not to include it in some output.

As these filters are declared once and then used on multiple nodes, we model them as object
hierarchies that encapsulate the required test and take a node (with its context) and return True or
False.

If you wanted a test which figures out if a node has the node_type 'memberdef' you might create the
following object hierarchy:

    node_is_memberdef = InFilter(AttributeAccessor(Node(), 'node_type'), ['memberdef'])

This reads from the inside out, as get the node, then get the node_type attribute from it, and see
if the value of the attribute is in the list ['memberdef'].

The Node() is called a 'Selector'. Parent() is also a selector. It means given the current context,
work with the parent of the current node rather than the node itself. This allows you to frame tests
in terms of a node's parent as well as the node which helps when we want nodes with particular
parents and not others.

The AttributeAccessor() is called an 'Accessor'. It wraps up an attempt to access a particular
attribute on the selected node. There are quite a few different specific accessors but they can
mostly be generalised with the AttributeAccessor. This code has evolved over time and initially the
implementation involved specific accessor classes (which are still used in large parts of it.)

The InFilter() is unsurprisingly called a 'Filter'. There are lots of different filters. Filters
either act on the results of Accessors or on the results of other Filters and they always return
True or False. The AndFilter and the OrFilter can be used to combine the outputs of other Filters
with logical 'and' and 'or' operations.

You can build up some pretty complex expressions with this level of freedom as you
might imagine. The complexity is unfortunate but necessary as the nature of filtering the xml is
quite complex.


Finder Filters
~~~~~~~~~~~~~~

The implementation of the filters can change a little depending on how they are called. Finder
filters are called from the breathe.finder.doxygen.index and breathe.finder.doxygen.compound files.
They are called like this:

    # Descend down the hierarchy
    # ...

    if filter_.allow(node_stack):
        matches.append(self.data_object)

    # Keep on descending
    # ...

This means that the result of the filter does not stop us descending down the hierarchy and testing
more nodes. This simplifies the filters as they only have to return true for the exact nodes they
are interested in and they don't have to worry about allowing the iteration down the hierarchy to
continue for nodes which don't match.

An example of a finder filter is:

    AndFilter(
        InFilter(NodeTypeAccessor(Node()), ["compound"]),
        InFilter(KindAccessor(Node()), ["group"]),
        InFilter(NameAccessor(Node()), ["mygroup"])
        )

This says, return True for all the nodes of node_type 'compound' with 'kind' set to 'group' which
have the name 'mygroup'. It returns false for everything else, but when a node matching this is
found then it is added to the matches list by the code above.

It is therefore relatively easy to write finder filters. If you have two separate node filters like
the one above and you want to match on both of them then you can do:

    OrFilter(
        node_filter_1,
        node_filter_2
        )

To combine them.


Content Filters
~~~~~~~~~~~~~~~

Content filters are harder than the finder filters as they are responsible for halting the iteration
down the hierarchy if they return false. This means that if you're interested in memberdef nodes
with a particular attribute then you have to check for that but also include a clause which allows
all other non-memberdef nodes to pass through as you don't want to interrupt them.

This means you end up with filters like this:

    OrFilter(
        AndFilter(
            InFilter(NodeTypeAccessor(Node()), ["compound"]),
            InFilter(KindAccessor(Node()), ["group"]),
            InFilter(NameAccessor(Node()), ["mygroup"])
            ),
        NotFilter(
            AndFilter(
                InFilter(NodeTypeAccessor(Node()), ["compound"]),
                InFilter(KindAccessor(Node()), ["group"]),
                )
            )
        )

Which is to say that we want to let through a compound, with kind group, with name 'mygroup' but
we're also happy if the node is **not** a compund with kind group. Really we just don't want to let
through any compounds with kind group with name other than 'mygroup'. As such, we can rephrase this
as:

    NotFilter(
        AndFilter(
            InFilter(NodeTypeAccessor(Node()), ["compound"]),
            InFilter(KindAccessor(Node()), ["group"]),
            NotFilter(InFilter(NameAccessor(Node()), ["mygroup"]))
            )
        )

Using logical manipulation we can rewrite this as:

    OrFilter(
        NotFilter(InFilter(NodeTypeAccessor(Node()), ["compound"])),
        NotFilter(InFilter(KindAccessor(Node()), ["group"])),
        InFilter(NameAccessor(Node()), ["mygroup"])
        )

We reads: allow if it isn't a compound, or if it is a compound but doesn't have a 'kind' of 'group',
but if it is a compound and has a 'kind' of 'group then only allow it if it is named 'mygroup'.


Helper Syntax
~~~~~~~~~~~~~

Some of these filter declarations get a little awkward to read and write. They are not laid out in
manner which reads smoothly. Additional helper methods and operator overloads have been introduced
to help with this.

AttributeAccessor objects are created in property methods on the Selector classes so:

    node.kind

Where node has been declared as a Node() instance. Results in:

    AttributeAccessor(Node(), 'kind')

The '==' and '!=' operators on the Accessors have been overloaded to return the appropriate filters
so that:

    node.kind == 'group'

Results in:

    InFilter(AttributeAccessor(Node(), 'kind'), ['kind'])

We also override the binary 'and' (&), 'or' (|) and 'not' (~) operators in Python to apply
AndFilters, OrFilters and NotFilters respectively. We have to override the binary operators as they
actual 'and', 'or' and 'not' operators cannot be overridden. So:

    (node.node_type == 'compound') & (node.name == 'mygroup')

Translates to:

    AndFilter(
        InFilter(NodeTypeAccessor(Node()), ["compound"])),
        InFilter(NameAccessor(Node()), ["mygroup"])
        )

Where the former is hopefully more readable without sacrificing too much to the abstract magic of
operator overloads.


Operator Precedences & Extra Parenthesis
''''''''''''''''''''''''''''''''''''''''

As the binary operators have a lower operator precedence than '==' and '!=' and some other operators
we have to include additional parenthesis in the expressions to group them as we want. So instead of
writing:

    node.node_type == 'compound' & node.name == 'mygroup'

We have to write:

    (node.node_type == 'compound') & (node.name == 'mygroup')

"""


class UnrecognisedKindError(Exception):
    pass


class Selector(object):

    @property
    def node_type(self):
        return NodeTypeAccessor(self)

    @property
    def kind(self):
        return AttributeAccessor(self, 'kind')

    @property
    def node_name(self):
        return AttributeAccessor(self, 'node_name')

    @property
    def name(self):
        return AttributeAccessor(self, 'name')

    @property
    def briefdescription(self):
        return AttributeAccessor(self, 'briefdescription')

    @property
    def detaileddescription(self):
        return AttributeAccessor(self, 'detaileddescription')

    @property
    def prot(self):
        return AttributeAccessor(self, 'prot')

    @property
    def valueOf(self):
        return AttributeAccessor(self, 'valueOf_')

    @property
    def id(self):
        return AttributeAccessor(self, 'id')


class Ancestor(Selector):

    def __init__(self, generations):
        self.generations = generations

    def __call__(self, node_stack):
        return node_stack[self.generations]


class Parent(Selector):

    def __call__(self, node_stack):
        return node_stack[1]


class Node(Selector):

    def __call__(self, node_stack):
        return node_stack[0]


class Accessor(object):

    def __init__(self, selector):
        self.selector = selector

    def __eq__(self, value):
        return InFilter(self, [value])

    def __ne__(self, value):
        return NotFilter(InFilter(self, [value]))

    def is_one_of(self, collection):
        return InFilter(self, collection)

    def has_content(self):
        return HasContentFilter(self)

    def endswith(self, options):
        return EndsWithFilter(self, options)


class NameAccessor(Accessor):

    def __call__(self, node_stack):
        return self.selector(node_stack).name


class NodeNameAccessor(Accessor):
    """Check the .node_name member which is declared on refTypeSub nodes

    It distinguishes between innerclass, innernamespace, etc.
    """

    def __call__(self, node_stack):
        return self.selector(node_stack).node_name


class NodeTypeAccessor(Accessor):

    def __call__(self, node_stack):

        data_object = self.selector(node_stack)
        try:
            return data_object.node_type
        except AttributeError as e:

            # Horrible hack to silence errors on filtering unicode objects
            # until we fix the parsing
            if type(data_object) == unicode:
                return "unicode"
            else:
                raise e


class KindAccessor(Accessor):

    def __call__(self, node_stack):
        return self.selector(node_stack).kind


class AttributeAccessor(Accessor):
    """Returns the value of a particular attribute on the selected node.

    AttributeAccessor(Node(), 'name') returns the value of ``node.name``.
    """

    def __init__(self, selector, attribute_name):
        Accessor.__init__(self, selector)

        self.attribute_name = attribute_name

    def __call__(self, node_stack):
        return getattr(self.selector(node_stack), self.attribute_name)


class LambdaAccessor(Accessor):

    def __init__(self, selector, func):
        Accessor.__init__(self, selector)

        self.func = func

    def __call__(self, node_stack):
        return self.func(self.selector(node_stack))


class NamespaceAccessor(Accessor):

    def __call__(self, node_stack):
        return self.selector(node_stack).namespaces


class Filter(object):

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)

    def __invert__(self):
        return NotFilter(self)


class HasAncestorFilter(Filter):

    def __init__(self, generations):
        self.generations = generations

    def allow(self, node_stack):
        return len(node_stack) > self.generations


class HasContentFilter(Filter):

    def __init__(self, accessor):
        self.accessor = accessor

    def allow(self, node_stack):
        """Detects if the node in questions has an empty .content_ property.
        """

        return bool(self.accessor(node_stack).content_)


class EndsWithFilter(Filter):
    """Detects if the string result of the accessor ends with any of the strings in the ``options``
    iterable parameter.
    """

    def __init__(self, accessor, options):
        self.accessor = accessor
        self.options = options

    def allow(self, node_stack):
        string = self.accessor(node_stack) 
        for entry in self.options:
            if string.endswith(entry):
                return True

        return False


class InFilter(Filter):
    """Checks if what is returned from the accessor is 'in' in the members"""

    def __init__(self, accessor, members):

        self.accessor = accessor
        self.members = members

    def allow(self, node_stack):

        name = self.accessor(node_stack)

        return name in self.members


class GlobFilter(Filter):

    def __init__(self, accessor, glob):

        self.accessor = accessor
        self.glob = glob

    def allow(self, node_stack):

        text = self.accessor(node_stack)
        return self.glob.match(text)


class FilePathFilter(Filter):

    def __init__(self, accessor, target_file, path_handler):

        self.accessor = accessor
        self.target_file = target_file
        self.path_handler = path_handler

    def allow(self, node_stack):

        location = self.accessor(node_stack).file

        if self.path_handler.includes_directory(self.target_file):
            # If the target_file contains directory separators then
            # match against the same length at the end of the location
            #
            location_match = location[-len(self.target_file):]
            return location_match == self.target_file

        else:
            # If there are no separators, match against the whole filename
            # at the end of the location
            #
            # This is to prevent "Util.cpp" matching "PathUtil.cpp"
            #
            location_basename = self.path_handler.basename(location)
            return location_basename == self.target_file


class NamespaceFilter(Filter):

    def __init__(self, namespace_accessor, name_accessor):

        self.namespace_accessor = namespace_accessor
        self.name_accessor = name_accessor

    def allow(self, node_stack):

        namespaces = self.namespace_accessor(node_stack)
        name = self.name_accessor(node_stack)

        try:
            namespace, name = name.rsplit("::", 1)
        except ValueError:
            namespace, name = "", name

        return namespace in namespaces


class OpenFilter(Filter):

    def allow(self, node_stack):

        return True


class ClosedFilter(Filter):

    def allow(self, node_stack):

        return False


class NotFilter(Filter):

    def __init__(self, child_filter):
        self.child_filter = child_filter

    def allow(self, node_stack):

        return not self.child_filter.allow(node_stack)


class AndFilter(Filter):

    def __init__(self, *filters):

        self.filters = filters

    def allow(self, node_stack):

        # If any filter returns False then return False
        for filter_ in self.filters:
            if not filter_.allow(node_stack):
                return False

        return True


class OrFilter(Filter):
    """Provides a short-cutted 'or' operation between two filters"""

    def __init__(self, *filters):

        self.filters = filters

    def allow(self, node_stack):

        # If any filter returns True then return True
        for filter_ in self.filters:
            if filter_.allow(node_stack):
                return True

        return False


class IfFilter(Filter):

    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def allow(self, node_stack):

        if self.condition.allow(node_stack):
            return self.if_true.allow(node_stack)
        else:
            return self.if_false.allow(node_stack)


class Glob(object):

    def __init__(self, method, pattern):

        self.method = method
        self.pattern = pattern

    def match(self, name):

        return self.method(name, self.pattern)


class GlobFactory(object):

    def __init__(self, method):

        self.method = method

    def create(self, pattern):

        return Glob(self.method, pattern)


class Gather(object):

    def __init__(self, accessor, names):

        self.accessor = accessor
        self.names = names

    def allow(self, node_stack):

        self.names.extend(self.accessor(node_stack))

        return False


class FilterFactory(object):

    # C++ style public entries
    public_kinds = set([
            "public-type",
            "public-func",
            "public-attrib",
            "public-slot",
            "public-static-func",
            "public-static-attrib",
            ])

    def __init__(self, globber_factory, path_handler):

        self.globber_factory = globber_factory
        self.path_handler = path_handler
        self.default_members = ()
        self.implementation_filename_extensions = ()

    def create_render_filter(self, kind, options):
        """Render filter for group & namespace blocks"""

        if kind not in ['group', 'namespace']:
            raise UnrecognisedKindError(kind)

        # Generate new dictionary from defaults
        filter_options = dict((entry, u'') for entry in self.default_members)

        # Update from the actual options
        filter_options.update(options)

        # Convert the doxygengroup members flag (which just stores None as the value) to an empty
        # string to allow the create_class_member_filter to process it properly
        if 'members' in filter_options:
            filter_options['members'] = u''

        node = Node()
        parent = Parent()
        grandparent = Ancestor(2)
        has_grandparent = HasAncestorFilter(2)

        non_class_memberdef = \
            has_grandparent \
            & (grandparent.node_type == 'compounddef') \
            & (grandparent.kind != 'class') \
            & (grandparent.kind != 'struct') \
            & (node.node_type == 'memberdef')

        node_is_public = node.prot == 'public'

        non_class_public_memberdefs = non_class_memberdef & node_is_public | ~ non_class_memberdef

        return ( self.create_class_member_filter(filter_options) | non_class_memberdef ) \
            & self.create_innerclass_filter(filter_options) \
            & self.create_outline_filter(filter_options)

    def create_class_filter(self, target, options):
        """Content filter for classes based on various directive options"""

        # Generate new dictionary from defaults
        filter_options = dict((entry, u'') for entry in self.default_members)

        # Update from the actual options
        filter_options.update(options)

        return AndFilter(
            self.create_class_member_filter(filter_options),
            self.create_innerclass_filter(filter_options, outerclass=target),
            self.create_outline_filter(filter_options),
            self.create_show_filter(filter_options),
            )

    def create_innerclass_filter(self, options, outerclass=''):
        """
        :param outerclass: Should be the class/struct being target by the directive calling this
                           code. If it is a group or namespace directive then it should be left
                           blank. It is used when looking for names listed in the :members: option.

                           The name should include any additional namespaces that the target class
                           is in.
        """

        node = Node()
        node_is_innerclass = (node.node_type == "ref") & (node.node_name == "innerclass")

        parent = Parent()
        parent_is_compounddef = parent.node_type == 'compounddef'
        parent_is_class = parent.kind.is_one_of(['class', 'struct'])

        allowed = set()
        all_options = {
            'protected-members': 'protected',
            'private-members': 'private',
            }

        for option, scope in all_options.iteritems():
            if option in options:
                allowed.add(scope)

        node_is_innerclass_in_class = parent_is_compounddef & parent_is_class & node_is_innerclass

        public_innerclass_filter = ClosedFilter()

        if 'members' in options:

            if options['members'].strip():

                text = options["members"]

                prefix = ('%s::' % outerclass) if outerclass else ''

                # Matches sphinx-autodoc behaviour of comma separated values
                members = set(['%s%s' % (prefix, x.strip()) for x in text.split(",")])

                node_valueOf_is_in_members = node.valueOf.is_one_of(members)

                # Accept any nodes which don't have a "sectiondef" as a parent or, if they do, only
                # accept them if their names are in the members list
                public_innerclass_filter = ~ node_is_innerclass_in_class | node_valueOf_is_in_members

            else:
                allowed.add('public')


        node_is_in_allowed_scope = node.prot.is_one_of(allowed)

        innerclass = ~ node_is_innerclass_in_class | node_is_in_allowed_scope
        description = self._create_description_filter(True, 'compounddef', options)

        # Put parent check last as we only want to check parents of innerclass's otherwise we have
        # to check the parent's type as well
        return innerclass | public_innerclass_filter | description

    def create_show_filter(self, options):
        """Currently only handles the header-file entry"""

        try:
            text = options["show"]
        except KeyError:
            # Allow through everything except the header-file includes nodes
            return OrFilter(
                NotFilter(InFilter(NodeTypeAccessor(Parent()), ["compounddef"])),
                NotFilter(InFilter(NodeTypeAccessor(Node()), ["inc"]))
                )

        if text == "header-file":
            # Allow through everything, including header-file includes
            return OpenFilter()

        # Allow through everything except the header-file includes nodes
        return OrFilter(
            NotFilter(InFilter(NodeTypeAccessor(Parent()), ["compounddef"])),
            NotFilter(InFilter(NodeTypeAccessor(Node()), ["inc"]))
            )

    def _create_description_filter(self, allow, level, options):
        """Whether or not we allow descriptions is determined by the calling function and we just do
        whatever the 'allow' function parameter tells us.
        """

        node = Node()
        node_is_description = node.node_type == 'description'
        parent = Parent()
        parent_is_level = parent.node_type == level

        # Nothing with a parent that's a sectiondef
        description_filter = ~ parent_is_level

        # Let through any description children of sectiondefs if we output any kind members
        if allow:

            description_filter = \
                (parent_is_level & node_is_description) | ~ parent_is_level

        return description_filter

    def _create_public_members_filter(self, options):

        node = Node()
        node_is_memberdef = node.node_type == "memberdef"
        node_is_public = node.prot == "public"

        parent = Parent()
        parent_is_sectiondef = parent.node_type == "sectiondef"

        # Nothing with a parent that's a sectiondef
        is_memberdef = parent_is_sectiondef & node_is_memberdef
        public_members_filter = ~ is_memberdef

        # If the user has specified the 'members' option with arguments then we only pay attention
        # to that and not to any other member settings
        if "members" in options:

            if options['members'].strip():

                text = options["members"]

                # Matches sphinx-autodoc behaviour of comma separated values
                members = set([x.strip() for x in text.split(",")])

                node_name_is_in_members = node.name.is_one_of(members)

                # Accept any nodes which don't have a "sectiondef" as a parent or, if they do, only
                # accept them if their names are in the members list
                public_members_filter = \
                    (parent_is_sectiondef & node_name_is_in_members) | ~ parent_is_sectiondef

            else:

                # Select anything that doesn't have a parent which is a sectiondef, or, if it does,
                # only select the public ones
                public_members_filter = \
                    (is_memberdef & node_is_public) | ~ is_memberdef

        return public_members_filter

    def _create_non_public_members_filter(self, prot, option_name, options):
        """'prot' is the doxygen xml term for 'public', 'protected' and 'private' categories."""

        node = Node()
        node_is_memberdef = node.node_type == "memberdef"
        node_is_public = node.prot == prot

        parent = Parent()
        parent_is_sectiondef = parent.node_type == "sectiondef"

        # Nothing with a parent that's a sectiondef
        is_memberdef = parent_is_sectiondef & node_is_memberdef
        filter_ = ~ is_memberdef

        if option_name in options:

            # Allow anything that isn't a memberdef, or if it is only allow the public ones
            filter_ = ~ is_memberdef | node_is_public

        return filter_

    def _create_undoc_members_filter(self, options):

        node = Node()
        node_is_memberdef = node.node_type == 'memberdef'

        node_has_description = node.briefdescription.has_content() \
            | node.detaileddescription.has_content()

        # Allow anything that isn't a memberdef, or if it is only allow the ones with a description
        undoc_members_filter = ~ node_is_memberdef | node_has_description

        if 'undoc-members' in options:

            undoc_members_filter = OpenFilter()

        return undoc_members_filter

    def create_class_member_filter(self, options):
        """Content filter based on :members: and :private-members: classes"""

        # I can't fully explain the filtering of descriptions here. More testing needed to figure
        # out when it is needed. This approach reflects the old code that was here but it wasn't
        # commented (my fault.) I wonder if maybe the public and private declarations themselves can
        # be documented and we need to let them through. Not sure.
        allow = 'members' in options \
            or 'protected-members' in options \
            or 'private-members' in options

        description = self._create_description_filter(allow, 'sectiondef', options)

        # Create all necessary filters and combine them
        public_members = self._create_public_members_filter(options)

        protected_members = self._create_non_public_members_filter(
            'protected',
            'protected-members',
            options
            )

        private_members = self._create_non_public_members_filter(
            'private',
            'private-members',
            options
            )

        undoc_members = self._create_undoc_members_filter(options)

        # Allow any public/private members which also fit the undoc filter and all the descriptions
        allowed_members = ( public_members | protected_members | private_members ) & undoc_members
        return allowed_members | description

    def create_outline_filter(self, options):
        if 'outline' in options:
            node = Node()
            return ~ node.node_type.is_one_of(["description", "inc"])
        else:
            return OpenFilter()

    def create_file_filter(self, filename, options):

        valid_names = []

        filter_ = AndFilter(
            NotFilter(
                # Gather the "namespaces" attribute from the
                # compounddef for the file we're rendering and
                # store the information in the "valid_names" list
                #
                # Gather always returns false, so, combined with
                # the NotFilter this chunk always returns true and
                # so does not affect the result of the filtering
                AndFilter(
                    InFilter(NodeTypeAccessor(Node()), ["compounddef"]),
                    InFilter(KindAccessor(Node()), ["file"]),
                    FilePathFilter(
                        LambdaAccessor(Node(), lambda x: x.location),
                        filename, self.path_handler
                        ),
                    Gather(LambdaAccessor(Node(), lambda x: x.namespaces), valid_names)
                    )
                ),
            NotFilter(
                # Take the valid_names and everytime we handle an
                # innerclass or innernamespace, check that its name
                # was one of those initial valid names so that we
                # never end up rendering a namespace or class that
                # wasn't in the initial file. Notably this is
                # required as the location attribute for the
                # namespace in the xml is unreliable.
                AndFilter(
                    InFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    InFilter(NodeTypeAccessor(Node()), ["ref"]),
                    InFilter(NodeNameAccessor(Node()), ["innerclass", "innernamespace"]),
                    NotFilter(
                        InFilter(
                            LambdaAccessor(Node(), lambda x: x.content_[0].getValue()),
                            valid_names
                            )
                        )
                    )
                ),
            NotFilter(
                # Ignore innerclasses and innernamespaces that are inside a
                # namespace that is going to be rendered as they will be
                # rendered with that namespace and we don't want them twice
                AndFilter(
                    InFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    InFilter(NodeTypeAccessor(Node()), ["ref"]),
                    InFilter(NodeNameAccessor(Node()), ["innerclass", "innernamespace"]),
                    NamespaceFilter(
                        NamespaceAccessor(Parent()),
                        LambdaAccessor(Node(), lambda x: x.content_[0].getValue())
                        )
                    )
                ),
            NotFilter(
                # Ignore memberdefs from files which are different to
                # the one we're rendering. This happens when we have to
                # cross into a namespace xml file which has entries
                # from multiple files in it
                AndFilter(
                    InFilter(NodeTypeAccessor(Node()), ["memberdef"]),
                    NotFilter(
                        FilePathFilter(LambdaAccessor(Node(), lambda x: x.location),
                                       filename, self.path_handler)
                        )
                    )
                ),
            NotFilter(
                # Ignore compounddefs which are from another file
                # (normally means classes and structs which are in a
                # namespace that we have other interests in) but only
                # check it if the compounddef is not a namespace
                # itself, as for some reason compounddefs for
                # namespaces are registered with just a single file
                # location even if they namespace is spread over
                # multiple files
                AndFilter(
                    InFilter(NodeTypeAccessor(Node()), ["compounddef"]),
                    NotFilter(InFilter(KindAccessor(Node()), ["namespace"])),
                    NotFilter(
                        FilePathFilter(LambdaAccessor(Node(), lambda x: x.location),
                                       filename, self.path_handler)
                        )
                    )
                )
            )

        return AndFilter(
            self.create_outline_filter(options),
            filter_
            )

    def create_content_filter(self, kind, options):
        """Returns a filter which matches the contents of the or namespace but not the group or
        namepace name or description.

        This allows the groups to be used to structure sections of the documentation rather than to
        structure and further document groups of documentation

        As a finder/content filter we only need to match exactly what we're interested in.
        """

        if kind not in ['group', 'namespace']:
            raise UnrecognisedKindError(kind)

        node = Node()

        # Filter for public memberdefs
        node_is_memberdef = node.node_type == 'memberdef'
        node_is_public = node.prot == 'public'

        public_members = node_is_memberdef & node_is_public

        # Filter for public innerclasses
        parent = Parent()
        parent_is_compounddef = parent.node_type == 'compounddef'
        parent_is_class = parent.kind == kind

        node_is_innerclass = (node.node_type == "ref") & (node.node_name == "innerclass")
        node_is_public = node.prot == 'public'

        public_innerclass = parent_is_compounddef & parent_is_class \
            & node_is_innerclass & node_is_public

        return public_members | public_innerclass

    def create_index_filter(self, options):

        filter_ = AndFilter(
            NotFilter(
                AndFilter(
                    InFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    InFilter(NodeTypeAccessor(Node()), ["ref"]),
                    InFilter(NodeNameAccessor(Node()), ["innerclass", "innernamespace"])
                    )
                ),
            NotFilter(
                AndFilter(
                    InFilter(NodeTypeAccessor(Parent()), ["compounddef"]),
                    InFilter(KindAccessor(Parent()), ["group"]),
                    InFilter(NodeTypeAccessor(Node()), ["sectiondef"]),
                    InFilter(KindAccessor(Node()), ["func"])
                    )
                )
            )

        return AndFilter(
            self.create_outline_filter(options),
            filter_
            )

    def create_open_filter(self):
        """Returns a completely open filter which matches everything"""

        return OpenFilter()

    def create_id_filter(self, node_type, refid):

        node = Node()
        return (node.node_type == node_type) & (node.id == refid)

    def create_file_finder_filter(self, filename):

        filter_ = AndFilter(
            InFilter(NodeTypeAccessor(Node()), ["compounddef"]),
            InFilter(KindAccessor(Node()), ["file"]),
            FilePathFilter(LambdaAccessor(Node(), lambda x: x.location), filename,
                           self.path_handler)
            )

        return filter_

    def create_function_finder_filter(self, namespace, function_name):

        node = Node()
        parent = Parent()

        node_matches = (node.node_type == 'member') \
                & (node.kind == 'function') \
                & (node.name == function_name)

        if namespace:
            parent_matches = (parent.node_type == 'compound') \
                    & ((parent.kind == 'namespace') | (parent.kind == 'class')) \
                    & (parent.name == namespace)

            return parent_matches & node_matches

        else:
            is_implementation_file = parent.name.endswith(self.implementation_filename_extensions)
            parent_is_compound = parent.node_type == 'compound'
            parent_is_file = (parent.kind == 'file') & (~ is_implementation_file)
            parent_is_not_file = parent.kind != 'file'

            return (parent_is_compound & parent_is_file & node_matches) \
                | (parent_is_compound & parent_is_not_file & node_matches)

    def create_finder_filter(self, kind, name):
        """Returns a filter which looks for the compound node from the index which is a group node
        (kind=group) and has the appropriate name

        The compound node should reference the group file which we can parse for the group
        contents.
        """

        if kind == 'group':

            filter_ = AndFilter(
                InFilter(NodeTypeAccessor(Node()), ["compound"]),
                InFilter(KindAccessor(Node()), ["group"]),
                InFilter(NameAccessor(Node()), [name])
                )
        else:
            # Assume kind == 'namespace'
            filter_ = AndFilter(
                InFilter(NodeTypeAccessor(Node()), ["compound"]),
                InFilter(KindAccessor(Node()), ["namespace"]),
                InFilter(NameAccessor(Node()), [name])
                )

        return filter_

    def get_config_values(self, app):
        """Extract the breathe_default_members config value and store it.

        This method is called on the 'builder-init' event in Sphinx"""

        self.default_members = app.config.breathe_default_members

        self.implementation_filename_extensions = \
            app.config.breathe_implementation_filename_extensions

