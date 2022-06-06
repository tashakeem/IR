from Calculate import Calculate
from DocumentProcess import DocumentProcess
from QueryProcess import QueryProcess
from Similarity import Similarity
from TermsProcess import TermsProcess
from Testing import Testing
from TextProcess import TextProcess
from Vector import Vector
from operator import itemgetter

query_process=QueryProcess()
document_process=DocumentProcess()
terms_process=TermsProcess()
vector=Vector()
similarity=Similarity()
calculate = Calculate()
testing=Testing()
textprocess=TextProcess()

d=2
def read_documents():
    data1_folder = "cacm/"
    data2_folder = "cisi/"
    file1_to_open = data1_folder + "cacm.all"
    file2_to_open = data2_folder + "CISI.ALL"
    if d == 1:
        data = file1_to_open
    else:
        data = file2_to_open
    f = open(data)
    lines = ""
    for a_line in f.readlines():
        if a_line.startswith("."):
            lines += "\n" + a_line.strip()
        else:
            lines += " " + a_line.strip()
    documents = {}
    content = ""
    doc_id = ""
    for a_line in lines.split("\n"):
        if a_line.startswith(".I"):
            doc_id = a_line.split(" ")[1].strip()
        elif a_line.startswith(".X"):
            documents[doc_id] = content
            content = ""
            doc_id = ""
        else:
            content += a_line.strip()[3:] + " "
    f.close()
    return documents

documents = read_documents()


def read_queries():
    data1_folder = "cacm/"
    data2_folder = "cisi/"
    file1_to_open = data1_folder + "query.text"
    file2_to_open = data2_folder + "CISI.QRY"
    if d == 1:
        data = file1_to_open
    else:
        data = file2_to_open
    f = open(data)
    merged = ""
    for a_line in f.readlines():
        if a_line.startswith("."):
            merged += "\n" + a_line.strip()
        else:
            merged += " " + a_line.strip()
    queries = {}
    content = ""
    qry_id = ""
    for a_line in merged.split("\n"):
        if a_line.startswith(".I"):
            if not content == "":
                queries[qry_id] = content
                content = ""
                qry_id = ""
            qry_id = a_line.split(" ")[1].strip()
        elif a_line.startswith(".W") or a_line.startswith(".T"):
            content += a_line.strip()[3:] + " "
    queries[qry_id] = content
    f.close()
    return queries

queries = read_queries()

with open("evaluation1.txt", 'w') as f:
    for key , query in queries.items():
        mykey=key
        q_tokens = {}
        word_list = query_process.process(query)
        q_tokens[key] = word_list
        q_stem = {}
        for key, value in q_tokens.items():
            val = value
            word_list = query_process.stemming(val)
            q_stem[key] = word_list
        q_lem = {}
        for key, value in q_tokens.items():
            val = value
            word_list = query_process.lemming(val)
            q_lem[key] = word_list
        d_tokens = {}
        for key, value in documents.items():
            val = value
            word_list = document_process.process(val)
            d_tokens[key] = word_list
        d_stem = {}
        for key, value in d_tokens.items():
            val = value
            word_list = document_process.stemming(val)
            d_stem[key] = word_list
        d_lem = {}
        for key, value in d_tokens.items():
            val = value
            word_list = document_process.lemming(val)
            d_lem[key] = word_list
        for key, value in documents.items():
            textprocess.check(value)
            textprocess.get_date(value)
        document_terms = {}
        qurey_terms = {}
        for doc_id in d_lem.keys():
            document_terms[doc_id] = terms_process.get_terms(d_lem.get(doc_id))
        for q_id in q_lem.keys():
            qurey_terms[q_id] = terms_process.get_terms(q_lem.get(q_id))
        extracted_terms  = terms_process.extract_terms(document_terms,qurey_terms)
        document_idfs = similarity.get_idf(extracted_terms,document_terms)
        qurey_vectors = vector.query_vectorize(qurey_terms, extracted_terms)
        document_vectors = vector.docs_vectorize(document_terms, document_idfs, extracted_terms)
        results = {}
        query = qurey_vectors.get(mykey)
        for doc_id in document_vectors.keys():
            document = document_vectors.get(doc_id)
            cosine = calculate.dot_product(query,document)/(calculate.length(query)*calculate.length(document))
            if cosine != 0.0:
                results[doc_id] = cosine
        sorted_results=sorted(results.items(), key=itemgetter(1), reverse=True)
        print("query: "+mykey)
        def read_rels():
            d=2
            mdata1_folder = "cacm/"
            mdata2_folder = "cisi/"
            mfile1_to_open = mdata1_folder + "qrels.text"
            mfile2_to_open = mdata2_folder + "CISI.REL"
            if d == 1:
                mdata = mfile1_to_open
            else:
                mdata = mfile2_to_open
            f = open(mdata)
            lines = {}
            for a_line in f.readlines():
                voc = a_line.strip().split()
                key = voc[0].strip()
                current_value = voc[1].strip()
                value = []
                if key in lines.keys():
                    value = lines.get(key)
                value.append(current_value)
                lines[key] = value
            f.close()
            return lines

        rels = read_rels()
        relevant=rels.get(mykey)

        precision=testing.calculate_precision(results,relevant)
        print(f"precision : {precision}")

        recall=testing.calculate_recall(results,relevant)
        print(f"recall : {recall}")

        MAP=testing.MAP(relevant,results)
        print(f"MAP : {MAP}")

        AP=testing.AP(relevant, results, k=10)
        print(f"AP : {AP} ")

        MRR = testing.mean_reciprocal_rank( results)
        print(f"MRR : {MRR} ")

        # f.write('%s %s %s %s\n' % (precision,recall,MAP,AP))


        print("####################")
f.close()




