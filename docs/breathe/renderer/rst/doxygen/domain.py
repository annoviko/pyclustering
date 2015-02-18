

class DomainHelper(object):
    pass


class NullDomainHelper(DomainHelper):
    pass


class CppDomainHelper(DomainHelper):

    def __init__(self, definition_parser, substitute):

        self.definition_parser = definition_parser
        self.substitute = substitute

        self.duplicates = {}

    def check_cache(self, _id):
        try:
            return True, self.duplicates[_id]
        except KeyError:
            return False, ""

    def cache(self, _id, project_info):
        self.duplicates[_id] = project_info

    def remove_word(self, word, definition):
        return self.substitute(r"(\s*\b|^)%s\b\s*" % word, "", definition)


class CDomainHelper(DomainHelper):

    def __init__(self):

        self.duplicates = set()

    def is_duplicate(self, name):
        return name in self.duplicates

    def remember(self, name):
        self.duplicates.add(name)


class DomainHandler(object):

    def __init__(self, node_factory, document, env, helper, project_info, target_handler):

        self.node_factory = node_factory
        self.document = document
        self.env = env
        self.helper = helper
        self.project_info = project_info
        self.target_handler = target_handler


class NullDomainHandler(DomainHandler):

    def __init__(self, *args, **kwargs):
        """Swallow args and forget them as we don't need them"""

    def create_function_id(self, data_object):
        return ""

    def create_function_target(self, data_object):
        return []

    def create_class_id(self, data_object):
        return ""

    def create_class_target(self, data_object):
        return []

    def create_inner_ref_target(self, data_object):
        return []

    def create_typedef_target(self, node_stack):
        return []

    def create_enumvalue_target(self, node_stack):
        return []


class CDomainHandler(DomainHandler):

    def create_function_id(self, data_object):

        name = data_object.definition.split()[-1]

        return name

    def create_function_target(self, data_object):

        name = data_object.definition.split()[-1]

        return self._create_target(name, "function")

    def _create_target(self, name, type_):

        if self.helper.is_duplicate(name):
            print ("Warning: Ignoring duplicate '%s'. As C does not support overloaded "
                   "functions. Perhaps you should be using the cpp domain?" % name)
            return

        self.helper.remember(name)

        # Create target node. This is required for LaTeX output as target nodes are converted to the
        # appropriate \phantomsection & \label for in document LaTeX links
        (target,) = self.target_handler.create_target(name)

        inv = self.env.domaindata['c']['objects']
        if name in inv:
            self.env.warn(
                self.env.docname,
                'duplicate C object description of %s, ' % name +
                'other instance in ' + self.env.doc2path(inv[name][0]),
                self.lineno)
        inv[name] = (self.env.docname, "function")

        return [target]


class CppDomainHandler(DomainHandler):

    def get_fully_qualified_name(self, node_stack):

        names = []
        if node_stack[0].node_type == 'enumvalue':
            names.append(node_stack[0].name)
            # Skip the name of the containing enum because it is not a part of the fully qualified name.
            node_stack = node_stack[2:]

        for node in node_stack:
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

    def create_class_id(self, data_object):

        def_ = data_object.name

        parser = self.helper.definition_parser(def_)
        sigobj = parser.parse_class()

        return sigobj.get_id()

    def create_class_target(self, data_object):

        id_ = self.create_class_id(data_object)
        name = data_object.name

        return self._create_target(name, "class", id_)

    def create_inner_ref_target(self, data_object):
        """Creates a target for a class or namespace defined in another class or namespace. This
        will get called for any 'refType' node which includes a number of doxygen documentation
        nodes like 'innerpage' & 'innergroup'. So we return nothing unless it is a class or
        namespace.

        See breathe.parser.doxygen.compoundsuper:compounddefType.buildChildren for the full list.
        """

        if data_object.node_name not in ['innerclass', 'innernamespace']:
            return []

        # Drop 'inner' to get 'class' or 'namespace'. Sphinx does support 'namespace' types in the
        # cpp domain yet but we'll do this properly for the moment and correct it or updated Sphinx
        # if needed
        type_ = data_object.node_name.replace('inner', '')

        # Extract fully qualified name (OuterClass::InnerClass) from node with xml like:
        #    <innerclass refid="..." prot="public">OuterClass::InnerClass</innerclass>
        name = data_object.content_[0].getValue()
        return self._create_target(name, type_, name)

    def create_typedef_target(self, node_stack):

        name = self.get_fully_qualified_name(node_stack)
        return self._create_target(name, "type", name)

    def create_enumvalue_target(self, node_stack):

        name = self.get_fully_qualified_name(node_stack)
        return self._create_target(name, "member", name)

    def create_function_id(self, data_object):

        definition = self.helper.remove_word("virtual", data_object.definition)
        argstring = data_object.argsstring

        explicit = "explicit " if data_object.explicit == "yes" else ""

        def_ = "%(explicit)s%(definition)s%(argstring)s" % {
            "explicit": explicit,
            "definition": definition,
            "argstring": argstring,
            }

        parser = self.helper.definition_parser(def_)
        sigobj = parser.parse_function()

        return sigobj.get_id()

    def create_function_target(self, data_object):

        id_ = self.create_function_id(data_object)

        name = data_object.definition.split()[-1]

        return self._create_target(name, "function", id_)

    def _create_target(self, name, type_, id_):
        """Creates a target node and registers it with the appropriate domain
        object list in a style which matches Sphinx's behaviour for the domain
        directives like cpp:function"""

        # Check if we've already got this id
        in_cache, project = self.helper.check_cache(id_)
        if in_cache:
            print("Warning: Ignoring duplicate domain reference '%s'. "
                  "First found in project '%s'" % (id_, project.reference()))
            return []

        self.helper.cache(id_, self.project_info)

        # Create target node. This is required for LaTeX output as target nodes are converted to the
        # appropriate \phantomsection & \label for in document LaTeX links
        target = self.target_handler.create_target(id_)

        # Register object with the sphinx objects registry
        self.document.settings.env.domaindata['cpp']['objects'].setdefault(
            name, (self.document.settings.env.docname, type_, id_))

        return target


class DomainHandlerFactory(object):

    def __init__(self, project_info, node_factory, document, env, target_handler, helpers):

        self.project_info = project_info
        self.node_factory = node_factory
        self.document = document
        self.env = env
        self.target_handler = target_handler
        self.domain_helpers = helpers

    def create_null_domain_handler(self):

        return NullDomainHandler()

    def create_domain_handler(self, file_):

        domains_handlers = {
            "c": CDomainHandler,
            "cpp": CppDomainHandler,
            }

        domain = self.project_info.domain_for_file(file_)

        helper = self.domain_helpers.get(domain, NullDomainHelper())

        DomainHandler = domains_handlers.get(domain, NullDomainHandler)

        return DomainHandler(self.node_factory, self.document, self.env, helper,
                             self.project_info, self.target_handler)


class NullDomainHandlerFactory(object):

    def create_null_domain_handler(self):

        return NullDomainHandler()

    def create_domain_handler(self, file_):

        return NullDomainHandler()


class DomainHandlerFactoryCreator(object):

    def __init__(self, node_factory, helpers):

        self.node_factory = node_factory
        self.helpers = helpers

    def create_domain_handler_factory(self, project_info, document, env, options, target_handler):

        if "no-link" in options:
            return NullDomainHandlerFactory()

        return DomainHandlerFactory(
            project_info,
            self.node_factory,
            document,
            env,
            target_handler,
            self.helpers
            )

