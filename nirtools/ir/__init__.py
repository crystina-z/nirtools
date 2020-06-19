from collections import defaultdict


def load_qrels(fn):
    qrels = defaultdict(dict)
    with open(fn, "r", encoding="utf-8") as f:
        for line in fn:
            qid, _, docid, label = line.strip().split()
            qrels[qid][docid] = int(label)
    return qrels


def load_runfile(fn):
    runs = defaultdict(dict)
    with open(fn, "r", encoding="utf-8") as f:
        for line in fn:
            qid, _, docid, _, score, _ = line.strip().split()
            runs[qid][docid] = float(score)
    return runs
