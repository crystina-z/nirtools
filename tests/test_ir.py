from collections import OrderedDict
from nirtools.ir import sort_qid_docid_value_dict


def test_sort_qid_docid_value_dict():
    qrels = {"2": {"DOC-01": 0, "DOC-02": 1}, "10": {"DOC-3": 0, "DOC-30": 2}}
    expected = OrderedDict({
        "2": {"DOC-02": 1, "DOC-01": 0},
        "10": {"DOC-30": 2, "DOC-3": 0},
    })
    assert sort_qid_docid_value_dict(qrels) == expected