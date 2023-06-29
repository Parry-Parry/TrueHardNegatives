from collections import defaultdict


def get_hardest_negatives(scored):
    groups = scored.groupby("query_id")
    negatives = defaultdict(list)

    for group in groups:
        while True:
            for row in group.itertuples():
                if row.relevance == 3:
                    break
                else:
                    negatives[row.query_id].append(row.doc_id)

def get_hard_negatives(scored, cutoff=25):
    groups = scored.groupby("query_id")
    negatives = defaultdict(list)

    for group in groups:
        while True:
            for i, row in enumerate(group.itertuples()):
                if i == cutoff:
                    break
                elif row.relevance == 3:
                    pass 
                else:
                    negatives[row.query_id].append(row.doc_id)