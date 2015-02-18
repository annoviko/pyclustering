
class TargetHandler(object):

    def __init__(self, project_info, node_factory, document):

        self.project_info = project_info
        self.node_factory = node_factory
        self.document = document

    def create_target(self, id_):
        """Creates a target node and registers it with the document and returns it in a list"""

        target = self.node_factory.target(ids=[id_], names=[id_])

        try:
            self.document.note_explicit_target(target)
        except Exception:
            # TODO: We should really return a docutils warning node here
            print("Warning: Duplicate target detected: %s" % id_)

        return [target]

class NullTargetHandler(object):

    def create_target(self, refid):
        return []

class TargetHandlerFactory(object):

    def __init__(self, node_factory):

        self.node_factory = node_factory

    def create_target_handler(self, options, project_info, document):

        if options.has_key("no-link"):
            return NullTargetHandler()

        return TargetHandler(project_info, self.node_factory, document)

