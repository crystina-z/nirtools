from collections import defaultdict


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


def load_topic_trec(topic_fn, field="title"):
    """
    Yield query id and specified field from trec-format topic file

    :param topic_fn: the path to the trec-topic file
    :return: a iterator yielding (qid, field content)
    """
    qid = ""
    with open(topic_fn, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("<num>"):
                qid = line.replace("<num>", "").replace("Number: ", "").strip()

            if not line.startswith(f"<{field}>"):
                continue

            assert qid != ""
            topic = line.replace(f"<{field}>", "").strip()
            yield qid, topic.split()
            qid = ""


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

