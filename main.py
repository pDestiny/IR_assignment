# main

# 1. calculate statistics of index


"""
2. querying
    * X or Y
    * X and Y
    * X and not Y
    * X or not Y
"""

# 3. implement ranked retrieval using tf-idf scoring that supports free text queries.
import os, json

from index_build import merge_blocks
from query_model import ranked_retrieval, boolean_query, return_filename
# from chardet.universaldetector import UniversalDetector
# from pathlib import Path
# import codecs


"""
#### info #####

stories/archive
stories/imonly17.txt
stories/snow.txt
stories/write

files are removed from docs collection

"""
if __name__ == '__main__':
    # below code was used for encoding files to utf-8
    # dirlist = os.listdir('stories')
    # base_dir = 'stories'
    # for fn in dirlist:
    #     try:
    #         file_path = os.path.join(base_dir, fn)
    #         detector = UniversalDetector()
    #         filesize = os.path.getsize(file_path)
    #         with Path(file_path).open('rb') as f:
    #             detector.feed(f.read())
    #         detector.close()
    #         encoding = detector.result['encoding']
    #
    #         # convert to utf-8
    #         with codecs.open(file_path, "r", encoding=encoding) as source_file:
    #             contents = source_file.read(filesize)
    #             with codecs.open(file_path, "w", "utf-8") as target_file:
    #                 target_file.write(contents)
    #     except Exception as e:
    #         print(f'{file_path}')
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
    print('==========and query for \'access and accustom\'============')
    print(list(return_filename(boolean_query("access and accustom", inverted_index))), end='\n')

    # or
    print('==========or query for \'access or accustom\'============')
    print(list(return_filename(boolean_query("access or accustom", inverted_index))), end='\n')

    # and not
    print('==========and not query for \'access and not accustom\'============')
    print(list(return_filename(boolean_query("access and not accustom", inverted_index))), end='\n')

    # or not
    print('==========or not query for \'access or not accustom\'============')
    print(list(return_filename(boolean_query("access or not accustom", inverted_index))), end='\n')

    # taat ranked retrieval test
    query = 'sre game play'

    top5_taat = dict(ranked_retrieval(query, inverted_index, method='taat', n=5))
    top5_daat = dict(ranked_retrieval(query, inverted_index, method='daat', n=5))

    print("Term at a time for query \'%s\'" % query)
    print(list(return_filename(top5_taat.keys())))

    print("Doc at a time for query \'%s\'" % query)
    print(list(return_filename(top5_daat.keys())))




