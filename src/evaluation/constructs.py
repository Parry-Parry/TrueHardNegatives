import pyterrier as pt

def generate_experiment(*models, dataset=None, **kwargs):
    if pt.not_started(): pt.init()
    if not dataset:
        topics = kwargs.get("topics", None)
        qrels = kwargs.get("qrels", None)
        assert topics is not None and qrels is not None, "Topics and Qrels must be specified if Dataset is not"
    else:
        topics = dataset.get_topics()
        qrels = dataset.get_qrels()

    args = {
        "retr_systems" : list(*models),
        "topics" : topics,
        "qrels" : qrels,
        "metrics" : kwargs.get("metrics", ["map", "ndcg_cut_10", "mrr"]),
        "names" : kwargs.get("names", [f'model_{i}' for i in range(len(models))]),
        "perquery" : kwargs.get("per_query", False),
        "batch_size" : kwargs.get("batch_size", None),
        "save_dir" : kwargs.get("save_dir", None),
        "baseline" : kwargs.get("baseline", None),
        "test" : kwargs.get("test", None),
        "correction" : kwargs.get("correction", None),
        "verbose" : kwargs.get("verbose", False)
    }

    return pt.Experiment(**args)
