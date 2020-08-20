import os
from collections import defaultdict, OrderedDict


def sort_qid_docid_value_dict(d):
    sorted_d = OrderedDict()
    qids = sorted(d.keys(), key=lambda k: int(k))  # sort according to qid int value rather than string value
    for qid in qids:  # sort according to label/score, from large to small
        docs = sorted(d[qid].items(), key=lambda kv: kv[1], reverse=True)
        sorted_d[qid] = {k: v for k, v in docs}
    return sorted_d


def load_qrels(fn):
    """
    Loading trec format query relevance file into a dictionary

    :param fn: qrel file path
    :return: dict, in format {qid: {docid: label, ...}, ...}
    """
    qrels = defaultdict(dict)
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            qid, _, docid, label = line.strip().split()
            qrels[qid][docid] = int(label)
    return qrels


def load_runs(fn):
    """
    Loading trec format runfile into a dictionary

    :param fn: runfile path
    :return: dict, in format {qid: {docid: score, ...}, ...}
    """
    runs = defaultdict(dict)
    with open(fn, "r", encoding="utf-8") as f:
        for line in f:
            qid, _, docid, _, score, _ = line.strip().split()
            runs[qid][docid] = float(score)
    return runs


def write_qrels(qrels_dict, outp_fn):
    os.makedirs(os.path.dirname(outp_fn), exist_ok=True)
    sorted_qrels = sort_qid_docid_value_dict(qrels_dict)
    with open(outp_fn, "w", encoding="utf-8") as f:
        for qid in sorted_qrels:
            for docid, value in sorted_qrels[qid].items():
                f.write(f"{qid}\tQ0\t{docid}\t{value}\n")


def write_runs(run_dict, outp_fn, label="test"):
    os.makedirs(os.path.dirname(outp_fn), exist_ok=True)
    sorted_run_dict = sort_qid_docid_value_dict(run_dict)
    with open(outp_fn, "w", encoding="utf-8") as f:
        for qid in sorted_run_dict:
            for rank, (docid, score) in enumerate(sorted_run_dict[qid].items()):
                f.write(f"{qid}\tQ0\t{docid}\t{rank+1}\t{score}\t{label}\n")
                # e.g. 1 Q0 DOC_1 1 -0.1 test


def _read_until_close_tag(f, close_tags):
    def _is_end(line):
        for close_tag in close_tags:
            if line.startswith(close_tag):
                return True
        return False

    content = ""
    while True:
        line = f.readline()
        if _is_end(line) or line == "":
            content = content.split()
            return content, line

        content += line.strip()


def load_topic_trec(topic_fn, fields=["title"]):
    """
    Yield query id and specified field from trec-format topic file

    :param topic_fn: the path to the trec-topic file
    :return: a iterator yielding (qid, field content)
    """
    qid, topic = "-1", {}
    fields = sorted(fields, key=lambda name: {"title": 0, "desc": 1, "narr": 2}[name])

    with open(topic_fn, "rt", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if line == "":
                break

            line = line.strip()
            if line.startswith("<num>"):
                if qid != "-1":
                    yield qid, topic
                qid = line.replace("<num>", "").replace("Number: ", "").strip()
                topic = {}
                continue

            for field in fields:
                if not line.startswith(f"<{field}>"):
                    continue

                if field == "title":
                    curline = line.replace(f"<title>", "").strip().split()
                    topic["title"], line = _read_until_close_tag(f, ["\n", "<desc>"])
                    topic["title"] = curline + topic["title"]

                if field == "desc" or ("desc" in fields and line.startswith("<desc>")):
                    curline = line.replace(f"<desc>", "").replace("Description:", "").strip().split()
                    topic["desc"], line = _read_until_close_tag(f, ["\n", "<narr>"])
                    topic["desc"] = curline + topic["desc"]

                if field == "narr" or ("narr" in fields and line.startswith("<narr>")):
                    curline = line.replace(f"<narr>", "").replace("Narrative:", "").strip().split()
                    topic["narr"], line = _read_until_close_tag(f, ["\n", "</top>"])
                    topic["narr"] = curline + topic["narr"]
        yield qid, topic


def load_topic_tsv(topic_fn, delimiter="\t"):
    """
    Yield query id and specified field from a id\tcontent format topic file

    :param topic_fn: the path to the trec-topic file
    :param delimiter: str, the delimiter betwen id and content
    :return: a iterator yielding (qid, field content)
    """
    with open(topic_fn) as f:
        for line in f:
            qid, content = line.strip().split(delimiter)
            yield qid, content


def load_collection_trec(coll_fn):
    """
    Return a iterator yielding doc id and contnet from trec-format collection file

    :param coll_fn: path to the trec-format collection file
    :return: a iterator yielding (docid, document content)
    """
    docid = ""
    with open(coll_fn, "rt", encoding="utf-8") as f:
        while True:
            line = f.readline().strip()
            if line == "":
                line = f.readline().strip()
                if line == "":
                    break

            if line.startswith("<DOCNO>"):
                docid = line.replace("<DOCNO>", "").replace("</DOCNO>", "").strip()

            if line == "<TEXT>":
                doc = f.readline().strip()
                while True:
                    line = f.readline().strip()
                    if line == "</TEXT>":
                        break
                    doc += line

                assert docid != ""
                yield docid, doc.strip()
                docid = ""


def load_collection_tsv(coll_fn, delimiter="\t"):
    """
    Yield document id and specified field from a id\tcontent format collection file

    :param topic_fn: the path to the trec-topic file
    :param delimiter: str, the delimiter betwen id and content
    :return: a iterator yielding (qid, field content)
    """
    with open(coll_fn) as f:
        for line in f:
            docid, content = line.strip().split(delimiter)
            yield docid, content

