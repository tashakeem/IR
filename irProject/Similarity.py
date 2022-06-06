import math
from Calculate import Calculate


class Similarity:
    calculate=Calculate()

    def get_idf(self,ext_terms, doc_features):
        doc_idfs = {}
        for term in ext_terms:
            doc_count = 0
            for doc_id in doc_features.keys():
                terms = doc_features.get(doc_id)
                if term in terms.keys():
                    doc_count += 1
                    #idf= log (N/count)
            doc_idfs[term] = math.log(float(len(doc_features.keys())) / float(1 + doc_count), 10)
        return doc_idfs


    def cosine_similarity(self,query,document):
        cosine = Calculate.dot_product(query,document)/(Calculate.length(query)*Calculate.length(document))
        return cosine

