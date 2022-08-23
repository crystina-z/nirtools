""" A comparison between each significant test can be found here: https://ciir-publications.cs.umass.edu/getpdf.php?id=744#:~:text=Information%20retrieval%20(IR)%20researchers%20commonly,test%2C%20and%20the%20sign%20test.&text=Both%20the%20Wilcoxon%20and%20sign,to%20false%20detections%20of%20significance. """
from argparse import ArgumentParser

import numpy as np
import ir_measures
from ir_measures import *

from scipy import stats
from nirtools.ir import load_qrels, load_runs


def _calc_scores(runs, qrels, metric="AP", return_qid=False):
    if isinstance(metric, str):
        metric = eval(metric)
        # todo: ensure the metric is from ir_measures

    # return ir_measures.calc_aggregate([metric], qrels, runs)[metric]
    qids_scores = [(m.query_id, m.value) for m in ir_measures.iter_calc([metric], qrels, runs)]
    qids_scores = sorted(qids_scores, key=lambda kv: kv[0])
    qids, scores = zip(*qids_scores)

    if not return_qid:
        return scores
    else:
        return qids, scores


def sig_test_from_runs(qrels, runs1, runs2, metric="AP", return_scores=False):
    if set(runs1) != set(runs2):
        raise ValueError(f"Expect same keys from two run objects.")

    scores1 = _calc_scores(runs1, qrels=qrels, metric=metric, return_qid=False)
    scores2 = _calc_scores(runs2, qrels=qrels, metric=metric, return_qid=False)
    t, p = stats.ttest_rel(scores1, scores2)
    if return_scores:
        return t, p, np.mean(scores1), np.mean(scores2)
    return t, p


def sig_test_from_files(qrelfile, runfile1, runfile2, metric="AP", return_scores=False):
    qrels = load_qrels(qrelfile)
    runs1, runs2 = load_runs(runfile1), load_runs(runfile2)
    return sig_test_from_runs(qrels, runs1, runs2, metric=metric, return_scores=return_scores)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--qrels", "-q", required=True, type=str)
    parser.add_argument("--runfile1", "-r1", required=True, type=str)
    parser.add_argument("--runfile2", "-r2", required=True, type=str)
    parser.add_argument("--metric", "-m", required=True, type=str)
    args = parser.parse_args()

    m = args.metric
    t, p, s1, s2 = sig_test_from_files(qrelfile=args.qrels, runfile1=args.runfile1, runfile2=args.runfile2, metric=m, return_scores=True)
    print(f"t: {t:.4f}\tp: {p:.4f}\t|\t{m}(1): {s1:.3f}\t{m}(2): {s2:.3f}")
