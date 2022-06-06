from fast_autocomplete import AutoComplete

class Complete:
    def read_queries(d):
        data1_folder = "cacm/"
        data2_folder = "cisi/"
        file1_to_open = data1_folder + "query.text"
        file2_to_open = data2_folder + "CISI.QRY"
        if d == "1":
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


    def Complete(self,d,query):
        queries = Complete.read_queries(d)
        words = {}
        for key, value in queries.items():
            new_key_values_dict = {value: {}}
            words.update(new_key_values_dict)
        autocomplete = AutoComplete(words=words)
        new = autocomplete.search(query, max_cost=3, size=3)
        w={}
        for index, value in enumerate(new):
                w[index]=value
        return w


