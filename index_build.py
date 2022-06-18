from collections import defaultdict, OrderedDict
import os
from toolz.curried import *

from preprocess import load_data, sent_preprocess



"""
todo: construct inverted index by spimi algorithm.
"""
# inverted index construction by spimi algorithm
def _spimi(fn: str, docid: int):
    # dictionary
    dictionary = defaultdict(dict)
    # automatically docid is sorted
    doc = load_data(fn)
    for term in sent_preprocess(doc):
        if docid not in dictionary[term]:
            dictionary[term][docid] = 1
        else:
            dictionary[term][docid] += 1
    # sort dictionary
    dictionary = OrderedDict(sorted(dictionary.items()))

    return dictionary

def merge_blocks(doc_fns: list):
    blocks = [_spimi(fn, docid) for docid, fn in zip(range(len(doc_fns)), doc_fns)]
    # merge blocks
    total_block = defaultdict(dict)
    for block in blocks:
        for term, postings_dict in block.items():
            total_block[term].update(postings_dict)

    return total_block


if __name__ == "__main__":
    dirlist = os.listdir("stories")
    # for test
    inverted_index = merge_blocks(dirlist)

    print(inverted_index)
