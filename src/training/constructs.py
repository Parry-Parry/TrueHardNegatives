import pandas as pd

def dataset_from_idx(dataset, triplets=None, cut=None, RND=42, nproc=1):
    frame = pd.DataFrame(dataset.docpairs_iter()) if not triplets else triplets
    docs = pd.DataFrame(dataset.docs_iter()).set_index('doc_id').text.to_dict()
    queries = pd.DataFrame(dataset.queries_iter()).set_index('query_id').text.to_dict()
    if cut: frame = frame.sample(cut, random_state=RND) 
    if nproc:
        from multiprocessing import Pool
        idx = zip(frame['query_id'].tolist(), frame['doc_id_a'].tolist(), frame['doc_id_b'].tolist())
        def construct(q, a, b):
            return {'query' : queries[q], 'pid' : docs[a], 'nid' : docs[b]}
        with Pool(nproc) as p:
            res = p.map(lambda x : construct(*x), idx)
        return pd.DataFrame.from_records(res)
    else:
        frame['query'] = frame['query_id'].apply(lambda x: queries[x])
        frame['pid'] = frame['doc_id_a'].apply(lambda x: docs[x])
        frame['nid'] = frame['doc_id_b'].apply(lambda x: docs[x])
    
        return frame[['query', 'pid', 'nid']]

def iterate(df, style='triplet'):
    assert style in ['t5', 'triplet'], "Style must be either 't5' or 'triplet'"
    def t5_style():  
        OUTPUTS = ['true', 'false'] 
        while True:
            for row in df.itertuples():
                yield 'Query: ' + row.query + ' Document: ' + row.pid + ' Relevant:', OUTPUTS[0]
                yield 'Query: ' + row.query + ' Document: ' + row.nid + ' Relevant:', OUTPUTS[1]
    def triplet_style():
        while True:
            for row in df.itertuples():
                yield row.query, row.pid, row.nid

    return t5_style if style == 't5' else triplet_style
