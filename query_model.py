# query model
from collections import OrderedDict, defaultdict
import os, math
from toolz.curried import *

from preprocess import sent_preprocess
from index_build import merge_blocks

import json

from copy import copy



def _and(p1:dict, p2:dict):
    p1, p2 = set(p1.keys()), set(p2.keys())
    return p1.intersection(p2)


def _or(p1:dict, p2:dict):
    p1, p2 = set(p1.keys()), set(p2.keys())
    return p1.union(p2)


def _not_in_later(p1:dict, p2:dict):
    p1, p2 = set(p1.keys()), set(p2.keys())
    return p1.difference(p2)


def boolean_query(query: str, inverted_index: OrderedDict):
    # X or Y
    # X and Y
    # X and ~Y - X가 있고, Y가 없는,
    # X or ~Y  - X가 있거나, Y가 없는 그냥 X postings list 반환

    make_term = compose(first, sent_preprocess)
    # separate query
    tokens = query.split(' ')
    term1 = make_term(first(tokens))
    term2 = make_term(last(tokens))
    try:
        p1 = inverted_index[term1]
        p2 = inverted_index[term2]
    except KeyError as e:
        print(e)
        return []

    if 'and not' in query.lower():
        return _not_in_later(p1, p2)
    elif 'or not' in query.lower():
        return sorted(p1.keys())
    elif 'and' in query.lower():
        return _and(p1, p2)
    elif 'or' in query.lower():
        return _or(p1, p2)
    else:
        raise Exception(f'{query} is not valid query. only [and not, or not, and, or] operations are allowed')

# return tf-idf for a term
def tf_idf(term, docid, inverted_index):
    # log(1 + tf_td) * log_10(N/df_t)
    tf_td = inverted_index[term][docid]
    df_t = len(inverted_index[term])
    N = len(os.listdir('stories'))
    return math.log(1 + tf_td) * (math.log(N / df_t) / math.log(10))

# for w_tq. 쿼리에 대한 score는 그 쿼리의 텀들이 가지고 있는 postings list의 document의 합으로 한다.
def query_score(term, inverted_index):
    score = 0
    pl = inverted_index[term] # postings list for a each term
    for docid, tf_t in pl.items():
        score += tf_idf(term, docid, inverted_index)

    return score
# global score calculation
def calc_doc_score_of_query(query_terms:list, doc_package, inverted_index):
    scores = defaultdict(int)
    for term, doc_list in zip(query_terms, doc_package):
        for docid in doc_list:
            w_tq = query_score(term, inverted_index)
            w_td = tf_idf(term, docid, inverted_index)
            scores[docid] += w_td * w_tq

    # divide length for normalization
    lengths = valmap(lambda val: math.sqrt(val), scores)
    scores = [(docid, val / lengths[docid]) for docid, val in scores.items()]
    return scores

# term at a time - 모든 query term의 postings 에 대한 tf_idf를 계산
def _taad(query_terms: list, inverted_index):
    doc_package = [inverted_index[term].keys() for term in query_terms]
    return calc_doc_score_of_query(query_terms, doc_package, inverted_index)


# doc at a time - 모든 query term을 가지고 있는 document만 tf_idf 계산
def _daat(query_terms: list, inverted_index):
    pl = set(inverted_index[first(query_terms)].keys())
    for term in query_terms[1:]:
        pl = pl.intersection(set(inverted_index[term].keys()))
    if len(pl):
        doc_package = [list(pl) for _ in range(len(query_terms))]
        return calc_doc_score_of_query(query_terms, doc_package, inverted_index)
    else:
        query = ' '.join(query_terms)
        print(f'No document found from \'{query}\'')
        return []

# tf-idf base ranked_retrival
def ranked_retrieval(query, inverted_index, method='taat', n=3):
    # process query
    query_terms = list(sent_preprocess(query))

    # retrieve top k
    if method == 'taat':
        scores = _taad(query_terms, inverted_index)
    elif method == 'daat':
        scores = _daat(query_terms, inverted_index)
    else:
        raise Exception(f'method must be in [taat, daat] not {method}')

    return topk(n, scores, key=lambda x: x[1])

def return_filename(doc_list):
    dirlist = os.listdir('stories')
    for docid in doc_list:
        yield dirlist[int(docid)]

# for test
if __name__ == '__main__':
    inverted_index_fn = 'inverted_index.json'
    if not os.path.exists(inverted_index_fn):
        dirlist = os.listdir("stories")
        # for test
        inverted_index = merge_blocks(dirlist)

        # save inverted_index dictionary for query selection and fast load
        with open(inverted_index_fn, 'w') as fw:
            fw.write(json.dumps(inverted_index, indent=1))
    else:
        with open(inverted_index_fn, 'r') as fr:
            inverted_index = json.load(fr)

    # print(inverted_index)

    # boolean query test
    # and

    # print(list(return_filename(boolean_query("access and accustom", inverted_index))))
    # or

    # print(list(return_filename(boolean_query("access or accustom", inverted_index))))

    # and not
    # print(list(return_filename(boolean_query("access and not accustom", inverted_index))))


    # taat ranked retrieval test
    query = 'sre game play'

    top5 = dict(ranked_retrieval(query, inverted_index, method='daat', n=5))
    print(list(return_filename(top5.keys())))








