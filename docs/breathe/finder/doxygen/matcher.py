
class MissingLevelError(Exception):
    pass


class Matcher(object):
    pass


class ItemMatcher(Matcher):

    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

    def match(self, data_object):
        return self.name == data_object.name and self.type_ == data_object.kind

    def __repr__(self):
        return "<ItemMatcher - name:%s, type_:%s>" % (self.name, self.type_)


class NameMatcher(Matcher):

    def __init__(self, name):
        self.name = name

    def match(self, data_object):
        return self.name == data_object.name


class RefMatcher(Matcher):

    def __init__(self, refid):

        self.refid = refid

    def match(self, data_object):
        return self.refid == data_object.refid


class AnyMatcher(Matcher):

    def match(self, data_object):
        return True


class MatcherStack(object):

    def __init__(self, matchers, lowest_level):

        self.matchers = matchers
        self.lowest_level = lowest_level

    def match(self, level, data_object):

        try:
            return self.matchers[level].match(data_object)
        except KeyError:
            return False

    def full_match(self, level, data_object):

        try:
            return self.matchers[level].match(data_object) and level == self.lowest_level
        except KeyError:
            raise MissingLevelError(level)

    def __repr__(self):
        return '<MatcherStack matchers="%s">' % self.matchers


class ItemMatcherFactory(Matcher):

    def create_name_type_matcher(self, name, type_):

        return ItemMatcher(name, type_)

    def create_name_matcher(self, name):

        return NameMatcher(name) if name else AnyMatcher()

    def create_ref_matcher(self, ref):

        return RefMatcher(ref)

    def create_matcher_stack(self, matchers, lowest_level):

        return MatcherStack(matchers, lowest_level)

    def create_ref_matcher_stack(self, class_, ref):

        matchers = {
            "compound": ItemMatcher(class_, "class") if class_ else AnyMatcher(),
            "member": RefMatcher(ref),
            }

        return MatcherStack(matchers, "member")

