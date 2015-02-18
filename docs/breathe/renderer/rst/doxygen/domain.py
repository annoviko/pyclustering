

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

    def create_class_id(self, data_object):

        def_ = data_object.name

        parser = self.helper.definition_parser(def_)
        sigobj = parser.parse_class()

        return sigobj.get_id()

    def create_class_target(self, data_object):

        id_ = self.create_class_id(data_object)
        name = data_object.name

        return self._create_target(name, "class", id_)

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

