from Testing import Testing
testing=Testing()

def read_queries():
    f = open("cisi/CISI.QRY")
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


def read_mappings():
    f = open("cisi/CISI.REL")

    mappings = {}

    for a_line in f.readlines():
        voc = a_line.strip().split()
        key = voc[0].strip()
        current_value = voc[1].strip()
        value = []
        if key in mappings.keys():
            value = mappings.get(key)
        value.append(current_value)
        mappings[key] = value

    f.close()
    return mappings
def prefilter(doc_terms, query):
    docs = []
    for doc_id in doc_terms.keys():
        found = False
        i = 0
        while i<len(query.keys()) and not found:
            term = list(query.keys())[i]
            if term in doc_terms.get(doc_id).keys():
                docs.append(doc_id)
                found=True
            else:
                i+=1
    return docs

class QueriesTest():
    queries = read_queries()
    mappings = read_mappings()
