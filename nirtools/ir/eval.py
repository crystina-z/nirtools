import pytrec_eval

from nirtools.ir import load_qrels, load_runs


def query_wise_compare(run1, run2, qrels, output_fn="query_wise_compare.txt", metrics="map"):
    evaluator = pytrec_eval.RelevanceEvaluator(qrels, {metrics})
    id2score_1 = evaluator.evaluate(run1)
    id2score_2 = evaluator.evaluate(run2)

    with open(output_fn, "w") as f:
        for qid in (set(id2score_1) | set(id2score_2)):
            s1 = id2score_1.get(qid, {metrics: "--"})[metrics]
            s2 = id2score_2.get(qid, {metrics: "--"})[metrics]
            f.write(f"{qid}\t{s1}\t{s2}\n")


def query_wise_compare_runfiles(runfile1, runfile2, qrelfile, output_fn="query_wise_compare.txt", metrics="map"):
    run1, run2 = load_runs(runfile1), load_runs(runfile2)
    qrels = load_qrels(qrelfile)
    query_wise_compare(run1, run2, qrels, output_fn, metrics)
