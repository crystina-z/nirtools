""" A comparison between each significant test can be found here: https://ciir-publications.cs.umass.edu/getpdf.php?id=744#:~:text=Information%20retrieval%20(IR)%20researchers%20commonly,test%2C%20and%20the%20sign%20test.&text=Both%20the%20Wilcoxon%20and%20sign,to%20false%20detections%20of%20significance. """
from argparse import ArgumentParser

import pytrec_eval
from scipy import stats
from . import load_qrels, load_runs


def _calc_scores(runs, qrels=None, evaluator=None, metric="map", return_qid=False):
    if qrels is None and evaluator is None:
        raise ValueError(f"Should give one of qrels or evaluator")

    if not evaluator:
        evaluator = pytrec_eval.RelevanceEvaluator(qrels, {metric})
    scores = evaluator.evaluate(runs)
    scores = sorted(scores.items, key=lambda kv: kv[0])

    score_values = [v[metric] for k, v in scores]
    if not return_qid:
        return score_values

    qids = [k for k, v in scores]
    return qids, score_values


def sig_test_from_runs(qrels, runs1, runs2, metric="map"):
    if set(runs1) != set(runs2):
        raise ValueError(f"Expect same keys from two run objects.")

    evaluator = pytrec_eval.RelevanceEvaluator(qrels, {metric})
    scores1 = _calc_scores(runs1, metric=metric, evaluator=evaluator)
    scores2 = _calc_scores(runs2, metric=metric, evaluator=evaluator)
    t, p = stats.ttest_rel(scores1, scores2)
    return t, p


def sig_test_from_files(qrelfile, runfile1, runfile2, metric="map"):
    qrels = load_qrels(qrelfile)
    runs1, runs2 = load_runs(runfile1), load_runs(runfile2)
    return sig_test_from_runs(qrels, runs1, runs2, metric=metric)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--qrels", "-q", required=True, type=str)
    parser.add_argument("--runfile1", "-r1", required=True, type=str)
    parser.add_argument("--runfile2", "-r2", required=True, type=str)
    parser.add_argument("--metric", "-m", required=True, type=str)
    args = parser.parse_args()

    t, p = sig_test_from_files(qrelfile=args.qrels, runfile1=args.runfile1, runfile2=args.runfile2, metric=args.metric)
    print("t value:", t, "p value: ", p)
