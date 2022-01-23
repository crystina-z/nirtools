from collections import OrderedDict
from argparse import ArgumentParser

import pytrec_eval
from scipy import stats
from . import load_qrels, load_runs


def query_wise_compare(
    run1, run2, qrels, mark=False, output_fn="query_wise_compare.txt", metrics="map"
):
    evaluator = pytrec_eval.RelevanceEvaluator(qrels, {metrics})
    id2score_1 = evaluator.evaluate(run1)
    id2score_2 = evaluator.evaluate(run2)

    with open(output_fn, "w") as f:
        for qid in set(id2score_1) | set(id2score_2):
            s1 = id2score_1.get(qid, {metrics: "--"})[metrics]
            s2 = id2score_2.get(qid, {metrics: "--"})[metrics]
            if not mark or s1 == "--" or s2 == "--":
                line = f"{qid}\t{s1}\t{s2}"
            else:
                line = line + "\t<" if s1 <= s2 else "\t>"
            f.write(line + "\n")


def query_wise_compare_runfiles(
    runfile1, runfile2, qrelfile, output_fn="query_wise_compare.txt", metrics="map"
):
    run1, run2 = load_runs(runfile1), load_runs(runfile2)
    qrels = load_qrels(qrelfile)
    query_wise_compare(run1, run2, qrels, output_fn, metrics)


def _calc_scores(runs, qrels=None, evaluator=None, metric="map", return_qid=False):
    if qrels is None and evaluator is None:
        raise ValueError(f"Should give one of qrels or evaluator")

    if not evaluator:
        evaluator = pytrec_eval.RelevanceEvaluator(qrels, {metric})
    scores = evaluator.evaluate(runs)
    scores = sorted(scores.items(), key=lambda kv: kv[0])

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
