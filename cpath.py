#!/usr/bin/env python

import clang.cindex as ci
import libxml2 as xml
from xml.dom import minidom

class XmlWriter:
    def __init__(self, filename):
        self._filename = filename
        self._xml = None
        self._index = ci.Index.create()
        self._translation_unit = self._index.parse(filename)
        self._loop_guard = []
    def _add_type_info(self, parent, type, line_number):
        elem = xml.newNode("type")
        elem.newProp("line_number", str(line_number))
        parent.addChild(elem)
        canonical_type = type.get_canonical()
        elem.newProp("canonical_kind", canonical_type.kind.name)
        elem.newProp("kind", type.kind.name)
        decl_name = canonical_type.get_declaration().displayname
        if decl_name:
            elem.newProp("declaration", decl_name)

        qualifiers = []
        if type.is_const_qualified():
            qualifiers.append("const")
        if type.is_restrict_qualified():
            qualifiers.append("restrict")
        if type.is_volatile_qualified():
            qualifiers.append("volatile")
        if len(qualifiers) > 0:
            elem.newProp("qualifiers", str(qualifiers))
        if canonical_type.kind == ci.TypeKind.POINTER:
            self._add_type_info(elem, canonical_type.get_pointee(), line_number)
        if canonical_type.kind in [ci.TypeKind.FUNCTIONPROTO, ci.TypeKind.FUNCTIONNOPROTO]:
            result = xml.newNode("result")
            elem.addChild(result)
            self._add_type_info(result, type.get_result(), line_number)
        #if canonical_type.kind == ci.TypeKind.RECORD:
        #    decl = canonical_type.get_declaration()
        #    decl_node = xml.newNode("declaration")
        #    elem.addChild(decl_node)
        #    self._create_xml(decl_node, decl)
        #    #for c in decl.get_children():
        #    #    print "---"
        #    #    self._create_xml(decl_node, c)
        #    self._add_type_info(elem, type.get_declaration().type)
    def _add_token(self, parent, token):
        elem = xml.newNode("token")
        parent.addChild(elem)
        elem.setProp("spelling", token.spelling)
    def _create_node(self, node):
        elem = xml.newNode(node.kind.name)
        elem.newProp("line_number", str(node.location.line))
        if node.type.kind != ci.TypeKind.INVALID:
            self._add_type_info(elem, node.type, node.location.line)
        if node.displayname != "":
            elem.newProp("displayname", node.displayname)
        for token in node.get_tokens():
            self._add_token(elem, token)
        #elem.newProp("spelling", node.spelling)
        return elem
    def _create_xml(self, parent, node):
        elem = self._create_node(node)
        parent.addChild(elem)
        for c in node.get_children():
            self._create_xml(elem, c)
    @property
    def xml(self):
        if self._xml == None:
            self._xml = xml.newDoc("")
            elem = xml.newNode("file")
            elem.newProp("filename", self._translation_unit.spelling)
            self._xml.addChild(elem)
            self._create_xml(elem, self._translation_unit.cursor)
        return self._xml

def main():
    import argparse
    parser = argparse.ArgumentParser(description="xpath search for c/c++ code")
    parser.add_argument('files', metavar='file', nargs='+', help='c/c++ files to parse')
    parser.add_argument("-x", "--xpath", type=str, help="xpath query")
    args = parser.parse_args()

    for filename in args.files:
        xml_writer = XmlWriter(filename)
        if args.xpath is None:
            print minidom.parseString(xml_writer.xml.serialize()).toprettyxml()
        else:
            res = xml_writer.xml.xpathEval(args.xpath)
            if res is not None and len(res) > 0:
                print "filename: {}".format(filename)
                for node in res:
                    print minidom.parseString(str(node)).toprettyxml()

if __name__ == '__main__':
  main()
