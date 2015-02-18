#!/usr/bin/env python

"""
Generated Mon Feb  9 19:08:05 2009 by generateDS.py.
"""

from xml.dom import minidom
from xml.dom import Node
from xml.parsers.expat import ExpatError

from . import compoundsuper as supermod
from .compoundsuper import MixedContainer


class DoxygenTypeSub(supermod.DoxygenType):

    node_type = "doxygendef"

    def __init__(self, version=None, compounddef=None):
        supermod.DoxygenType.__init__(self, version, compounddef)
supermod.DoxygenType.subclass = DoxygenTypeSub
# end class DoxygenTypeSub


class compounddefTypeSub(supermod.compounddefType):

    node_type = "compounddef"

    def __init__(self, kind=None, prot=None, id=None, compoundname='', title='',
                 basecompoundref=None, derivedcompoundref=None, includes=None, includedby=None,
                 incdepgraph=None, invincdepgraph=None, innerdir=None, innerfile=None,
                 innerclass=None, innernamespace=None, innerpage=None, innergroup=None,
                 templateparamlist=None, sectiondef=None, briefdescription=None,
                 detaileddescription=None, inheritancegraph=None, collaborationgraph=None,
                 programlisting=None, location=None, listofallmembers=None):

        supermod.compounddefType.__init__(self, kind, prot, id, compoundname, title,
                                          basecompoundref, derivedcompoundref, includes, includedby,
                                          incdepgraph, invincdepgraph, innerdir, innerfile,
                                          innerclass, innernamespace, innerpage, innergroup,
                                          templateparamlist, sectiondef, briefdescription,
                                          detaileddescription, inheritancegraph, collaborationgraph,
                                          programlisting, location, listofallmembers)

supermod.compounddefType.subclass = compounddefTypeSub
# end class compounddefTypeSub


class listofallmembersTypeSub(supermod.listofallmembersType):

    node_type = "listofallmembers"

    def __init__(self, member=None):
        supermod.listofallmembersType.__init__(self, member)
supermod.listofallmembersType.subclass = listofallmembersTypeSub
# end class listofallmembersTypeSub


class memberRefTypeSub(supermod.memberRefType):

    node_type = "memberref"

    def __init__(self, virt=None, prot=None, refid=None, ambiguityscope=None, scope='', name=''):
        supermod.memberRefType.__init__(self, virt, prot, refid, ambiguityscope, scope, name)
supermod.memberRefType.subclass = memberRefTypeSub
# end class memberRefTypeSub


class compoundRefTypeSub(supermod.compoundRefType):

    node_type = "compoundref"

    def __init__(self, virt=None, prot=None, refid=None, valueOf_='', mixedclass_=None,
                 content_=None):
        supermod.compoundRefType.__init__(self, mixedclass_, content_)
supermod.compoundRefType.subclass = compoundRefTypeSub
# end class compoundRefTypeSub


class reimplementTypeSub(supermod.reimplementType):

    node_type = "reimplement"

    def __init__(self, refid=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.reimplementType.__init__(self, mixedclass_, content_)
supermod.reimplementType.subclass = reimplementTypeSub
# end class reimplementTypeSub


class incTypeSub(supermod.incType):

    node_type = "inc"

    def __init__(self, local=None, refid=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.incType.__init__(self, mixedclass_, content_)
supermod.incType.subclass = incTypeSub
# end class incTypeSub


class refTypeSub(supermod.refType):

    node_type = "ref"

    def __init__(self, node_name, prot=None, refid=None, valueOf_='', mixedclass_=None,
                 content_=None):
        supermod.refType.__init__(self, mixedclass_, content_)

        self.node_name = node_name

supermod.refType.subclass = refTypeSub


class refTextTypeSub(supermod.refTextType):

    node_type = "reftex"

    def __init__(self, refid=None, kindref=None, external=None, valueOf_='', mixedclass_=None,
                 content_=None):
        supermod.refTextType.__init__(self, mixedclass_, content_)

supermod.refTextType.subclass = refTextTypeSub
# end class refTextTypeSub


class sectiondefTypeSub(supermod.sectiondefType):

    node_type = "sectiondef"

    def __init__(self, kind=None, header='', description=None, memberdef=None):
        supermod.sectiondefType.__init__(self, kind, header, description, memberdef)

supermod.sectiondefType.subclass = sectiondefTypeSub
# end class sectiondefTypeSub


class memberdefTypeSub(supermod.memberdefType):

    node_type = "memberdef"

    def __init__(self, initonly=None, kind=None, volatile=None, const=None, raise_=None, virt=None,
                 readable=None, prot=None, explicit=None, new=None, final=None, writable=None,
                 add=None, static=None, remove=None, sealed=None, mutable=None, gettable=None,
                 inline=None, settable=None, id=None, templateparamlist=None, type_=None,
                 definition='', argsstring='', name='', read='', write='', bitfield='',
                 reimplements=None, reimplementedby=None, param=None, enumvalue=None,
                 initializer=None, exceptions=None, briefdescription=None, detaileddescription=None,
                 inbodydescription=None, location=None, references=None, referencedby=None):

        supermod.memberdefType.__init__(self, initonly, kind, volatile, const, raise_, virt,
                                        readable, prot, explicit, new, final, writable, add, static,
                                        remove, sealed, mutable, gettable, inline, settable, id,
                                        templateparamlist, type_, definition, argsstring, name,
                                        read, write, bitfield, reimplements, reimplementedby, param,
                                        enumvalue, initializer, exceptions, briefdescription,
                                        detaileddescription, inbodydescription, location,
                                        references, referencedby)

        self.parameterlist = supermod.docParamListType.factory()
        self.parameterlist.kind = "param"

    def buildChildren(self, child_, nodeName_):
        supermod.memberdefType.buildChildren(self, child_, nodeName_)

        if child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'param':

            # Get latest param
            param = self.param[-1]

            # If it doesn't have a description we're done
            if not param.briefdescription:
                return

            # Construct our own param list from the descriptions stored inline
            # with the parameters
            paramdescription = param.briefdescription
            paramname = supermod.docParamName.factory()

            # Add parameter name
            obj_ = paramname.mixedclass_(MixedContainer.CategoryText, MixedContainer.TypeNone, '',
                                         param.declname)
            paramname.content_.append(obj_)

            paramnamelist = supermod.docParamNameList.factory()
            paramnamelist.parametername.append(paramname)

            paramlistitem = supermod.docParamListItem.factory()
            paramlistitem.parameternamelist.append(paramnamelist)

            # Add parameter description
            paramlistitem.parameterdescription = paramdescription

            self.parameterlist.parameteritem.append(paramlistitem)

        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'detaileddescription':

            if not self.parameterlist.parameteritem:
                # No items in our list
                return

            # Assume supermod.memberdefType.buildChildren has already built the
            # description object, we just want to slot our parameterlist in at
            # a reasonable point

            if not self.detaileddescription:
                # Create one if it doesn't exist
                self.detaileddescription = supermod.descriptionType.factory()

            detaileddescription = self.detaileddescription

            para = supermod.docParaType.factory()
            para.parameterlist.append(self.parameterlist)

            obj_ = detaileddescription.mixedclass_(MixedContainer.CategoryComplex,
                                                   MixedContainer.TypeNone, 'para', para)

            index = 0
            detaileddescription.content_.insert(index, obj_)


supermod.memberdefType.subclass = memberdefTypeSub
# end class memberdefTypeSub


class descriptionTypeSub(supermod.descriptionType):

    node_type = "description"

    def __init__(self, title='', para=None, sect1=None, internal=None, mixedclass_=None,
                 content_=None):
        supermod.descriptionType.__init__(self, mixedclass_, content_)

supermod.descriptionType.subclass = descriptionTypeSub
# end class descriptionTypeSub


class enumvalueTypeSub(supermod.enumvalueType):

    node_type = "enumvalue"

    def __init__(self, prot=None, id=None, name='', initializer=None, briefdescription=None,
                 detaileddescription=None, mixedclass_=None, content_=None):
        supermod.enumvalueType.__init__(self, mixedclass_, content_)

        self.initializer = None

    def buildChildren(self, child_, nodeName_):
        # Get text from <name> child and put it in self.name
        if child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'name':
            value_ = []
            for text_ in child_.childNodes:
                value_.append(text_.nodeValue)
            valuestr_ = ''.join(value_)
            self.name = valuestr_
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'briefdescription':
            obj_ = supermod.descriptionType.factory()
            obj_.build(child_)
            self.set_briefdescription(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'detaileddescription':
            obj_ = supermod.descriptionType.factory()
            obj_.build(child_)
            self.set_detaileddescription(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'initializer':
            childobj_ = supermod.linkedTextType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex, MixedContainer.TypeNone,
                                    'initializer', childobj_)
            self.set_initializer(obj_)
            self.content_.append(obj_)

supermod.enumvalueType.subclass = enumvalueTypeSub
# end class enumvalueTypeSub


class templateparamlistTypeSub(supermod.templateparamlistType):

    node_type = "templateparamlist"

    def __init__(self, param=None):
        supermod.templateparamlistType.__init__(self, param)
supermod.templateparamlistType.subclass = templateparamlistTypeSub
# end class templateparamlistTypeSub


class paramTypeSub(supermod.paramType):

    node_type = "param"

    def __init__(self, type_=None, declname='', defname='', array='', defval=None,
                 briefdescription=None):
        supermod.paramType.__init__(self, type_, declname, defname, array, defval, briefdescription)
supermod.paramType.subclass = paramTypeSub
# end class paramTypeSub


class linkedTextTypeSub(supermod.linkedTextType):

    node_type = "linkedtext"

    def __init__(self, ref=None, mixedclass_=None, content_=None):
        supermod.linkedTextType.__init__(self, mixedclass_, content_)
supermod.linkedTextType.subclass = linkedTextTypeSub
# end class linkedTextTypeSub


class graphTypeSub(supermod.graphType):

    node_type = "graph"

    def __init__(self, node=None):
        supermod.graphType.__init__(self, node)
supermod.graphType.subclass = graphTypeSub
# end class graphTypeSub


class nodeTypeSub(supermod.nodeType):

    node_type = "node"

    def __init__(self, id=None, label='', link=None, childnode=None):
        supermod.nodeType.__init__(self, id, label, link, childnode)
supermod.nodeType.subclass = nodeTypeSub
# end class nodeTypeSub


class childnodeTypeSub(supermod.childnodeType):

    node_type = "childnode"

    def __init__(self, relation=None, refid=None, edgelabel=None):
        supermod.childnodeType.__init__(self, relation, refid, edgelabel)
supermod.childnodeType.subclass = childnodeTypeSub
# end class childnodeTypeSub


class linkTypeSub(supermod.linkType):

    node_type = "link"

    def __init__(self, refid=None, external=None, valueOf_=''):
        supermod.linkType.__init__(self, refid, external)
supermod.linkType.subclass = linkTypeSub
# end class linkTypeSub


class listingTypeSub(supermod.listingType):

    node_type = "listing"

    def __init__(self, codeline=None):
        supermod.listingType.__init__(self, codeline)
supermod.listingType.subclass = listingTypeSub
# end class listingTypeSub


class codelineTypeSub(supermod.codelineType):

    node_type = "codeline"

    def __init__(self, external=None, lineno=None, refkind=None, refid=None, highlight=None):
        supermod.codelineType.__init__(self, external, lineno, refkind, refid, highlight)
supermod.codelineType.subclass = codelineTypeSub
# end class codelineTypeSub


class highlightTypeSub(supermod.highlightType):

    node_type = "highlight"

    def __init__(self, class_=None, sp=None, ref=None, mixedclass_=None, content_=None):
        supermod.highlightType.__init__(self, mixedclass_, content_)
supermod.highlightType.subclass = highlightTypeSub
# end class highlightTypeSub


class referenceTypeSub(supermod.referenceType):

    node_type = "reference"

    def __init__(self, endline=None, startline=None, refid=None, compoundref=None, valueOf_='',
                 mixedclass_=None, content_=None):
        supermod.referenceType.__init__(self, mixedclass_, content_)
supermod.referenceType.subclass = referenceTypeSub
# end class referenceTypeSub


class locationTypeSub(supermod.locationType):

    node_type = "location"

    def __init__(self, bodystart=None, line=None, bodyend=None, bodyfile=None, file=None,
                 valueOf_=''):
        supermod.locationType.__init__(self, bodystart, line, bodyend, bodyfile, file)
supermod.locationType.subclass = locationTypeSub
# end class locationTypeSub


class docSect1TypeSub(supermod.docSect1Type):

    node_type = "docsect1"

    def __init__(self, id=None, title='', para=None, sect2=None, internal=None, mixedclass_=None,
                 content_=None):
        supermod.docSect1Type.__init__(self, mixedclass_, content_)
supermod.docSect1Type.subclass = docSect1TypeSub
# end class docSect1TypeSub


class docSect2TypeSub(supermod.docSect2Type):

    node_type = "docsect2"

    def __init__(self, id=None, title='', para=None, sect3=None, internal=None, mixedclass_=None,
                 content_=None):
        supermod.docSect2Type.__init__(self, mixedclass_, content_)
supermod.docSect2Type.subclass = docSect2TypeSub
# end class docSect2TypeSub


class docSect3TypeSub(supermod.docSect3Type):

    node_type = "docsect3"

    def __init__(self, id=None, title='', para=None, sect4=None, internal=None, mixedclass_=None,
                 content_=None):
        supermod.docSect3Type.__init__(self, mixedclass_, content_)
supermod.docSect3Type.subclass = docSect3TypeSub
# end class docSect3TypeSub


class docSect4TypeSub(supermod.docSect4Type):

    node_type = "docsect4"

    def __init__(self, id=None, title='', para=None, internal=None, mixedclass_=None,
                 content_=None):
        supermod.docSect4Type.__init__(self, mixedclass_, content_)
supermod.docSect4Type.subclass = docSect4TypeSub
# end class docSect4TypeSub


class docInternalTypeSub(supermod.docInternalType):

    node_type = "docinternal"

    def __init__(self, para=None, sect1=None, mixedclass_=None, content_=None):
        supermod.docInternalType.__init__(self, mixedclass_, content_)
supermod.docInternalType.subclass = docInternalTypeSub
# end class docInternalTypeSub


class docInternalS1TypeSub(supermod.docInternalS1Type):

    node_type = "docinternals1"

    def __init__(self, para=None, sect2=None, mixedclass_=None, content_=None):
        supermod.docInternalS1Type.__init__(self, mixedclass_, content_)
supermod.docInternalS1Type.subclass = docInternalS1TypeSub
# end class docInternalS1TypeSub


class docInternalS2TypeSub(supermod.docInternalS2Type):

    node_type = "docinternals2"

    def __init__(self, para=None, sect3=None, mixedclass_=None, content_=None):
        supermod.docInternalS2Type.__init__(self, mixedclass_, content_)
supermod.docInternalS2Type.subclass = docInternalS2TypeSub
# end class docInternalS2TypeSub


class docInternalS3TypeSub(supermod.docInternalS3Type):

    node_type = "docinternals3"

    def __init__(self, para=None, sect3=None, mixedclass_=None, content_=None):
        supermod.docInternalS3Type.__init__(self, mixedclass_, content_)
supermod.docInternalS3Type.subclass = docInternalS3TypeSub
# end class docInternalS3TypeSub


class docInternalS4TypeSub(supermod.docInternalS4Type):

    node_type = "docinternals4"

    def __init__(self, para=None, mixedclass_=None, content_=None):
        supermod.docInternalS4Type.__init__(self, mixedclass_, content_)
supermod.docInternalS4Type.subclass = docInternalS4TypeSub
# end class docInternalS4TypeSub


class docURLLinkSub(supermod.docURLLink):

    node_type = "docurllink"

    def __init__(self, url=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.docURLLink.__init__(self, mixedclass_, content_)
supermod.docURLLink.subclass = docURLLinkSub
# end class docURLLinkSub


class docAnchorTypeSub(supermod.docAnchorType):

    node_type = "docanchor"

    def __init__(self, id=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.docAnchorType.__init__(self, mixedclass_, content_)
supermod.docAnchorType.subclass = docAnchorTypeSub
# end class docAnchorTypeSub


class docFormulaTypeSub(supermod.docFormulaType):

    node_type = "docformula"

    def __init__(self, id=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.docFormulaType.__init__(self, mixedclass_, content_)
supermod.docFormulaType.subclass = docFormulaTypeSub
# end class docFormulaTypeSub


class docIndexEntryTypeSub(supermod.docIndexEntryType):

    node_type = "docindexentry"

    def __init__(self, primaryie='', secondaryie=''):
        supermod.docIndexEntryType.__init__(self, primaryie, secondaryie)
supermod.docIndexEntryType.subclass = docIndexEntryTypeSub
# end class docIndexEntryTypeSub


class docListTypeSub(supermod.docListType):

    node_type = "doclist"

    def __init__(self, listitem=None, subtype=""):
        self.node_subtype = "itemized"
        if subtype is not "":
            self.node_subtype = subtype
        supermod.docListType.__init__(self, listitem)
supermod.docListType.subclass = docListTypeSub
# end class docListTypeSub


class docListItemTypeSub(supermod.docListItemType):

    node_type = "doclistitem"

    def __init__(self, para=None):
        supermod.docListItemType.__init__(self, para)
supermod.docListItemType.subclass = docListItemTypeSub
# end class docListItemTypeSub


class docSimpleSectTypeSub(supermod.docSimpleSectType):

    node_type = "docsimplesect"

    def __init__(self, kind=None, title=None, para=None):
        supermod.docSimpleSectType.__init__(self, kind, title, para)
supermod.docSimpleSectType.subclass = docSimpleSectTypeSub
# end class docSimpleSectTypeSub


class docVarListEntryTypeSub(supermod.docVarListEntryType):

    node_type = "docvarlistentry"

    def __init__(self, term=None):
        supermod.docVarListEntryType.__init__(self, term)
supermod.docVarListEntryType.subclass = docVarListEntryTypeSub
# end class docVarListEntryTypeSub


class docRefTextTypeSub(supermod.docRefTextType):

    node_type = "docreftext"

    def __init__(self, refid=None, kindref=None, external=None, valueOf_='', mixedclass_=None,
                 content_=None):
        supermod.docRefTextType.__init__(self, mixedclass_, content_)

        self.para = []

    def buildChildren(self, child_, nodeName_):
        supermod.docRefTextType.buildChildren(self, child_, nodeName_)

        if child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'para':
            obj_ = supermod.docParaType.factory()
            obj_.build(child_)
            self.para.append(obj_)

supermod.docRefTextType.subclass = docRefTextTypeSub
# end class docRefTextTypeSub


class docTableTypeSub(supermod.docTableType):

    node_type = "doctable"

    def __init__(self, rows=None, cols=None, row=None, caption=None):
        supermod.docTableType.__init__(self, rows, cols, row, caption)
supermod.docTableType.subclass = docTableTypeSub
# end class docTableTypeSub


class docRowTypeSub(supermod.docRowType):

    node_type = "docrow"

    def __init__(self, entry=None):
        supermod.docRowType.__init__(self, entry)
supermod.docRowType.subclass = docRowTypeSub
# end class docRowTypeSub


class docEntryTypeSub(supermod.docEntryType):

    node_type = "docentry"

    def __init__(self, thead=None, para=None):
        supermod.docEntryType.__init__(self, thead, para)
supermod.docEntryType.subclass = docEntryTypeSub
# end class docEntryTypeSub


class docHeadingTypeSub(supermod.docHeadingType):

    node_type = "docheading"

    def __init__(self, level=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.docHeadingType.__init__(self, mixedclass_, content_)

    def buildChildren(self, child_, nodeName_):
        supermod.docHeadingType.buildChildren(self, child_, nodeName_)

        # Account for styled content in the heading. This might need to be expanded to include other
        # nodes as it seems from the xsd that headings can have a lot of different children but we
        # really don't expect most of them to come up.
        if child_.nodeType == Node.ELEMENT_NODE and (
                nodeName_ == 'bold' or
                nodeName_ == 'emphasis' or
                nodeName_ == 'computeroutput' or
                nodeName_ == 'subscript' or
                nodeName_ == 'superscript' or
                nodeName_ == 'center' or
                nodeName_ == 'small'):
            obj_ = supermod.docMarkupType.factory()
            obj_.build(child_)
            obj_.type_ = nodeName_
            self.content_.append(obj_)

supermod.docHeadingType.subclass = docHeadingTypeSub
# end class docHeadingTypeSub


class docImageTypeSub(supermod.docImageType):

    node_type = "docimage"

    def __init__(self, width=None, type_=None, name=None, height=None, valueOf_='',
                 mixedclass_=None, content_=None):
        supermod.docImageType.__init__(self, mixedclass_, content_)
supermod.docImageType.subclass = docImageTypeSub
# end class docImageTypeSub


class docDotFileTypeSub(supermod.docDotFileType):

    node_type = "docdocfile"

    def __init__(self, name=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.docDotFileType.__init__(self, mixedclass_, content_)
supermod.docDotFileType.subclass = docDotFileTypeSub
# end class docDotFileTypeSub


class docTocItemTypeSub(supermod.docTocItemType):

    node_type = "doctocitem"

    def __init__(self, id=None, valueOf_='', mixedclass_=None, content_=None):
        supermod.docTocItemType.__init__(self, mixedclass_, content_)
supermod.docTocItemType.subclass = docTocItemTypeSub
# end class docTocItemTypeSub


class docTocListTypeSub(supermod.docTocListType):

    node_type = "doctoclist"

    def __init__(self, tocitem=None):
        supermod.docTocListType.__init__(self, tocitem)
supermod.docTocListType.subclass = docTocListTypeSub
# end class docTocListTypeSub


class docLanguageTypeSub(supermod.docLanguageType):

    node_type = "doclanguage"

    def __init__(self, langid=None, para=None):
        supermod.docLanguageType.__init__(self, langid, para)
supermod.docLanguageType.subclass = docLanguageTypeSub
# end class docLanguageTypeSub


class docParamListTypeSub(supermod.docParamListType):

    node_type = "docparamlist"

    def __init__(self, kind=None, parameteritem=None):
        supermod.docParamListType.__init__(self, kind, parameteritem)
supermod.docParamListType.subclass = docParamListTypeSub
# end class docParamListTypeSub


class docParamListItemSub(supermod.docParamListItem):

    node_type = "docparamlistitem"

    def __init__(self, parameternamelist=None, parameterdescription=None):
        supermod.docParamListItem.__init__(self, parameternamelist, parameterdescription)
supermod.docParamListItem.subclass = docParamListItemSub
# end class docParamListItemSub


class docParamNameListSub(supermod.docParamNameList):

    node_type = "docparamnamelist"

    def __init__(self, parametername=None):
        supermod.docParamNameList.__init__(self, parametername)
supermod.docParamNameList.subclass = docParamNameListSub
# end class docParamNameListSub


class docParamNameSub(supermod.docParamName):

    node_type = "docparamname"

    def __init__(self, direction=None, ref=None, mixedclass_=None, content_=None):
        supermod.docParamName.__init__(self, mixedclass_, content_)
supermod.docParamName.subclass = docParamNameSub
# end class docParamNameSub


class docXRefSectTypeSub(supermod.docXRefSectType):

    node_type = "docxrefsect"

    def __init__(self, id=None, xreftitle=None, xrefdescription=None):
        supermod.docXRefSectType.__init__(self, id, xreftitle, xrefdescription)
supermod.docXRefSectType.subclass = docXRefSectTypeSub
# end class docXRefSectTypeSub


class docCopyTypeSub(supermod.docCopyType):

    node_type = "doccopy"

    def __init__(self, link=None, para=None, sect1=None, internal=None):
        supermod.docCopyType.__init__(self, link, para, sect1, internal)
supermod.docCopyType.subclass = docCopyTypeSub
# end class docCopyTypeSub


class docCharTypeSub(supermod.docCharType):

    node_type = "docchar"

    def __init__(self, char=None, valueOf_=''):
        supermod.docCharType.__init__(self, char)
supermod.docCharType.subclass = docCharTypeSub
# end class docCharTypeSub


class verbatimTypeSub(object):
    """
    New node type. Structure is largely pillaged from other nodes in order to
    match the set.
    """

    node_type = "verbatim"

    def __init__(self, valueOf_='', mixedclass_=None, content_=None):
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.text = ""

    def factory(*args, **kwargs):
        return verbatimTypeSub(*args, **kwargs)

    factory = staticmethod(factory)

    def buildAttributes(self, attrs):
        pass

    def build(self, node_):
        attrs = node_.attributes
        self.buildAttributes(attrs)
        self.valueOf_ = ''
        for child_ in node_.childNodes:
            nodeName_ = child_.nodeName.split(':')[-1]
            self.buildChildren(child_, nodeName_)

    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            self.text += child_.nodeValue


class docParaTypeSub(supermod.docParaType):

    node_type = "docpara"

    def __init__(self, char=None, valueOf_=''):
        supermod.docParaType.__init__(self, char)

        self.parameterlist = []
        self.simplesects = []
        self.content = []
        self.programlisting = []
        self.images = []

    def buildChildren(self, child_, nodeName_):
        supermod.docParaType.buildChildren(self, child_, nodeName_)

        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                                    MixedContainer.TypeNone, '', child_.nodeValue)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "ref":
            obj_ = supermod.docRefTextType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'parameterlist':
            obj_ = supermod.docParamListType.factory()
            obj_.build(child_)
            self.parameterlist.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'simplesect':
            obj_ = supermod.docSimpleSectType.factory()
            obj_.build(child_)
            self.simplesects.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'programlisting':
            obj_ = supermod.listingType.factory()
            obj_.build(child_)
            self.programlisting.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'image':
            obj_ = supermod.docImageType.factory()
            obj_.build(child_)
            self.images.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and (
                nodeName_ == 'bold' or
                nodeName_ == 'emphasis' or
                nodeName_ == 'computeroutput' or
                nodeName_ == 'subscript' or
                nodeName_ == 'superscript' or
                nodeName_ == 'center' or
                nodeName_ == 'small'):
            obj_ = supermod.docMarkupType.factory()
            obj_.build(child_)
            obj_.type_ = nodeName_
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'verbatim':
            childobj_ = verbatimTypeSub.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex, MixedContainer.TypeNone,
                                    'verbatim', childobj_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'formula':
            childobj_ = docFormulaTypeSub.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex, MixedContainer.TypeNone,
                                    'formula', childobj_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "itemizedlist":
            obj_ = supermod.docListType.factory(subtype="itemized")
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == "orderedlist":
            obj_ = supermod.docListType.factory(subtype="ordered")
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'heading':
            obj_ = supermod.docHeadingType.factory()
            obj_.build(child_)
            self.content.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'ulink':
            obj_ = supermod.docURLLink.factory()
            obj_.build(child_)
            self.content.append(obj_)

supermod.docParaType.subclass = docParaTypeSub
# end class docParaTypeSub


class docMarkupTypeSub(supermod.docMarkupType):

    node_type = "docmarkup"

    def __init__(self, valueOf_='', mixedclass_=None, content_=None):
        supermod.docMarkupType.__init__(self, valueOf_, mixedclass_, content_)
        self.type_ = None

    def buildChildren(self, child_, nodeName_):
        if child_.nodeType == Node.TEXT_NODE:
            obj_ = self.mixedclass_(MixedContainer.CategoryText, MixedContainer.TypeNone, '',
                                    child_.nodeValue)
            self.content_.append(obj_)
        elif child_.nodeType == Node.ELEMENT_NODE and nodeName_ == 'ref':
            childobj_ = supermod.docRefTextType.factory()
            childobj_.build(child_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex, MixedContainer.TypeNone, 'ref',
                                    childobj_)
            self.content_.append(obj_)
        if child_.nodeType == Node.TEXT_NODE:
            self.valueOf_ += child_.nodeValue
        elif child_.nodeType == Node.CDATA_SECTION_NODE:
            self.valueOf_ += '![CDATA[' + child_.nodeValue + ']]'

supermod.docMarkupType.subclass = docMarkupTypeSub
# end class docMarkupTypeSub


class docTitleTypeSub(supermod.docTitleType):

    node_type = "doctitle"

    def __init__(self, valueOf_='', mixedclass_=None, content_=None):
        supermod.docTitleType.__init__(self, valueOf_, mixedclass_, content_)
        self.type_ = None

supermod.docTitleType.subclass = docTitleTypeSub
# end class docTitleTypeSub


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


