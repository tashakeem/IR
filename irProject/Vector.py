class Vector:

    def query_vectorize(self,terms,ext_terms):
        output = {}
        for item_id in terms.keys():
            features = terms.get(item_id)
            output_vector = []
            for word in ext_terms:
                if word in features.keys():
                    output_vector.append(int(features.get(word)))
                else:
                    output_vector.append(0)
            output[item_id] = output_vector
        return output



    def docs_vectorize(self,input_terms, idfs, ext_terms):
        output = {}
        for item_id in input_terms.keys():
            terms = input_terms.get(item_id)
            output_vector = []
            for term in ext_terms:
                if term in terms.keys():
                    #tf-idf=tf*idf
                    output_vector.append(idfs.get(term) * float(terms.get(term)))
                else:
                    output_vector.append(float(0))
            output[item_id] = output_vector
        return output