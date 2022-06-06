import pickle
from Calculate import Calculate
from Clustering import Clustering
from DocumentProcess import DocumentProcess
from QueryProcess import QueryProcess
from Similarity import Similarity
from TermsProcess import TermsProcess
from Testing import Testing
from Vector import Vector
from operator import itemgetter

query_process=QueryProcess()
document_process=DocumentProcess()
terms_process=TermsProcess()
vector=Vector()
similarity=Similarity()
calculate = Calculate()
testing=Testing()
clustering=Clustering()

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

string="What is information science?  Give definitions where possible."
query={"1":""}
query["1"]=string

cluster=clustering.get_cluster(documents)
# for key,value in cluster.items():
#     print(f" {key} : {value} \n ")

q_tokens = {}
for key, value in query.items():
    val = value
    word_list = query_process.process(val)
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


cluster_terms = {}
qurey_terms = {}
for c_id in cluster.keys():
    cluster_terms[c_id] = terms_process.get_terms(cluster.get(c_id))

for q_id in q_lem.keys():
    qurey_terms[q_id] = terms_process.get_terms(q_lem.get(q_id))

# for key,value in qurey_terms.items():
#     print(f" {key} : {value} \n\n\n")
# for key,value in cluster_terms.items():
#      print(f" {key} : {value} \n")


extracted_terms  = terms_process.extract_terms(cluster_terms,qurey_terms)

qurey_vectors = vector.query_vectorize(qurey_terms, extracted_terms)
cluster_idfs = similarity.get_idf(extracted_terms,cluster_terms)
cluster_vectors = vector.docs_vectorize(cluster_terms, cluster_idfs, extracted_terms)

results = {}
final={}

qry = qurey_vectors.get("1")
for c_id in cluster_vectors.keys():
    clusters = cluster_vectors.get(c_id)
    cosine = calculate.dot_product(qry,clusters)/(calculate.length(qry)*calculate.length(clusters))
    if cosine > 0.0:
        results[c_id] = cosine


###############################33

for key,value in results.items():
    print(f" {key} : {value} \n ")

sorted_results = sorted(results.items(), key=itemgetter(1), reverse=True)


for items in sorted_results:
    key = items[0]
    c_res = cluster.get(key)
    print(items[0])
    print(c_res)



print("\n\n")

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

document_terms = {}
qurey1_terms = {}
for doc_id in d_lem.keys():
    document_terms[doc_id] = terms_process.get_terms(d_lem.get(doc_id))

for q_id in q_lem.keys():
    qurey1_terms[q_id] = terms_process.get_terms(q_lem.get(q_id))

extracted1_terms  = terms_process.extract_terms(document_terms,qurey1_terms)


docs=[]
for key, value in cluster.items():
    for i in value:
        docs.append(terms_process.term_index.get(i))
print(docs)




# print(len(docs))

