def append_value(dict_obj, key, value):
    if key in dict_obj:
        if not isinstance(dict_obj[key], list):
            dict_obj[key] = [dict_obj[key]]
        dict_obj[key].append(value)
    else:
        dict_obj[key] = value


class TermsProcess:
    term_index={}
    
    def get_terms(self,text):
        terms = {}
        for word in text:
            terms[word] = terms.get(word, 0) + 1
        return terms


    def extract_terms(self,doc_terms,qry_terms):
        extracted_terms = []
        for doc_id in doc_terms.keys():
            for term in doc_terms.get(doc_id).keys():
                extracted_terms.append(term)
                append_value(TermsProcess.term_index, term, doc_id)

        for qry_id in qry_terms.keys():
            for term in qry_terms.get(qry_id).keys():
                extracted_terms.append(term)
        return sorted(set(extracted_terms))