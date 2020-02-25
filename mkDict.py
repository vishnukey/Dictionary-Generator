#!/usr/bin/env python

import sys
import os
from glob import glob

DEBUG = False

def debug(msg):
    if DEBUG:
        print("[INFO] ", msg)

EXTS = {
        "definition" : "def",
        "template" : "template"
        }

DEF_PATH = "Definitions"
TEMPLATE_PATH = "Templates"

def getDefs(root = DEF_PATH, ext = EXTS['definition']):
    definitions = []
    for fname in glob(os.path.join(root, "*.%s" % ext)):
        with open(fname, 'r') as f:
            data = list(map(lambda s: s.replace("\n", ''), f))
            title = data[0:1][0]
            body = "".join(data[2:])
            definitions.append((title, body, fname))
    definitions.sort(key = lambda x: x[0])
    return definitions


def getTemplate(fname, root = TEMPLATE_PATH, ext = EXTS['template']):
    with open(os.path.join(root, "%s.%s" % (fname, ext)), 'r') as f:
        return f.read()

def substitue(template):
    def inner(definition):
        title, body, _ = definition
        return template.format(term=title, defintion=body)
    return inner

def build(defintions):
    return "\n".join(defintions)

def genDict(body, template):
    return template.format(defs=body)

def mkDict(body, oname):
    with open(oname, 'w') as f:
        f.write(body)
ofile = "Dictionary.md"
if len(sys.argv) >= 2:
    ofile = sys.argv[1]
print("Generating %s..." % ofile)
defs = getDefs()
defTemplate = getTemplate('definition')
dictTemplate = getTemplate('dictionary')
dictionary = build(map(substitue(defTemplate), defs))
mkDict(genDict(dictionary, dictTemplate), ofile)
print("Done")


