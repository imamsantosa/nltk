# Natural Language Toolkit: IEER Corpus Reader
#
# Copyright (C) 2001-2007 University of Pennsylvania
# Author: Steven Bird <sb@csse.unimelb.edu.au>
#         Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://nltk.sf.net>
# For license information, see LICENSE.TXT

"""
Corpus reader for the Information Extraction and Entity Recognition Corpus.

NIST 1999 Information Extraction: Entity Recognition Evaluation
http://www.itl.nist.gov/iad/894.01/tests/ie-er/er_99/er_99.htm

This corpus contains the NEWSWIRE development test data for the
NIST 1999 IE-ER Evaluation.  The files were taken from the
subdirectory: /ie_er_99/english/devtest/newswire/*.ref.nwt
and filenames were shortened.

The corpus contains the following files: APW_19980314, APW_19980424,
APW_19980429, NYT_19980315, NYT_19980403, and NYT_19980407.
"""

from util import *
from nltk import chunk, extract
from nltk.etree import ElementTree as ET
import os

#: A dictionary whose keys are the names of documents in this corpus;
#: and whose values are descriptions of those documents' contents.
documents = {
    'APW_19980314': 'Associated Press Weekly, 14 March 1998',
    'APW_19980424': 'Associated Press Weekly, 24 April 1998',
    'APW_19980429': 'Associated Press Weekly, 29 April 1998',
    'NYT_19980315': 'New York Times, 15 March 1998',
    'NYT_19980403': 'New York Times, 3 April 1998',
    'NYT_19980407': 'New York Times, 7 April 1998',
    }

#: A list of all documents in this corpus.
items = list(documents)

def read_document(name, format='parsed'):
    filename = find_corpus_file('ieer', name)
    if format == 'parsed':
        docs = StreamBackedCorpusView(filename, read_parsed_ieer_block)
    elif format == 'docs':
        return StreamBackedCorpusView(filename, read_ieer_block)
    elif format == 'raw':
        return open(filename).read()
    else:
        raise ValueError('Expected format to be "parsed" or "raw"')

def read_parsed_ieer_block(stream):
    return [chunk.ieerstr2tree(read_ieer_block(stream))]
    
def read_ieer_block(stream):
    out = []
    # Skip any preamble.
    for line in stream:
        if line.strip() == '<DOC>': break
    # Read the document
    out.append(line)
    for line in stream:
        out.append(line)
        if line.strip() == '</DOC>': break
    # Return the document
    return ['\n'.join(out)]

######################################################################
#{ Convenience Functions
######################################################################
read = read_document

def raw(name):
    return read_document(name, format='raw')

def parsed(name):
    return read_document(name, format='parsed')

def docs(name):
    return read_document(name, format='docs')

######################################################################
#{ Demo
######################################################################
def demo():
    from nltk.corpus import ieer
    from pprint import pprint

    print '%r ... %r' % (ieer.read('NYT_19980407', format='raw')[3][:30],
                         ieer.read('NYT_19980407', format='raw')[3][-30:])
    pprint(ieer.read('NYT_19980407', format='parsed')[3])

if __name__ == '__main__':
    demo()

