import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from Complete import Complete
from Calculate import Calculate
from DocumentProcess import DocumentProcess
from QueryProcess import QueryProcess
from Similarity import Similarity
from TermsProcess import TermsProcess
from Testing import Testing
from Vector import Vector
from operator import itemgetter
import pickle

query_process=QueryProcess()
document_process=DocumentProcess()
terms_process=TermsProcess()
vector=Vector()
similarity=Similarity()
calculate = Calculate()
testing=Testing()
autocomplete=Complete()

class SearchUI(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        options = {'padx': 5, 'pady': 5}

        self.dataset_label = ttk.Label(self, text='1) CACM    2) CISI')
        self.dataset_label.grid(column=1, row=0, sticky=tk.W, **options)

        self.dataset = tk.StringVar()
        self.dataset_entry = ttk.Entry(self, width=12, textvariable=self.dataset)
        self.dataset_entry.grid(column=2, row=0, **options)
        self.dataset_entry.focus()

        self.query = tk.StringVar()
        self.query_entry = ttk.Entry(self,width=130, textvariable=self.query)
        self.query_entry.grid(column=1, row=1, **options)
        self.query_entry.focus()

        self.search_button = ttk.Button(self, text='search')
        self.search_button['command'] = self.Search
        self.search_button.grid(column=2, row=1, sticky=tk.W, **options)

        self.label=ttk.Label(self, text='did you mean:')
        self.label.grid(column=1, row=3, sticky=tk.W, **options)

        self.text1 = tk.Text(self, height=5, width=100)
        self.scroll1 = tk.Scrollbar(self)
        self.text1.configure(yscrollcommand=self.scroll1.set)
        self.text1.grid(row=4, column=1)
        self.scroll1.config(command=self.text1.yview)
        self.scroll1.grid(row=4, column=10)
        self.button = ttk.Button(self, text='complete')
        self.button['command'] = self.Acomplete
        self.button.grid(column=2, row=4, sticky=tk.W, **options)

        self.label1 = ttk.Label(self, text='results:')
        self.label1.grid(column=1, row=9, sticky=tk.W, **options)

        self.text = tk.Text(self, height=30, width=100)
        self.scroll = tk.Scrollbar(self)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.grid(row=10,column=1)

        self.scroll.config(command=self.text.yview)
        self.scroll.grid(row=10,column=10)

        self.grid(padx=60, pady=10, sticky=tk.NSEW)


    def Acomplete(self):
        y=[]
        word = self.query.get()
        d = self.dataset.get()
        res=autocomplete.Complete(d,word)
        for key,value in res.items():
            y.append(value)
            y.append("\n")
        self.text1.insert(tk.END, y)

    def Search(self):

            q = self.query.get()
            # What is information science?  Give definitions where possible.
            query = {"1": ""}
            query["1"] = q
            ds = self.dataset.get()
            documents = read_documents(ds)

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
            qurey_terms = {}
            for doc_id in d_lem.keys():
                document_terms[doc_id] = terms_process.get_terms(d_lem.get(doc_id))

            for q_id in q_lem.keys():
                qurey_terms[q_id] = terms_process.get_terms(q_lem.get(q_id))

            extracted_terms = terms_process.extract_terms(document_terms, qurey_terms)

            qurey_vectors = vector.query_vectorize(qurey_terms, extracted_terms)

            document_idfs = similarity.get_idf(extracted_terms, document_terms)
            document_vectors = vector.docs_vectorize(document_terms, document_idfs, extracted_terms)

            # with open('vec.txt', 'rb') as handle:
            #     data = handle.read()
            # d = pickle.loads(data)

            results = {}
            query = qurey_vectors.get("1")

            for doc_id in document_vectors.keys():
                document = document_vectors.get(doc_id)
                cosine = calculate.dot_product(query, document) / (calculate.length(query) * calculate.length(document))
                # cosine = similarity.cosine_similarity(query,document)
                if cosine != 0.0:
                    results[doc_id] = cosine
            x = []

            sorted_results = sorted(results.items(), key=itemgetter(1), reverse=True)
            for items in sorted_results[:10]:
                key = items[0]
                doc_res = documents.get(key)
                # print()
                x.append(items[0] + " : " + doc_res + "\n\n")


            self.text.insert(tk.END, x)

            # rels = read_rels(ds)
            # # print("################")p
            # relevant = rels.get("65")
            # # print(relevant)
            #
            # precision = testing.calculate_precision(results, relevant)
            # print(precision)
            #
            # recall = testing.calculate_recall(results, relevant)
            # print(recall)
            #
            # MAP = testing.MAP(relevant, results)
            # print(MAP)
            #
            # AP = testing.AP(relevant, results, k=10)
            # print(AP)



def read_documents(ds):
    data1_folder = "cacm/"
    data2_folder = "cisi/"
    file1_to_open = data1_folder + "cacm.all"
    file2_to_open = data2_folder + "CISI.ALL"
    if ds == "1":
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


def read_rels(ds):
    mdata1_folder = "cacm/"
    mdata2_folder = "cisi/"
    mfile1_to_open = mdata1_folder + "qrels.text"
    mfile2_to_open = mdata2_folder + "CISI.REL"
    if ds == "1":
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


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('search engine')
        self.geometry('1000x600')
        self.resizable(True, True)


if __name__ == "__main__":
    app = App()
    SearchUI(app)
    app.mainloop()
