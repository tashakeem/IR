import numpy as np

import operator
import math




class Testing:

    def calculate_precision(self,res, rel):
        true_pos = 0
        for item in res:
            if item in rel:
                true_pos += 1
        return float(true_pos) / float(len(res))

    def calculate_recall(self,res, rel):
        true_pos = 0
        for item in res:
            if item in rel:
                true_pos += 1
        return float(true_pos) / float(len(rel))

    def AP(self, rel, res, k=10):
        if not rel:
            return 0.0
        true_pos = 0
        for item in res:
            if item in rel:
                true_pos += 1
        return true_pos / min(len(rel), k)

    def MAP(self, rel, res, k=10):
        return np.mean([self.AP(rl, rs, k) for rl, rs in zip(rel, res)])


    def mean_reciprocal_rank(self,rs):
        rs = (np.asarray(r).nonzero()[0] for r in rs)
        return np.mean([1. / (r[0] + 1) if r.size else 0. for r in rs])

