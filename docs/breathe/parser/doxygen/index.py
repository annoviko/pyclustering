#!/usr/bin/env python

"""
Generated Mon Feb  9 19:08:05 2009 by generateDS.py.
"""

from xml.dom import minidom
from xml.parsers.expat import ExpatError


from . import indexsuper as supermod

class DoxygenTypeSub(supermod.DoxygenType):

    node_type = "doxygen"

    def __init__(self, version=None, compound=None):
        supermod.DoxygenType.__init__(self, version, compound)
supermod.DoxygenType.subclass = DoxygenTypeSub
# end class DoxygenTypeSub


class CompoundTypeSub(supermod.CompoundType):
    
    node_type = "compound"

    def __init__(self, kind=None, refid=None, name='', member=None):
        supermod.CompoundType.__init__(self, kind, refid, name, member)
supermod.CompoundType.subclass = CompoundTypeSub
# end class CompoundTypeSub


class MemberTypeSub(supermod.MemberType):

    node_type = "member"

    def __init__(self, kind=None, refid=None, name=''):
        supermod.MemberType.__init__(self, kind, refid, name)
supermod.MemberType.subclass = MemberTypeSub
# end class MemberTypeSub


class ParseError(Exception):
    pass

class FileIOError(Exception):
    pass

def parse(inFilename):

    try:
        doc = minidom.parse(inFilename)
    except IOError as e:
        raise FileIOError(e)
    except ExpatError as e:
        raise ParseError(e)

    rootNode = doc.documentElement
    rootObj = supermod.DoxygenType.factory()
    rootObj.build(rootNode)

    return rootObj

